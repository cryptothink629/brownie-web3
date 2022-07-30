import json

from discord_webhook import DiscordWebhook

from src.log import logger


def discord(url, content):
    if not url:
        logger.warning('did not config discord webhook')
        return
    logger.debug('send discord message')
    if isinstance(content, dict):
        content = json.dumps(content)
    webhook = DiscordWebhook(url=url, content=content)
    response = webhook.execute()
    logger.debug('discord webhook response: {}'.format(response))
