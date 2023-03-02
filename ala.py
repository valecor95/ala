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


'''
def must_load(path):
    source_dir = Path(path)
    #print(source_dir)
    files = source_dir.iterdir()
    #print(files)
    df = pd.DataFrame()
    print("Loading audit-logs...")

    start = time.time()
    for file in files:
        with file.open('r') as file_handle:
            print(file)
            
            for line in file_handle:
                #print(line)
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                #mustGather.append(jsonline)
                #print(str(jsonline))

            if df.empty:
                df = pd.read_json(file_handle, lines=True)
            else:
                df = df.append(pd.read_json(file_handle, lines=True), ignore_index=True)
            #print(df)
    end = time.time()
    print("TIME =====> " + str(end - start))
    print("Complete")
'''            


def delete_verb(path):

    print("\nCHECK DELETE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather-audit/quay/audit_logs/'+path)
    #print(source_dir)
    files = source_dir.iterdir()
    #print(files)
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            #print(file)
            for line in file_handle:
                #print(line)
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                #print(str(jsonline))
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if jsonline["objectRef"]["namespace"] == "ndp-ocp2val":
                        if jsonline["verb"] == "delete":
                            #print('\t\t'.join([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"]]))
                            t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"]])
    
    t.align = 'l'
    print(t)
    print("\nCOMPLETED\n")



def create_verb(path):

    print("\nCHECK CREATE EVENTS...\n")

    t = PrettyTable(['USER', 'VERB', 'RESOURCE', 'NAMESPACE'])
    source_dir = Path('/Users/valeriocoretti/Desktop/aul/must-gather-audit/quay/audit_logs/'+path)
    #print(source_dir)
    files = source_dir.iterdir()
    #print(files)
    
    for file in files:
        #print(file)
        with file.open('r') as file_handle:
            #print(file)
            for line in file_handle:
                #print(line)
                try:
                    jsonline = json.loads(line)
                except Exception as e:
                    pass
                #print(str(jsonline))
                if "objectRef" in jsonline and "namespace" in jsonline["objectRef"]:
                    if jsonline["objectRef"]["namespace"] == "ndp-ocp2val":
                        if jsonline["verb"] == "create":
                            #print('\t\t'.join([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"]]))
                            t.add_row([jsonline["user"]["username"], jsonline["verb"], jsonline["objectRef"]["resource"], jsonline["objectRef"]["namespace"]])
    
    t.align = 'l'
    print(t)
    print("\nCOMPLETED\n")

def count_verbs():
    counter = {}
    print(str(counter))
    '''
                if jsonline["verb"] not in counter:
                    counter[jsonline["verb"]] =1
                else:
                    counter[jsonline["verb"]] +=1
                '''

def main():
    use = False
    if sys.argv[1] == "use":
        if len(sys.argv) > 2:
            path = str(sys.argv[2])
            must_load(path)
            use = True

    elif sys.argv[1] == "delete":
        if len(sys.argv) > 2:
            path = sys.argv[2]
            delete_verb(path)

    elif sys.argv[1] == "create":
        if len(sys.argv) > 2:
            path = sys.argv[2]
            create_verb(path)
    
    else:
        print("\n Command not found \n")


if __name__ == "__main__":
    print(f"Arguments count: {str(sys.argv)})")
    main()