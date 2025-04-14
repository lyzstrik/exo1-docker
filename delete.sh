
CONTAINER_NAME="attacker"

sudo docker stop $(sudo docker ps -a | grep $CONTAINER_NAME | grep -Eo "^[0-9a-f]{12}")
sudo docker rm $(sudo docker ps -a | grep $CONTAINER_NAME | grep -Eo "^[0-9a-f]{12}")
sudo docker rmi $(sudo docker images | grep $CONTAINER_NAME | grep -Eo "[0-9a-f]{12}")
# sudo docker compose up
