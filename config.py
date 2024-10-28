# Contains settings and constants for files

# !!!--- EDIT THESE VALUES ----!!!

# CONFIGURE THESE VALUES TO FIT IPS
ATTACKER_IP = '10.0.2.4'
TARGET_IP = '10.0.2.8' 
PORT_NUMBER = 4321 # port used by server machine 

# Message length constants (minimum and maximum allowed message size to be sent between the machines)
MIN_MESSAGE_LENGTH = 16
MAX_MESSAGE_LENGTH = 2**24 # Increase if too small (# TODO: some connection breaking errors probably related to this)

# list of allowed message lengths (please only input up to 10 sizes)
fixed_message_length_list = [MIN_MESSAGE_LENGTH, 32, 64, 128, 256, 512, 1024, 2048, 4096, MAX_MESSAGE_LENGTH]

# Symmetric Key
SYMMETRIC_KEY = b'NWUn3HPURE16A6nrJaGqxyGi21TK5Bvgx3VEroafa94=' # generated using Fernet.generate_key() (from cryptography.fernet import Fernet)

# Sleep Time
SLEEP_TIME = 10 # number of seconds target machine will wait between making calls to the attacker machine


# !!!--- LEAVE BELOW ALONE ---!!!

TARGET_SHELL_PROMPT_REGEX_LIST = ['\][\s\S]*\$', '\[.+@.+ [\s\S]+\][#\$]', 'Are you sure you want to continue connecting (yes/no)?', '.+@.+ password:', '\[sudo\] password for .+:']

# [\u@\h \W]\$

# This creates a dict where the keys are the indices and the values are the message length that corresponds to that index. The type of the keys are characters instead of ints
message_type_to_length = dict((str(k), v) for k, v in enumerate(fixed_message_length_list))
# This table allows us to look up how long the message sent by the socket is just by looking at the first character sent by the socket (which should be one of the indices that correspond with a message length)
# # Reason for having this is so that we can make the messages a fixed length 
# # (which will allow us to use the same one socket for messages back and forth instead of destroying the socket after one message after sending 0 bytes)
# # but also allow us to send messages of arbitrary length (which can be done by adding more entries into the lookup table)

message_length_to_type = dict((v, k) for k, v in message_type_to_length.items()) # flips keys and values of message_type_to_length dict