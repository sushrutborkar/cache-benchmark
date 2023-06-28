import requests
import re
import time
import numpy as np

def runBenchmark(dataSize, numRuns):
    times = np.zeros((2, 22, numRuns))

    for run in range(numRuns):
        print(run, end=" ", flush=True)
        for i in range(1, 23):
            f = open("queries/query" + str(i) + ".txt", "r")
            query = f.read()
            f.close()
            bypass_cache = (run % 2 == 0)
            query = f'USE w_{dataSize};\n' + query
            no_comment_query_string = re.sub(r'//.*?(\r\n?|\n)|/\*.*?\*/', '', query, flags=re.S)
            compressed_query_string = ' '.join(no_comment_query_string.split())
            data = {'statement':compressed_query_string, 'bypass_cache':bypass_cache}
            
            if i not in [2,3,8,9,16]:
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
    queryNumbers = np.array([i for i in range(1,23) if i not in [2,3,8,9,16]])
    for dataSize in [1,4,16]:
        times = runBenchmark(dataSize, 12)[:, queryNumbers-1, 2:].round(5)
        np.save('results/none'+str(dataSize), times[:, :, ::2])
        np.save('results/with'+str(dataSize), times[:, :, 1::2])
        print()