all:
	python3 -m flask --app src/app.py run
debug:
	python3 -m flask --app src/app.py --debug run
