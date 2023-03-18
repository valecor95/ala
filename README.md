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

ala [verb] [dir] [COMMANDS]


verb: ['create', 'delete', 'deletecollection', 'get', 'list', 'patch', 'update', 'watch']

dir: ['openshift-apiserver', 'oauth-apiserver', 'kube-apiserver']

COMMANDS:

  -u <user> 		:= analyze log for a specific user
  -n <namespace> 	:= analyze log for a specific namespace
  -f <out_file> 	:= write the result in an output file (txt)
  -h 			:= print ala help info


Correct usage examples
python3 ala.py [verb] [dir] -u <user> -n <namespace> -f 	------->	correct
python3 ala.py [verb] [dir] -n <namespace> -u <user> -f 	------->	correct
python3 ala.py [verb] [dir] -f -n <namespace> -u <user> 	------->	correct
python3 ala.py [verb] [dir] -h 					------->	correct
python3 ala.py [verb] [dir] -f -n <namespace> -u <user> -h 	------->	correct, but print only help info


!!! WRONG usage examples !!! 
python3 ala.py [dir] [verb] -u <user> -n <namespace> -f 	------->	wrong (don't invert dir and verb)
python3 ala.py [dir] -u <user> -n <namespace> -f 		------->	wrong (dir and verb are mandatory)
python3 ala.py [verb] [dir] -n <user> -u <namespace> -f 	------->	wrong (-n and namespace are correlated (same for user))
python3 ala.py -f -n <namespace> -u <user> [verb] [dir]  	------->	wrong (varb and dir must be first and second args)

##############################################################################
```