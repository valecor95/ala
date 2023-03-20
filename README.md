# Audit Logs Analyzer
ALA is a client to analyze openshift must-gather audit logs.

### Contents
<!-- vscode-markdown-toc -->
- [Setup Linux/Mac](#SetupLinuxMac)
-  [Usage](#Usage)
	- [Start](#Start)
	- [Ala](#Ala)
	- [Stop](#Stop)
- [Examples](#Examples)
	- [Correct examples](#Correctexamples)
	- [Wrong examples](#Wrongexamples)
<!-- vscode-markdown-toc -->

##  1. <a id='SetupLinuxMac'></a>Setup Linux/Mac
**1.** Clone the repository

**2.** Copy the `ala.py` file to /usr/local/lib:
```bash
sudo cp ala.py /usr/local/lib/
```

**3.** Add ala tool in your CLASSPATH
```bash
export CLASSPATH=".:/usr/local/lib/ala.py:$CLASSPATH"
```

**4.** Add aliases to simplify the use of ALA:
```bash
alias ala="python3 ala.py"
```


##  2. <a id='Usage'></a>Usage

###  2.1. <a id='Start'></a>Start
The first command to do:
```bash
ala start <path_to_must-gather>
```
It loads the must-gather path. This command is mandatory otherwise you'll have an error.

ATTENTION: at the current version the audit logs file must be unzipped manually. Hint:
```bash
gunzip ./*.zip
```
Inside `openshift-apiserver` and `kube-apiserver` folders.

###  2.2. <a id='Ala'></a>Ala
The ala client is used with this main command:
```bash
ala [verb] [COMMANDS]
```
- The possible verbs to inspect are the main kubernetes verbs:
  ```bash
  verb: {
    'create', 
    'delete', 
    'deletecollection', 
    'get', 
    'list', 
    'patch', 
    'update', 
    'watch'
  }
  ```

- The possible commands to use are:
  ```bash
  -u <user> 		:= analyze log for a specific user
  -n <namespace> 	        := analyze log for a specific namespace
  -f 			:= write the result in an output file (txt)
  -h 			:= print ala help info
  ```

###  2.3. <a id='Stop'></a>Stop
Once you have finished your analysis remember to delete all resources:
```bash
ala stop
```

##  3. <a id='Examples'></a>Examples
###  3.1. <a id='Correctexamples'></a>Correct examples
```bash
ala [verb] -u <user> -n <namespace> -f 		------->	correct
ala [verb] -n <namespace> -u <user> -f 		------->	correct
ala [verb] -f -n <namespace> -u <user> 		------->	correct
ala [verb] -h 					------->	correct
ala [verb] -f -n <namespace> -u <user> -h 	------->	correct, but print only help info
```

###  3.2. <a id='Wrongexamples'></a>Wrong examples
```bash
ala -u <user> -n <namespace> -f 		------->	wrong (verb is mandatory)
ala [verb] [dir] -n <user> -u <namespace> -f 	------->	wrong (-n and namespace are correlated (same for user))
ala -f -n <namespace> -u <user> [verb]  	------->	wrong (verb must be the first arg)
```