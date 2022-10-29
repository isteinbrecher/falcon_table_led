#!/bin/bash
arduino-cli upload -v -p /dev/ttyACM0 --fqbn arduino:avr:uno table_controller.ino 
