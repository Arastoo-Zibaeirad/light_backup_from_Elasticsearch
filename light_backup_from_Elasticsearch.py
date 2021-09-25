
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import  *
import requests as r
import json

query = {"query": {        "bool": {         }    },    "size": 0,    "from": 0,    "sort": [        {            "@timestamp": {                "order": "DESC"            }        }    ],    "aggs": {        "aggregated_field": {            "terms": {                "field": "event.code",                "size": 10000            }        }    }}

# query = json.loads(query)
query = json.dumps(query)

uri = f"http://192.168.250.120:9200/winlogbeat-*/_search?pretty"
headers = {
'Content-Type': 'application/json'
}
res = r.get(uri, headers = headers, data = query)
res = res.json()
aggs_res = res['aggregations']['aggregated_field']['buckets']
aggs_length = len(aggs_res)

aggs_key_collector = []
for i in range(aggs_length):
    aggs_key = res['aggregations']['aggregated_field']['buckets'][i]['key']
    
    aggs_key_collector.append(aggs_key)

aggs_key = aggs_key_collector

###give this output (aggs_key) to another query in order to have one query from each event.code(or any special field you want)
msg_collector = []
for ii in range(len(aggs_key)):
    query2 = '{"query": {        "bool": {            "must": [              {                    "match": {                        "event.code": %s                    }                }            ],            "must_not": [],            "should": []        }    },    "size": 1,    "from": 0,    "sort": [        {            "@timestamp": {                "order": "DESC"            }        }    ]}'%aggs_key[ii]
    query2 = json.loads(query2)
    query2 = json.dumps(query2)
    # print("\nquery: ",query2)
    res2 = r.get(uri, headers = headers, data = query2)
    res2 = res2.json()
    # print("\nres: ",res2)
    hits = res2['hits']['hits'][0]
    # print("\nhits: ", hits)
    try:
        # msg = hits['anp']['rawdata']
        msg = hits['_source']['message']
        # print("\nmsg: ",msg)
        msg_collector.append(msg)
    except:
        pass

f = open("myOutFile.txt", "w")
for line in msg_collector:
    f.write(str(line.encode("utf-8")) + "\n\n\n\n\n")
f.close()
















