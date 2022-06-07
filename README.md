# rob - remove old backups

[![CI](https://github.com/deeagle/rob/actions/workflows/ci.yml/badge.svg)](https://github.com/deeagle/rob/actions/workflows/ci.yml)
[![Release version](https://github.com/deeagle/rob/actions/workflows/release.yml/badge.svg)](https://github.com/deeagle/rob/actions/workflows/release.yml)

Very simple implementation of a configurable backup management (file-level).

## Config

It's very basic and supports one folder with files and prefix only.
You can config the following keys:

```ini
# config.ini
[Common]
keep_files: 10
keep_path: /tmp/
keep_file_prefix: db-backup
```

## Usage

Supported commands are:

- `-h` for help
- `-d` for active deletion mode (*dry run* is default)

There is a `docker-compose.yml` for local testing.

## Links

- [CHANGELOG](CHANGELOG.md)
