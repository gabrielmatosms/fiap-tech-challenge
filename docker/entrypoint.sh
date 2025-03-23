#!/bin/sh
alembic upgrade head
uvicorn main:app --port 8009 --host 0.0.0.0 --reload
