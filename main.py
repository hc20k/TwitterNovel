import twitter                  # pip3 install python-twitter
import time
import re

# CONFIGURE (requires Twitter dev app. https://developer.twitter.com/en/apps)
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""

TWITTER_HANDLE = ""

#----------------------------------------------------------------------------
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

api.VerifyCredentials() # program will exit if keys are bad

# fetch tweets
timeline = api.GetUserTimeline(screen_name=TWITTER_HANDLE, count=9999)
print("Fetched {} tweets".format(len(timeline)))

# reverse
timeline.reverse()

# make book
tweets_html = ""

print("Creating novel...")

for status in timeline:
    text = status.text
    handle = status.user.screen_name
    name = status.user.name
    date = status.created_at_in_seconds # epoch

    date = time.strftime('%B %e, %Y at %l:%M %p', time.localtime(date))

    # parse media

    medias = "<br />"

    if status.media:
        for media in status.media:
            medias += """
                <img src="{}" alt="">
            """.format(media.media_url_https)

    # is there a better way to do this?
    tweets_html+=u"""
        <div class="tweet">
            <span class="tweet-text">{}</span>
            {}
            <div class="tweet-info">
                <span>{}</span>
                <span style="font-size:15px;font-weight:400;">@{}</span>
                <span style="float:right;">{}</span>
            </div>
        </div>
    """.format(text,medias,name,handle,date)

with open("assets/main.css") as f:
    style = f.read()

# write to file!
print("Writing to {}.html ...".format(TWITTER_HANDLE))

f = open("{}.html".format(TWITTER_HANDLE), "w")

f.write(
    """
        <style>
        {}
        </style>

        {}
    """.format(style,tweets_html)
)

f.close()

print("Done! (If everything went smoothly)")
