# This script follows all followers of another account.
# Since the API is rate-limited it follows ~1800 accounts/h.
from atproto import Client
import ast
import time
import os

own_account = ""
own_password = ""

client = Client()
client.login(own_account, own_password)
cursor = ""
# This should contain all the accounts that you are following or have followed
# before running this script, so that you don't follow the same accounts again
# after unfollowing them.
following = set()
following_uri = {}
followers = set()
filename = f"following-{own_account}.txt"

if os.path.exists(filename):
    print(f"Used content from {filename}")
    with open(filename, "r") as file:
        content = file.read()
        following = ast.literal_eval(content)

while True:
    page = client.get_follows(actor=own_account, cursor=cursor)
    following.update(set(map(lambda f: f.did, page.follows)))
    following_uri.update({f.did: f.viewer.following for f in page.follows})
    if page.cursor == None:
        break
    cursor = page.cursor
    print(f"{cursor} next")
    time.sleep(2)

print(f"{own_account} is currently following {len(following)} accounts.")

try:
    cursor = ""
    while True:
        page = client.get_followers(actor=own_account, cursor=cursor)
        followers.update(set(map(lambda f: f.did, page.followers)))
        if page.cursor == None:
            break
        cursor = page.cursor
        print(f"{cursor} next")
        time.sleep(4)

    print(f"{own_account} currently has {len(followers)} followers.")

    not_following_us = following - followers
    unfollowed = 0
    print(f"Starting to unfollow {len(not_following_us)} accounts.")

    for did in not_following_us:
        uri = following_uri[did]
        client.delete_follow(uri)
        unfollowed += 1
        time.sleep(4)
except Exception as error:
    print(f"Something went wrong, probably rate limiting.\n{error}")
else:
    print(f"Done! Unfollowed {unfollowed} accounts.")
finally:
    with open(filename, 'w', newline='') as file:
        file.write(str(following))

