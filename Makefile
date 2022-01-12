install :

	pip3 install -r requirements.txt
	mkdir $(HOME)/.notify
	mkdir $(HOME)/.notify/client_secret/
	python3 notify.py -I install
	# cp -r  client_secret $(HOME)/.notify
	echo "Installed Sucessfully"

uninstall :
	rm -r $(HOME)/.notify
	# rm -r client_secret

tet:
	echo $(PWD)