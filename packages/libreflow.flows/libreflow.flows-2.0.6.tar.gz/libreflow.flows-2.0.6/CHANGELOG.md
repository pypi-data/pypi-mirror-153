# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [Unreleased]

## [2.0.6] - 2022-06-01

### Changed

* Use `ManagedTask` and `ManagedTaskCollection` (from `libreflow.baseflow.task`) to the configuration and creation of tasks and their files.

## [2.0.5.1] - 2022-05-26

### Fixed

* Define a missing project method returning the project's action value store. It fixes the error raising when the AE playblast rendering dialog shows up and tries to call this method.

## [2.0.5] - 2022-05-17

### Added

* A default flow with the following structure: *film* > *sequence* > *shot* > *task* > *file* > *revision*.
* Whenever a shot is created, its tasks are created according to the default tasks defined in the project's task manager.

## [2.0.3] - 2022-02-04

### Added

* A Blender 3.0 file template for the TinyKin project

### Fixed

* Update of the user's last visit at login

## [2.0.2] - 2022-02-02

### Fixed

* Properly get versions of libreflow and libreflow.flows in order to make them appear on the home page.

## [2.0.1] - 2022-02-02

### Added

* A `Background` department in the shot.

### Changed

* Integrate Libreflow default file feature (2.0.1) to configure and create default files in shot departments.

## [2.0.0] - 2022-01-28

Initial commit for TinyKin project