install:
	# install the epiphany browser and the webkit driver
	sudo apt install webkit2gtk-driver epiphany-browser -y
	# install python script dependencies 
	pip3 install -U -r requirements.txt