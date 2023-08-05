__version__ = '0.1.0'

import requests

# Privacy Settings: 0 (Public), 1 (Unlisted)
def paste(api_key:str, content:str, title:str, privacy:str="0", expiry:str="N", raw:int=0, format:str="gettext"):
  """
# PasteBinPy
> An easy to learn, use, and contribute to api for python.
---

## Getting Started
> To get your pastebin api key, create or login to your pastebin account [here](https://pastebin.com/signup)
>> after creating your account, [head over to the api documentation](https://pastebin.com/doc_api) and grab your api key under `Your Unique Developer API Key`
---
## Example
```py
import pastebinpy as pbp

# All thats needed for a successfull response
pbp.paste("api_key", "title", "body")

pbp.paste("api_key", "title", "body", raw=1, expiry="10M", privacy="1", format="python")
```

## `pastebinpy.paste()`
**API_KEY** can be retrieved by making a pastebin account and getting your api key from [this link](https://pastebin.com/doc_api)

**CONTENT** is the *body* of the paste, the inside that your user will be looking at.

**TITLE** is at the top of the paste, users will probably not notice this, but its a good attribute to still use.

**PRIVACY** has two values, `0` being public, and `1` being unlisted, meaning only people with the pastebin link can view it.

**EXPIRY** is defining the expiration time and/or time limit that you give your paste. Allowed variables are below.

```
N = Never
10M = 10 Minutes
1H = 1 Hour
1D = 1 Day
1W = 1 Week
2W = 2 Weeks
1M = 1 Month
6M = 6 Months
1Y = 1 Year
```

**RAW** is the toggle attribute for obtaining a raw pastebin link, with `1` equaling the raw pastebin link, and `0` being the default, returning the normal pastebin link.

**FORMAT** is the selected language attribute to format and color the content given. `(e.g HTML, PHP, LUA, PYTHON, BF, CSS, CPP, CSHARP, RUBY, RAILS, etc)`

---
Created by css / cesiyi
  """
  
  req = requests.post(
    "https://pastebin.com/api/api_post.php", 
    data = {
      "api_dev_key": api_key,
      "api_paste_expire_date": expiry,
      "api_user_key": None,
      "api_option": "paste",
      "api_paste_code": content,
      "api_paste_private": privacy,
      "api_paste_name": title,
      "api_paste_format": format
    }
  )
  if raw == 0:
    return req.text
  else:
    return (req.text).replace("pastebin.com/", "pastebin.com/raw/")