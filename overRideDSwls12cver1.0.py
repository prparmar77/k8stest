##############################################
# Original Author : Nagesh Kumar 
# Creation Date : 24-Mar-2020 
# Filename : overRideDS.py.
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
taglabel			= sys.argv[1]
ruser                           = sys.argv[2]
domainUID			= sys.argv[3]
serverStartPolicy		= "IF_NEEDED"
clusterName			= "cluster-1"
namespace			= sys.argv[4]
weblogicCredentialsSecretName   = domainUID
dsName				= sys.argv[5]
dsHost				= sys.argv[6]
dsPort				= sys.argv[7]
dsService			= sys.argv[8]
dsUserName			= sys.argv[9]
dsUserPassword			= sys.argv[10]


print(("Connecting Node %s")%(instance_nodename))

print("Executing the Automation Process to Provision WebLogic Environment Managed by Kubernetes")

try:
    command = "ssh -x opc@%s -i %s 'bash -c \"	/home/opc/wlsk8s/repconfig.sh %s %s %s %s %s %s %s %s %s %s \" \' " %(instance_ip,instance_identityfile,taglabel,domainUID,namespace,dsHost,dsPort,dsService,dsUserName,dsUserPassword,dsName,ruser)
    output = subprocess.check_output(['bash','-c', command])
    print(output.decode('utf-8').strip())

except subprocess.CalledProcessError as e:
    print("Something wrong in override")
    exit()

time.sleep(200)
command = "ssh -t opc@%s -i %s 'kubectl get all -n %s -l ruser=%s' " %(instance_ip,instance_identityfile,namespace,ruser)
from subprocess import Popen, PIPE
stdout, stderr = Popen(['bash','-c', command],stdout=PIPE).communicate()
print(stdout.decode('utf-8').strip())

