#!/bin/bash

rel_path="$(dirname ${BASH_SOURCE[0]})"
rsync -a --progress --delete --exclude ".*" $rel_path pi@10.0.0.181:/home/pi/falcon_table/.
