import socket
import argparse
import time
import sys
import textgen as tg
import json

available_ports = { "master1" : 9898, "master2" : 9897 , "master3" : 9896 }

def main():

    node_name = sys.argv[1]
    master_name = sys.argv[2]

    print(node_name, master_name)

    try:
        host = socket.gethostbyname(master_name)
        port = available_ports[master_name]
    except Exception as e:
        print(master_name + ' not found...')
        return

    ntext = 1 

    while True:

        s = socket.socket()
        s.connect((host,port))

        text = tg.generateTxt()
        sortedOccurences = tg.calculateOccurrences()
        topTen = tg.topTenWords(node_name)

        for item in topTen:
            item["occurrences"][0] += " (" + str(ntext) + "° gen. text)"
        
        message = json.dumps(topTen)

        print (str(node_name)+': send ' + str(message))
        s.send(message.encode())
   
        s.close()

        ntext += 1
        time.sleep(tg.randomNumber(20, 50)) #seconds for sending new text
 
if __name__ == '__main__':
    main()