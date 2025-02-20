from pathlib import Path

from dotenv import load_dotenv


def load_env():
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)


load_env()
