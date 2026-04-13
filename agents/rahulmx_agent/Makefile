.PHONY: install run dev build up down logs clean lint format

install:
	pip install -r requirements.txt

run:
	uvicorn main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

build:
	docker build -t rahulmx-agent .

up:
	docker run --rm -p 8000:8000 --env-file .env rahulmx-agent

down:
	docker stop $$(docker ps -q --filter ancestor=rahulmx-agent) 2>/dev/null || true

logs:
	docker logs -f $$(docker ps -q --filter ancestor=rahulmx-agent)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

lint:
	ruff check .

format:
	ruff format .
