##############################################
# Original Author : Nagesh Kumar 
# Creation Date : 24-Mar-2020 
# Filename : createwls12c.py.
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
version				= "create-weblogic-sample-domain-inputs-v1"
adminPort			= "7001"
adminServerName			= "admin-server"
domainUID			= sys.argv[3]
serverStartPolicy		= "IF_NEEDED"
clusterName			= "cluster-1"
configuredManagedServerCount	= sys.argv[7]
initialManagedServerReplicas	= sys.argv[8]
managedServerNameBase		= "managed-server"
managedServerPort		= "8001"
productionModeEnabled		= "true"
image				= sys.argv[4]
imagePullPolicy			= "IfNotPresent"
includeServerOutInPodLog	= "true"
logHomeOnPV			= "false"
logHome				= "/mnt/logs/domain1"
t3ChannelPort			= "30012"
exposeAdminT3Channel		= "false"
adminNodePort			= "30701"
exposeAdminNodePort		= "false"
namespace			= sys.argv[5]
javaOptions			= "-Dweblogic.StdoutDebugEnabled=false"
persistentVolumeClaimName	= "domain1-weblogic-sample-pvc"
domainPVMountPath		= "/shared"
domainHomeImageBase		= sys.argv[6] 
domainHomeImageBuildPath	= "./docker-images/OracleWebLogic/samples/12213-domain-home-in-image"
weblogicCredentialsSecretName    = domainUID
weblogicUserName                = sys.argv[9]
weblogicPassword                = sys.argv[10]
serverPodCpuLimit               = sys.argv[11]
serverPodMemoryLimit            = sys.argv[12]
appName				= "testapp"
appfilename			= "testds"
deptype				= "war"

env = Environment(loader=PackageLoader('app'))
template = env.get_template('wls12ck8s.yaml') 

root = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(root, 'yaml', taglabel + '.yaml')
 
with open(filename, 'w') as fh:
    fh.write(template.render(
        pvname = taglabel + "wls12c" + "-pv",
        taglabel = taglabel,
		pvcname = taglabel + "wls12c" + "-pvc",
		version = version,
	        adminPort = adminPort,
		adminServerName = adminServerName,
		domainUID = domainUID,
		serverStartPolicy = serverStartPolicy,
		clusterName = clusterName,
		configuredManagedServerCount = configuredManagedServerCount,
		initialManagedServerReplicas = initialManagedServerReplicas,
		managedServerNameBase = managedServerNameBase,
		managedServerPort = managedServerPort,
		productionModeEnabled = productionModeEnabled,
		image = image,
		imagePullPolicy = imagePullPolicy,
		weblogicCredentialsSecretName = weblogicCredentialsSecretName,
		includeServerOutInPodLog = includeServerOutInPodLog,
		logHomeOnPV = logHomeOnPV,
		logHome = logHome,
		t3ChannelPort = t3ChannelPort,
		exposeAdminT3Channel = exposeAdminT3Channel,
		adminNodePort = adminNodePort,
		exposeAdminNodePort = exposeAdminNodePort,
		namespace = namespace,
		javaOptions = javaOptions,
		persistentVolumeClaimName = persistentVolumeClaimName,
		domainPVMountPath = domainPVMountPath,
                domainHomeImageBase = domainHomeImageBase,
		domainHomeImageBuildPath = domainHomeImageBuildPath,
                serverPodCpuLimit = serverPodCpuLimit,
	 	serverPodMemoryLimit = serverPodMemoryLimit,
		ruser = ruser			

    ))
	
print(("Connecting Node %s")%(instance_nodename))

print("Executing the Automation Process to Provision WebLogic Environment Managed by Kubernetes")
try:
    command = "scp -i %s  /home/rundeck/mwrundeck/yaml/%s.yaml opc@%s:/home/opc/weblogic-kubernetes-operator/kubernetes/samples/scripts/create-weblogic-domain/domain-home-in-image/%s.yaml" %(instance_identityfile,taglabel,instance_ip,taglabel)
    output = subprocess.check_output(['bash','-c', command])
    print(output.rstrip())

except subprocess.CalledProcessError as e:
    print("Copy yaml file from Rundeck to Master Node")
    exit()


