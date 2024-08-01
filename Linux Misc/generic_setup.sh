#!/bin/bash

# This script was designed for Rocky 8.9, and may not work on all other Linux distributions.
# Also, you will have to replace the ip address used in the FTP section with your own to run the test.

# USER CREATION
users=("Michael" "Dwight" "Jim" "Phyllis" "Andy" "Stanley" "Pam" "Kevin" "Oscar" "Angela" "Meredith" "Creed" "Kelly" "Toby")

for user in "${users[@]}"
do
    sudo useradd "$user"
    echo "student" | sudo passwd --stdin "$user"
done

# GROUP CREATION
groups=("manager" "accounting" "sales" "support" "hr")

for group in "${groups[@]}"
do
    sudo groupadd "$group"
done

# GROUP ASSIGNMENTS
sudo usermod -aG manager Michael
sudo usermod -aG sales Dwight
sudo usermod -aG sales Jim
sudo usermod -aG sales Phyllis
sudo usermod -aG sales Andy
sudo usermod -aG sales Stanley
sudo usermod -aG accounting Kevin
sudo usermod -aG accounting Oscar
sudo usermod -aG accounting Angela
sudo usermod -aG support Pam
sudo usermod -aG support Meredith
sudo usermod -aG support Creed
sudo usermod -aG hr Kelly
sudo usermod -aG hr Toby

# DIRECTORY STRUCTURE SETUP
    # /var/www is good for web server work, and comes standard in many Linux distributions,
    # so it serves as a useful choice for the start of a directory structure.

# Make the directories
    # Creating a new directory in the home directory for this script
sudo mkdir ~/IaCProj
sudo mkdir ~/IaCProj/manager
sudo mkdir ~/IaCProj/accounting
sudo mkdir ~/IaCProj/sales
sudo mkdir ~/IaCProj/support
sudo mkdir ~/IaCProj/hr

# Set group ownership for new directories
sudo chown :manager ~/IaCProj/manager
sudo chown :accounting ~/IaCProj/accounting
sudo chown :sales ~/IaCProj/sales
sudo chown :support ~/IaCProj/support
sudo chown :hr ~/IaCProj/hr

# Set permissions so only owner and group have access
sudo chmod 770 ~/IaCProj/manager
sudo chmod 770 ~/IaCProj/accounting
sudo chmod 770 ~/IaCProj/sales
sudo chmod 770 ~/IaCProj/support
sudo chmod 770 ~/IaCProj/hr

# Give Michael and Toby full access to the entire directory structure
sudo setfacl -R -m u:Michael:rwx ~/IaCProj/
sudo setfacl -R -m u:Toby:rwx ~/IaCProj/

# WEB SERVER INSTALLATION
sudo dnf install httpd -y  # httpd is Apache, -y means auto-yes to prompts
sudo systemctl start httpd  # auto-serves files in /var/www/html
sudo systemctl enable httpd  # listens on port 80 by default

# Create a basic index.html Hello World file, or overwrite the existing index.html
    # Storing it in /var/www/html (created with Apache) should mean accessing localhost returns this page
    # Outputting to /dev/null avoids unwanted output to terminal
echo -e "\nCreating sample web page..."  # -e lets echo accept \n
echo "<html><body><h1>Hello, World from Eli!</h1></body></html>" | sudo tee /var/www/html/index.html >/dev/null

# Quick test to see if httpd is servng the new webpage correctly at localhost
echo -e "\nTesting Apache, retrieving sample page code..."
curl -sS http://localhost  # -sS will supress loading and error messages
echo  # new line

# FTP SERVER INSTALLATION
# Set up vsftpd, a common FTP server software for Linux. It will use port 21 by default
sudo dnf install vsftpd -y
sudo systemctl start vsftpd
sudo systemctl enable vsftpd

# Run a quick test on localhost to make sure the FTP server is running/listening
    # -zv is used to check ports and provide more detailed info
echo -e "\nTesting FTP server connection..."
nc -zv 127.0.0.1 21