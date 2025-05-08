# BlueSky Follow

This script follows all accounts that follows another account.

## Instructions

Install atproto to run the script:

```sh
python3 -m pip install atproto
```

Set the `own_account`, `own_password` and `other_account` variables in the script.

Run `follow.py` and enjoy following lots of new accounts!

> [!NOTE]
> Note: Since the BlueSky API is rate limited, this script only follows
> ~1800 accounts/h, so it might take a while to run it if `other_account` is
> followed by a lot of users.

