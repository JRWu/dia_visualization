all:
	docker-compose up --build -d

shell: force
	docker-compose exec visualization bash

force:

