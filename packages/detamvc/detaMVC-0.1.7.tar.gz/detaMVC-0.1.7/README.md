# DetaMVC


DetaMVC is a framework for rapidly developing web applications using:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2](https://fastapi.tiangolo.com/advanced/templates/?h=jinja2)
- [Deta](https://docs.deta.sh/docs/home)
- [ODetaM](https://github.com/rickh94/ODetaM)

## Work in Progress
Please note that DetaMVC is a work in progress currently. Some planned updates include:
- Support for more data types when scaffolding
- Implement Deta Auth when available
- Generate with other front ends ? (may take significant restructuring)

## Installation
```
pip install detamvc
```
   

## Basics
If you are familiar with Ruby on Rails, the commands are very similar for creating an application. 

```
detamvc new project

cd project

detamvc scaffold post title:str content:str
```

Before running your project, be sure to set your PROJECT_KEY for Deta. You can get this from your dashboard under 'settings'.


```
echo PROJECT_KEY="#######_#############" > .env
```

**NOTE**: Deta Base is used as your database. I would strongly recommend creating a new Project called 'development' where you can play around with ideas while building. When you go to production, create a new project in Deta for this to be managed in.

## Run a Server Manually

This assumes you have uvicorn installed. You can run with other servers as you wish - just set up like you would for a normal [FastAPI](https://fastapi.tiangolo.com/deployment/manually/ "Run a Server Manually - Uvicorn") application.
```
detamvc s
```
or
```
uvicorn main:app --reload
```

## Deploy on Deta
Now you can deploy this on Deta!
```
deta new --project default
```