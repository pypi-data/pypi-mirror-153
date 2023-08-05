# Changelog

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2021-07-21

### Added

- Select which databases to backup in `[MySQL]` configuration

### Changed

- Now uses blulib for parsing configuration

### Fixed

- Now uses `address` and `port` in `[MySQL]` configuration

## [0.1.0] - 2021-07-04

### Breaking changes

- Moved configuration from `config.py` into ini-like configuration `~/.backup-runner.cfg`

### Changes

- Using tealprint to log messages

## [0.0.4] - 2021-04-01

### Fixed

- Fix license in setup package

## [0.0.3] - 2021-01-17

### Added

- Colored logger
- Logging capabilities

### Changed

- Modified diffs only works on files, not entire directories
- Does not follow symlinks
- Removed spaces in backup files

### Fixed

- MySQL backup extension .sql
- Fixed daily, weekly, and monthly backups
- Fixed FileNotFoundError when a file/dir is removed while indexing

## [0.0.2] - 2021-01-17

### Fixed

- `config.example.py` now has correct string examples
- MySQL `--all-databases` instead of `--all-databeses`

## [0.0.1] - 2021-01-17

### Added

- Backup
  - Daily full backups
  - Weekly full backups with daily diffs
  - Monthly full backups with weekly and daily diffs
  - MySQL daily backups
- Remove old backups
- Mail user if backups failed
- Mail user if backup disk drive is almost full
- Force a full backup with `--full-backup`
