from invoke import task


@task
def install(c, dev=False):
    command = "poetry install"
    if dev:
        command += " --with dev --with deploy --with client --with test"
    c.run(command)


@task
def build_local(c):
    c.run("docker build -t evolution -f deploy/Dockerfile .")


@task
def run_local(c):
    c.run("docker run -p 8000:8000 --env-file .env evolution")