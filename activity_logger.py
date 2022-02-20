#!/usr/bin/env python3.8

import shutil
import sys 
import os
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from zipfile import ZipFile
from tqdm import tqdm



# SCRIPT VERSION
VERSION = 0.0.3


# PARSER instantiation
parser = argparse.ArgumentParser()
parser.add_argument("--init", help='Initialises Archive directory structure', action='store_true')
parser.add_argument("-t", "--tasks", type=str, help='Enter all the key-topics formatted with hypens("-").')
parser.add_argument("-i", "--info", type=str, help="Input Y/N to enter additional details in the catalog.", choices=['Y','N','y','n'])
parser.add_argument("--summary", help='Displays summary of the most recent work.', action='store_true')
parser.add_argument("--backup", type=str, help='Backsup the Logdata with a dedicated timedelta.',choices=['partial','absolute'])
parser.add_argument('--version', action='version', help='Program version.', version=f'Activity Logger (actlogger) \033[96m(V{VERSION})\033[0m')
                    
args = parser.parse_args()

# print(args.init)
# print(args.info)
# print(args.tasks)
# print(args.backup)



abspath = os.getcwd()
path = os.path.join(abspath, '.archive')


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

        # backup folder
        if os.path.exists(os.path.join(path, 'backup')):
            print('- Backup repository exists.')
        else:
            print("x Backup repository doesn't exist")
            os.mkdir(os.path.join(path, 'backup'))
            print('+ Backup repository established.')

            
        if args.init == True:
            print('Setup Complete, use actlogger --help for functionality and assistance.')
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

         # backup folder
        os.mkdir(os.path.join(path, 'backup'))
        print('+ Backup repository established.')

        if args.init == True:
            print('Setup Complete, use activity_logger --help for functionality and assistance.')
        else:
            print('Setup Complete.')

            
        print('')


def fetch_records():

    global path 
    if os.path.exists(os.path.join(path,'logdata.csv')):

        # Global Day Counter : Initial 
        try:
            records = pd.read_csv(os.path.join(path,'logdata.csv').drop('Unnamed: 0',axis=1))
        except: 
            records = pd.read_csv(os.path.join(path,'logdata.csv'))
        try:
            day = records['DAY'][-1:].values[0]
        except:
            day = 0

        # secondary check 
        if 'Unnamed: 0' in records.columns:
            records = records.drop('Unnamed: 0',axis=1)
        

        return records, day
    else:

        print('x Missing required archive, executing --init to establish files.')
        init()
        print('*' * 25)
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
    date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") 
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
    path = os.path.join(abspath, '.archive')
    
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
            print('-- Proceeding')
            print('')
            
            

        if os.path.exists(os.path.join(path, 'tasksequence.log')):
            # print('- Tasks Sequence LogFile exists.')
            pass

        else:
            # create
            print("x \033[91m[FATAL]\033[0m Task Sequence LogFile doesn't exist")
            with open(os.path.join(path, 'tasksequence.log'), 'w') as f:
                pass
            print("+ Task Sequence LogFile established.")
        
            print('-- Proceeding')
            print('')

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

        # backup folder
        if os.path.exists(os.path.join(path, 'backup')):
            # print('- Additional content repository exists.')
            pass
        else:
            print("x \033[91m[FATAL]\033[0m Backup repository doesn't exist")
            os.mkdir(os.path.join(path, 'backup'))
            print('+ Backup repository established.')

            
            print('-- Proceeding')
            print('')

        '''
        Display a Note to inform the user that if at all after the FATAL prompt the data logged is not the first, then in that case
        user should be prompted to use --restore (V.2)
        
        '''
        
        
## ARGUMENT PROCESSING

funcs = {}
try:
    funcs['init'] = args.init
    funcs['tasks'] = args.tasks
    funcs['info'] = args.info
    funcs['summary'] = args.summary
    funcs['backup'] = args.backup
    funcs['version'] = args.version
except:
    pass

# print(funcs)

if not funcs['tasks'] == None:
    
    # silent check for all the requirced file's existence
    silent_check()

    # fetching records
    records, day = fetch_records()
    packet, template, display_template = package_details(args.tasks, args.info)
    DAY = packet['DAY']

    #backup prompt check
    backup_suggestion(DAY)

    # print logged information
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
            
            with open(os.path.join(path, f'details/{idnum}.txt'),'w') as f:
                f.write(content)
            
            print('+ Addtional content',end='')
            print('\033[96m logged \033[0m')
            

elif not funcs['backup'] == None:

    # check if the logs are absolutely empt
    # check if the logfile and the logdatabase have atleast 20 Logs else prompt to override the backy which doesn't require any backup procedureup procedure
    

    # to make sure everything's in place
    silent_check()

    records, _ = fetch_records()
    control = 'proceed'

    # initial checks
    if len(records) == 0:
        print('x No Records exists to be backed up.')
        control = 'halt'
    elif len(records) <= 20:
        print('~ Logs are limited, not in the optimal backup range. ')
        while True:
            flag = input('\nEnter `override` or `stop` to control : ')
            if flag == 'override':
                print('+ overriding backup, mode = ', end='')
                control = 'proceed'
                break
            elif flag == 'stop':
                print('stopping backup')
                control = 'halt'
                break
            else:
                print('x Invalid control choice!')
                
        
    if control == 'proceed':
    
        if args.backup == 'partial':
            # mode
            print('Partial')
            logdatapath = os.path.join(path, 'logdata.csv')
            tasksequencepath = os.path.join(path, 'tasksequence.log')

            
            # Generating Filename -- Time Delta
            dt = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            dt = dt.replace('.','x')
            dt = '_'.join(dt.split(' '))


            # zipping
            tqdmprompts = [logdatapath,tasksequencepath]
            arcnames = ['logdata.csv','tasksequence.csv']
            cprname = dt+'.zip'
            with ZipFile(os.path.join(path,cprname), 'w') as zipper:
                for cprfile in tqdm(tqdmprompts, desc='compressing'):
                    zipper.write(cprfile, arcname=cprfile.split('/')[-1:][0])
                    
            # move the generated zip into the backup folder
            shutil.move(os.path.join(path,cprname),os.path.join(path,'backup/'))

        
        elif args.backup == 'absolute':
            print('Absolute Backup')
            print('- under development')

       


elif args.init:

    # check if the archive/ logdata.csv and tasksequence.log exists; if Yes then terminate else establish
    init()

elif args.summary:

    # fetch records
    records, day = fetch_records()
    
    if len(records) != 0:
        print('+ \033[96mSummary\033[0m')
        print(f'- Streak - Days: [{day}]')
        print(f"- Most Recent Work - [{records['TID'].values[-1:][0]}] : [{records['TASK'].values[-1:][0]}]")
        print(f"- Date Logged- [{records['DATE'].values[-1:][0]}]")

        '''
        Additional Info exists print that 
        '''


    else:
        print('x No Records to summarise.')

elif not args.info == None:
    print('x [invalid usage] --info is used in conjuction to --tasks. try --help for assistance.')

elif args.init == False and args.backup == None and args.info == None and args.tasks == None:
    print('x Try seeking assitance with --help.') 


    

        
    
