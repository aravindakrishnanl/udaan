# Project Udaan – Translation Microservice

This project is a lightweight, modular translation microservice using FastAPI.

## To run
uvicorn app.main:app --reload

## Features
    * Uses REST api (FastAPI) (/api/)
    * Accepts a Block of Text and target language in ISO code(eg. hi, ta, etc..)  (/api/translate)
    * Uses Google Translate API
    * Input Validation and Error Handling
    * Maintain Logs (api/logs)
    * Health endpoint (api/health)