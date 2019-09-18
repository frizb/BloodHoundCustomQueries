import argparse
import os
from neo4j import GraphDatabase

# Requirements:
# pip install neo4j
parser = argparse.ArgumentParser(description='Provides a list of administrator and admin groups for a specific Computer or list of computers and output to CSV.'
                                             ' Appends any labels to the CSV and also if the account is enabled. ')
parser.add_argument("-computername", type=str, help='Name of the computer in the DC (EX. CORP-DC01.TEST.LOCAL)')
parser.add_argument("-computerlist", type=str, help='Path to the computer list file to use in the query.')
parser.add_argument("-csv", type=str, default="ComputerAdmins.csv",
                    help='The CSV file to export containing the results (default: %(default)s)')
parser.add_argument("-username", type=str, default="neo4j", help="Neo4j username (default: %(default)s)")
parser.add_argument("-password", type=str, default="BloodHound", help="Neo4j password (default: %(default)s)")
parser.add_argument("-serverurl", type=str, default="bolt://localhost:7687", help="Neo4j server URL (default: %(default)s)")
args = parser.parse_args()

driver = GraphDatabase.driver(args.serverurl, auth=(args.username, args.password))

def get_list_of_computer_admins(tx, computer):
    query = "MATCH p=(n)-[b:AdminTo]->(c:Computer {name:\""+computer+"\"}) RETURN p"
    #print query
    records = tx.run(query)
    return records

if args.computername != None:
    output_file = open(args.csv, "w")
    with driver.session() as session:
        records = session.read_transaction(get_list_of_computer_admins, args.computer.strip())
        for record in records:
            print record[0]._nodes[0]._properties[u'name']
            if u'enabled' in record[0]._nodes[0]._properties:
                output_file.write(record[0]._nodes[0]._properties[u'name'].strip() + "," + str(
                    record[0]._nodes[0]._labels) + "," + str(record[0]._nodes[0]._properties[u'enabled']) + "\r")
            else:
                output_file.write(
                    record[0]._nodes[0]._properties[u'name'].strip() + "," + str(record[0]._nodes[0]._labels) + "\r")
    output_file.close()
elif args.computerlist != None:
    output_file = open(args.csv, "w")
    input_file = open(args.computerlist, "r")
    for computer in input_file:
        with driver.session() as session:
            records = session.read_transaction(get_list_of_computer_admins, computer.strip())
            for record in records:
                print record[0]._nodes[0]._properties[u'name']
                if u'enabled' in record[0]._nodes[0]._properties:
                    output_file.write(record[0]._nodes[0]._properties[u'name'].strip() + "," + str(
                        record[0]._nodes[0]._labels) + "," + str(record[0]._nodes[0]._properties[u'enabled']) + "\r")
                else:
                    output_file.write(
                        record[0]._nodes[0]._properties[u'name'].strip() + "," + str(record[0]._nodes[0]._labels) + "\r")

    output_file.close()
    input_file.close()
else:
    parser.print_help()
    print "Please specify the -computername parameter"
