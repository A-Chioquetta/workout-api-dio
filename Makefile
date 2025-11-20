APP=workout_api.main:app

run:
	@echo "🚀 Iniciando API..."
	@poetry run uvicorn $(APP) --reload

create-migrations:
	@echo "📦 Criando migração: $(m)"
	@poetry run alembic revision --autogenerate -m "$(m)"

run-migrations:
	@echo "🔧 Executando migrações..."
	@poetry run alembic upgrade head