from invoke import task


@task
def install(c, dev=False):
    command = "poetry install"
    if dev:
        command += " --with dev --with deploy --with test"
    c.run(command)


@task
def test_apps(c, pty=True):
    c.run("poetry run python -m evolution.manage test", pty=pty)


@task
def test_libs(c, pty=True):
    c.run("poetry run pytest", pty=pty)


@task
def test(c, pty=True):
    c.run("poetry run pytest", pty=pty)
    c.run("poetry run python -m evolution.manage test", pty=pty)
