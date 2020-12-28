# Pi setup

- Download the **Raspberry Pi OS Lite** image from [here](ihttps://www.raspberrypi.org/software/operating-systems/).
- Unzip the image and copy it to the sd card via
  ```bash
  sudo dd if=<PATH TO IMG> of=/dev/<SD CARD> status=progress bs=4M
  ```
- Start the pi and change the password (default `raspberry`) with `passwd`, be aware that the default keyboart is `UK`.
- Enable `ssh` with (under `Interface Options / SSH`)
  ```bash
  sudo raspi-config
  ```
- Update packages:
  ```bash
  sudo apt update
  sudo apt upgrade
  ```
- Get the ip adress with `ip addr show` or alternatively use the script `find-pi.sh`.


# Setup libraries for WS2812B
- Install `python3` virtual environment package
  ```bash
  sudo apt install python3-venv
  ```
- Setup virtual environment
  ```bash
  python3 -m venv <PATH TO VENV>
  ```
- Install the python package for the led strip
  ```bash
  <PATH TO VENV>/bin/pip install rpi_ws281x
  ```
- Call a script that uses the python library via
  ```bash
  sudo <PATH TO VENV>/bin/python3 <PATH TO SCRIPT>
  ```
