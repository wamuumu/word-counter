import socket               # Import socket module
import threading
import json
import operator
import sys
import time
import os
import requests

masterWords = []
updateWords = []

available_ports = { "master_monitor": 9899, "master1" : 9898, "master2" : 9897 , "master3" : 9896}

def on_new_communication(socket, addr, node_name):
    global masterWords, updateWords
    while True:
        try:
            node_words = json.loads(socket.recv(2048).decode()) #set of words

            for i in range(len(node_words)):

                if len(masterWords) == 0:
                    masterWords.append(node_words[i])
                elif not contains(masterWords, node_words[i]["word"]):
                    masterWords.append(node_words[i])
                else:
                    for j in range(len(masterWords)):
                        if(node_words[i]["word"] == masterWords[j]["word"]):
                            masterWords[j]["count"] += int(node_words[i]["count"])
                            for k in range(len(node_words[i]["occurrences"])):
                                if not node_words[i]["occurrences"][k] in masterWords[j]["occurrences"]:
                                    masterWords[j]["occurrences"].append(node_words[i]["occurrences"][k])
                        


            updateWords = sorted(masterWords, key=operator.itemgetter('count'), reverse=True) #sort by number of occurrences
            printWords(updateWords[:10]) #master top ten words

        except json.decoder.JSONDecodeError:
            print("There was a problem accessing the data.")
            break

    socket.close()

def contains(wlist, word):
    for i in range(len(wlist)):
        if(wlist[i]["word"] == word):
            return True
    return False

def listenToNodes(node_name, master_name):

    node_socket = socket.socket()         # Create a socket object to handle nodes
    node_host = socket.gethostbyname(node_name) #accettare sul master attuale
    node_port = available_ports[node_name]    

    print("Waiting for nodes...")

    node_socket.bind((node_host, node_port))        # Bind to the port
    node_socket.listen(5)  

    while True:
        n, naddr = node_socket.accept()     # Establish connection with client.

        thr = threading.Thread(target=on_new_communication, args=(n, naddr, node_name, ))
        thr.start()
        thr.join()

    node_socket.close()

def writeToMaster(node_name, master_name):

    global updateWords
    try:
        host = socket.gethostbyname(master_name)
        port = available_ports[master_name]
    except Exception as e:
        print(master_name + ' not found...')
        return

    while True:

        print("Waiting for words to send to " + master_name + "...")
        while(len(updateWords) == 0):
            time.sleep(.5)

        master_socket = socket.socket()
        master_socket.connect((host,port))

        message = json.dumps(updateWords[0:10])

        master_socket.send(message.encode())

        master_socket.close()

        updateWords = []

def writeToMonitor():
    global updateWords
    try:
        host = socket.gethostbyname("monitor")
        port = 80
    except Exception as e:
        print('monitor not found...')
        return

    while True:

        print("Waiting for words to send to monitor...")
        while(len(updateWords) == 0):
            time.sleep(5)

        url = "http://" + host + ":" + str(port)
        data = json.dumps(updateWords[:10])
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        req = requests.post(url, json=data, headers=headers)

        updateWords = []

def printWords(words):
    print("Top 10 Words:")

    count = 0
    for i in range(len(words)):
        print(words[i]["word"] + ": " + str(words[i]["count"]) + " in " + str(words[i]["occurrences"]))
        count += 1
        if count == 10:
            break

def main():

    node_name = sys.argv[1]
    master_name = sys.argv[2]

    print(node_name, master_name)

    print(node_name + ' started!')

    if not len(master_name) == 0:

        #master can listen to nodes and write to monitor

        node_thread = threading.Thread(target=listenToNodes, args=(node_name, master_name, ))
        node_thread.start()

        master_thread = threading.Thread(target=writeToMaster, args=(node_name, master_name, ))
        master_thread.start()
    else:

        #monitor can only listen to other master or write to monitor 

        monitor_thread = threading.Thread(target=writeToMonitor, args=())
        monitor_thread.start()

        monitor_socket = socket.socket()         # Create a socket object to handle nodes
        monitor_host = socket.gethostbyname(node_name)
        monitor_port = 9899    

        print("Waiting for masters...")

        monitor_socket.bind((monitor_host, monitor_port))        # Bind to the port
        monitor_socket.listen(5)  

        while True:
            m, maddr = monitor_socket.accept()     # Establish connection with client.

            thr = threading.Thread(target=on_new_communication, args=(m, maddr, node_name, ))
            thr.start()
            thr.join()

        monitor_socket.close()

if __name__ == '__main__':
    main()