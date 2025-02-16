from invoke import task

@task
def install(c, dev=False):
    command = "poetry install"
    if dev:
        command += " --with dev --with deploy --with test"
    c.run(command)

@task
def test_apps(c):
    c.run("poetry run python -m evolution.manage test", pty=True)

@task
def test_libs(c):
    c.run("poetry run pytest", pty=True)

@task
def test(c):
    c.run("poetry run pytest", pty=True)
    c.run("poetry run python -m evolution.manage test", pty=True)
