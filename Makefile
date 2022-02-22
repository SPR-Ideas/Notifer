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

test:
	python3 -m unittest run test_notify.py

test-report:
	coverage  run -m unittest test_notify
	coverage  html --include=notify.py
