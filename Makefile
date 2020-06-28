SHELL := /bin/bash
NUM_FILES := 5

install:
	# install the epiphany browser and the webkit driver
	sudo apt install webkit2gtk-driver epiphany-browser -y
	# install python script dependencies 
	pip3 install --user -r requirements.txt

run:
	python domato/generator.py --output_dir html --no_of_files $(NUM_FILES)
	python executor.py html result