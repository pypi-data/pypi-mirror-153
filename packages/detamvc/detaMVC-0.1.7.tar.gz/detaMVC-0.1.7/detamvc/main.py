import typer
import os
from .generator import build_base, gen_scaffold
from typing import List
from pathlib import Path

app = typer.Typer()

@app.command()
def new(project: str):
    """ create a new project """
    new_folder = os.path.join(os.curdir, project)
    try:      
        typer.secho(f"\nBuilding new project: {project}\n", fg='green')
        build_base(new_folder, project)
        typer.echo(f"\n{project} was created.\n")
    except FileExistsError:
        typer.secho(f"'{project}' already exists in this folder.\n", fg='red')

@app.command()
def server():
    """ run the app locally """
    os.system("uvicorn main:app --reload")

@app.command()
def s():
    """ alias for 'server' """
    server()

@app.command()
def scaffold(obj: str, attributes: List[str]):
    """ create a router and views for a described object """
    typer.secho(f"\nScaffolding views and router for: {obj}\n", fg='green')
    gen_scaffold(os.curdir, obj, attributes)
    typer.echo(f"\n{obj} was created.\n")
