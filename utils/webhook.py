from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
import json
time_now = datetime.datetime.now().strftime("%H:%M:%S")

with open("settings.json", "r") as f:
     settings = json.load(f)

class webhooks:
     def __init__(web):   
          web.webhook = settings["webhook"]

     def stats_webhook(web, site, product_link, successfull_tasks, failed_tasks, total_tasks):
          if web.webhook == "":
               return False
          else:     
               webhook = DiscordWebhook(url=web.webhook, rate_limit_retry=True)
               embed = DiscordEmbed(title="Drugs Stolen!", url=product_link, color='212121')
               embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/962857189381394442/1004870401026965564/nitty.png")
               embed.add_embed_field(name="**Site:**", value=f"||{site}||", inline=False)
               embed.add_embed_field(name="**Product Link:**", value=product_link, inline=False)
               embed.add_embed_field(name="**Successfull Tasks:**", value=successfull_tasks, inline=False)
               embed.add_embed_field(name="**Failed Tasks:**", value=failed_tasks, inline=False)
               embed.add_embed_field(name="**Total Tasks:**", value=total_tasks, inline=False)
               
               embed.set_footer(text=f"Nitty AIO | {time_now}")
               webhook.add_embed(embed)
               response = webhook.execute()