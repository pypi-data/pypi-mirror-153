# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Fixed
- Serializer - Fixed a bug which caused the serializer to fail when given completely arbitrary integration weights
- Serializer - Fixed a bug which caused the serializer to fail when given a list of correction matrices
- Serializer - Added support for "pass" inside blocks (if, for, etc). "pass" inside "else" is not supported.
### Added
- play - Add support for continue chirp feature
- High Resolution Time Tagging - Add support for high resolution time-tagging measure process
- Input Stream - Add support for streaming data from the computer to the program
- OPD - Added missing OPD timetagging function
### Changed
- set_dc_offset - 2nd input for function was renamed from `input_reference` to `element_input`
- QuantumMachineManager will try to connect to ports 9510 and 80 if the user did not specify a port.
- set_output_dc_offset_by_element - can now accept a tuple of ports and offsets
- `signalPolarity` in the timetagging parameters (`outputPulseParameters` in configuration) now accept `Above` and `Below` instead of `Rising` and `Falling`, which better represent it's meaning.

## [0.3.6] - 2021-01-23
### Added
- `signalPolarity` in the timetagging parameters (`outputPulseParameters` in configuration) now accept also `Rising` and `Falling`, which better represent it's meaning. 
- `derivativePolarity` in the timetagging parameters (`outputPulseParameters` in configuration) now accept also `Above` and `Below`, which better represent it's meaning. 
- Add unsafe switch to `generate_qua_config` function
- Add library functions and *amp() in measure statement to `generate_qua_config` function
### Changed
- Better error for library functions as save source

## [0.3.5] - 2021-12-27
### Added
- Raises an error when using Python logical operators 
- Add elif statement to `generate_qua_config` function

### Changed
- Fix indentation problem on the end of for_each block in `generate_qua_config` function
- The `generate_qua_config` now compresses lists to make the resulting file smaller and more readable

## [0.3.4] - 2021-12-05
### Added
- :guardswoman: Define multiple elements with shared oscillator.
- :guardswoman: Define an analog port with channel weights.
- Add measure and play features to `generate_qua_config` function
- format `generate_qua_config` function output
- improve `wait_for_all_values` execution time

## [0.3.3] - 2021-10-24
### Added
- :guardswoman: Define an analog port with delay.
- :guardswoman: New `set_dc_offset()` statement that can change the DC offset of element input in real time.
- :guardswoman: New input stream capabilities facilitating data transfer from job to QUA.
- :guardswoman: New flag for stream processing fft operator to control output type.
- :page_with_curl: Add information about demod on a tuple.
- :page_with_curl: Added best practice guide.
### Changed
- Validate that element has one and only one of the available input type QMQUA-26

## [0.3.2] - 2021-10-03
### Added
- :guardswoman: QuantumMachinesManager health check shows errors and warnings.
- :guardswoman: Fetching job results indicates if there were execution errors.
- :guardswoman: Define an element with multiple input ports.
- :guardswoman: Stream processing demod now supports named argument `integrate`. If `False` is provided
the demod will not sum the items, but only multiply by weights.
### Changed
- Documentation structure and content.

## [0.3.1] - 2021-09-13
### Fixed
- Fixed serialization of IO values.
- Support running `QuantumMachinesManager` inside ipython or jupyter notebook.
### Changed
- Removing deprecation notice from `with_timestamps` method on result streams.
- Setting `time_of_flight` or `smearing` are required if element has `outputs` and
must not appear if it does not.

## [0.3.0] - 2021-09-03
### Changed
- Support for result fetching of both versions of QM Server.
- Now the SDK supports all version of QM server.

## [0.2.1] - 2021-09-01
### Changed
- Default port when creating new `QuantumMachineManager` is now `80` and user 
config file is ignored.

## [0.2.0] - 2021-08-31
### Added
- The original QM SDK for QOP 2.

## [0.1.0] - 2021-08-31
### Added
- The original QM SDK for QOP 1.

[Unreleased]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.6...HEAD
[0.3.6]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/qm-labs/qm-qua-sdk/releases/tag/v0.1.0

## Legend 
* :guardswoman: Features that are server specific and depend on capabilities and version
* :page_with_curl: Documentation only change