from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: int
    support_id: int
    chat_id : int
    tarif_15 : float
    tarif_50 : float
    tarif_100 : float
    tarif_200 : float
    yoomoney_access_token: str
    yoomoney_receiver: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=env('ADMIN_IDS'),
                               support_id=env('SUPPORT_ID'),
                               chat_id=env('CHAT_ID'),
                               tarif_15=env('TARIF_15'),
                               tarif_50=env('TARIF_50'),
                               tarif_100=env('TARIF_100'),
                               tarif_200=env('TARIF_200'),
                               yoomoney_access_token=env('YOOMONEY_ACCESS_TOKEN'),
                               yoomoney_receiver=env('YOOMONEY_RECEIVER'),
                               ))
