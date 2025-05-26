# This script follows all followers of another account.
# Since the API is rate-limited it follows ~1800 accounts/h.
from atproto import Client
import ast
import time
import os

own_account = ""
own_password = ""
other_accounts = []

min_followers = 5

client = Client()
client.login(own_account, own_password)
cursor = ""
currently_following = set()
filename = f"following-{own_account}.txt"

if os.path.exists(filename):
    print(f"Used content from {filename} as base.")
    with open(filename, "r") as file:
        content = file.read()
        currently_following = ast.literal_eval(content)

while True:
    page = client.get_follows(actor=own_account, cursor=cursor)
    currently_following.update(set(map(lambda f: f.did, page.follows)))
    if page.cursor == None:
        break
    cursor = page.cursor
    print(f"{cursor} next")
    time.sleep(4)

print(f"{own_account} is currently following {len(currently_following)} accounts.")

cursor = ""
followed = 0
skipped_following = 0
already_following = 0
other_account_index = 0
print(f"Starting with {other_accounts[other_account_index]}")

try:
    while True:
        other_account = other_accounts[other_account_index]
        data = client.get_followers(actor=other_account, cursor=cursor)
        users = data.followers
        for user in users:
            did = user.did
            if did in currently_following:
                already_following += 1
                continue
            if min_followers > 0:
                profile = client.get_profile(actor=did)
                if profile.followers_count < min_followers:
                    skipped_following += 1
                    continue
            followed += 1
            client.follow(did)
            currently_following.add(did)
            time.sleep(4)
        if data.cursor == None:
            if other_account_index + 1 < len(other_accounts):
                other_account_index += 1
                cursor = ""
                print(f"Starting with {other_accounts[other_account_index]}")
                continue
            else:
                break
        print(f"Followed {followed} accounts ({already_following} {skipped_following}).")
        cursor = data.cursor
        print(f"Cursor: {cursor}")
except Exception as error:
    print(f"Something went wrong, probably rate limiting.\n{error}")
else:
    print(f"Done! Followed {followed} accounts.")
    print(f"Already followed {already_following} accounts.")
    print(f"Skipped following {skipped_following} accounts due to too low follower count (<{min_followers}).")
finally:
    print(f"Writes down current followers to {filename}")
    with open(filename, 'w', newline='') as file:
        file.write(str(currently_following))

