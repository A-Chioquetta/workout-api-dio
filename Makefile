run:
	@uvicorn workout_api.main:app --reload

create-migrations:
	@PYTHONPATH=$PYTHONPAH:$(pwd) alembic revision --autogenerate -m "$(m)"

run-migrations:
	@PYTHONPATH=$PYTHONPAH:$(pwd) alembic upgrade head