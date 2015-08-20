# box-oauth2
Box OAuth2 authorization flow example

## Installation
```
pip install virtualenv
virtualenv .boxsdk
. .boxsdk/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a file called `config.cfg` in the checkout directory.

```
[main]
AUTH_URL=<Public URL of this service. Must be HTTPS.>
CLIENT_ID=<Client id from Box.>
CLIENT_SECRET=<Client secret from Box.>
```

## Usage
```
. .boxsdk/bin/activate
python redirect.py
```
