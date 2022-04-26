# TrapBot

> It's a trap!

Tells you that it's a trap. Send pics to the bot to suggest new pics.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)

## Install

```console
$ # Install Python3 somehow
$ pip3 install --user -r requirements.txt
```

That should be it.

## Usage

- Copy `secret_template.py` to `secret.py`
- Create your bot
    * This means you have to talk to the `@BotFather`: https://web.telegram.org/z/#93372553
    * Do `/newbot`, edit it as much as you like (i.e. description, photo)
    * For the commands, paste the following as-is:
      ```
      trap - The bot will tell you that it's a trap!
      ```
    * Copy the API token
    * Invite him into the group chat(s) you like
- Fill in your own username and the API token in `secret.py`
- Run `bot.py`. I like to run it as `./bot.py 2>&1 | tee bot_$(date +%s).log`, because that works inside screen and I still have arbitrary scrollback.
- You can Ctrl-C the bot at any time and restart it later. The "state" is the directory `trap_pics/`.
- The bot will ask you about new traps; click the corresponding "/accept_0123456789" or "/reject_0123456789" command to accept or reject a pic.

## Structure

The directory `trap_pics/` contains:
- The magic file `.TRAP_PICS`, which must contain the string `RIGHT HERE\n` (where the `\n` is the "newline byte"). This is checked on startup, to make sure all paths are expected.
- The directory `suggested`, which contains images that have been suggested. The names are random 24-byte hex strings, without extension.
      - It also contains the magic file `.keep`, which must be empty, and is mainly for git
- The directory `accepted`, which contains accepted images. This directory must be non-empty on startup.
      - It also contains the magic file `.keep`, which must be empty, and is mainly for git

## TODOs

Not much, maybe seed more pics?

## NOTDOs

Here are some things this project will definitely (probably) not support:
* Complex interactions
* More response types
* 

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/der-wopper-bot/issues/new) or submit PRs.
