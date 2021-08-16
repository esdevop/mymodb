# mymodb
A budget tracking web database

## Features
- Register users via login and e-mail.
- Register user incomes/expences/sources.
- Provide information on the user's incomes/expenses/sources via API.
- Dockerized: working out-of-the-box.

## Installation
First, set up the working environment in `env/env.production`. Then

```shell
docker-compose -f docker-compose.prod.yml up --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python mange.py collect static
```
## Schema
![](https://github.com/esdevop/mymodb/blob/main/schema.jpg)


