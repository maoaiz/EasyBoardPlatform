#!/bin/bash
sudo cp $1 /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/$2 /etc/nginx/sites-enabled/
sudo service nginx reload