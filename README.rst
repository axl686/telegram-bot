learn1_axl_bot
==========

learn1_axl_bot is the bot for educational purpose of Aleksei Malinovsky.
----------
Create virtual environment and activate it.
..code-block:: text
	pip install -r requirementns.txt

Settings
----------
Create a file settings.py with the next variables:
..code-block:: python
	PROXY = {
	    'proxy_url': 'socks5://YOUR PROXY SERVER:1080',
	    'urllib3_proxy_kwargs': { 'username': 'LOGIN', 'password': 'PASSWORD' }
	}

	API_KEY = "YOUR API KEY HERE"	

	USER_EMOJI = [EMOJI COLLECTIONS]

Start
----------
In active venv insert:
..code-block:: text
	python3 bot.py