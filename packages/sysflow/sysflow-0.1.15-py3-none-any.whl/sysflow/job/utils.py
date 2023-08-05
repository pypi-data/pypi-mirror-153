import subprocess

def get_avail_nodes(node_name):
    bash_command_line = " sinfo -p '{}'".format(node_name) + " | grep --color=auto idle  | awk '{ print $4}' | xargs -n 1 echo"
    task = subprocess.Popen(bash_command_line, shell=True, stdout=subprocess.PIPE)
    task_return = task.stdout.read()
    if task_return.isspace():
        node_number = 0
    else: 
        node_number = int(task_return)
    return node_number

def get_node_info(node_name_list = ['savio', 'savio2', 'savio3', 'savio3_gpu']): 
    node_info_dict = {}
    for node_name in node_name_list:
        node_count = get_avail_nodes(node_name)
        print('{}: {}'.format(node_name, node_count))
        node_info_dict[node_name] = node_count
    return node_info_dict
