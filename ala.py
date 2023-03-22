import os
from pathlib import Path
import sys
import json
import builtins
import sys
import pickle
import pandas as pd
import time
from prettytable import PrettyTable
import operator
import re
from datetime import datetime
import progressbar

VERBS = ["create", "delete", "deletecollection", "get", "list", "patch", "update", "watch"]
t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME', 'RESPONSE'])
DIRS = ["openshift-apiserver", "kube-apiserver"]
FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


def progressBar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_Length = int(round(bar_length * count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
    sys.stdout.flush()

def setInterval():
    t_start_d = input("Insert start date (AAAA-MM-DD): ")
    t_start_t = input("Insert start time (HH:MM): ")
    t_end_d = input("Insert end date (AAAA-MM-DD): ")
    t_end_t = input("Insert end time (HH:MM): ")
    #2023-03-14T23:55:00.0Z
    t_start = f"{t_start_d}T{t_start_t}:00.0Z"
    t_end = f"{t_end_d}T{t_end_t}:00.0Z"
    
    try:
        res1 = bool(datetime.strptime(t_start, FORMAT))
        res2 = bool(datetime.strptime(t_end, FORMAT))
    except ValueError:
        print("Date or time not well format (try -h to see help info)")
        exit()
    
    return [t_start, t_end]

### CHECK ALL EVENTS OF {user} IN {namespace}
def allEventsUsrNs(source_dir, user, namespace, to_f, source):
    print(f"\nCHECK ALL EVENTS OF {user} IN {namespace}...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                        if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                            t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{source}/all_events_{user}_{namespace}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### CHECK ALL EVENTS OF {user}
def allEventsUsr(source_dir, user, to_f, source):
    print(f"\nCHECK ALL EVENTS OF {user}...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    #if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                        if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                            t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'all_events_{user}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### CHECK ALL EVENTS IN {namespace}
def allEventsNs(source_dir, namespace, to_f, source):
    print(f"\nCHECK ALL EVENTS IN {namespace}...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                        #if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                        if "username" in jsonline["user"]:
                            t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{source}/all_events_{namespace}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### CHECK ALL EVENTS TBD
def allEventsTime(source_dir, to_f, source, t_start, t_end):
    print(f"\nCHECK ALL EVENTS...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    #"2023-03-14T23:55:00.0Z"
    start = datetime.strptime(t_start, FORMAT) 
    end = datetime.strptime(t_end, FORMAT) 
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    #if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                        #if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                        timestamp = datetime.strptime(jsonline["requestReceivedTimestamp"], FORMAT)
                        if "username" in jsonline["user"]:
                            if timestamp >= start and timestamp <= end:
                                t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{source}/all_events.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### CHECK {verb} EVENTS
def verb(verb, source_dir, to_f, source):

    print(f"\nCHECK {verb} EVENTS...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if jsonline["verb"] == verb:
                        #if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                            #if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                            if "username" in jsonline["user"]:
                                t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{source}/{verb}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### CHECK {verb} EVENTS of {user}
def verbUsr(verb, source_dir, user, to_f, source):

    print(f"\nCHECK {verb} EVENTS of {user}...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if jsonline["verb"] == verb:
                        #if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                            if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                                t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{source}/{verb}_{user}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### CHECK {verb} EVENTS IN {namespace}
def verbNs(verb, source_dir, namespace, to_f, source):

    print(f"\nCHECK {verb} EVENTS IN {namespace}...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if jsonline["verb"] == verb:
                        if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                            #if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                            if "username" in jsonline["user"]:
                                t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{source}/{verb}_{namespace}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### CHECK {verb} EVENTS OF {user} IN {namespace}
def verbUsrNs(verb, source_dir, user, namespace, to_f, source):

    print(f"\nCHECK {verb} EVENTS OF {user} IN {namespace}...\n")
    print(f"SOURCE = {source_dir}")

    files = source_dir.iterdir()
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            for line in file_handle:
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if jsonline["verb"] == verb:
                        if namespace != '' and jsonline["objectRef"]["namespace"] == namespace:
                            if user != '' and ("username" in jsonline["user"]) and jsonline["user"]["username"] == user:
                                t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"], jsonline["requestReceivedTimestamp"], jsonline["responseStatus"]["code"]])

    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{source}/{verb}_{user}_{namespace}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

### Print help info
def help():
    print("\n################################################ AUDIT LOGS ANALYZER ##################################################\n")

    print("  USE\n")
    print("  ala [verb] [COMMANDS]\n")

    print(f"verb: {str(VERBS)}\n\n")

    print("COMMANDS:")
    print("  start <ABS_path_to_must-gather> \t:= load the must-gather path")
    print("  stop \t\t\t\t:= delete tmp files used\n")
    print("  [verb] -u <user> \t\t:= analyze log for a specific user")
    print("  [verb] -n <namespace> \t:= analyze log for a specific namespace")
    print("  [verb] -f \t\t\t:= write the result in an output file (txt)")
    print("  [verb] -h \t\t\t:= print ala help info")
    print("  [verb] -t \t\t\t:= search on a time interval (only with 'all' verb)")

    print("\n\nCorrect usage examples")
    print("  ala [verb] -u <user> -n <namespace> -f \t\t------->\tcorrect")
    print("  ala [verb] -n <namespace> -u <user> -f \t\t------->\tcorrect")
    print("  ala [verb] -f -n <namespace> -u <user> \t\t------->\tcorrect")
    print("  ala [verb] -h \t\t\t\t\t------->\tcorrect")
    print("  ala [verb] -f -n <namespace> -u <user> -h \t------->\tcorrect, but print only help info")
    
    print("\n\nWRONG usage examples !!! ")
    print("  ala -u <user> -n <namespace> -f \t\t------->\twrong (verb is mandatory)")
    print("  ala [verb] [dir] -n <user> -u <namespace> -f \t------->\twrong (-n and namespace are correlated (same for user))")
    print("  ala -f -n <namespace> -u <user> [verb]  \t------->\twrong (verb must be the first arg)")

    print("\n#######################################################################################################################\n")


### LOAD the must-gather path. If the file exist, delete and recreate
def start(path):
    p = Path('./alatmp.txt')
    if p.is_file():
        os.remove("./alatmp.txt")
    f = open('./alatmp.txt', 'w')
    f.write(str(path))

### delete tmp files used
def stop():
    p = Path('./alatmp.txt')
    if p.is_file():
        os.remove("./alatmp.txt")

### Launch the analysis 
def ala(source):
    namespace = ''
    user = ''
    to_f = False
    vrb = sys.argv[1]
    t_start = ''
    t_end = ''

    # Set source_dir
    source_dir = None
    for dir in DIRS:
        path = source + dir
        source_dir=Path(path)
        
        # -n specify namespace
        if "-n" in sys.argv:
            namespace = sys.argv[sys.argv.index("-n") + 1]
        
        # -u specify user
        if "-u" in sys.argv:
            user = sys.argv[sys.argv.index("-u") + 1]

        # -f copy output in a file user
        if "-f" in sys.argv:
            to_f = True

        # -t insert interval
        if "-t" in sys.argv:
            interval = setInterval()
            t_start = interval[0]
            t_end = interval[1]
            

        #Openshift verbs
        if vrb in VERBS:
            if namespace == '' and user == '':
                verb(vrb, source_dir, to_f, source)
            elif namespace == '' and user != '':
                verbUsr(vrb, source_dir, user, to_f, source)
            elif namespace != '' and user == '':
                verbNs(vrb, source_dir, namespace, to_f, source)
            elif namespace != '' and user != '':
                verbUsrNs(vrb, source_dir, user, namespace, to_f, source)

        #My verb
        elif sys.argv[1] == "all":

            if namespace != '' and user != '':
                allEventsUsrNs(source_dir, user, namespace, to_f, source)
            elif namespace == '' and user != '':
                allEventsUsr(source_dir, user, to_f, source)
            elif namespace != '' and user == '':
                allEventsNs(source_dir, namespace, to_f, source)
            elif namespace == '' and user == '' and "-t" in sys.argv:
                allEventsTime(source_dir, to_f, source, t_start, t_end)
        else:
            print("\n Command not found (try -h to see help info)\n")
            return

######################################################################################
######################################## MAIN ########################################
######################################################################################

def main():
    if len(sys.argv) <= 1:
        print("\n Too few arguments, verb and dir are mandatory (try -h to see help info) \n")
        return

    # If there is -h print help
    if "-h" in sys.argv:
        help()
        return

    if sys.argv[1] == "stop":
        stop()
        return

    if sys.argv[1] == "start":
        if len(sys.argv) <= 2:
            print("\n Too few arguments, verb and dir are mandatory (try -h to see help info) \n")
            return
        start(sys.argv[2])
        return

    # Extract path of must-gather (AFTER START)
    source = ""
    f = open('./alatmp.txt', 'r')
    path = f.readline()

    p = Path(str(path)).glob("**")
    for file in p:
        if "audit_logs" in str(file) and "audit_logs/" not in str(file):
            source = str(file) + "/"
            break
    
    # Check if path of must-gather exist 
    if source == '':
        print("\n Path not found (try -h to see help info). Did you launch the start command?\n")    
        return

    # Launch the ala utilities
    ala(source)

if __name__ == "__main__":
    #print(f"Arguments count: {str(sys.argv)})")
    main()