try:
    command = "ssh -x opc@%s -i %s 'bash -c \"cd /home/opc/weblogic-kubernetes-operator/kubernetes/samples/scripts/create-weblogic-domain-credentials/;./create-weblogic-credentials.sh -u %s -p %s -n %s -d %s -s %s\" \' " %(instance_ip,instance_identityfile,weblogicUserName,weblogicPassword,namespace,domainUID,weblogicCredentialsSecretName)
    output = subprocess.check_output(['bash','-c', command])
    print(output.rstrip())

except subprocess.CalledProcessError as e:
    print("Error Create Weblogic Credentials")
#    exit()


try:
    command = "ssh -x opc@%s -i %s \"cd /home/opc/weblogic-kubernetes-operator/kubernetes/samples/scripts/create-weblogic-domain/domain-home-in-image/;./create-domain.sh -i %s.yaml -o /home/opc/wlsk8s/%s -u %s -p %s \" " %(instance_ip,instance_identityfile,taglabel,ruser,weblogicUserName,weblogicPassword)
    output = subprocess.check_output(['bash','-c', command])
    print(output.decode('utf-8').strip())
except subprocess.CalledProcessError as e:
    print(e)
    exit()

try:
    command = "ssh -x opc@%s -i %s \"/home/opc/wlsk8s/dsAdd.sh %s %s \" " %(instance_ip,instance_identityfile,namespace,domainUID)
    output = subprocess.check_output(['bash','-c', command])
    print(output)
except subprocess.CalledProcessError as e:
    print(e)
    exit()
try:
    command = "ssh -x opc@%s -i %s \"/home/opc/wlsk8s/appAdd.sh %s %s %s %s %s\" " %(instance_ip,instance_identityfile,appName,appfilename,deptype,domainUID,ruser)
    output = subprocess.check_output(['bash','-c', command])
    print(output.decode('utf-8').strip())
except subprocess.CalledProcessError as e:
    print(e)
    exit()

try:
    command = "ssh -x opc@%s -i %s \"cd /home/opc/weblogic-kubernetes-operator/kubernetes/samples/scripts/create-weblogic-domain/domain-home-in-image/;./create-domain.sh -i %s.yaml -o /home/opc/wlsk8s/%s -u weblogic -p welcome1 -k \" " %(instance_ip,instance_identityfile,taglabel,ruser)
    output = subprocess.check_output(['bash','-c', command])
    print(output.decode('utf-8').strip())
except subprocess.CalledProcessError as e:
    print(e)
    exit()

try:
    command = "ssh -x opc@%s -i %s 'bash -c \"sudo docker push %s \" \' " %(instance_ip,instance_identityfile,image)
    output = subprocess.check_output(['bash','-c', command])
    print(output.decode('utf-8').strip())
except subprocess.CalledProcessError as e:
    print("Error Create Domain from YAML file in Master Node")
    exit()

try:
    command = "ssh -x opc@%s -i %s 'bash -c \"/home/opc/wlsk8s/repuser.sh %s %s \" \' " %(instance_ip,instance_identityfile,ruser,domainUID)
    output = subprocess.check_output(['bash','-c', command])
    print(output.rstrip())
except subprocess.CalledProcessError as e:
    print("SED Error Create Kubernates Cluster YAML file in Master Node")
    exit()

try:
    command = "ssh -x opc@%s -i %s 'bash -c \"cd /home/opc/wlsk8s/%s/weblogic-domains/%s/;kubectl apply -f domain.yaml \" \' " %(instance_ip,instance_identityfile,ruser,domainUID)
    output = subprocess.check_output(['bash','-c', command])
    print(output.decode('utf-8').strip())

except subprocess.CalledProcessError as e:
    print("Create Kubernates Cluster YAML file in Master Node")
    exit()

time.sleep(200)
command = "ssh -t opc@%s -i %s 'kubectl get all -n %s -l ruser=%s' " %(instance_ip,instance_identityfile,namespace,ruser)
from subprocess import Popen, PIPE
stdout, stderr = Popen(['bash','-c', command],stdout=PIPE).communicate()
print(stdout.decode('utf-8').strip())

