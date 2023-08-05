# pynnacle

> A utility class to simplify sending emails.

[![pre-commit][pre-commit-image]][pre-commit-url]
[![Imports: isort][isort-image]][isort-url]
[![Code style: black][black-image]][black-url]
[![Checked with mypy][mypy-image]][mypy-url]
[![security: bandit][bandit-image]][bandit-url]
[![licence: mit][mit-license-image]][mit-license-url]

![](assets/header.png)

## Installation

OS X & Linux:

```sh
pip3 install pynnacle
```

Windows:

```sh
pip install pynnacle
```

## Usage example

Firstly import the module

```sh
from pynnacle.pynnacle import SendEmail
```

Then instantiate the class with the initialization arguments.

```sh
mailer = SendEmail(
    user_id=user_id,
    user_pass=user_pass,
    smtp_server=server,
    smtp_port=port,
    smtp_authentication=auth,
    smtp_encryption=encrypt,
)
```

Then simply send the email

```sh
mailer.message_send(
    subject="Hi There",
    sender="sender@abc.com",
    recipient="recipient@xyz.com",
    body="This is where the text of the email body goes",
)
```

cc, bcc and attachments arguments can also be used, supplied as lists

```sh
mailer.message_send(
    subject="Hi There",
    sender="sender@abc.com",
    recipient="recipient@xyz.com",
    body="This is where the text of the email body goes",
    cc=["person1@def.com", "person2@ghi.com"],
    bcc=["person3@jkl.com", "person4@mno.com"],
    attachments=["path_to_file1", "path_to_file2"]
)
```

## Further simplifications

### Storing and Reusing SMTP

Iy you have a requirement to use multiple SMTP servers then the settings can be stored in a config file:

e.g.config.ini

```sh
[gmail]
smtp_server = smtp.gmail.com
smtp_port = 587
smtp_authentication = yes
smtp_encryption = yes
pop3_server = pop.gmail.com
pop3_port = 995
pop3_authentication = yes
pop3_encryption = yes
```

Then in your application simply specify the "service" and extract the required elements with the Python [configparser](https://docs.python.org/3/library/configparser.html) library.

```sh
import configparser

service = "gmail"

ini = configparser.ConfigParser()
ini.read("config.ini")
server = ini.get(service, "smtp_server")
port = int(ini.get(service, "smtp_port"))
auth = ini.get(service, "smtp_authentication")
encrypt = ini.get(service, "smtp_encryption")
```

### Storing credentials

To avoid hard-coding any credentials I use the Python [keyring](https://github.com/jaraco/keyring) library

```sh
service = "gmail"

user_id = keyring.get_password(service, "service_id")
user_pass = keyring.get_password(service, "service_password")
```

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
pip install --editable pynnacle
```

## Documentation

[**Read the Docs**](https://pynnacle.readthedocs.io/en/latest/?)

## Meta

[![](assets/linkedin.png)](https://linkedin.com/in/stephen-k-3a4644210)
[![](assets/github.png)](https://github.com/Stephen-RA-King/Stephen-RA-King)
[![](assets/www.png)](https://www.Stephen-RA-King)
[![](assets/email.png)](mailto:stephen.ra.king@gmail.com)

Author: Stephen R A King

Distributed under the MIT License. See `LICENSE` for more information.

<!-- Markdown link & img dfn's -->

[pre-commit-image]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[isort-image]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
[isort-url]: https://pycqa.github.io/isort/
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[bandit-image]: https://img.shields.io/badge/security-bandit-yellow.svg
[bandit-url]: https://github.com/PyCQA/bandit
[mypy-image]: http://www.mypy-lang.org/static/mypy_badge.svg
[mypy-url]: http://mypy-lang.org/
[mit-license-image]: https://img.shields.io/badge/license-MIT-blue
[mit-license-url]: https://choosealicense.com/licenses/mit/
[wiki]: https://github.com/Stephen-RA-King/pynnacle/wiki
