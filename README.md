# SoloKeys firmware downgrade PoC

## What is this?

This repo contains a proof-of-concept which allows to downgrade a Solo with bootloader version <=3.0.1 to a previous signed firmware version.
The PoC exploits a logic bug which allowed an attacker to choose which bytes of the signed firmware were interpreted as the firmware version. The issue was fixed in [PR 368](https://github.com/solokeys/solo/pull/368).

## Running

The exploit imports code from the Solo Python library, so be sure to install its dependencies by following the setup guide in the original repo.

Download an original signed firmware (e.g. version 3.0.0) and adjust the path in the exploit (`fw_downgrade_poc.py`).
The Solo key must be in bootloader mode (hold the button while plugging it in until the LED flashes yellow).

Using this PoC we successfully downgraded a Solo running firmware (application and bootloader) version 3.0.1 to firmware 3.0.0, making the bootloader believe the firmware being flashed was 3.0.37.

## Credits & license

This repo is a fork of [solo-python](https://github.com/solokeys/solo-python). All modifications are distributed in accordance to its licensing terms.
