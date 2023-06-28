import json
from random import randint, choices
import string
import requests

def genRecord(i, N):
    n = 10
    return {"id": i,
            "f1": randint(1,n),
            "f2": randint(1,n),
            "f3": randint(1,n),
            "f4": randint(1,n),
            "st": ''.join(choices(string.ascii_uppercase, k=100)),
            "fk": randint(0, N-1)}

def joinData():
    N = 50000
    for j in range(6):
        f = open("exp_data/R"+str(j+1)+".json", "w")

        for i in range(N):
            json.dump(genRecord(i, N), f)
            f.write("\n")

        f.close()

def indexData():
    N = 2000000
    f = open("exp_data/R.json", "w")

    for i in range(N):
        json.dump(genRecord(i, N), f)
        f.write("\n")

    f.close()

def setup():
    f = open("exp/ddl.txt", "r")
    ddl = f.read()
    f.close()
    data = {'statement':ddl}
    resp = requests.post('http://localhost:19002/query/service', data=data)
    if resp.json()['status'] != 'success':
        raise Exception

if __name__ == "__main__":
    joinData()
    indexData()
    setup()