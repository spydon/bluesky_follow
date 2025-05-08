# BlueSky Follow

This script follows all accounts that follows another account.

## Instructions

Install atproto to run the script:

```sh
python3 -m pip install atproto
```

Set the `own_account`, `own_password` and `other_account` variables in the script.
Set `min_followers` to make sure that you only follow accounts with at least
`min_followers` amount of followers.

Run `follow.py` and enjoy following lots of new accounts!

> [!NOTE]
> Note: Since the BlueSky API is rate limited, this script only follows
> ~1200 accounts/h, so it might take a while to run it if `other_account` is
> followed by a lot of users.

