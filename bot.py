import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram.utils.markdown import hbold

import docker

from docker_types import ContainerInfo, ImageInfo, NetworkInfo


token = getenv("SIMPLEST_TG_BOT_APIKEY")

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer('Hello, this is bot used to provide docker host information in telegram')


@dispatcher.message(Command('help'))
async def command_help_handler(message: Message):
    await message.answer(f"This is bot used to provide docker host information in telegram")


@dispatcher.message(Command('containers'))
async def containers_handler(message: Message):
    try:
        docker_client = docker.from_env()
        containers = docker_client.containers.list(all=True)
        answer = ""
        for container in containers:
            container_info = ContainerInfo.from_docker_container(container)
            answer += container_info.to_html()
            answer += "\n"
        if answer == "":
            answer = "No containers"
        await message.answer(answer)
    except TypeError as e:
        await message.answer("Good!)")


@dispatcher.message(Command('images'))
async def images_handler(message: Message):
    try:
        docker_client = docker.from_env()
        images = docker_client.images.list()
        answer = ""
        for image in images:
            image_info = ImageInfo.from_docker_image(image)
            answer += image_info.to_html()
            answer += "\n"
        if answer == "":
            answer = "No images"
        await message.answer(answer)
    except TypeError as e:
        await message.answer("Good!)")


@dispatcher.message(Command('networks'))
async def networks_handler(message: Message):
    try:
        docker_client = docker.from_env()
        networks = docker_client.networks.list()
        answer = ""
        for network in networks:
            network_info = NetworkInfo.from_docker_network(network)
            answer += network_info.to_html()
            answer += "\n"
        if answer == "":
            answer = "No networks"
        await message.answer(answer)
    except TypeError as e:
        await message.answer("Good!)")


async def main() -> None:
    if token is None:
        raise Exception("Dont forget to set environment var \"SIMPLEST_BOT_TG_APIKEY\" to api key")

    bot = Bot(token, parse_mode=ParseMode.HTML)
    await bot.set_my_commands([
        BotCommand(command='/networks', description='Get info about networks'),
        BotCommand(command='/containers', description='Get info about containers'),
        BotCommand(command='/images', description='Get info about images'),
    ])
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())