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


# Setup libraries for python
- Install `python3` virtual environment package
  ```bash
  sudo apt install python3-venv
  ```
- Setup virtual environment
  ```bash
  python3 -m venv <PATH TO VENV>
  ```
- Install the python packages
  ```bash
  <PATH TO VENV>/bin/pip install rpi_ws281x Flask
  ```
- Call a script that uses the python library via
  ```bash
  sudo <PATH TO VENV>/bin/python3 <PATH TO SCRIPT>
  ```

# Run the server at startup
To run the server at startup, the `run.py` script has to be added to the cronjobs.
Edit the cronjobs with (has to be sudo, otherwise the strip can not be controlled)
```bash
sudo crontab -e
```
and add the line
```
@reboot <PATH TO VENV>/bin/python3 <PATH TO REPOSITORY>/led_strip/run.py
```
