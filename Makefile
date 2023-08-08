build:
	sudo docker-compose --env-file .env up -d --build --remove-orphans

start:
	sudo docker-compose --env-file .env up -d

stop:
	sudo docker-compose down

restart:
	sudo docker-compose restart