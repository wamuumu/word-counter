app="node"
docker build -t ${app} .
docker run -d --name=${app}1 --net=word_counterNET -v "${PWD}:/node" ${app} Node_1 master1
docker run -d --name=${app}2 --net=word_counterNET -v "${PWD}:/node" ${app} Node_2 master3
docker run -d --name=${app}3 --net=word_counterNET -v "${PWD}:/node" ${app} Node_3 master2
docker run -d --name=${app}4 --net=word_counterNET -v "${PWD}:/node" ${app} Node_4 master2