#!/bin/bash

echo "Find pi in local network"
sudo arp-scan --localnet | grep "Raspberry Pi Foundation"
