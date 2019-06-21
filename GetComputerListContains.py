import argparse
import os
from neo4j import GraphDatabase
import datetime

# Requirements:
# pip install neo4j
parser = argparse.ArgumentParser(description='Generate a list of computers from Bloodhound that contain a specific string'
                                             ' and exports the list as a csv.  This script can also optionally add '
                                             ' additional properties to the CSV results.')
parser.add_argument("-contains", type=str, help='A string that the computer contains')
parser.add_argument("-csv", type=str, default="ComputerList.csv",
                    help='The CSV file to export containing the results (default: %(default)s)')
parser.add_argument("-delim", type=str, default=",", help="CSV Delimiter (default: %(default)s)")
parser.add_argument("-printresults", action="store_true", help="Also prints the results to the console")
parser.add_argument("-isenabled", action="store_true", help="Only output enabled computers")
parser.add_argument("-isowned", action="store_true", help="Only output Owned computers")
parser.add_argument("-isadmin", action="store_true", help="Only output Admin Count computers")
parser.add_argument("-issensitive", action="store_true", help="Only output sensitive computers")
parser.add_argument("-ishighvalue", action="store_true", help="Only output high value computers")
parser.add_argument("-isunconstraineddelegation", action="store_true", help="Only output computers with unconstrained delegation")
parser.add_argument("-isdontreqpreauth", action="store_true", help="Only output computers that do not require preauth")
parser.add_argument("-allthedata", action="store_true", help="Adds all the data columns from BloodHound to the CSV output")
parser.add_argument("-username", type=str, default="neo4j", help="Neo4j username (default: %(default)s)")
parser.add_argument("-password", type=str, default="BloodHound", help="Neo4j password (default: %(default)s)")
parser.add_argument("-serverurl", type=str, default="bolt://localhost:7687", help="Neo4j server URL (default: %(default)s)")
args = parser.parse_args()

driver = GraphDatabase.driver(args.serverurl, auth=(args.username, args.password))

def match_user_name_contains(tx, contains, where):
    neo4j_query = 'MATCH (n:Computer) WHERE n.name contains "' + contains.upper() + '" ' + where + ' RETURN n'
    print neo4j_query
    records = tx.run(neo4j_query)
    output_file = open(args.csv, "w")
    if args.allthedata:  # Create headers
        output_file.write("Name"+args.delim+"Display Name"+args.delim+"Domain"+args.delim+"Enabled"+args.delim+"Owned"+
                          args.delim+"Unconstrained Delegation"+args.delim+"High Value"+args.delim+"Password Last Set"+
                          args.delim+"Last Login"+args.delim+"Operating System"+args.delim+"SID"+args.delim+"Notes"+"\r")
    records_found = process_records(records, output_file)
    output_file.close()
    print "Records Found: " + str(records_found)

def process_records(records, output_file):
    records_found = 0
    for record in records:
        this_result = record[0]._properties[u'name']
        if args.allthedata:
            if 'displayname' in record[0]._properties:
                this_result += args.delim+record[0]._properties[u'displayname'].replace("\n"," ").replace("\r", " ").replace(","," ")
            else: this_result += args.delim
            if 'domain' in record[0]._properties:
                this_result += args.delim+record[0]._properties[u'domain']
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
            if 'unconstraineddelegation' in record[0]._properties:
                this_result += args.delim + str(record[0]._properties[u'unconstraineddelegation'])
            else:
                this_result += args.delim
            if 'highvalue' in record[0]._properties:
                this_result += args.delim+str(record[0]._properties[u'highvalue'])
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
            if 'operatingsystem' in record[0]._properties:
                this_result += args.delim+record[0]._properties[u'operatingsystem'].replace("\n"," ").replace("\r", " ").replace(","," ")
            else:
                this_result += args.delim
            if 'objectsid' in record[0]._properties:
                this_result += args.delim+record[0]._properties[u'objectsid']
            else:
                this_result += args.delim
            if 'notes' in record[0]._properties:
                this_result += args.delim+record[0]._properties[u'notes'].replace("\n"," ").replace("\r", " ").replace(","," ")
            else:
                this_result += args.delim
        if args.printresults: print this_result
        output_file.write(this_result.encode('utf8') + "\r")
        records_found += 1
    return records_found


if args.contains is None:
    args.contains = ""  # Return all results

# Create the custom query
where = ""
if args.isenabled is True: where += " and n.enabled = true "
if args.isowned is True: where += " and n.owned = true "
if args.issensitive is True: where += " and n.sensitive = true "
if args.ishighvalue is True: where += " and n.highvalue = true "
if args.isunconstraineddelegation is True: where += " and n.unconstraineddelegation = true "

with driver.session() as session:
        session.read_transaction(match_user_name_contains, args.contains, where)


