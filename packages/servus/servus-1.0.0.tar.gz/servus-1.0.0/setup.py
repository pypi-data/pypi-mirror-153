# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['servus']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.0,<3.8.0']

setup_kwargs = {
    'name': 'servus',
    'version': '1.0.0',
    'description': 'Human-friendly wrapper around the aiohttp library for making asynchronous web requests',
    'long_description': '\n\n\n# Servus\n\nA wrapper for the aiohttp library for making asynchronous web requests in Python.\n\nTrying to preserve speed and flexibility provided by `aiohttp`, without sacrificing the human-friendliness of `requests`,  `servus` abstracts using client sessions and context managers when making asynchronous HTTP requests in Python.\n\nExample usage:\n```py\nimport servus\nimport aiohttp\nimport asyncio\n\nasync def main():\n\t# Create a new session\n\tmySession = aiohttp.ClientSession()\n\t\n\t# Use Servus to send a request. \n\t# Servus automatically parses and serializes the response, and returns a ready to use object\n\tresponse = await servus.get(mySession, "http://httpbin.org")\n\t\n\tprint(response.response) # (aiohttp.ClientResponse )\n\tprint(response.json) # (dict)\n\n\t# Remeber to close the session!\n\tmySession.close()\n\nasyncio.run(main())\n```\n\n`servus` also has inbuilt support for working with Discord bots. \n\nExample Usage:\n```py\nimport discord\nfrom discord.ext import commands\nimport asyncio\nimport servus\nfrom servus.discord_utils import createRequestsClient\n\nMY_TOKEN = "<YOUR_TOKEN>"\nbot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))\n\n\n@bot.command()\nasync  def hello(ctx):\n\t"""Hello world, with a HTTP request!"""\n\tr = await servus.get(bot.session,"https://httpbin.org")\n\tdata = r.json\n\tawait ctx.send(f"World! {data}")\n\n# Add the createRequestClient coroutine to `bot` async loop\nbot.loop.create_task(createRequestsClient(bot))\n\n# Run the bot\nbot.run(MY_TOKEN)\n```\n',
    'author': 'TobeTek',
    'author_email': 'katchyemma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheDynamics/servus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
