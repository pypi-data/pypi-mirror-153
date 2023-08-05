![logo](https://raw.githubusercontent.com/elieltonkremer/logos_cdi/main/logo.svg)

[![Upload Python Package](https://github.com/elieltonkremer/logos_cdi/actions/workflows/python-publish.yml/badge.svg)](https://github.com/elieltonkremer/logos_cdi/actions/workflows/python-publish.yml)

Simple and powerful python container dependency injection module


## installation

```bash
> poetry add logos_cdi
```

## usage

create `main.py` file and create `logos_cdi.application:Application` instance with a modules for usage.

```py

from logos_cdi.application import Application


app = Application([
    'logos_cdi',
    'logos_cdi.command'
])

```

in your terminal with venv actived type `logos -h` command and press enter.

```

> logos -h
usage: logos [-h] {} ...

options:
  -h, --help  show this help message and exit

command:
  {}          command to execute

```

this is your app's command manager all your commands you can see here

PS. your commands are loaded from the modules used in the application, you can implement them, see `./logos_cdi/command.py` file to understand how to create a module.
