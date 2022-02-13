#!/Users/rohan/opt/anaconda3/bin/python

import sys 
import os
import argparse
import numpy as np
import pandas as pd
import datetime

from sqlalchemy import desc


# SCRIPT VERSION
VERSION = 1.0


# PARSER instantiation
parser = argparse.ArgumentParser()
parser.add_argument("--init", help='Initialise Setup.', action='store_true')
parser.add_argument("-t", "--tasks", type=str, help='Enter all the key-topics formatted with hypens("-").')
parser.add_argument("-i", "--info", type=str, help="Input Y/N to enter additional details in the catalog.", choices=['Y','N','y','n'])
parser.add_argument("--backup", type=str, help='backup.',choices=['partial','absolute', 'par','abs'])
parser.add_argument('--version', action='version', version=f'- %(prog)s (V{VERSION})')
                    
args = parser.parse_args()

abspath = os.getcwd()
path = os.path.join(abspath, 'archive')


# INIT
def init():
    
    global path

    # archive existence check
    if os.path.exists(path):
        print('- Archive exists')

        if os.path.exists(os.path.join(path,'logdata.csv')):
            print('- Log Database exists.')
    
        else:
            # create
            print("x Log Database doesn't exist.")
            header = "TID,DATE,DAY,TASK,DETAILS\n"
            with open(os.path.join(path,'logdata.csv'),'w') as f:
                f.write(header)
            print("- Log Database established.")
            
            

        if os.path.exists(os.path.join(path, 'tasksequence.log')):
            print('- Tasks Sequence LogFile exists.')

        else:
            # create
            print("x Task Sequence LogFile doesn't exist")
            with open(os.path.join(path, 'tasksequence.log'), 'w') as f:
                pass
            print("+ Task Sequence LogFile established.")

            
        # details folder
        if os.path.exists(os.path.join(path, 'details')):
            print('- Additional content repository exists.')
        else:
            print("x Additional content repository doesn't exist")
            os.mkdir(os.path.join(path, 'details'))
            print('+ Additional content repository established.')

            
        if args.init == True:
            print('Setup Complete, use activity_logger --help for functionality and assistance.')
        else:
            print('Setup Complete.')
        print('')
        


    else:
        
        
        # establish directory
        os.makedirs(path)
        print('- establishing the requirements.')
        # Log Database 
        header = "TID,DATE,DAY,TASK,DETAILS\n"
        with open(os.path.join(path,'logdata.csv'),'w') as f:
            f.write(header)
        print("+ Log Database established.")
    
        # LogFile
        with open(os.path.join(path, 'tasksequence.log'), 'w') as f:
            pass
        print("+ Task Sequence LogFile established.")


        # details folder
        os.mkdir(os.path.join(path, 'details'))
        print('+ Additional content repository established.')

        if args.init == True:
            print('Setup Complete, use activity_logger --help for functionality and assistance.')
        else:
            print('Setup Complete.')
        print('')


def fetch_records():
    global path 
    if os.path.exists(path):

        # Global Day Counter : Initial 
        try:
            records = pd.read_csv(os.path.join(path,'logdata.csv').drop('Unnamed: 0',axis=1))
        except: 
            records = pd.read_csv(os.path.join(path,'logdata.csv'))
        try:
            day = records['DAY'][-1:].values[0]
        except:
            day = 0

        return records, day
    else:

        print('x Missing required archive, executing --init to establish files.')
        init()
        records, day = fetch_records()
        return records, day





# create log-ID number for the datetime provided
def idgen(filepath):
    
    idnum = np.random.randint(1000,9999)

    # read-id sequence from csv
    numseq = pd.read_csv(filepath)['TID']

    while True:
        if idnum in numseq:
            idnum = np.random.randint(1000,9999)
            continue
        else:
            break
    return idnum

def package_details(tasks, info='N'):

    global path
    _, day = fetch_records()
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") 
    day = day+1
    idnum = idgen(os.path.join(path,'logdata.csv'))
    task = '; '.join(list(map(str.capitalize, args.tasks.split('-'))))
    template = "[{}] x {} -- ({}) -- day=[{}], files-created:{}".format(idnum,date,task,day,args.info)
    display_template =  "[{}] -- ({}) -- day=[{}]".format(idnum,task,day)

    packet = {"TID":idnum, "DATE":date, "DAY": day, "TASK":task, "DETAILS": info}

    return packet, template, display_template


