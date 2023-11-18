from invoke import task
from sys import platform
from subprocess import call

@task
def start(ctx):
    ctx.run("python .\characters\characters.py")

@task
def test(ctx):
    ctx.run("poetry shell")
    ctx.run("pytest characters")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest characters -c .coveragerc")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
    if platform != "win32":
        call(("xdg-open", "htmlcov/index.html"))