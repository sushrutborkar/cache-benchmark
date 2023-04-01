import requests
import re
import time

for i in range(1, 23):
    f = open("query" + str(i) + ".txt", "r")
    query = f.read()
    no_comment_query_string = re.sub(r'//.*?(\r\n?|\n)|/\*.*?\*/', '', query, flags=re.S)
    compressed_query_string = ' '.join(no_comment_query_string.split())
    data = {'statement':compressed_query_string, 'pretty':'true', 'cache':'false'}

    for j in range(5):
        start = time.time()
        resp = requests.post('http://localhost:19002/query/service', data=data)
        end = time.time()
        measuredTime = end-start
        print(measuredTime)
    
    #print(resp.json())

#ddls, data
