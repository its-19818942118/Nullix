# TODO List for Nullix Project 🚀

## General Tasks 🛠️

- [X] Set up project structure 🔴✅
- [X] Configure logging with RichHandler 🔴✅
- [ ] Implement base classes and interfaces 🔴🔄
- [ ] Add support for package installation from a Git repository 🔴🔄
- [ ] Add support for package installation from a local directory 🔴🔄
- [ ] Fix better visualization of the package installation process for both GUI and CLI 🔴🔄

## Package Management 📦

- [ ] Implement package installation for:
  - [X] Arch Linux 🔴✅
  - [ ] NixOS 🔴🔄
  - [ ] Debian 🔴🔄
- [X] Add support for AUR packages in Arch Linux 🔴✅
- [X] Handle package availability checks 🔴✅

## Configuration ⚙️

- [X] Load distribution configurations from YAML file 🔴✅
- [ ] Add support for custom configuration files 🔴🔄
- [ ] Validate configuration keys 🔴🔄
- [ ] Handle configuration errors 🔴🔄

## Exception Handling 🚨

- [X] Define custom exceptions:
  - [X] `NullixError` 🔴✅
  - [X] `DistroNotSupportedError` 🔴✅
  - [X] `PackageInstallationError` 🔴✅
  - [X] `PackageUpdateError` 🔴✅
  - [X] `ConfigurationError` 🔴✅

## Commands Execution 🖥️

- [X] Implement command classes:
  - [X] `InstallCommand` 🔴✅
  - [X] `UpdateCommand` 🔴✅
  - [X] `RunCommand` 🔴✅
  - [ ] Need more commands? 🔴🔄
- [X] Ensure proper error handling in command execution 🔴✅

## Distribution Detection 🔍

- [X] Implement `DistroDetector` class 🔴✅
- [X] Use `distro` library for detection 🔴✅
- [X] Prioritize distribution family over specific ID 🔴✅

## Testing 🧪

- [ ] Write unit tests for:
  - [ ] Package management 🟠⏳
  - [ ] Configuration loading 🟠⏳
  - [ ] Command execution 🟠⏳
  - [ ] Distribution detection 🟠⏳
- [ ] Set up CI/CD pipeline for automated testing 🟠⏳

## Documentation 📚

- [ ] Write docstrings for all classes and methods 🟢⏳
- [ ] Create a README file with project overview 🟢⏳
- [ ] Add usage examples and installation instructions 🟢⏳

## Future Enhancements 🌟

- [ ] Add support for more Linux distributions 🟢⏳
- [ ] Implement parallel package installation 🔴🔄
- [ ] Optimize performance and error handling 🔴🔄

## Miscellaneous 📝

- [ ] Clean up code and remove unused imports 🔴⏳
- [ ] Refactor code for better readability and maintainability 🔴⏳
- [ ] Ensure compliance with PEP 8 standards 🟠⏳

## Priority Legend

- 🔴 **High Priority**: Critical tasks that need immediate attention
- 🟠 **Medium Priority**: Important tasks that should be addressed soon
- 🟢 **Low Priority**: Tasks that can be scheduled for later

## Status Legend

- ⏳ **Not Started**: Task has not been initiated
- 🔄 **In Progress**: Task is currently being worked on
- ✅ **Completed**: Task has been finished

## Notes

- Ensure all tasks are tested thoroughly on different environments.
- Document any issues encountered during the implementation process.
- Prioritize tasks based on their impact and urgency.
- Regularly review and update the TODO list to reflect current priorities and progress.
