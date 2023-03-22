# Audit Logs Analyzer
ALA is a script that simulate a client to analyze openshift must-gather audit logs.

---
### Contents
<!-- vscode-markdown-toc -->
- 1.  [Setup Linux/Mac](#setuplinuxmac)
- 2.  [Usage](#usage)
  - 2.1.  [Unzip files](#unzip)
  - 2.2.  [Start](#start)
  - 2.3.  [Ala](#ala)
    - 2.3.1 [Interval](#interval)
  - 2.4.  [Stop](#stop)
- 3.  [Examples](#examples)
  - 3.1.  [Correct examples](#correctexamples)
  - 3.2.  [Wrong examples](#wrongexamples)
<!-- vscode-markdown-toc -->
---

##  1. <a id="setuplinuxmac"></a>Setup Linux/Mac
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
alias ala="python3 /usr/local/lib/ala.py"
```


##  2. <a id='usage'></a>Usage

### 2.1. <a id='unzip'></a>Unzip files
At the current version the audit logs files must be unzipped manually. Go inside `openshift-apiserver` and `kube-apiserver` folders and launch:
```bash
gunzip ./*.gz
```

###  2.2. <a id='start'></a>Start
The first command to do:
```bash
ala start <ABSOLUTE_path_to_must-gather>
```
It loads the must-gather ***absolute*** path. This command is mandatory otherwise you'll have an error. Relative path are not supported.

###  2.3. <a id='ala'></a>Ala
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
  -t                      := search on a time interval (only with 'all' verb)
  ```

#### 2.3.1 <a id='interval'></a>Interval
At the moment ala is able to query an inteval time only in *ala* verb command:
- Command:
  ```bash
  ala all -t
  ```
- This command read the input froma file. The script use the following format for the timestamps: `%Y-%m-%dT%H:%M:%S.%f%z`
- Correct usage:
  ```sh
  Insert start date (AAAA-MM-DD): 2023-03-14
  Insert start time (HH:MM): 23:55
  Insert end date (AAAA-MM-DD): 2023-03-15
  Insert end time (HH:MM): 00:05
  ```

###  2.4. <a id='stop'></a>Stop
Once you have finished your analysis remember to delete all resources:
```bash
ala stop
```

##  3. <a id='examples'></a>Examples
###  3.1. <a id='correctexamples'></a>Correct examples
```bash
ala [verb] -u <user> -n <namespace> -f 		------->	correct
ala [verb] -n <namespace> -u <user> -f 		------->	correct
ala [verb] -f -n <namespace> -u <user> 		------->	correct
ala [verb] -h 					------->	correct
ala [verb] -f -n <namespace> -u <user> -h 	------->	correct, but print only help info
```

###  3.2. <a id='wrongexamples'></a>Wrong examples
```bash
ala -u <user> -n <namespace> -f 		------->	wrong (verb is mandatory)
ala [verb] [dir] -n <user> -u <namespace> -f 	------->	wrong (-n and namespace are correlated (same for user))
ala -f -n <namespace> -u <user> [verb]  	------->	wrong (verb must be the first arg)
```
