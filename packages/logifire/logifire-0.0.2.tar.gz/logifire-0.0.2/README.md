# Logifire v0.0.2

Simplifying the use of logs based on build-in logging.

## Main features

* The ability to configure a pause in sending messages, even if the service is running on different servers.
* Modern log message formatting with Python `format` way
* Support for any handlers based on the logging.Handler
* Slack handler

## Install

    pip install logifire

## Minimal example

```python
from logifire import Logifire

log = Logifire()  # init log with stderr handler by default

log.debug("Test arg='{}' and kwargs: foo='{foo}', bar='{bar}'", "first arg", foo="fval", bar="bval")
# 2022-05-27T23:27:42.721 28696   [DEBUG   ] main.<module>: Test arg='first arg' and kwargs: foo='fval', bar='bval'
```

## Post-configuration example

```python
# shared/config.py

import logging
from logifire import Logifire, Logbranch

log = Logifire(branches=[
    logging.FileHandler('main.log')
])
```
```python
# some_service/config.py

import logging
from logifire import Logbranch
from logifire.handlers import SysLogifireHandler

from shared.config import log

log.set_name('some_service')  # set name for logger
log.set_level(logging.INFO)   # set global level
log.add(                      # add syslog for only warnings
    Logbranch(SysLogifireHandler(), level=logging.WARNING)
)
```

## Example with log mute feature

This example sets up a Logifire (DEBUG as main level) with a Syslog handler and a Slack handler with a 5-second mute using Memcached.

This allows all DEBUG-level messages to be written to syslog and CRITICAL level messages to be sent to the Slack channel, but no more than once every 5 seconds.
Since Memcached (in this case) is used as the backend for mute, it'll work across the entire cluster if the service is running on multiple servers.

```python
import logging

from logifire import Logifire, Logbranch
from logifire.blowout import BlowoutMemcached
from logifire.handlers import SysLogifireHandler, SlackLogifireHandler

log = Logifire(
    name='my_service',  # your service name
    level=logging.DEBUG,  # main log level
    branches=[
        Logbranch(SysLogifireHandler()),  # add Syslog handler, you can use any logging.Handler
        Logbranch(  # add Slack handler
            handler=SlackLogifireHandler("<token>"),
            level=logging.CRITICAL,  # send only critical messages to Slack
            blowout_seconds=5  # after sending a message, mute the sending for 5 seconds
        )
    ],
    blowout=BlowoutMemcached([('127.0.0.1', 11211)])  # use Memcached for the mute feature (pymemcache lib required)
)

log.debug("Test debug message")  # send to syslog
log.info("Test info message")  # send to syslog
log.critical("Test critical message")  # send to syslog and slack
```

Copyright (C) 2022 by Dmitry Parfyonov <parfyonov.dima@gmail.com>  
MIT License, see http://opensource.org/licenses/MIT
