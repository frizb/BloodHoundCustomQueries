# BloodHound Custom Queries
Python Powered Bloodhound Custom Queries which I have found to be handy on engagements and for reporting purposes.

You will need to install neo4j in python 2.7 to run these tools:
```
pip install neo4j
```
## GetUsers.py - Bloodhound User CSV Query Dump
This will create a CSV file from a BloodHound database and run each query that populates information in the Node Info table such as:
* Sibling Objects in the same OU
* Reachable High Value Targets
* Effective Inbound GPOs
* First Degree Group Membership
* Unrolled Group Membership
* First Degree Local Admin
* Group Delegated Local Admin
* Derivative Local Admin Rights
* First Degree RDP
* Group Delegated RDP
* First Degree DCOM
* Group Delegated DCOM
* Constrained Delegation Privleges

**Warning** this takes a LOONG time (2+ hours in some cases) to run against a large dataset but create a great view of the Powerful Bloodhound data for further exploitation and reporting. 

```
usage: GetUsers.py [-h] [-contains CONTAINS] [-csv CSV] [-userlist USERLIST]
                   [-delim DELIM] [-printresults] [-isenabled] [-isowned]
                   [-isadmin] [-issensitive] [-ishighvalue] [-ishasspn]
                   [-isdontreqpreauth] [-username USERNAME]
                   [-password PASSWORD] [-serverurl SERVERURL]

Generate a csv list of users from Bloodhound that contains all the data that
appears under User Info table in Neo4j. Flattens out the Bloodhound Neo4J data
into a large data table.

optional arguments:
  -h, --help            show this help message and exit
  -contains CONTAINS    A string that the username contains (helpful for AD /
                        SA / Service Account list generation)
  -csv CSV              The CSV file to export containing the results
                        (default: Users.csv)
  -userlist USERLIST    Path to userlist to use in the query
  -delim DELIM          CSV Delimiter (default: ,)
  -printresults         Also prints the results to the console
  -isenabled            Only output enabled accounts
  -isowned              Only output Owned accounts
  -isadmin              Only output Admin Count accounts
  -issensitive          Only output sensitive accounts
  -ishighvalue          Only output high value accounts
  -ishasspn             Only output accounts that have spn
  -isdontreqpreauth     Only output accounts that do not require preauth
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
```

A user string contains statement or a list of users to query can be optionally provided, but by default it will query all users. 
The script expect the user input format to look like this:
```
USER@DOMAIN.COM
USER2@DOMAIN.COM
USER3@DOMAIN.COM
```

## GetUserListContains.py - Generate a list of Users from Bloodhound
This Python script can be used to generate lists of users (to be passed into the other scripts below) or dump data from Bloodhound in a table form (CSV).  Sometimes it nice to just use excel to parse through data for reporting and cross referencing. 
```
usage: GetUserListContains.py [-h] [-contains CONTAINS] [-csv CSV]
                              [-userlist USERLIST] [-delim DELIM]
                              [-printresults] [-isenabled] [-isowned]
                              [-isadmin] [-issensitive] [-ishighvalue]
                              [-ishasspn] [-isdontreqpreauth] [-allthedata]
                              [-username USERNAME] [-password PASSWORD]
                              [-serverurl SERVERURL]

Generate a list of users from Bloodhound that contain a specific string and
exports the list as a csv. This script can also optionally add additional
properties to the CSV results.

optional arguments:
  -h, --help            show this help message and exit
  -contains CONTAINS    A string that the username contains (helpful for AD /
                        SA / Service Account list generation)
  -csv CSV              The CSV file to export containing the results
                        (default: UserList.csv)
  -userlist USERLIST    Path to userlist to use in the query
  -delim DELIM          CSV Delimiter (default: ,)
  -printresults         Also prints the results to the console
  -isenabled            Only output enabled accounts
  -isowned              Only output Owned accounts
  -isadmin              Only output Admin Count accounts
  -issensitive          Only output sensitive accounts
  -ishighvalue          Only output high value accounts
  -ishasspn             Only output accounts that have spn
  -isdontreqpreauth     Only output accounts that do not require preauth
  -allthedata           Adds all the data columns from BloodHound to the CSV
                        output
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)

```

## PathToDomainAdmin.py - Users with Path to Domain Admin from a specified list
Check to see if anyone on a list of users can reach domain admin. Users and domains MUST BE ALLCAPS in the list file.
```
From a list of BloodHound users (must be in uppercase format like:
USER@DOMAIN.COM) this script will check the number of paths to Domain Admin
each user has on the list and exports the list as a csv.

optional arguments:
  -h, --help            show this help message and exit
  -userlist USERLIST    Path to userlist to use in the query
  -domainadmin DOMAINADMIN
                        Name of the domain admin group on the DC.
  -csv CSV              The CSV file to export containing the results
                        (default: PathsToDomainAdmin.csv)
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
Please specify the -userlist parameter and the -domainadmin parameter
```

