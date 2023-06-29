run:
	python translator.py test/input1.txt test/input2.txt

test:
	python translatortest.py -v
	python readCIGARtest.py -v
	python readQuerytest.py
.PHONY:test