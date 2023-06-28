import requests
import time
import numpy as np

def runBenchmark(numRuns):
    times = np.zeros((2, 5, numRuns))

    for run in range(numRuns):
        print(run, end=" ", flush=True)
        for i in range(1, 6):
            f = open("exp/join" + str(i) + ".txt", "r")
            query = f.read()
            f.close()
            if run % 2 == 0:
                query = 'SET `compiler.querycache.bypass` "true";\n' + query
            data = {'statement':query}
            
            start = time.time()
            resp = requests.post('http://localhost:19002/query/service', data=data)
            end = time.time()
            if resp.json()['status'] != 'success':
                raise Exception
            
            times[0, i-1, run] = end - start
            times[1, i-1, run] = parseCompileTime(resp)
                
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
    times = runBenchmark(12)[:, :, 2:].round(5)
    np.save('results_join/none', times[:, :, ::2])
    np.save('results_join/with', times[:, :, 1::2])
    print()