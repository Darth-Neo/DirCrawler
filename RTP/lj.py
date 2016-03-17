import os
import pprint
import json

fp = os.getcwd() + os.sep + "ex.json"

# Reading data back
with open(fp, 'r') as f:
     data = json.load(f)

     pp = pprint.PrettyPrinter(indent=4)

     pp.pprint(data)

