# drf-temptoken

DRF temporary authentication token

## Installation 
```bash
pip install drf-temptoken
```

## Usage
Include drf_temptoken in INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...,
    'drf_temptoken'
]
```
Add drf_temptoken.auth.TempTokenAuthentication into your authentication classes 
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drf_temptoken.auth.TempTokenAuthentication',
    )
}
```

Create token for user 

```python
from django.contrib.auth import get_user_model
from drf_temptoken.utils import create_token, get_user_tokens

User = get_user_model()

user = User.objects.first()

token = create_token(user)

# Sets token's expiration date to current
token = token.expire()

key = token.key # Used in authentication process

tokens = get_user_tokens(user) # Returns a queryset of TempTokens belonging to the user

```

Default settings (can be overriden in Django's settings)

```python
TMP_TOKEN_HEADER_PREFIX = 'TMP'

TMP_TOKEN_AUTH_HEADER = 'Authorization'

# Set any value in order to get the token from query
TMP_TOKEN_QUERY_PARAM = None



# Python's timedelta kwargs passed in order to set token's expiration date
TMP_TOKEN_TIME_DELTA_KWARGS = {
    'days': 7 # Token will be expired in 7 days by default
}
```

Auth backend will check for HTTP_AUTHORIZATION: TMP {token} by default

Assuming your token (token.key) is equal to "123", your request should look like this:

```python
import requests

headers = {
    'Authorization': 'TMP 123'
}

response = requests.get(url, headers=headers)
```

Or like this if you set query param to _api_key:

```python
import requests

url = 'https://example.com?_api_key=123'

response = requests.get(url)

```
