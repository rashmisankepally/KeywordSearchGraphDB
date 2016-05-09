import time
import sys
from py2neo import authenticate, Graph

authenticate("localhost:7474", "username", "password")
graph = Graph("http://localhost:7474/db/data/")

print " In this sample you will be given 3 queries. You need to convert them to Cypher queries:"

myfile = open("user_test_results.txt", "a")
query_string = raw_input("Please type 1 to get the first question: ")
t0 = time.time()
print " What is Ninja's level?"
s=raw_input("Please type in your solution and press enter ")
t1= time.time()
diff=t1-t0;
results=graph.cypher.execute(s);
print results
myfile.write(str(diff) + '  ')


query_string = raw_input("Please type 2 to get the second question: ")
t0 = time.time()
print " How many Upvotes and Downvotes does Ninja have"
s=raw_input("Please type in your solution and press enter ")
t1= time.time()
diff=t1-t0;
results=graph.cypher.execute(s);
print results
myfile.write(str(diff) + '  ')

query_string = raw_input("Please type 3 to get the third question: ")
t0 = time.time()
print " What is the rating of Tim's answer?"
s=raw_input("Please type in your solution and press enter ")
t1= time.time()
diff=t1-t0;
results=graph.cypher.execute(s);
print results
myfile.write(str(diff) + '\n')