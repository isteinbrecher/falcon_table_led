# Pi setup

- Download the **Raspberry Pi OS Lite** image from [here](ihttps://www.raspberrypi.org/software/operating-systems/).
- Unzip the image and copy it to the sd card via
  ```bash
  sudo dd if=<PATH TO IMG> of=/dev/<SD CARD> status=progress bs=4M
  ```
- Start the pi and change the password (default `raspberry`) with `passwd`, be aware that the default keyboart is `UK`.
- Enable `ssh` with `sudo raspi-config`, `Interface Options / SSH`.
- Update packages:
  ```bash
  sudo apt update
  sudo apt upgrade
  ```
- Get the ip adress with `ip addr show` or alternatively use the script `find-pi.sh`.
