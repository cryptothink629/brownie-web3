import json

from discord_webhook import DiscordWebhook

from src.log import logger


def discord(url, content):
    if not url:
        logger.warning('did not config discord webhook')
        return
    if isinstance(content, dict):
        content = json.dumps(content)
    webhook = DiscordWebhook(url=url, content=content)
    response = webhook.execute()
    logger.info('discord webhook response: {}'.format(response))
