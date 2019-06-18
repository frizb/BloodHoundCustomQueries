# BloodHoundCustomQueries
List of Bloodhound Custom Queries which I have found to be handy on engagements.

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

## Users with Path to Domain Admin
Check to see if anyone on a list of users can reach domain admin. Users and domains MUST BE ALLCAPS in the list file.
