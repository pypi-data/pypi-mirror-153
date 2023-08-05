import dask
import joblib
import ray
import multiprocessing
import time 
from sysflow.utils.common_utils.basic_utils import flattenlist, chunklist

def parallelize(func, data_list, backend=None, n_jobs=None, ray_mega=False):
    """Naive parallelization of a function. One usecase is to parallelize the for loop in a function.

    Args:
        func (function): the main function to be parallelized
        data_list (list / generator): the data to be parallelized
        backend (sring, optional): backend to use (support dask, ray and joblib). Defaults to None.
        n_jobs (int, optional): -1 means using all the cpus resources. Defaults to None.
        ray_mega (boolean, optional): set true to avoid tiny jobs. Defaults to False.

    Returns:
        list: The list of the results of the parallelized function.
    """
    if backend is None:
        return map(func, data_list)
    elif backend == 'multiprocessing':
        with multiprocessing.Pool(n_jobs) as pool:
            return pool.map(func, data_list)
    elif backend == 'dask':
        return dask.compute([dask.delayed(func)(data) for data in data_list])
    elif backend == 'joblib':
        return joblib.Parallel(n_jobs)([joblib.delayed(func)(data) for data in data_list])
    elif backend == 'ray':
        if ray_mega: 
            @ray.remote
            def func_mega(datas):
                return [func(data) for data in datas]
            num_chunk = n_jobs if n_jobs is not None else multiprocessing.cpu_count()
            out = ray.get([func_mega.remote(datas) for datas in chunklist(data_list, num_chunk)])
            return flattenlist(out)
        else: 
            func_ = ray.remote(func)
            return ray.get([func_.remote(data) for data in data_list])


if __name__ == '__main__':
    # testing the parallelization
    
    def process(i):
        return i * i

    for backend in [None, "multi-processing", "dask", "joblib", "ray"]:
        print("backend:", backend)
        for n_jobs in [1, 2, 4, 8, 16, 32, 64, 128]:
            print("n_jobs:", n_jobs)
            data_list = list(range(10))
            # time the parallelization
            tic = time.time()
            parallel_result = parallelize(process, data_list, backend=backend, n_jobs=n_jobs)
            print("time:", time.time() - tic)
    
    
    data_list = list(range(10))
    tic = time.time()
    parallel_result = parallelize(process, data_list, backend=backend, n_jobs=n_jobs, ray_mega=True)
    print("time:", time.time() - tic)
    print(parallel_result)
    