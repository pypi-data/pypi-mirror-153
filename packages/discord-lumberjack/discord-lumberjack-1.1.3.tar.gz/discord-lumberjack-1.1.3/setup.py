# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_lumberjack',
 'discord_lumberjack.handlers',
 'discord_lumberjack.message_creators']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26,<3.0']

setup_kwargs = {
    'name': 'discord-lumberjack',
    'version': '1.1.3',
    'description': 'A Python logging handler which sends its logs to a Discord Channel',
    'long_description': '# discord-lumberjack\n\nA Python logging handler which sends its logs to a Discord Channel or Webhook.\n\n## Documentation\n\nYou can find the documentation [here](https://abrahammurciano.github.io/discord-lumberjack/discord_lumberjack/).\n\n## Installation\n\nTo install this python module, run the following command\n\n```\n$ pip install discord-lumberjack\n```\n\n<!-- handlers_start -->\n\n## Handlers\n\nThis python module provides several logging handlers (located in the `discord_lumberjack.handlers` module) which will send the logs it recieves to a Discord webhook, server channel, or DM channel.\n\nThe available handlers are:\n\n-   `DiscordChannelHandler` - Uses a bot token and a channel ID to send logs to the given channel from the given bot.\n-   `DiscordDMHandler` - Uses a bot token and a user ID to send logs to the given user from the given bot.\n-   `DiscordWebhookHandler` - Uses a webhook URL to send the logs to.\n-   `DiscordHandler` - This is the base class for the other three. You probably don\'t want to use this unless you\'re creating your own fancy handler.\n\n<!-- handlers_end -->\n<!-- message_creators_start -->\n\n## Message Creators\n\nIn order to send nice looking messages, there are a few message creators available (located in the `discord_lumberjack.message_creators` module). These are responsible for converting a `logging.LogRecord` into a message structure that will be sent to Discord\'s API.\n\nThe message creators provided currently will split extremely long messages into several in order to fit within Discord\'s message limits. If you decide to create your own one, keep that in mind too.\n\nThe available message creators are:\n\n-   `BasicMessageCreator` - This is a simple message creator which will use the handler\'s set formatter to send the message as plain text. By default, the message will be formatted in monospace, but this can be disabled via the constructor.\n-   `EmbedMessageCreator` - This message creator will create a fancy-looking embed message from the log record. It will ignore the handler\'s formatter.\n\n<!-- message_creators_end -->\n\n## Usage\n\nThe easiest way to get started is to create a webhook and use that, but if you\'re using this to log a Discord bot, you can use it\'s token directly, without needing to create webhooks.\n\n### Import\n\nFirst, you should import the handlers you want to use. For this example, we\'ll assume we have a Discord bot and we\'d like to use it to log every message to a channel and also to send errors to a DM.\n\nWe\'ll be using the `DiscordChannelHandler` to send all messages of level `INFO` and above to the channel and `DiscordDMHandler` to send messages of level `ERROR` and above to a DM.\n\n```py\nfrom discord_lumberjack.handlers import DiscordChannelHandler, DiscordDMHandler\n```\n\n### Basic Setup\n\nYou should really read the [documentation for the `logging` module](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) to learn how to set up your logging, but here\'s a quick snippet to get you started.\n\n```py\nimport logging\nlogging.basicConfig(\n\tlevel=logging.INFO,\n\thandlers=[\n\t\tDiscordChannelHandler(token=my_bot_token, channel_id=my_channel_id),\n\t\tDiscordDMHandler(token=my_bot_token, user_id=my_user_id, level=logging.ERROR),\n\t]\n)\n```\n\nOnce you\'ve set up your logging, you can start logging messages like this:\n\n```py\nlogging.info("This is an informative message that will be sent to the channel.")\nlogging.error("This is an error, so it will also be sent to the DM.")\n```\n',
    'author': 'Abraham Murciano',
    'author_email': 'abrahammurciano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abrahammurciano/discord-lumberjack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