def write_data(packet,records,template):
    global path
    # Write Data into DataFrame
    row = list(packet.values())
    # print(row)
    records.loc[len(records.index)] = row
    records.to_csv(os.path.join(path,'logdata.csv'))

    # Logfile
    with open(os.path.join(path,'tasksequence.log'),'a+') as f:
        f.write(template+'\n')

    
def backup_suggestion(day):

    if day%10 == 0:
        print('Partial backup recommended.')
    elif day%25 == 0:
        print('Full backup recommended')

    # Next Version
    # elif day%50 == 0:
    #     print('commencing Full Backup')

    else:
        pass



def silent_check():

    abspath = os.getcwd()
    path = os.path.join(abspath, '/archive')
    
    # archive existence check
    if os.path.exists(path):
        # print('- Archive Exists')

        if os.path.exists(os.path.join(path,'logdata.csv')):
            # print('- Log Database exists.')
            pass
    
        else:
            # create
            print("x \033[91m[FATAL]\033[0m Log Database doesn't exist.")
            header = "TID,DATE,DAY,TASK,DETAILS\n"
            with open(os.path.join(path,'logdata.csv'),'w') as f:
                f.write(header)
            print("- New Log Database established.")
            print("x \033[93m[WARNING]\033[0m Day Tracking Disrupted!. Day count will start from 1")

            '''
                Write a functionality or an addtional flag prompt to synchronise the day counter.
            
            '''
            
            

        if os.path.exists(os.path.join(path, 'tasksequence.log')):
            # print('- Tasks Sequence LogFile exists.')
            pass

        else:
            # create
            print("x \033[91m[FATAL]\033[0m Task Sequence LogFile doesn't exist")
            with open(os.path.join(path, 'tasksequence.log'), 'w') as f:
                pass
            print("+ Task Sequence LogFile established.")

            
        # details folder
        if os.path.exists(os.path.join(path, 'details')):
            # print('- Additional content repository exists.')
            pass
        else:
            print("x \033[91m[FATAL]\033[0m Additional content repository doesn't exist")
            os.mkdir(os.path.join(path, 'details'))
            print('+ Additional content repository established.')

            
        print('-- Proceeding')
        print('')
        
        
## ARGUMENT PROCESSING

funcs = {}
try:
    funcs['init'] = args.init
    funcs['tasks'] = args.tasks
    funcs['info'] = args.info
    funcs['backup'] = args.backup
    funcs['version'] = args.version
except:
    pass

# print(funcs)

if not funcs['tasks'] == None:
    
    # silent check for all the requirced file's existence
    silent_check()

    

    records, day = fetch_records()
    packet, template, display_template = package_details(args.tasks, args.info)
    DAY = packet['DAY']

    #backup prompt check
    backup_suggestion(DAY)
    print('+',display_template, end='--')
    
    packet['DETAILS'] = 'n'
    write_data(packet,records,template)
    
    print('\033[96m logged \033[0m')

    if not funcs['info'] == None:

        if args.info in ['Y','y']:
            
            idnum = packet['TID']
            print(f'-- Additional Content [{idnum}]-- ')
            content = input('Enter content to be entered: ')
            print(f'File Created - {idnum}.txt')
            with open(f'./archive/details/{idnum}.txt','w') as f:
                f.write(content)
            
            print('+ Addtional content',end='')
            print('\033[96m logged \033[0m')
            

elif not funcs['backup'] == None:

    # check if the logs are absolutely empty which doesn't require any backup procedure
    # check if the logfile and the logdatabase have atleast 20 Logs else prompt to override the backup procedure


    if args.backup == 'partial':

        print('Partial Backup')
        
    
    elif args.backup == 'absolute':

        print('Absolute Backup')

    else:
        print('Invalid Backup type')


elif args.init:

    # check if the archive/ logdata.csv and tasksequence.log exists; if Yes then terminate else establish
    init()



    

        
    
