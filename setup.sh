#!/bin/bash


# confirmation
echo "This setup presumes that you have Python-3>= pre-installed on your PC along with Pip. Enter [y/n]: "
read control

# details 
BLUE='\033[0;36m'
NC='\033[0m' # No Color


if [[ $control == 'y' ]]
then
    echo "+ Instantiating Logger Functionality"
    echo "+ Establishing assets."

    # requirements
    pip install -r requirements.txt
    
    echo "+ Done."
    
    # storing the file path
    logger_script="./activity_logger.py"

    echo -e "+ Forging Command: ${BLUE}actlogger${NC}"
    touch actlogger
    cp $logger_script actlogger

    echo "+ converting script into executable"
    echo "+ writing permissions; enter password if prompted."
    # making it into an executable
    chmod +x actlogger

    # copied into execs
    sudo cp ./actlogger /usr/local/bin/
    echo -e "+ $ ${BLUE}actlogger${NC} is now forged as a commandline tool. Please try actlogger --help to initiate usage."



else
    echo "x Please install both Python and Pip package handler."
fi
    







