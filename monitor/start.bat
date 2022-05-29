@echo off

SET app=monitor
docker build -t %app% "%CD%"
docker run -d -p 8080:80 --name=%app% --net=word_counterNET -v "%CD%":/monitor %app%