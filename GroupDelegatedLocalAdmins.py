import argparse
import os
from neo4j import GraphDatabase

# Requirements:
# pip install neo4j
parser = argparse.ArgumentParser(description='From a list of BloodHound users (must be in uppercase format like:'
                                             ' USER@DOMAIN.COM) this script will check the number of Group Delegated'
                                             ' Local Admin rights each user has on the list and exports the list '
                                             ' as a csv.')
parser.add_argument("-userlist", type=str, help='Path to userlist to use in the query')
parser.add_argument("-csv", type=str, default="GroupDelegatedLocalAdmins.csv",
                    help='The CSV file to export containing the results (default: %(default)s)')
parser.add_argument("-username", type=str, default="neo4j", help="Neo4j username (default: %(default)s)")
parser.add_argument("-password", type=str, default="BloodHound", help="Neo4j password (default: %(default)s)")
parser.add_argument("-serverurl", type=str, default="bolt://localhost:7687", help="Neo4j server URL (default: %(default)s)")
args = parser.parse_args()

driver = GraphDatabase.driver(args.serverurl, auth=(args.username, args.password))

def count_group_delegated_local_admins(tx, name):
    records = tx.run("MATCH p=(m:User {name:\""+name+"\"})-[r1:MemberOf*1..]->(g:Group)-[r2:AdminTo]->(n:Computer) RETURN p")
    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count


if args.userlist != None:
    output_file = open(args.csv, "w")
    input_file = open(args.userlist, "r")
    for user in input_file:
        with driver.session() as session:
            record_count = session.read_transaction(count_group_delegated_local_admins, user.strip())
            if record_count > 0:
                print user.strip() + " = " + str(record_count)
                output_file.write(user.strip()+","+str(record_count)+"\r")
    output_file.close()
    input_file.close()
else:
    parser.print_help()
    print "Please specify the -userlist parameter."