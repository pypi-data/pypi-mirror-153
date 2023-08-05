# this is the proto-type template for launching the job from the python command lines
import math
import time
import os
import subprocess
from functools import partial 
from dataclasses import dataclass

from sysflow.job.utils import get_node_info
from sysflow.utils.common_utils.basic_utils import chunklist
from sysflow.web.email.email_utils import send_mail

######################################## constants
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
user_config_path = os.path.join(BASE_DIR, "slurm_config")
GROUP_CPU_LIMIT = 4 # savio3
SBATCH_JAX = 'XLA_FLAGS=--xla_gpu_cuda_data_dir=/global/software/sl-7.x86_64/modules/langs/cuda/11.2 '

@dataclass
class TaskManager:
    # users are supposed to overload this class!
    # base_cmd_format can be input 
    # base_cmd = 'python  ../src/run_qaoa_eval.py --testcase hubbard --q {} --T {}  --env_dim {}  --num_ham {} '.format(p, T, N, nham)
    base_cmd_format = None
    
    def get_all_tasks(self):
        # specify the whole task configurations 
        return []
    
    def get_done_tasks(self):
        # spedcify the task ids that are done
        return []

    def get_remaining_tasks(self):
        all_tasks = self.get_all_tasks()
        done_tasks = self.get_done_tasks()
        # ordering perserves the original order
        # remaining_tasks = list( set(all_tasks) - set(done_tasks) )
        remaining_tasks = [i for i in all_tasks if i not in done_tasks]
        return remaining_tasks


    def __post_init__(self):
        self.remaining_tasks = self.get_remaining_tasks()
        self.task_len = len(self.remaining_tasks)
        self.task_ids = [i for i in range(self.task_len)]
        self.remaining_len = self.task_len
        self.current_index = 0


    def concat_tasks(self, task_ids):
        ### utils functions 
        # concatenate the tasks with the space
        if isinstance(task_ids, (list, tuple)):
            if len(task_ids) == 1:
                return self.remaining_tasks[task_ids[0]]
            else: 
                return ' '.join([ str(self.remaining_tasks[task_id]) for task_id in task_ids])
        else: 
            return self.remaining_tasks[task_ids]
        
    def get_jobs(self, num_jobs):     
        # maintain an index here
        out = list(range(self.current_index, min(self.current_index + num_jobs, self.task_len)))
        # update the index
        self.current_index = min(self.current_index + num_jobs, self.task_len)
        self.remaining_len -= num_jobs
        return out
    
    def get_cmd(self, task_ids):
        tasks = self.concat_tasks(task_ids)
        if isinstance(tasks, (list, tuple)):
            return self.base_cmd_format(*tasks)
        else: 
            return self.base_cmd_format(tasks)
            
