# CarrierFuelBot-Release-Version
A repository to maintain a cleaned up and up to date version of the discord bot for managing fuel levels. The dev repository is linked to this account if you want to help out!

## How to use this bot
At the moment there is no way to add a global version of the bot to your server, but that could change soon! Keep an eye out for that! However, if you want to, you can run your own instance of the bot with a little setup (Procedure below)!

## What it's supposed to do
The bot is meant to help manage Fleet Carrier fuel levels in the game Elite: Dangerous. It was developed during the Odyssey Galactic Expedition, to help the mining team manage which carriers they donate Tritium to. It's primary use case is expeditions such as this, but you could just as easily use it on a Squadron discord server or any other place where you're interacting with multiple carriers at the same time.

## Setup

I think it's important to start off by saying that even though this is a wall of text, there's nothing to be afraid of. There's a fair few steps but they shouldn't take you very long to finish (you can be done in about 5-10 minutes working at a moderate speed).

To run your own instance of the bot, first clone this repository to your local machine. I prefer to use git in the command prompt but how you do this is entirely up to you (this will be a necessity later though, so I advise getting it downloaded and set up). Next you're going to want to go to [Heroku](https://www.heroku.com/) and create an account. It's free, you don't have to pay anything up front. There's a quickstart guide for working with python that's a nice to read at [Guide](https://devcenter.heroku.com/articles/getting-started-with-python). Give it a skim before going to deployment.

Navigate to the location that you have cloned the repository to. You can run `heroku create` in the command line. While you can run it with a specific name in mind, I just let it generate names because they're sometimes a little whacky and always fun to read :) This will run the create function, and will generate an application under your heroku account. Mind that there are steps in between that I am skipping such as signing in and the like as they have been mentioned in the python quickstart guide linked above.

Go to your heroku account in a browser, and find your dashboard. You should now see a new application under it. Click on the application, and add "Heroku Postgres" as an add-on. It's free and shouldn't charge you anything. After it's been added, you can click on the link in the dashboard to launch the management screen. It'll generate a database for you, and will give you some login details under the settings tab when you click on the "View Credentials". We'll use these in a second.

Before you go further though, you're going to have to change some stuff to make the bot your own. Open up the .py file that's in the folder in a text editor of some sort. Scroll all the way to the bottom and look at the last line of code. Within the quotes, you'll have to put in your own Bot token. You can find out how to do this here: [DiscordPy Docs](https://discordpy.readthedocs.io/en/latest/discord.html). Now scroll back up to the top of the file, and look for a peice of code that asks for:
* Host
* User
* password
* database

You'll have these details from the heroku postgres dashboard. Copy and paste them inside the quotes. Save the document and exit.

#### **Now for the really fun part**

Run the command `git push heroku main` in command line (while you're in the folder with all the files). It'll push your file to the servers where it can be run and kept online! After a bunch of really cool output statements in the command line, you should be online and good to go!

Try running the command `heroku ps` to check how many dynos your app is running on. If it says that there are no dynos assigned then run the command `heroku ps:scale worker=1` to assign one (1) dyno to the application. It'll also give you the number of server hours left for your application. Try to leave the application running on a single dyno if you want it to be up as long as possible. The performance won't suffer as long as you're not reading and writing huge quantities of data at once.

If your the bot goes offline for some reason, navigate to the source folder in the command prompt and run `heroku logs --tail` to get a log readout. This alone is usually able to give you a good enough idea of what's going on (maybe some information is wrong).

That's it! It's a little long winded but it should get you up to speed on how to deploy this bot effectively!
