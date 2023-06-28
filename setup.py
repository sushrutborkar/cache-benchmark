import requests

def loadData(size):
    f = open("ddl.txt", "r")
    ddl = f.read().format(i=size)
    f.close()
    data = {'statement':ddl}
    resp = requests.post('http://localhost:19002/query/service', data=data)
    if resp.json()['status'] != 'success':
        raise Exception

if __name__ == "__main__":
    for i in [1, 4, 16]:
        loadData(i)
        print(i)