# This script follows all followers of another account.
# Since the API is rate-limited it follows ~1800 accounts/h.
from atproto import Client
import time

own_account = ""
own_password = ""
other_account = ""

min_followers = 50

client = Client()
client.login(own_account, own_password)
cursor = ""
currently_following = []
while True:
    page = client.get_follows(actor=own_account, cursor=cursor)
    currently_following += list(map(lambda f: f.did, page.follows))
    if page.cursor == None:
        break
    cursor = page.cursor

print(f"{own_account} is currently following {len(currently_following)} accounts.")

cursor = ""
followed = 0
skipped_following = 0
already_following = 0

while True:
    data = client.get_followers(actor=other_account, cursor=cursor)
    users = data.followers
    for user in users:
        did = user.did
        if min_followers > 0:
            profile = client.get_profile(actor=did)
            if profile.followers_count < min_followers:
                skipped_following += 1
                continue
        if did in currently_following:
            already_following += 1
            continue
        followed += 1
        client.follow(did)
        time.sleep(3)
    if data.cursor == None:
        break
    cursor = data.cursor
    print(f"Cursor: {cursor}")

print(f"Done! Followed {followed} accounts.")
print(f"Already followed {already_following} accounts.")
print(f"Skipped following {skipped_following} accounts due to too low follower count (<{min_followers}).")

