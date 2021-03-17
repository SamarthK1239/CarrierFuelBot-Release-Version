# CarrierFuelBot-Release-Version
A repository to maintain a cleaned up and up to date version of the discord bot for managing fuel levels. The dev repository is linked to this account if you want to help out!

## How to use this bot
At the moment there is no way to add a global version of the bot to your server, but that could change soon! Keep an eye out for that! However, if you want to, you can run your own instance of the bot with a little setup (Procedure below)!

## What it's supposed to do
The bot is meant to help manage Fleet Carrier fuel levels in the game Elite: Dangerous. It was developed during the Odyssey Galactic Expedition, to help the mining team manage which carriers they donate Tritium to. It's primary use case is expeditions such as this, but you could just as easily use it on a Squadron discord server or any other place where you're interacting with multiple carriers at the same time.

## Setup

1. Clone the repository with `git clone`
```cmd
git clone https://github.com/SamarthK1239/CarrierFuelBot-Release-Version.git
```
2. Populate your environment variables. These are specified in .env.example. DISCORD_TOKEN is your discord bot token which can be created at [Discord Applications](https://discord.com/developers/applications). DATABASE_URL is the url to your SQL database. An example could be `sqlite:///test.db`
3. Install all the python packages necessary for this bot to run
```cmd
pip install -r requirements.txt
```
4. Run the bot with python
```cmd
python bot.py
``` 

## Optional Procedures

### 1. Deploying to Heroku
1. You can deploy the bot to [Heroku](https://www.heroku.com/). Steps for that can be found [here](https://devcenter.heroku.com/articles/getting-started-with-python). You can also watch [this video](https://www.youtube.com/watch?v=BPvg9bndP1U&ab_channel=TechWithTim) if you prefer a video format of the step by step instructions.
2. If you do decide to deploy to heroku, you will need a database. You can watch [this video](https://www.youtube.com/watch?v=ffEtxbbzCKQ&ab_channel=NickBisignano) to setup heroku postgres. You don't need to change any bot code!
3. Go to the Settings page and add a config variable called ENVIRONMENT with the value "production". The bot depends on this.
4. Add a config variable called DISCORD_TOKEN with the value of your discord token.
5. You're all setup with heroku! Have fun with the bot!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
