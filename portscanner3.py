import socket
# from netaddr import IPNetwork
import threading
from queue import Queue
from datetime import datetime
import sys
import os
# from os import system

runtime = True

while runtime == True:
    try:
        print("\nGareth Porter IT Services\n")
        queue = Queue()
        open_ports = []

        
        # Function defined to restart port scan
        def go_again():
            again = input("\nWould you like to perform another scan? y/n: ")
            if again == 'y':
                print("\n")
                validate_hostname()
            else:
                print("Exit Program")


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
            startPort = 1
            endPort = 1024
            default = input("\nDefault port range scan is 1-1024. Press 'y' to proceed, 'n' to edit ")
            if default == "y":
                main()
            else:
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
                        endPort = int(input("Enter ending port (reserved range 1-1024, max is 65535): "))
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
            response = os.system("ping -a -n 1 " + hostname)
            if response == 0:
                validate_ports()
            else:
                if input(f" No response from {hostname}. Would you like to run on localhost instead? y/n : ") == "y":
                    hostname = "localhost"
                    validate_ports()
                else:
                    validate_hostname()
        

        def main():
            global open_ports
            global thread_list
            open_ports = []
            port_list = range(startPort, endPort)
            fill_queue(port_list)
            thread_list = []

            for thread in range(512):
                thread = threading.Thread(target=worker)
                thread_list.append(thread)

            for thread in thread_list:
                thread.start()

            for thread in thread_list:
                thread.join()

            result()


        def result():
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            if not open_ports:
                print("There are no open ports on " + hostname + " between the port range " + str(startPort) + " and " + str(
                    endPort) + ".\nThe date and time is: ", dt_string)
                with open('portscanner_results.txt', 'a+') as f:
                    print("\nThere are no open ports on " + hostname + " between the port range " + str(
                        startPort) + " and " + str(endPort) + ".\nPort scan was run at: ", dt_string, file=f)
            else:
                print("\nOpen ports on " + hostname + " between the port range " + str(startPort) + " and " + str(
                    endPort) + " are: ", open_ports, ".\nThe date and time is: ", dt_string)
                with open('portscanner_results.txt', 'a+') as f:
                    print("\nOpen ports on " + hostname + " between the port range " + str(startPort) + " and " + str(
                        endPort) + " are: ", open_ports, ".\nPort scan was run at: ", dt_string, file=f)

            go_again()


        validate_hostname()
        runtime = False

    except KeyboardInterrupt:
        if input("Ctrl-C. Seriously? y/n: ") == "y":
            print("Exit Program")
            runtime = False
        else:
            pass
