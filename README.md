# rob - remove old backups

[![CI](https://github.com/deeagle/rob/actions/workflows/ci.yml/badge.svg)](https://github.com/deeagle/rob/actions/workflows/ci.yml)
[![Release version](https://github.com/deeagle/rob/actions/workflows/release.yml/badge.svg)](https://github.com/deeagle/rob/actions/workflows/release.yml)

Very simple implementation of a configurable backup management (file-level).

## Config

It's very basic and supports one folder with files and prefix only.
You can config the following keys:

```yml
---
# config.yml
Common:
  - keep:
    files: 10
    path: /tmp/
    file_prefix: db-backup
```

Note: currently only one (the latest) entry will be handled.

## Usage

Supported commands are:

- `-h` for help
- `-d` for active deletion mode (*dry run* is default)

There is a `docker-compose.yml` for local testing.

## Links

- [CHANGELOG](CHANGELOG.md)
