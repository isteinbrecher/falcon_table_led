# Pi setup
- Download the **Raspberry Pi Imager** from [here](https://www.raspberrypi.com/software/)

## Headless setup
- For headless setup set the necessary WIFI and ssh options before writing the image to the flash drive

## Setup with a monitor
- Start the pi and change the password (default `raspberry`) with `passwd`, be aware that the default keyboart is `UK`.
- Enable `ssh` with (under `Interface Options / SSH`)
  ```bash
  sudo raspi-config
  ```
- Get the ip adress with `ip addr show` or alternatively use the script `find-pi.sh`.


## Setup OS
- Update packages:
  ```bash
  sudo apt update
  sudo apt upgrade
  ```
- Add the public ssh key to `.ssh/authorized_keys`.

# Setup python libraries

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
