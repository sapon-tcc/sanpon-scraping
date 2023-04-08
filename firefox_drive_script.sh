
#!/bin/bash

sudo apt-get update
sudo apt-get install firefox -y
wget https://github.com/mozilla/geckodriver/releases/download/vX.XX.X/geckodriver-vX.XX.X-linux64.tar.gz
tar -xvzf geckodriver-vX.XX.X-linux64.tar.gz

dir_atual = pwd
echo $dir_atual/geckodriver
export PATH=$PATH:$dir_atual/geckodriver

sudo apt-get install python3-selenium -y





