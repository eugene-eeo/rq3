run:
	python test.py
	mkdir -p results
	python plot.py

setup:
	pip install -r requirements.txt
