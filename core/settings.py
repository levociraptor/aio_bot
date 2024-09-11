from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    channel_link: str

@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN_API'),
            admin_id=env.int('ADMIN_ID'),
            channel_link=env.str('CHANNEL_LINK')
        )
    )

settings = get_settings('config')