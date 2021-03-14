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
2. Create a Heroku account and install the heroku cli
3. Run `heroku create project-name` in the command line to generate a new project with that specific project name
4. Populate your environment variables. These are specified in .env.example. DISCORD_TOKEN is your discord bot token which can be created at [Discord Applications](https://discord.com/developers/applications). DATABASE_URL is the url to your SQL database. An example could be `sqlite:///test.db`
5. Install all the python packages necessary for this bot to run
```cmd
pip install -r requirements.txt
```
6. Run the bot with python
```cmd
python bot.py
``` 

## Optional Steps

1. You can deploy the bot to [Heroku](https://www.heroku.com/). Steps for that can be found [here](https://devcenter.heroku.com/articles/getting-started-with-python). You can also watch [this video](https://www.youtube.com/watch?v=BPvg9bndP1U&ab_channel=TechWithTim) if you prefer a video format of the step by step instructions.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Have Fun!
