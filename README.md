# Fastapi Line Bot

## Features

- Response random words when someone sends keyword in Line channel
  - P.S. both keyword and random words are setting in database
- Response random sticker when someone sends sticker in Line channel
- Response weather report when someone sends `supported region + 天氣` in Line channel
- Response minion image when someone sends keyword in Line channel

## Tools

- `Fastapi`: api server
- `alembic`: migration
- `sqlalchemy`: orm

## Start Project

- Insatll Python packages

```shell
pip3 install -r requirements.txt
```

- Set `.env`
- Export `PYTHONPATH`

```shell
export PYTHONPATH=.
```

- Database migrate

```shell
alembic upgrade head
```

- Start api server (local)

```shell
uvicorn main:app --reload
```

- Start api server (prod)

```shell
gunicorn main:app -k uvicorn.workers.UvicornWorker
```
