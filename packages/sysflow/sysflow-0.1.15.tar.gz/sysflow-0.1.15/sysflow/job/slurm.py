import argparse
import os
import subprocess
import sys
import socket 

from sysflow.utils.common_utils.file_utils import dump, is_empty, load
import ruamel.yaml

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
user_config = os.path.join(BASE_DIR, "slurm_user.yaml")


def _default_item(resources, key, value):
    if key not in resources:
        resources[key] = value


def _default_append_item(resources, key, value):
    if key not in resources:
        resources[key] = value
    elif isinstance(resources[key], str):
        resources[key] = [resources[key]] + value
    elif isinstance(resources[key], list):
        resources[key] = resources[key] + value

# reference: https://docs-research-it.berkeley.edu/services/high-performance-computing/user-guide/hardware-config/
CPU_CAP = {
    'savio': 20, 
    'savio2': 24, 
    'savio3': 32
}

class Slurm:
    def __init__(self, **args_dict):
        # whether on the local desktop or savio / brc
        hostname = socket.gethostname() 
        self._slurm = (hostname.startswith('ln') and 'brc' in hostname) or (hostname.startswith('n') and 'savio' in hostname)  

        self.config(**args_dict)

    def default_config(self, res_):
        """
        set default value if a key in res_ is not fhound
        """
        if res_ == None:
            res = {}
        else:
            res = res_
        _default_item(res, "numb_node", 1)
        _default_item(res, "job_name", "test")
        _default_item(res, "task_per_node", 32)
        _default_item(res, "time_limit", "24:00:00")
        _default_item(res, "partition", "savio3")
        _default_item(res, "account", "co_esmath")
        _default_item(res, "qos", "esmath_savio3_normal")
        _default_append_item(res, "module_list", ["gcc", "openmpi"])
        _default_item(res, "email", "jiahaoyao.math@gmail.com")
        _default_item(res, "conda_env", "qrl")

        self.limit_cpu_cap(res)
        return res

    def merge_config(self, res, res_):
        for key, value in res_.items():
            if key == "module_list":
                _default_append_item(res, key, value)
            else:
                _default_item(res, key, value)

        self.limit_cpu_cap(res)
        return res

    def limit_cpu_cap(self, res):
        if res['partition'] in CPU_CAP: 
            res['task_per_node'] = min(res['task_per_node'], CPU_CAP[res['partition']])
        return res 

    def sub_script_head(self, res):
        ret = ""
        ret += "#!/bin/bash\n"
        ret += "#SBATCH --job-name=%s \n" % res["job_name"]
        ret += "#SBATCH --account=%s \n" % res["account"]
        ret += "#SBATCH --partition=%s \n" % res["partition"]
        ret += "#SBATCH --qos=%s \n" % res["qos"]
        ret += "#SBATCH --nodes=%d\n" % res["numb_node"]
        ret += "#SBATCH --ntasks-per-node=%d\n" % res["task_per_node"]
        ret += "#SBATCH -t %s\n" % res["time_limit"]
        ret += "#SBATCH --mail-type=END,FAIL\n#SBATCH --mail-user=%s\n" % res["email"]
        ret += "\n"

        if isinstance(res["module_list"], str):
            ret += "module load %s\n" % res["module_list"]
        elif isinstance(res["module_list"], list):
            for ii in res["module_list"]:
                ret += "module load %s\n" % ii
        ret += 'eval "$(conda shell.bash hook)"\nconda activate %s\n' % res["conda_env"]
        ret += "\n"

        ret += "$@\n"
        return ret

    def config(self, **args_dict):
        if is_empty(user_config):
            self.default_config(args_dict)
            dump(args_dict, user_config)
        else:
            user_args_dict = load(user_config)
            self.merge_config(args_dict, user_args_dict)
            dump(args_dict, user_config)

        slurm_bash = self.sub_script_head(args_dict)
        dump(slurm_bash, "savio3.sh")

    def run(self, command_line, slurm=False):
        print(command_line)
        if slurm or self._slurm:
            subprocess.call("sbatch savio3.sh {}".format(command_line), shell=True)
        else:
            subprocess.call("{}".format(command_line), shell=True)


def config(args=None):
    parser = argparse.ArgumentParser(
        prog="slurm config",
        description="personalize configurations for the slurm.",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument("--numb_node", type=int, help="number of nodes")
    parser.add_argument("--job_name", type=str, help="the name for the job")
    parser.add_argument("--task_per_node", type=int, help="task number for each node")
    parser.add_argument(
        "--time_limit", type=str, help="set the cap for the time, format: hour:min:sec"
    )
    parser.add_argument("--partition", type=str, help="which partition for the job")
    parser.add_argument("--account", type=str, help="which account to use")
    parser.add_argument("--qos", type=str, help="which qos in the slurm account")
    parser.add_argument(
        "--module_list",
        type=str,
        nargs="*",
        help="the list of modules to load for the slurm",
    )
    parser.add_argument(
        "--email", type=str, help="the email to notify when the jobs are finished"
    )
    parser.add_argument(
        "--conda_env", type=str, help="conda environment to activate in the scripts"
    )
    args = parser.parse_args(args)

    args_dict = vars(args)

    if "job_name" not in args_dict:
        job_name = input("Enter your job name: ")
        if job_name: 
            args_dict["job_name"] = job_name

    if "email" not in args_dict:
        email = input("Enter your email: ")
        if email: 
            args_dict["email"] = email

    if "conda_env" not in args_dict:
        conda_env = input("Enter your anaconda environment: ")
        if conda_env: 
            args_dict["conda_env"] = conda_env

    slurm = Slurm(**args_dict)

    status()

def run(args=None):
    parser = argparse.ArgumentParser(
        prog="slurm run",
        description="run a command using the slurm job submission",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument("command", nargs="*", help="the command line to execute")

    command_line = " ".join(sys.argv[2:])

    slurm = Slurm()

    slurm.run(command_line)


def status(args=None):
    print()
    print('the current slurm configuration: ')
    user_args_dict = load(user_config)
    res = ''.join(ruamel.yaml.round_trip_dump(user_args_dict, indent=5, block_seq_indent=3).splitlines(True))
    print(res)

def main(args=None):
    parser = argparse.ArgumentParser(
        prog="slurm", description="A program to generate slurm command lines."
    )
    parser.add_argument(
        "command",
        help="specify the sub-command to run, possible choices: config, run, show",
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="arguments to be passed to the sub-command",
    )

    args = parser.parse_args(args)

    # sepatate all sub_command to make them useable independently
    if args.command.upper() == "CONFIG":
        sub_command = config
    elif args.command.upper() == "STATUS":
        sub_command = status
    elif args.command.upper() == "RUN":
        sub_command = run
    else:
        return ValueError(f"unsupported sub-command: {args.command}")

    sub_command(args.args)


if __name__ == "__main__":
    main()
