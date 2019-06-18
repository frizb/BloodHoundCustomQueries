# BloodHoundCustomQueries
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
