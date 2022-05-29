app="master"
monitor="master_monitor"
docker build -t ${app} .

docker run -d -p 9899:9899 --name=${monitor} --network=word_counterNET -v "${PWD}:/master_monitor" ${app} ${monitor} ""
docker run -d -p 9898:9898 --name=${app}1 --network=word_counterNET -v "${PWD}:/master" ${app} master1 ${monitor}
docker run -d -p 9897:9897 --name=${app}2 --network=word_counterNET -v "${PWD}:/master" ${app} master2 ${monitor}
docker run -d -p 9896:9896 --name=${app}3 --network=word_counterNET -v "${PWD}:/master" ${app} master3 ${app}1