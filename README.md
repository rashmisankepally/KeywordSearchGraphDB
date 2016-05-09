# KeywordSearchGraphDB
CMSC 724 DBMS project

This source code is for providing easier and faster querying on the neo4j graph database
This is organized in two parts:

1. Query suggestions
Run command is: 
python querySuggest.py <Cypher_dict> <dynamic_nodes_table_file.txt>

2. converting natural language queries to Cypher queries and querying the database
Run command is: 
python connect2neo4j.py dynamic_nodes_file.txt dynamic_nodes_table_file.txt

Then input your query
