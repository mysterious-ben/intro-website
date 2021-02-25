PROJECT := intro-website

default: project-name

project-name:
	@echo $(PROJECT)

start:
	python -m src.app

show-logs:
	cat logs/intro_website.log | tail

dc-start:
	docker-compose down; docker-compose build; docker-compose up -d --remove-orphans

dc-show-logs:
	docker-compose logs --tail 10