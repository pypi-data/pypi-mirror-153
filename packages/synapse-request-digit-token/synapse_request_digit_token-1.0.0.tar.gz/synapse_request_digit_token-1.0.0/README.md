# Request Digit Token

A Campgrounds Synapse module that generates an n-digit verification code when signing up through email.

## Installation

From the virtual environment that you use for Synapse, install this module with:
```shell
pip install path/to/synapse-request-digit-token
```
(If you run into issues, you may need to upgrade `pip` first, e.g. by running
`pip install --upgrade pip`)

## Config

Add the following to your homeserver configuration under `modules`:
```yaml
modules:
  - module: request_digit_token.RequestDigitToken
    config:
      # The length of the digit token.
      token_length: 6
      # How long before the digit token expires.
      token_lifetime: "1h"
```

## Routes

This module exposes two HTTP routes for requesting and validating a digit token:

### Request Token

Sends an n-digit token to the specified email.

**URL**
```
POST /_synapse/client/register/email/requestToken
```

**Data Params**
- `email` - The signup email.
- `client_secret` - The client secret.
- `send_attempt` - The number of request attempts.
```json
{
   "email": "test@mailer.com",
   "client_secret": "test_secret",
   "send_attempt": 1
}
```

**Response**

Status: 200 OK
```json
{
   "sid": "wcgdeXSQmlODwfDB"
}
```

Status: 400 Bad Request, 500 Server Error
```json
{
    "errcode": "",
    "error": ""
}
```

### Validate Token

Validates the token from the client.

**URL**
```
GET /_synapse/client/register/email/validateToken
```

**Query Params**
- `token` - The digit token.
- `client_secret` - The client secret.
- `sid` - The session id.
```
?token=123456&client_secret=test_secret&sid=wcgdeXSQmlODwfDB
```

**Response**

Status: 200 OK
```json
{}
```

Status: 400 Bad Request, 500 Server Error
```json
{
    "errcode": "",
    "error": ""
}
```

## Development

In a virtual environment with pip ≥ 21.1, run
```shell
pip install -e .[dev]
```

To run the unit tests, you can either use:
```shell
tox -e py
```
or
```shell
trial tests
```

To run the linters and `mypy` type checker, use `./scripts-dev/lint.sh`.


## Releasing

The exact steps for releasing will vary; but this is an approach taken by the
Synapse developers (assuming a Unix-like shell):

 1. Set a shell variable to the version you are releasing (this just makes
    subsequent steps easier):
    ```shell
    version=X.Y.Z
    ```

 2. Update `setup.cfg` so that the `version` is correct.

 3. Stage the changed files and commit.
    ```shell
    git add -u
    git commit -m v$version -n
    ```

 4. Push your changes.
    ```shell
    git push
    ```

 5. When ready, create a signed tag for the release:
    ```shell
    git tag -s v$version
    ```
    Base the tag message on the changelog.

 6. Push the tag.
    ```shell
    git push origin tag v$version
    ```

 7. If applicable:
    Create a *release*, based on the tag you just pushed, on GitHub or GitLab.

 8. If applicable:
    Create a source distribution and upload it to PyPI:
    ```shell
    python -m build
    twine upload dist/request_digit_token-$version*
    ```

