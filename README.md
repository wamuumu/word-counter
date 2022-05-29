# word-counter

Word-counter is an application that allows textual data sharing between nodes on a network. Each remote node calculates the top ten words of a generated text and send them to its master, which forward the data until it reaches the monitor, where the top ten words overall are displayed.

## Application structure

The application is tree structured, which means that each internal node (master) can have multiple leaf nodes (remote nodes). In particular, these are the main components:
* monitor - it's a Flask application that renders a html webpage where the top ten words overall are showed
* master_monitor - it's a special master that cannot have communications with other leaf nodes, retrieve data from other masters and send them to the monitor
* master - it's responsible for communicating with nodes. In particular, it has two main roles:
  * listen to remote nodes data
  * forward remote nodes data as a merged one to its master 
* node - it's responsible for generating the textual data, calculate the occurrences for each word in it and send the ten top words to its master

The communication between the nodes is via sockets, which means that every master, exept the master_monitor, can listen and write on some pre-defined and static ports. The master_monitor retrieves data from other masters using socket, but it sends a POST request to monitor when it has new data to be pushed.

Being that the application is tree structured, the scalability is not a problem because every master, exept for master_monitor, can accept new communications from new leaf nodes and new masters. The only one limitation is that the ports are static, and if you want to add new masters you have to expose new ports and bind them correctly to the host.

The default configuration made for testing is the following one:

* monitor
 * master_monitor
    * master1
      * node1
      * master3
        * node2
    * master2
      * node3
      * node4

## Application usage

The application, for simulation purposes, runs on docker. So if you haven't download it yet, just click [Docker Desktop](https://www.docker.com/products/docker-desktop/) and download it. Once you have done it, you can continue.

First of all, you have to create a bridged network inside docker to allow the containers to talk to each other via sockets. This because docker runs inside virtual machines. Thus, it will not bind the IP address to the host if you don't create a network for that purpose. To crate it, just open your terminal and run:

```
docker network create word_counterNET
```

Be sure that docker daemon is running otherwise it will fail.

If you want to check whether the network has been created, just run:

```
docker network list
```

More docker tips are available on the docker_tips.txt file.

Then, since the application follows a specific order to run its components, open the project folder, go inside the monitor's folder and run:

Windows only
```
start.bat
```

MacOS and Linux
```
bash start.bat
```

Repeat this action with the master's folder and with the node's folder in this order. If you have done all correctly, you should be able to see all the running containers on the docker dashboard.

Lastly, if you want to see the top ten words, you need to open your browser and type this url:
```
localhost:8080
```

If everything went good, you should see a table with this format:

| # | Word | Count | Occurrences |
| - | ---- | ----- | ----------- |
| 1 | word |   x   | Node_i (j° gen. text), Node_k (n° gen. text), ... |

The above row means that "word" has been found x times overall in the j-textual data generated by Node_i, in the n-textual data generated by Node_k and so on...
