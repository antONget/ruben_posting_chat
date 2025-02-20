from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: int
    support_id: int
    chat_id: str
    tarif_1: float
    tarif_5: float
    tarif_10: float
    tarif_50: float
    yoomoney_access_token: str
    yoomoney_receiver: str
    bot_link_name: str


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
                               tarif_1=env('TARIF_1'),
                               tarif_5=env('TARIF_5'),
                               tarif_10=env('TARIF_10'),
                               tarif_50=env('TARIF_50'),
                               yoomoney_access_token=env('YOOMONEY_ACCESS_TOKEN'),
                               yoomoney_receiver=env('YOOMONEY_RECEIVER'),
                               bot_link_name=env('BOT_LINK_NAME'),
                               ))
