# Telefier - Telegram notifier utility

[![Deploy to PyPI](https://github.com/ablil/telefier/actions/workflows/deploy.yml/badge.svg)](https://github.com/ablil/telefier/actions/workflows/deploy.yml)

Simple Telegram notification utility to inject on your python app or script.

## Get started

### Pre-requisites

You have to setup a Telegram bot (more info here):

1. Connect to [@BotFather](https://telegram.me/BotFather) and create Telegram Bot
2. Get api id and hash from [ Telegram apps ](https://my.telegram.org/apps)
3. Get bot token from @BotFather

### Usage

```py
#!/usr/bin/env python3

from telefier import Telefier

# create telefier 
telefier = Telefier(<api_id>, <api_hash>, <token>)
telefier.connect()

# send message
telefier.notify(<username>, <message here>)
```

**username** is the telegram username of the one who is gonna recieve the message 
