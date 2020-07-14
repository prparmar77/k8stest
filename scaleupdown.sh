echo $1
echo $2
echo $3
kubectl get domain $1 -n $2 -o yaml > domain-scale-$1.yaml && sed -i "s/replicas: .*$/replicas: $3/g" domain-scale-$1.yaml && kubectl replace -f domain-scale-$1.yaml
