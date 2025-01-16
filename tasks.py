from invoke import task


@task
def build_local(c):
    c.run("docker build -t evolution -f deploy/Dockerfile .")


@task
def run_local(c):
    c.run("docker run -p 8000:8000 --env-file .env evolution")