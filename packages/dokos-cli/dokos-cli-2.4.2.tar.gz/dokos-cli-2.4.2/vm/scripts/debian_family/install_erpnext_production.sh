#!/bin/bash -eux

# Install ERPNext
wget https://gitlab.com/dokos/docli/raw/master/playbooks/install.py
python install.py --production --user frappe --mysql-root-password frappe --admin-password admin