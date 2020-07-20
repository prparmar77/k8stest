import json
import os
import sys
inputfile = sys.argv[1]
item = {"name": "CLASSPATH","value": "./sample1.jar"}
with open(inputfile, 'r') as f:
    config = json.load(f)
config["spec"]["serverPod"]["env"].append(item)
with open(inputfile,'w') as f:
    json.dump(config, f)
