import json

str = """{"data":"this is secret value","pinId":"001agax6t","type":"false"}"""

Jsondata = json.loads(str)

print(Jsondata)  
print(Jsondata['data'])  
print(Jsondata['pinId'])
print(Jsondata['type'])