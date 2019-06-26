# BloodHound Custom Queries
List of Bloodhound Custom Queries which I have found to be handy on engagements.

Sample user list content:
```
USER@DOMAIN.COM
USER2@DOMAIN.COM
USER3@DOMAIN.COM
```

You will need to install neo4j in python 2.7 to run these tools:
```
pip install neo4j
```
## Generate a list of Users from Bloodhound
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

## Users with Path to Domain Admin from a specified list
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

## Users from a list who have First Degree Local Admin rights in the AD environment
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


## Users from a list who are a member of a Group
Determine which users from a list are a member of a specific group.
```
From a list of BloodHound users (must be in uppercase format like:
USER@DOMAIN.COM) this script will check which users are members of a specific
Group and exports the list as a csv.

optional arguments:
  -h, --help            show this help message and exit
  -userlist USERLIST    Path to userlist to use in the query
  -group GROUP          Name of the group in the DC
  -csv CSV              The CSV file to export containing the results
                        (default: GroupMembers.csv)
  -username USERNAME    Neo4j username (default: neo4j)
  -password PASSWORD    Neo4j password (default: BloodHound)
  -serverurl SERVERURL  Neo4j server URL (default: bolt://localhost:7687)
Please specify the -userlist parameter and the -group parameter
```

## Computers in the environment whose name contains
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
