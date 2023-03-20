# Audit Logs Analyzer
Audit logs analyzer - a client to analyze openshift must-gather audit logs


## Setup Linux/Mac
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


## Usage

```
############################ AUDIT LOGS ANALYZER ############################

USE

ala [verb] [COMMANDS]

verb: ['create', 'delete', 'deletecollection', 'get', 'list', 'patch', 'update', 'watch']


COMMANDS:
  start <path_to_must-gather> 	:= load the must-gather path
  stop 				:= delete tmp files used

  [verb] -u <user> 		:= analyze log for a specific user
  [verb] -n <namespace> 	:= analyze log for a specific namespace
  [verb] -f 			:= write the result in an output file (txt)
  [verb] -h 			:= print ala help info


Correct usage examples
ala [verb] -u <user> -n <namespace> -f 		------->	correct
ala [verb] -n <namespace> -u <user> -f 		------->	correct
ala [verb] -f -n <namespace> -u <user> 		------->	correct
ala [verb] -h 					------->	correct
ala [verb] -f -n <namespace> -u <user> -h 	------->	correct, but print only help info


!!! WRONG usage examples !!! 
ala -u <user> -n <namespace> -f 		------->	wrong (verb is mandatory)
ala [verb] [dir] -n <user> -u <namespace> -f 	------->	wrong (-n and namespace are correlated (same for user))
ala -f -n <namespace> -u <user> [verb]  	------->	wrong (verb must be the first arg)

##############################################################################

```