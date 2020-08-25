import socket
import threading
from queue import Queue

print("\nThreaded port scanner, Gareth Porter, Python v3.8\n")
queue = Queue()
open_ports = []


def go_again():
    again = input("\nWould you like to perform another scan? Y/N: ")
    if again == 'N' or again == 'n':
        exit()
    else:
        get_info()


def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False


def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            print("Port {} is open".format(port))
            open_ports.append(port)


def get_info():
    global target
    global startPort
    global endPort
    global queue
    global open_ports
    global thread_list
    target = input("Enter IP address of device to scan for open ports: ")
    while True:
        try:
            startPort = int(input("Enter starting port (usually 1): "))
        except ValueError:
            print("Please enter valid port number")
            continue
        else:
            break
    while True:
        try:
            endPort = int(input("Enter ending port (usual is 1-1024, max is 65535): "))
        except ValueError:
            print("Please enter valid port number")
            continue
        else:
            break
    if startPort >= endPort:
        print('The end port must be higher than the starting port')
        get_info()
    queue = Queue()
    open_ports = []
    port_list = range(startPort, endPort)
    fill_queue(port_list)
    thread_list = []

    for t in range(512):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Open ports on " + target + " between " + str(startPort) + " and " + str(endPort) + " are: ",
          open_ports)
    go_again()


get_info()
