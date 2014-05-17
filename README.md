# wikitweets

Twitter bots about Wikipedia, Wikimedia Commons and other wikis


## How to register a Twitter bot account?

Follow these steps:

1. Go to https://twitter.com and register a nickname for your bot
2. Go to https://apps.twitter.com and create an APP. The callback URL is not needed and the website URL can be modified later. In the "Permissions" tab, give Read and Write permissions. As of May 2014, that will ask you for a phone number and send a verification code. If you don't want to do this, do this Step 2 from a Smartphone/Tablet. (Read this https://dev.twitter.com/discussions/26174 and the tip by @UAlanbari)
3. In the "API keys" tab you will find the API key and the API secret, write both in a file named .twitter_keys with the folowwing structure: API_KEY = xxxxxx (newline) API_SECRET = xxxxxxxxxxxx
5. Now use the login.py script to get the tokens: python login.py. That will use .twitter_keys and show a link that you have to open in web browser. A code number will be displayed which you have to write in console, answering the question.
6. Two tokens will be printed, save them in a file named .twitter_tokens with the following structure: OAUTH_TOKEN = xxxxxxxxxx (newline) OAUTH_TOKEN_SECRET = xxxxxxxxxx

Now you can run your Twitter bot.
