#!/bin/bash -x
echo $1
echo $2
echo $3
export CLASSPATH=${3}
echo ${CLASSPATH}

kubectl get domains ${1} -n ${2} -o json | jq '.' > /home/opc/wlsk8s/domain-${1}-${2}.json


echo "executing current check on domain"

grep -w "CLASSPATH" /home/opc/wlsk8s/domain-$1-$2.json
   if [ $? -eq 0 ]
   then
    # code if found
   kubectl get domains $1 -n $2 -o json | jq '.spec.serverPod.env[2]'

   echo "kubectl get domains $1 -n $2 -o json | jq '.spec.serverPod.env[2].value = \"CLASSPATH\"' | kubectl replace -f -" > tmp-$1-$2-classpath.sh

   sed -i "s#CLASSPATH#${3}#g" tmp-$1-$2-classpath.sh

   chmod +x tmp-$1-$2-classpath.sh

   ./tmp-$1-$2-classpath.sh

   sleep 30s

   kubectl wait --timeout=200s --for=condition=ready pod -l weblogic.domainUID=$1 -n $2
   exit $?
   else  
   # code if not found 
   echo " In Setting CLASSPATH " 

   python /home/opc/wlsk8s/jsonclasspath.py "/home/opc/wlsk8s/domain-${1}-${2}.json"

   echo "cat /home/opc/wlsk8s/domain-$1-$2.json | jq '.spec.serverPod.env[2].value = \"CLASSPATH\"' | kubectl replace -f -" > tmp-$1-$2-classpath.sh

   sed -i "s#CLASSPATH#${3}#g" tmp-$1-$2-classpath.sh

   chmod +x tmp-$1-$2-classpath.sh

   ./tmp-$1-$2-classpath.sh

   sleep 30s

   kubectl wait --timeout=200s --for=condition=ready pod -l weblogic.domainUID=$1 -n $2
   exit $?
   fi

