import argparse
from neo4j import GraphDatabase
import datetime

# Requirements:
# pip install neo4j
parser = argparse.ArgumentParser(description='Generate a csv list of users from Bloodhound that contains '
                                             ' all the data that appears under User Info table in Neo4j. '
                                             ' Flattens out the Bloodhound Neo4J data into a large data table.')
parser.add_argument("-contains", type=str, help='A string that the username contains (helpful for AD / SA / '
                                                'Service Account list generation)')
parser.add_argument("-csv", type=str, default="Users.csv",
                    help='The CSV file to export containing the results (default: %(default)s)')
parser.add_argument("-userlist", type=str, help='Path to userlist to use in the query')
parser.add_argument("-delim", type=str, default=",", help="CSV Delimiter (default: %(default)s)")
parser.add_argument("-printresults", action="store_true", help="Also prints the results to the console")
parser.add_argument("-isenabled", action="store_true", help="Only output enabled accounts")
parser.add_argument("-isowned", action="store_true", help="Only output Owned accounts")
parser.add_argument("-isadmin", action="store_true", help="Only output Admin Count accounts")
parser.add_argument("-issensitive", action="store_true", help="Only output sensitive accounts")
parser.add_argument("-ishighvalue", action="store_true", help="Only output high value accounts")
parser.add_argument("-ishasspn", action="store_true", help="Only output accounts that have spn")
parser.add_argument("-isdontreqpreauth", action="store_true", help="Only output accounts that do not require preauth")
parser.add_argument("-username", type=str, default="neo4j", help="Neo4j username (default: %(default)s)")
parser.add_argument("-password", type=str, default="BloodHound", help="Neo4j password (default: %(default)s)")
parser.add_argument("-serverurl", type=str, default="bolt://localhost:7687", help="Neo4j server URL (default: %(default)s)")
args = parser.parse_args()

driver = GraphDatabase.driver(args.serverurl, auth=(args.username, args.password))
column_headers = [
    "Name",
    "Sessions",
    "Sibling Objects in the same OU",
    "Reachable High Value Targets",
    "Effective Inbound GPOs",
    "First Degree Group Membership",
    "Unrolled Group Membership",
    "First Degree Local Admin",
    "Group Delegated Local Admin",
    "Derivative Local Admin Rights",
    "First Degree RDP",
    "Group Delegated RDP",
    "First Degree DCOM",
    "Group Delegated DCOM",
    "Constrained Delegation Privleges",
    "Display Name",
    "Domain",
    "Password",
    "Title",
    "Enabled",
    "Owned",
    "Admin Count",
    "Sensitive",
    "High Value",
    "Do Not Require Preauth",
    "Has SPN",
    "Password Last Set",
    "Last Login",
    "SID",
    "Email",
    "Description",
    "Notes"
]
column_header = args.delim.join(column_headers)+"\r"

