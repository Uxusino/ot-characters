from invoke import task
from sys import platform
from subprocess import call

@task
def start(ctx):
    if platform == "win32":
        ctx.run("python ./characters/characters.py")
    else:
        ctx.run("python characters/characters.py", pty=True)

@task
def build(ctx):
    if platform == "win32":
        ctx.run("python ./characters/build.py")
    else:
        ctx.run("python characters/build.py", pty=True)

@task
def test(ctx):
    if platform == "win32":
        ctx.run("pytest characters")
    else:
        ctx.run("pytest characters", pty=True)

@task
def coverage(ctx):
    if platform == "win32":
        ctx.run("coverage run --branch -m pytest characters -c .coveragerc")
    else:
        ctx.run("coverage run --branch -m pytest characters -c .coveragerc", pty=True)

@task(coverage)
def coverage_report(ctx):
    if platform != "win32":
        ctx.run("coverage html", pty=True)
        call(("xdg-open", "htmlcov/index.html"))
    else:
        ctx.run("coverage html")