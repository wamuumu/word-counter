app="monitor"
docker build -t ${app} .
docker run -d -p 8080:80 --name=${app} --net=word_counterNET -v "${PWD}:/monitor" ${app}