def count_sessions(tx, name):
    records = tx.run("MATCH p = (m:Computer) - [r:HasSession]->(n:User {name:\""+name+"\"}) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_sibling_objects_in_same_ou(tx, name):
    records = tx.run("MATCH (o1)-[r1:Contains]->(o2:User {name:\""+name+"\"}) WITH o1 OPTIONAL MATCH p1=(d)-[r2:Contains*1..]->(o1) OPTIONAL MATCH p2=(o1)-[r3:Contains]->(n) WHERE n:User OR n:Computer RETURN p1,p2")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_reachable_high_value_targets(tx, name):
    records = tx.run("MATCH (m:User {name:\""+name+"\"}),(n {highvalue:true}),p=shortestPath((m)-[r*1..]->(n)) WHERE NONE (r IN relationships(p) WHERE type(r)= \"GetChanges\") AND NONE (r in relationships(p) WHERE type(r)=\"GetChangesAll\") AND NOT m=n RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_effective_inbound_gpos(tx, name):
    records = tx.run("MATCH (c:User {name:\""+name+"\"}) OPTIONAL MATCH p1 = (g1:GPO)-[r1:GpLink {enforced:true}]->(container1)-[r2:Contains*1..]->(c) OPTIONAL MATCH p2 = (g2:GPO)-[r3:GpLink {enforced:false}]->(container2)-[r4:Contains*1..]->(c) WHERE NONE (x in NODES(p2) WHERE x.blocksinheritance = true AND x:OU AND NOT (g2)-->(x)) RETURN p1,p2")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_first_degree_group_memberships(tx, name):
    records = tx.run("MATCH (m:User {name:\""+name+"\"}), (n:Group), p=(m)-[:MemberOf]->(n) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_unrolled_group_memberships(tx, name):
    records = tx.run("MATCH p = (m:User {name:\""+name+"\"})-[r:MemberOf*1..]->(n:Group) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_first_degree_local_admins(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r:AdminTo]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_group_delegated_local_admins(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r1:MemberOf*1..]->(g:Group)-[r2:AdminTo]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_derivative_local_admins(tx, name):
    records = tx.run("MATCH p=shortestPath((m:User {name:\""+name+"\"})-[r:HasSession|AdminTo|MemberOf*1..]->(n:Computer)) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_first_degree_rdp(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r:CanRDP]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_group_delegated_rdp(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r1:MemberOf*1..]->(g:Group)-[r2:CanRDP]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_first_degree_dcom(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r:ExecuteDCOM]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_group_delegated_dcom(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r1:MemberOf*1..]->(g:Group)-[r2:ExecuteDCOM]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_constrained_delegation(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r:AllowedToDelegate]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def count_first_degree_object_control(tx, name):
    records = tx.run("MATCH p=(u:User {name:\""+name+"\"})-[r1]->(n) WHERE r1.isacl=true RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def match_user_name_contains(tx, contains, where):
    neo4j_query = 'MATCH (n:User) WHERE n.name contains "' + contains.upper() + '" ' + where + ' RETURN n'
    #print neo4j_query
    records = tx.run(neo4j_query)
    output_file = open(args.csv, "w")
    # Create headers
    output_file.write(column_header)
    records_found = process_records(records, output_file)
    output_file.close()
    print "Records Found: " + str(records_found)

def match_users_from_list(tx, userlist, where):
    input_file = open(userlist, "r")
    output_file = open(args.csv, "w")
    output_file.write(column_header)
    records_found = 0
    for user in input_file:
        neo4j_query = 'MATCH (n:User) WHERE n.name = "' + user.upper().strip() + '" ' + where + ' RETURN n'
        #print neo4j_query
        records = tx.run(neo4j_query)
        records_found += process_records(records, output_file)
    output_file.close()
    input_file.close()
    print "Records Found: " + str(records_found)

def process_records(records, output_file):
    records_found = 0
    for record in records:
        this_name = record[0]._properties[u'name']
        print "Running Queries for: " + this_name

        this_result = this_name
        with driver.session() as session:
            this_result += args.delim+str(session.read_transaction(count_first_degree_local_admins, this_name))
            this_result += args.delim+str(session.read_transaction(count_sibling_objects_in_same_ou, this_name))
            this_result += args.delim + str(session.read_transaction(count_reachable_high_value_targets, this_name))
            this_result += args.delim + str(session.read_transaction(count_effective_inbound_gpos, this_name))
            this_result += args.delim + str(session.read_transaction(count_first_degree_group_memberships, this_name))
            this_result += args.delim + str(session.read_transaction(count_unrolled_group_memberships, this_name))
            this_result += args.delim + str(session.read_transaction(count_first_degree_local_admins, this_name))
            this_result += args.delim + str(session.read_transaction(count_group_delegated_local_admins, this_name))
            this_result += args.delim + str(session.read_transaction(count_derivative_local_admins, this_name))
            this_result += args.delim + str(session.read_transaction(count_first_degree_rdp, this_name))
            this_result += args.delim + str(session.read_transaction(count_group_delegated_rdp, this_name))
            this_result += args.delim + str(session.read_transaction(count_first_degree_dcom, this_name))
            this_result += args.delim + str(session.read_transaction(count_group_delegated_dcom, this_name))
            this_result += args.delim + str(session.read_transaction(count_constrained_delegation, this_name))

        if 'displayname' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'displayname'].replace("\n"," ").replace("\r", " ").replace(","," ")
        else: this_result += args.delim
        if 'domain' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'domain']
        else:
            this_result += args.delim
        if 'userpassword' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'userpassword']
        else:
            this_result += args.delim
        if 'title' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'title'].replace("\n"," ").replace("\r", " ").replace(","," ")
        else:
            this_result += args.delim
        if 'enabled' in record[0]._properties:
            this_result += args.delim+str(record[0]._properties[u'enabled'])
        else:
            this_result += args.delim
        if 'owned' in record[0]._properties:
            this_result += args.delim+str(record[0]._properties[u'owned'])
        else:
            this_result += args.delim
        if 'admincount' in record[0]._properties:
            this_result += args.delim+str(record[0]._properties[u'admincount'])
        else:
            this_result += args.delim
        if 'sensitive' in record[0]._properties:
            this_result += args.delim+str(record[0]._properties[u'sensitive'])
        else:
            this_result += args.delim
        if 'highvalue' in record[0]._properties:
            this_result += args.delim+str(record[0]._properties[u'highvalue'])
        else:
            this_result += args.delim
        if 'dontreqpreauth' in record[0]._properties:
            this_result += args.delim+str(record[0]._properties[u'dontreqpreauth'])
        else:
            this_result += args.delim
        if 'hasspn' in record[0]._properties:
            this_result += args.delim+str(record[0]._properties[u'hasspn'])
        else:
            this_result += args.delim
        if 'pwdlastset' in record[0]._properties and record[0]._properties[u'pwdlastset'] > 0:
            this_result += args.delim+datetime.datetime.fromtimestamp(int(record[0]._properties[u'pwdlastset'])).strftime('%x %X')
        else:
            this_result += args.delim
        if 'lastlogon' in record[0]._properties and record[0]._properties[u'lastlogon'] > 0:
            this_result += args.delim+datetime.datetime.fromtimestamp(int(record[0]._properties[u'lastlogon'])).strftime('%x %X')
        else:
            this_result += args.delim
        if 'objectsid' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'objectsid']
        else:
            this_result += args.delim
        if 'email' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'email'].replace("\n"," ").replace("\r", " ").replace(","," ")
        else:
            this_result += args.delim
        if 'description' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'description'].replace("\n"," ").replace("\r", " ").replace(","," ")
        else:
            this_result += args.delim
        if 'notes' in record[0]._properties:
            this_result += args.delim+record[0]._properties[u'notes'].replace("\n"," ").replace("\r", " ").replace(","," ")
        else:
            this_result += args.delim
        if args.printresults: print this_result
        output_file.write(this_result.encode('utf8')+ "\r")
        records_found += 1
    return records_found


if args.contains is None:
    args.contains = ""  # Return all results

# Create the custom query
where = ""
if args.isenabled is True: where += " and n.enabled = true "
if args.isowned is True: where += " and n.owned = true "
if args.isadmin is True: where += " and n.admincount = true "
if args.issensitive is True: where += " and n.sensitive = true "
if args.ishighvalue is True: where += " and n.highvalue = true "
if args.ishasspn is True: where += " and n.hasspn = true "
if args.isdontreqpreauth is True: where += " and n.dontreqpreauth = true "

with driver.session() as session:
    if args.userlist is not None:
        session.read_transaction(match_users_from_list, args.userlist, where)
    else:
        session.read_transaction(match_user_name_contains, args.contains, where)


