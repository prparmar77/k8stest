#############################################
# Original Author : Prakash Parmar 
# Creation Date : 24-Mar-2020 
# Filename : updateClasspathwls12cver1.0.py 
# Modified By : 
##############################################
import subprocess
import os
import sys
import jinja2
import time
from jinja2 import Environment, PackageLoader
instance_ip = "132.145.163.221"
instance_nodename = "masterk8s" 
instance_identityfile = "/home/rundeck/mwrundeck/id_rsa"
ruser                           = sys.argv[2]
namespace			= sys.argv[4]
domainUID			= sys.argv[3]
taglabel			= sys.argv[1]
classpath                       = sys.argv[5]


	
print(("Connecting Node %s")%(instance_nodename))

print("Executing the Automation Process to Provision WebLogic Environment Managed by Kubernetes")



command = "ssh -t opc@%s -i %s '/home/opc/wlsk8s/updateclasspath.sh %s %s \"%s\"' " %(instance_ip,instance_identityfile,domainUID,namespace,classpath)
print(command)
from subprocess import Popen, PIPE
stdout, stderr = Popen(['bash','-c', command],stdout=PIPE).communicate()
print(stdout.decode('utf-8').strip())

command = "ssh -t opc@%s -i %s 'kubectl get all -n %s -l ruser=%s -o wide' " %(instance_ip,instance_identityfile,namespace,ruser)
from subprocess import Popen, PIPE
stdout, stderr = Popen(['bash','-c', command],stdout=PIPE).communicate()
print(stdout.decode('utf-8').strip())
