import requests
import time
import numpy as np
from random import randint
import threading

def startQuery(run):
    chosenFileBit = randint(0,1)
    if  chosenFileBit == 0:
        f = open("exp/thread.txt", "r")
    else:
        f = open("exp/thread2.txt", "r")
    a = randint(1,20)
    query = f.read().format(a=a)
    if run == 0:
        query = 'SET `compiler.querycache.clear` "true";\n' + query
    f.close()
    data = {'statement':query}
    
    start = time.time()
    resp = requests.post('http://localhost:19002/query/service', data=data)
    end = time.time()
    if resp.json()['status'] != 'success':
        raise Exception
    if chosenFileBit and resp.json()['results'] != [a]:
        raise Exception
    
    times[0, run] = end - start
    times[1, run] = parseCompileTime(resp)


def runBenchmark(numRuns):
    threads = []
    for run in range(numRuns):
        print(run, end=" ", flush=True)
        t = threading.Thread(target=startQuery, args=(run,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


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
    numRuns = 200
    times = np.zeros((2, numRuns))
    runBenchmark(numRuns)
    print()