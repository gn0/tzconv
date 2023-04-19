
# `tzconv`: convert a date and time to several time zones at once

This Python package provides a command-line utility to convert a `YYYY-MM-DD HH:MM` formatted date and time to several other time zones.

## Installation

```
$ git clone https://codeberg.org/gnyeki/tzconv
$ python3 -m pip install --user ./tzconv
```

## Usage

```
$ tzconv \
    -f America/New_York \
    -t America/Los_Angeles \
    -t America/Halifax \
    -t Asia/Karachi \
    -t Asia/Calcutta \
    "2023-04-25 10:00"
EDT: 2023-04-25 10:00 (America/New_York)
PDT: 2023-04-25 07:00 (America/Los_Angeles)
ADT: 2023-04-25 11:00 (America/Halifax)
PKT: 2023-04-25 19:00 (Asia/Karachi)
IST: 2023-04-25 19:30 (Asia/Calcutta)
$
```

If you have a project that spans several time zones, it is convenient to define a function for it in your `.bashrc`, `.zshrc`, or equivalent dot file, depending on what shell you use.
For example, if you are using zsh, you can add the following to `~/.zshrc`:

```sh
project_tz() {
    tzconv \
        --from-tz America/New_York \
        --to-tz America/Los_Angeles \
        --to-tz America/Halifax \
        --to-tz Asia/Karachi \
        --to-tz Asia/Calcutta \
        "$*"
}
```

Now you can reload `~/.zshrc` and use `project_tz` as a shell command:

```
$ . ~/.zshrc
$ project_tz 2023-04-25 10:00
EDT: 2023-04-25 10:00 (America/New_York)
PDT: 2023-04-25 07:00 (America/Los_Angeles)
ADT: 2023-04-25 11:00 (America/Halifax)
PKT: 2023-04-25 19:00 (Asia/Karachi)
IST: 2023-04-25 19:30 (Asia/Calcutta)
$
```

