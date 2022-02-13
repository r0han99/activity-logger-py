#!/bin/bash


echo "Instantiating Logger Functionality"
echo "Establishing assets."


# storing the file path
logger_script="$(pwd)/activity_logger.py"


# Creating a executables folder 
mkdir ~/activity_logger
mkdir ~/activity_logger/bin

executables_dir="~/activity_logger/bin/"

# cp itself to that bin
chmod +x ./loggerpy.sh
cp ./loggerpy.sh $executables_dir


echo "Setting up executables folder. Exporting .."
export PATH=$PATH":$executables_dir"

echo "Command loggerpy Available."

# echo "Forging the command"

# writing to .profile and .bash_profile
# echo 'export PATH=$PATH":$executables_dir"' >> ~/.profile
# echo 'export PATH=$PATH":$executables_dir"' >> ~/.bash_profile