@dataclass
class JobLauncher:
    folder_name: str
    dry_run: bool 
    use_jax: bool 
    use_gpu: bool
    use_lowpriority: bool
    conda_env: str
    tamana: TaskManager
    CPU_WORKLOAD: int = 10
    GPU_WORKLOAD: int = 1
    CHECK_INTERVAL: int = 2 * 60
    SBATCH: bool = True
    node_name_list: tuple = ('savio', 'savio2', 'savio3', 'savio3_gpu')

    # file IO
    def create_folder(self, folder_name):
        timestamp = time.strftime('%m_%d_%y')
        folder_name += '_' + timestamp
        folder_name = os.path.join('job_scripts', folder_name)
        os.makedirs(folder_name, exist_ok=True)
        return folder_name

    def __post_init__(self):
        # make dir of a new folder 
        self.folder_name = self.create_folder(self.folder_name)
        self.sbatch_head_dict = self.get_sbatch_head_dict()

    def _get_sbatch_name(self, sbatch_head_file):
        return 'sbatch ' + os.path.join(user_config_path, sbatch_head_file) 

    def get_sbatch_head(self, node_name):
        if self.use_lowpriority:
            sbatch_name = node_name + '_lowprio'
        if self.conda_env: 
            sbatch_name = self.conda_env + '_' + sbatch_name
        
        sbatch_name = sbatch_name + '.sh '
        return self._get_sbatch_name(sbatch_name)

    def get_node_list(self):
        node_name_list = self.node_name_list
        
        if not self.use_gpu: 
            node_name_list = list(filter(lambda x: 'gpu' not in x, node_name_list))    
        return node_name_list

    def get_node_info_dict(self):
        node_name_list = self.get_node_list()
        node_info_dict = get_node_info(node_name_list)
        if not self.use_lowpriority: 
            node_info_dict['savio3'] = min(node_info_dict['savio3'], GROUP_CPU_LIMIT)
    
        return node_info_dict

    def get_sbatch_head_dict(self):
        node_name_list = self.get_node_list()
        sbatch_head_list = []
        for node_name in node_name_list:
            sbatch_head_list.append(self.get_sbatch_head(node_name))
        return dict(zip(node_name_list, sbatch_head_list))

    # tamana as an input here
    def launch_job(self, tamana, jobs, node_name, node_count):
        job_chunks = chunklist(jobs, node_count)
        for job_chunk in job_chunks:
            if len(job_chunk) == 0: continue
            cmd = tamana.get_cmd(job_chunk)
            
            if self.SBATCH:
                if self.use_gpu and self.use_jax:
                    cmd = SBATCH_JAX + cmd

                timestamp = time.strftime('%H_%M_%S')
                with open(os.path.join(self.folder_name, 'command_{}_{}.sh'.format(node_name, timestamp)), 'w') as f:
                    f.write(cmd)
                    
                sbatch_head = self.sbatch_head_dict[node_name]
                cmd = sbatch_head + 'bash ' + os.path.join(self.folder_name, 'command_{}_{}.sh '.format(node_name, timestamp))

                if self.dry_run: 
                    print(cmd)
                else: 
                    subprocess.run(cmd, shell=True)
                time.sleep(2)

    def launch_recuring_jobs(self):
        # recuring submitting jobs every CHECK_INTERVAL 
        
        while self.tamana.remaining_len > 0:
            # get the info status
            if self.dry_run: 
                node_info = dict(zip(self.node_name_list, [1] * len(self.node_name_list)))
            else:
                node_info = self.get_node_info_dict()
            total_workload = 0
            for node_name, node_count in node_info.items():
                if 'gpu' in node_name:
                    total_workload += self.GPU_WORKLOAD * node_count
                else:
                    total_workload += self.CPU_WORKLOAD * node_count

            if total_workload == 0: 
                # wait 2 min here
                time.sleep(self.CHECK_INTERVAL)
                continue
            ratio = min(self.tamana.remaining_len / total_workload, 1.0)
            cpu_workload = math.ceil(ratio * self.CPU_WORKLOAD)
            gpu_workload = math.ceil(ratio * self.GPU_WORKLOAD)
            total_workload = min(self.tamana.remaining_len, total_workload)

            # finish the work of total_workload
            # this can be index instead of real data? 
            # todo_tasks, remaining_tasks = remaining_tasks[:total_workload], remaining_tasks[total_workload:]
            todo_tasks = self.tamana.get_jobs(total_workload)

            for node_name, node_count in node_info.items():
                if node_count == 0: continue
                if 'gpu' in node_name:
                    tasks, todo_tasks = todo_tasks[:gpu_workload * node_count], todo_tasks[gpu_workload * node_count:]
                else:
                    tasks, todo_tasks = todo_tasks[:cpu_workload * node_count], todo_tasks[cpu_workload * node_count:]

                self.launch_job(self.tamana, tasks, node_name, node_count)

            # wait 2 min here
            time.sleep(self.CHECK_INTERVAL)

        # write an email to me
        message = '{} jobs finished.'.format(self.folder_name)
        send_mail(message)



if __name__ == '__main__': 
    # user define this data class 
    @dataclass
    class TaskManagerA(TaskManager):
        # example!
        paramA = 1
        paramB = 3
        base_cmd_format = partial('python test.py --paramA {paramA} --paramB {paramB} --paramC {}'.format, paramA=paramA, paramB=paramB)
        
        # manage the task list
        def get_all_tasks(self):
            return list([i * i for i in range(100)])
        
        def __repr__(self) -> str:
            return super().__repr__() + '\n' + str(self.paramA) + '\n' + str(self.paramB)

    tamana = TaskManagerA()
    
    jobsubmit = JobLauncher(
        folder_name='test',
        dry_run=True, 
        use_jax=False, 
        use_gpu=True, 
        use_lowpriority=True, 
        conda_env='qrl', 
        tamana=tamana)
    
    jobsubmit.launch_recuring_jobs()
        
