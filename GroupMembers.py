import argparse
import os
from neo4j import GraphDatabase

# Requirements:
# pip install neo4j
parser = argparse.ArgumentParser(description='From a list of BloodHound users (must be in uppercase format like:'
                                             ' USER@DOMAIN.COM) this script will check which users are members of a '
                                             ' specific Group and exports the list. Or alternatively you can specify just'
                                             ' a group and get a list of all members'
                                             ' as a csv.')
parser.add_argument("-userlist", type=str, help='Path to userlist file to use in the query')
parser.add_argument("-group", type=str, help='Name of the group in the DC')
parser.add_argument("-csv", type=str, default="GroupMembers.csv",
                    help='The CSV file to export containing the results (default: %(default)s)')
parser.add_argument("-username", type=str, default="neo4j", help="Neo4j username (default: %(default)s)")
parser.add_argument("-password", type=str, default="BloodHound", help="Neo4j password (default: %(default)s)")
parser.add_argument("-serverurl", type=str, default="bolt://localhost:7687", help="Neo4j server URL (default: %(default)s)")
args = parser.parse_args()

driver = GraphDatabase.driver(args.serverurl, auth=(args.username, args.password))

def count_paths_to_domain_admin(tx, name):
    query = "MATCH p=(m:User {name:\""+name+"\"})-[b:MemberOf]->" \
                     "(c:Group {name: \""+args.group+"\"}) RETURN p"
    #print query
    records = tx.run(query)

    query_record_count = 0
    for record in records:
        query_record_count += 1
    return query_record_count

def get_list_of_group_members(tx):
    query = "MATCH p =(n)-[r:MemberOf*1..]->" \
                     "(c:Group {name: \""+args.group+"\"}) RETURN p"
    #print query
    records = tx.run(query)
    return records

if args.userlist != None and args.group != None:
    output_file = open(args.csv, "w")
    input_file = open(args.userlist, "r")
    for user in input_file:
        with driver.session() as session:
            record_count = session.read_transaction(count_paths_to_domain_admin, user.strip())
            if record_count > 0:
                print user.strip() + " = " + str(record_count)
                output_file.write(user.strip()+","+str(record_count)+"\r")
    output_file.close()
    input_file.close()
elif args.group != None:
    output_file = open(args.csv, "w")
    with driver.session() as session:
        records = session.read_transaction(get_list_of_group_members)
        for record in records:
            print record[0]._nodes[0]._properties[u'name']
            output_file.write(record[0]._nodes[0]._properties[u'name'].strip()+"\r")
    output_file.close()
else:
    parser.print_help()
    print "Please specify the -userlist parameter and/or the -group parameter"
