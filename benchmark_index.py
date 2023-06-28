import requests
import time
import numpy as np
from random import randint

def runBenchmark(numRuns):
    times = np.zeros((2, 5, 2*numRuns))

    for run in range(numRuns):
        for i in range(1, 6):
            print(i, end=" ", flush=True)
            f = open("exp/select.txt", "r")
            n = 10
            query = f.read().format(a=randint(1,n), b=randint(1,n), c=randint(1,n), d=randint(1,n))
            f.close()
            for j in range(4):
                if j % 2 == 0:
                    data = {'statement':'SET `compiler.querycache.bypass` "true";\n' + query}
                else:
                    data = {'statement':query}
                
                start = time.time()
                resp = requests.post('http://localhost:19002/query/service', data=data)
                end = time.time()
                if resp.json()['status'] != 'success':
                    raise Exception
                if j >= 2:
                    times[0, i-1, 2*run + j-2] = end - start
                    times[1, i-1, 2*run + j-2] = parseCompileTime(resp)
            if i <= 4:
                f = open("exp/index_ddl.txt", "r")
                query = f.read().format(i=i)
                f.close()
            else:
                f = open("exp/index_drop.txt", "r")
                query = f.read()
                f.close()
            data = {'statement':query}
            resp = requests.post('http://localhost:19002/query/service', data=data)
            if resp.json()['status'] != 'success':
                raise Exception
        print()
        
    return times

def parseCompileTime(resp):
    compileTimeStr = resp.json()['metrics']['compileTime']
    if 'ms' in compileTimeStr:
        return float(compileTimeStr[:-2]) * 10e-4
    elif 'µs' in compileTimeStr:
        return float(compileTimeStr[:-2]) * 10e-7
    elif 's' in compileTimeStr:
        return float(compileTimeStr[:-1])
    else:
        raise Exception


if __name__ == "__main__":
    times = runBenchmark(20)[:, :, 2:].round(5)
    np.save('results_index/none', times[:, :, ::2])
    np.save('results_index/with', times[:, :, 1::2])
    print()