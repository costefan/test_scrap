build: Dockerfile requirements.txt
		docker-compose build

.PHONY: run
run:
		docker-compose up app

