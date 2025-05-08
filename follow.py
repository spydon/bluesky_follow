# This script follows all followers of another account.
# Since the API is rate-limited it follows ~1800 accounts/h.
from atproto import Client
import time

own_account = ""
own_password = ""
other_account = ""

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
while True:
    data = client.get_followers(actor=other_account, cursor=cursor)
    dids = map(lambda f: f.did, data.followers)
    for did in dids:
        if did in currently_following:
            skipped_following += 1
            continue
        followed += 1
        client.follow(did)
        time.sleep(2)
    if data.cursor == None:
        break
    cursor = data.cursor
    print(cursor)

print(f"Done! Followed {followed} accounts and skipped {skipped_following}.")

