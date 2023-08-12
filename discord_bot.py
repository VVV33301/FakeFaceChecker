import os

import discord
from discord import app_commands

from model import classify_image
from tokens import DS_TOKEN

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()


@tree.command(name='help', description='Помощь')
async def bot_help(interaction: discord.Interaction):
    await interaction.response.send_message('Отправьте фотографию и получите в ответ, реальное лицо или поддельное')


@tree.command(name='photo', description='Отправить фото на обработку')
async def ai_photo(interaction: discord.Interaction, photo: discord.Attachment):
    await interaction.response.defer()
    if photo.content_type.startswith('image'):
        path = f'Downloads_ds/{photo.id}'
        await photo.save(path)
        embed = discord.Embed(title=classify_image(path), type='image')
        embed.set_image(url=photo.url)
        await interaction.followup.send(embed=embed)
        os.remove(path)
    else:
        await interaction.followup.send('Недопустимый тип данных')
        print(photo.content_type)


if __name__ == '__main__':
    client.run(DS_TOKEN)
