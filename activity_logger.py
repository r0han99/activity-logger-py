#!/Users/rohan/opt/anaconda3/bin/python

from ast import arg
import sys 
import os
import argparse
import numpy as np
import pandas as pd
import datetime
import csv

from sqlalchemy import desc


# SCRIPT VERSION
VERSION = 1.0



# Global Day Counter : Initial 
try:
    records = pd.read_csv('./archive/logdata.csv').drop('Unnamed: 0',axis=1)
except: 
    records = pd.read_csv('./archive/logdata.csv')
try:
    day = records['DAY'][-1:].values[0]
except:
    day = 0


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

    
    global day 
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") 
    day = day+1
    idnum = idgen('./archive/logdata.csv')
    task = '; '.join(list(map(str.capitalize, args.tasks.split('-'))))
    template = "[{}] x {} -- ({}) -- day=[{}], files-created:{}".format(idnum,date,task,day,args.info)
    display_template =  "[{}] -- ({}) -- day=[{}]".format(idnum,task,day)

    packet = {"TID":idnum, "DATE":date, "DAY": day, "TASK":task, "DETAILS": info}

    return packet, template, display_template


def write_data(packet,records,template):

    # Write Data into DataFrame
    row = list(packet.values())
    # print(row)
    records.loc[len(records.index)] = row
    records.to_csv('./archive/logdata.csv')

    # Logfile
    with open(f'./archive/tasksequence.log','a+') as f:
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



parser = argparse.ArgumentParser()
parser.add_argument("--init", help='Initialise Setup.', action='store_true')
parser.add_argument("-t", "--tasks", type=str, help='Enter all the key-topics formatted with hypens("-").')
parser.add_argument("-i", "--info", type=str, help="Input Y/N to enter additional details in the catalog.", choices=['Y','N','y','n'])
parser.add_argument("--backup", type=str, help='backup.',choices=['partial','absolute', 'par','abs'])
parser.add_argument('--version', action='version', version=f'- %(prog)s (V{VERSION})')
                    
args = parser.parse_args()



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
    
    packet, template, display_template = package_details(args.tasks, args.info)
    print(display_template)
    
    packet['DETAILS'] = 'n'
    write_data(packet,records,template)
    
    print('logged')

    if not funcs['info'] == None:

        if args.info in ['Y','y']:
            
            idnum = packet['TID']
            print(f'-- Additional Content [{idnum}]-- ')
            content = input('Enter content to be entered: ')
            print(f'File Created - {idnum}.txt')
            with open(f'./archive/details/{idnum}.txt','w') as f:
                f.write(content)
            
            print('Addtional content logged')
            

elif not funcs['backup'] == None:

    if args.backup == 'partial':

        print('Partial Backup')
        
    
    elif args.backup == 'absolute':

        print('Absolute Backup')

    else:
        print('Invalid Backup type')


elif args.init:

    # check if the archive/ logdata.csv and tasksequence.log exists; if Yes then terminate else establish

