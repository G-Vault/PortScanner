import socket
import threading
from queue import Queue

print("\nThreaded port scanner, Gareth Porter, Python v3.8\n")
queue = Queue()
open_ports = []


# Function defined to restart port scan
def go_again():
    again = input("\nWould you like to perform another scan? Y/N: ")
    if again == 'Y' or again == 'y':
        print("\n")
        validate_hostname()


# Function defined to open port on target
def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        return True
    except:
        return False


# Function defined to fill queue for scanning ports
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


# Function defined to work through queue and advise open ports
def worker():
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            print("Port {} is open".format(port))
            open_ports.append(port)


# Function defined to validate port range from user
def validate_ports():
    global startPort
    global endPort
    while True:
        try:
            startPort = int(input("Enter starting port (usually 1): "))
        except ValueError:
            print("Enter a valid port number!")
            continue
        else:
            break
    while True:
        try:
            endPort = int(input("Enter ending port (usual is 1-1024, max is 65535): "))
        except ValueError:
            print("Enter a valid port number!")
            continue
        else:
            if startPort <= endPort:
                print("Scanning, please wait...\n")
                main()
                break
            else:
                print('The end port must be higher than the starting port')
                validate_ports()


# Function defined to get hostname or IP from user
def validate_hostname():
    global hostname
    hostname = input("Enter IP address or hostname to scan for open ports: ")
    if len(hostname) > 5:
        validate_ports()
    else:
        print("Enter a valid IP address or port number!")
        validate_hostname()


def main():
    global open_ports
    global thread_list
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

    result()


def result():
    if not open_ports:
        print("There are no open ports on " + hostname + " between the port range " + str(startPort) + " and " + str(
            endPort) + ".")
    else:
        print("\nOpen ports on " + hostname + " between the port range " + str(startPort) + " and " + str(
            endPort) + " are: ", open_ports)

    go_again()


validate_hostname()
