# customlib

A few tools for day to day work.

---

## Available tools:

<details>
<summary>CfgParser</summary>
<p>

```python
from customlib.config import cfg
from customlib.constants import CONFIG, DEFAULTS, BACKUP
# or
# from customlib.config import CfgParser
# cfg = CfgParser()


# feeding config parameters
cfg.set_defaults(**DEFAULTS)
cfg.open(file_path=CONFIG, encoding="UTF-8", fallback=BACKUP)

# we're parsing cmd-line arguments
cfg.parse()

# we can also do this...
# cfg.parse(["--logger-debug", "True", "--logger-handler", "file"])
```

Constants can be overridden or even better you can bring your own:

- `CONFIG` - Is the configuration file set by default to your project's path.
- `DEFAULTS` - Holds `ConfigParser`'s default section parameters.
- `BACKUP` - Is the configuration default dictionary to which we fallback if the config file does not exist.

```python
# module: constants.py

from os.path import dirname, join
from sys import modules

DIRECTORY: str = dirname(modules["__main__"].__file__)

# default config file
CONFIG: str = join(DIRECTORY, "config", "config.ini")

# config default section
DEFAULTS: dict = {
    "directory": DIRECTORY,
}

# backup configuration
BACKUP: dict = {
    "FOLDERS": {
        "logger": r"${DEFAULT:directory}\logs"
    },
    "LOGGER": {
        "name": "customlib.log",
        "handler": "console",  # or "file"
        "debug": False,
    },
}
```

To pass cmd-line arguments:
```
X:\path\to\project> python -O script-name.py --section-option value --section-option value
```
cmd-line args have priority over config file and will override the cfg params.

Because it inherits from `ConfigParser` and with the help of our converters we now have
four extra methods to use in our advantage.

```python
some_list = cfg.getlist("SECTION", "option")
some_tuple = cfg.gettuple("SECTION", "option")
some_set = cfg.getset("SECTION", "option")
some_dict = cfg.getdict("SECTION", "option")
```

The configuration files are read & written using `FileHandle` (see `customlib.handles`),
a custom context-manager with thread & file locking abilities.

</p>
</details>

<details>
<summary>Logger</summary>
<p>

```python
from customlib.logging import log
# or
# from customlib.logging import Logger
# log = Logger()


log.debug("Testing debug messages...")
log.info("Testing info messages...")
log.warning("Testing warning messages...")
log.error("Testing error messages...")
```

By default debugging is set to False and must be enabled to work.
See CfgParser section for this.

</p>
</details>

---

## NOTE:

**Documentation is not complete...**

**More tools to be added soon...**

**Work in progress...**

---