## Users from a list who have Group Delegated Local Admin Rights
Check to see if anyone on a list of users can reach domain admin. Users and domains MUST BE ALLCAPS in the list file.

```
From a list of BloodHound users (must be in uppercase format like:
USER@DOMAIN.COM) this script will check the number of Group Delegated Local
Admin rights each user has on the list and exports the list as a csv.

optional arguments:
  -h, --help            show this help message and exit
  -userlist USERLIST    Path to userlist to use in the query
  -csv CSV              The CSV file to export containing the results
                        (default: GroupDelegatedLocalAdmins.csv)
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
Please specify the -userlist parameter.

```

## FirstDegreeLocalAdmins.py - Users from a list who have First Degree Local Admin rights in the AD environment
Check to see if anyone on a list of users can reach domain admin. Users and domains MUST BE ALLCAPS in the list file.

```
From a list of BloodHound users (must be in uppercase format like:
USER@DOMAIN.COM) this script will check the number of First Degree Local Admin
rights each user has on the list and exports the list as a csv.

optional arguments:
  -h, --help            show this help message and exit
  -userlist USERLIST    Path to userlist to use in the query
  -csv CSV              The CSV file to export containing the results
                        (default: FirstDegreeLocalAdmins.csv)
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
Please specify the -userlist parameter.

```


## GroupMembers.py - Get all the members of a Group to a CSV file or Check Users from a list to see if they are a member of a Group
Determine which users from a list are a member of a specific group.
```
usage: GroupMembers.py [-h] [-userlist USERLIST] [-group GROUP] [-csv CSV]
                       [-username USERNAME] [-password PASSWORD]
                       [-serverurl SERVERURL]

From a list of BloodHound users (must be in uppercase format like:
USER@DOMAIN.COM) this script will check which users are members of a specific
Group and exports the list. Or alternatively you can specify just a group and
get a list of all members as a csv.

optional arguments:
  -h, --help            show this help message and exit
  -userlist USERLIST    Path to userlist file to use in the query
  -group GROUP          Name of the group in the DC
  -csv CSV              The CSV file to export containing the results
                        (default: GroupMembers.csv)
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
```

## GetComputersListContains.py - Computers in the environment whose name contains
This Python script can be used to generate lists of computers or dump data from Bloodhound in a table form (CSV).  Sometimes it nice to just use excel to parse through data for reporting and cross referencing. 
```
usage: GetComputerListContains.py [-h] [-contains CONTAINS] [-csv CSV]
                                  [-delim DELIM] [-printresults] [-isenabled]
                                  [-isowned] [-isadmin] [-issensitive]
                                  [-ishighvalue] [-isunconstraineddelegation]
                                  [-isdontreqpreauth] [-allthedata]
                                  [-username USERNAME] [-password PASSWORD]
                                  [-serverurl SERVERURL]

Generate a list of computers from Bloodhound that contain a specific string
and exports the list as a csv. This script can also optionally add additional
properties to the CSV results.

optional arguments:
  -h, --help            show this help message and exit
  -contains CONTAINS    A string that the computer contains
  -csv CSV              The CSV file to export containing the results
                        (default: ComputerList.csv)
  -delim DELIM          CSV Delimiter (default: ,)
  -printresults         Also prints the results to the console
  -isenabled            Only output enabled computers
  -isowned              Only output Owned computers
  -isadmin              Only output Admin Count computers
  -issensitive          Only output sensitive computers
  -ishighvalue          Only output high value computers
  -isunconstraineddelegation
                        Only output computers with unconstrained delegation
  -isdontreqpreauth     Only output computers that do not require preauth
  -allthedata           Adds all the data columns from BloodHound to the CSV
                        output
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
```


## ComputerAdministrators.py - List all administrators for a computer on DC using BloodHound
This Python script can be used to generate lists of users and groups or dump data from Bloodhound in a table form (CSV).  

```
usage: ComputerAdministrators.py [-h] [-computername COMPUTERNAME]
                                 [-computerlist COMPUTERLIST] [-csv CSV]
                                 [-username USERNAME] [-password PASSWORD]
                                 [-serverurl SERVERURL]

Provides a list of administrator and admin groups for a specific Computer or
list of computers and output to CSV. Appends any labels to the CSV and also if
the account is enabled.

optional arguments:
  -h, --help            show this help message and exit
  -computername COMPUTERNAME
                        Name of the computer in the DC (EX. CORP-
                        DC01.TEST.LOCAL)
  -computerlist COMPUTERLIST
                        Path to the computer list file to use in the query.
  -csv CSV              The CSV file to export containing the results
                        (default: ComputerAdmins.csv)
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
```
