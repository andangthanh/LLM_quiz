@echo off

start uvicorn backend.main:app --reload

start python frontend/app.py
