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

import progressbar

VERBS = ["create", "delete", "deletecollection", "get", "list", "patch", "update", "watch"]

def progressBar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_Length = int(round(bar_length * count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
    sys.stdout.flush()

def allEventsUsrNs(path, user, namespace, to_f):
    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME', "RESPONSE"])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather/quay/audit_logs/'+path)
    files = source_dir.iterdir()

    start = time.time()
    for file in files:
        print(file)
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
    end = time.time()

    print("TIME =========> " + str(end-start))
    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'all_events_{user}_{namespace}_{path}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

def allEventsUsr(path, user, to_f):
    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather/quay/audit_logs/'+path)
    files = source_dir.iterdir()

    start = time.time()
    for file in files:
        print(file)
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
    end = time.time()

    print("TIME =========> " + str(end-start))
    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'all_events_{user}_{path}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

def allEventsNs(path, namespace, to_f):
    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather/quay/audit_logs/'+path)
    files = source_dir.iterdir()

    start = time.time()
    for file in files:
        print(file)
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
    end = time.time()

    print("TIME =========> " + str(end-start))
    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'all_events_{namespace}_{path}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

def verb(verb, path, to_f):

    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather/quay/audit_logs/'+path)
    files = source_dir.iterdir()

    start = time.time()
    for file in files:
        print(file)
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
    end = time.time()

    print("TIME =========> " + str(end-start))
    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{verb}_{path}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

def verbUsr(verb, path, user, to_f):

    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather/quay/audit_logs/'+path)
    files = source_dir.iterdir()

    start = time.time()
    for file in files:
        print(file)
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
    end = time.time()

    print("TIME =========> " + str(end-start))
    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{verb}_{user}_{path}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

def verbNs(verb, path, namespace, to_f):

    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather/quay/audit_logs/'+path)
    files = source_dir.iterdir()

    start = time.time()
    for file in files:
        print(file)
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
    end = time.time()

    print("TIME =========> " + str(end-start))
    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{verb}_{namespace}_{path}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

def verbUsrNs(verb, path, user, namespace, to_f):

    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE', 'TIME'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather/quay/audit_logs/'+path)
    files = source_dir.iterdir()

    start = time.time()
    for file in files:
        print(file)
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
    end = time.time()

    print("TIME =========> " + str(end-start))
    t.align = 'l'
    t.sortby = "TIME"
    print(t)
    if to_f == True:
        f = open(f'{verb}_{user}_{namespace}_{path}.txt', 'w')
        f.write(str(t))

    print("\nCOMPLETED\n")

def help():
    print("\n############################ AUDIT LOGS ANALYZER ############################\n")

    print("USE\n")
    print("python3 ala.py [verb] [dir]\n\n")

    print("COMMANDS:\n")
    print("  -u <user> \t\t:= analyze log for a specific user")
    print("  -n <namespace> \t:= analyze log for a specific namespace")
    print("  -f <out_file> \t:= write the result in an output file (txt)")
    print("  -h \t\t\t:= print ala help info")

    print("\n##############################################################################\n")

def main():
    #use = False
    namespace = ''
    user = ''
    to_f = False
    verb = sys.argv[1]

    if "-n" in sys.argv:
        namespace = sys.argv[sys.argv.index("-n") + 1]
    
    if "-u" in sys.argv:
        user = sys.argv[sys.argv.index("-u") + 1]

    if "-f" in sys.argv:
        to_f = True
    
    if "-h" in sys.argv:
        help()
        return

    if verb == "use":
        if len(sys.argv) > 2:
            path = str(sys.argv[2])
            must_load(path)
            use = True

    elif verb in VERBS:
        if len(sys.argv) > 2:
            path = sys.argv[2]
            if namespace == '' and user == '':
                verb(verb, path, to_f)
            elif namespace == '' and user != '':
                verbUsr(verb, path, user, to_f)
            elif namespace != '' and user == '':
                verbNs(verb, path, namespace, to_f)
            elif namespace != '' and user != '':
                verbUsrNs(verb, path, user, namespace, to_f)

    elif sys.argv[1] == "all":
        if len(sys.argv) > 2:
            path = sys.argv[2]
            if namespace != '' and user != '':
                allEventsUsrNs(path, user, namespace, to_f)
            elif namespace == '' and user != '':
                allEventsUsr(path, user, to_f)
            elif namespace != '' and user == '':
                allEventsNs(path, namespace, to_f)
    else:
        print("\n Command not found \n")


if __name__ == "__main__":
    #print(f"Arguments count: {str(sys.argv)})")
    main()