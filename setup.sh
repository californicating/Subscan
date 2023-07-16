#!/bin/bash

# shellcheck disable=SC1009
# shellcheck disable=SC2155
# shellcheck disable=SC2092
# shellcheck disable=SC2006

export Red="$(tput setaf 1)"
export green="$(tput setaf 2)"
export yellow="$(tput setaf 3)"
export blue="$(tput setaf 4)"


if [ "$(id -u)" != "0" ]; then
  echo "${Red} [!] This script requires root privilege [run with : sudo bash setup.sh] "
  exit 1
fi

echo "${yellow}[!] Running installation script . Do not interrupt the process [!]"

# libs
apt-get install python3-requests -yy
apt-get install -y python3-urllib3 -yy
apt-get install python3 -yy
