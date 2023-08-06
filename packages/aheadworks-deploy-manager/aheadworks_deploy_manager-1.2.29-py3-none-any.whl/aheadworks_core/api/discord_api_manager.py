from discord import Webhook, RequestsWebhookAdapter


class DiscordApiManager:
    """api manager for discord"""

    def send_msg(self, url, msg):
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter()
        )
        webhook.send(msg)
