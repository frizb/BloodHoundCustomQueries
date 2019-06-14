# BloodHoundCustomQueries
List of Bloodhound Custom Queries which I have found to be handy on engagements

## Users with Path to Domain Admin
Check to see if anyone on a list of users can reach domain admin. Users and domains MUST BE ALLCAPS.

```
MATCH (n:User),(m:Group {name:"DOMAIN ADMINS@DOMAIN"}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m)) 
WHERE n.name IN ["USER1@DOMAIN","USER2@DOMAIN", "USER3DOMAIN"]
RETURN p
```
