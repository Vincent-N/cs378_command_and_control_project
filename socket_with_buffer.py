# Implements Socket with additional features such as: handling network buffering issues, authentification using symmetric key
# Made with help from https://docs.python.org/3/howto/sockets.html and https://realpython.com/python-sockets/
import socket
from config import *
from cryptography.fernet import Fernet

# Helper functions for socket class (kind of ugly being positioned here but oh well)

# Helper function that calculates the size of the message after we pad it to match one of the allowed message lengths in the message_type_to_length dict
# also returns the number of spaces we need to add
def calc_padded_message_size(message):
    message_length_before_padding = 1 + len(message) # add 1 because we need to include message type indicator 

    # Determine what the message length after padding to one of the fixed message lengths sizes we have (pads to the smallest length that is greather than or equal to message_length_Before_padding)
    message_too_big = True
    for fixed_length in fixed_message_length_list:
        if fixed_length >= message_length_before_padding:
            message_length_after_padding = fixed_length
            message_too_big = False
            break

    if message_too_big:
        # Hopefully this doesn't happen. If it does, increase the biggest message length we allow
        raise RuntimeError("message is too big to send. Please increase MAX_MESSAGE_LENGTH in the config.py file")

    num_spaces_to_add = message_length_after_padding - message_length_before_padding

    return message_length_after_padding, num_spaces_to_add

# Helper function that pads message to appropriate length, adds length indicator to start, and encrypts the message
def prep_message_to_send(message):
    message = Fernet(SYMMETRIC_KEY).encrypt(message.encode('utf-8', 'backslashreplace')).decode('utf-8') # encrypt the message with symmetric key for authentification (only the message is encrypted, not the message length indicator)

    final_message_length, num_spaces_to_add = calc_padded_message_size(message)

    # construct the final message string by adding type indicator, message, and padding end with spaces
    final_message = message_length_to_type[final_message_length] + message + (' ' * num_spaces_to_add)
    # debug messages
    # print('final message length is:', final_message_length)
    # print('type indicator is:', message_length_to_type[final_message_length])


    assert(len(final_message) == final_message_length) # TODO: debugging, get rid of later 
    # print('final message is:', final_message) # debugging command

    return final_message

# Basically a wrapper class around python socket that handles buffering and encryption/decryption
class Socket:
    def __init__(self, sock=None):
        if sock is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            # Will need this because when we accept connection, a socket is made for us so we want to use this instead of making a new one 
            self.socket = sock 

    # connect socket
    def connect(self, host, port):
        return self.socket.connect_ex((host, port)) # connect_ex instead of connect so exception isn't thrown

    # sends message through socket connection. handles network buffering and encryption
    def send(self, message):
        message = prep_message_to_send(message)
        message_length = len(message)
        total_bytes_sent = 0

        # Send the entire message while preventing the send from returning 0 (so the socket connection doesn't break) 
        while total_bytes_sent < message_length:
            sent = self.socket.send(message[total_bytes_sent:].encode('utf-8')) # attempt to send rest of message
            
            if sent == 0:
                # This if statement should not occur in normal use because the while loop should stop before 0 bytes are returned by send 
                raise RuntimeError("socket connection broken")

            total_bytes_sent = total_bytes_sent + sent # keep track of how many bytes were actually sent by send()

    # receives entire message sent through socket connection. handles network buffering and decryption
    def receive(self):
        chunks = []
        total_bytes_received = 0

        # First, receive one byte so that we can figure out how long the message will be
        message_type = self.socket.recv(1).decode('utf-8') # convert received byte back to normal string
        total_bytes_received += 1

        if message_type == '':
            raise RuntimeError('socket connection broken')
        
        message_length = message_type_to_length[message_type] # remember that this length is including the type indicator

        # then loop to receive the rest of the message while preventing recv from returning an empty string (so the socket connection doesn't break)
        while total_bytes_received < message_length:
            chunk = self.socket.recv(min(message_length - total_bytes_received, message_type_to_length['9'])) # recv argument indicates amount that recv will try to receive AT MOST (so choose smaller value between our allowed biggest size and remaining bytes to get)

            if chunk == b'':
                # again, this if statement should never occur in normal use because the while loop should stop before 0 bytes are returned by recv
                raise RuntimeError('socket connection broken')

            chunks.append(chunk)
            total_bytes_received += len(chunk)

        final_message_encrypted = b''.join(chunks) # combine everything to create the original message sent over
        final_message_encrypted = final_message_encrypted.strip() # get rid of the spaces we added for padding
        final_message_decrypted = Fernet(SYMMETRIC_KEY).decrypt(final_message_encrypted) # decrypt using symmetric key for authentification

        return final_message_decrypted.decode('utf-8', 'backslashreplace') # convert final result back to normal string version

