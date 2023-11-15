from invoke import task
from sys import platform
from subprocess import call

@task
def start(ctx):
    ctx.run("python characters.py")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
    if platform != "win32":
        call(("xdg-open", "htmlcov/index.html"))