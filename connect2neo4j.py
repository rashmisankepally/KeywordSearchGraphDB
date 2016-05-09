#Run the code : python connect2neo4j.py dynamic_nodes_file.txt dynamic_nodes_table_file.txt
#Then input your query


from py2neo import authenticate, Graph
import sys
from nltk.stem import *
import re

def main():
    authenticate("localhost:7474", "username", "password")#Change the username and password to your account ones
    graph = Graph("http://localhost:7474/db/data/")
    
    stemmer = PorterStemmer()
    
    #reading the file containing all the dynamic nodes and parsing the input query based on that into
    #static and dynamic nodes
    dynamic_nodes_set = open(sys.argv[1],'r').read().split(' ; ')
    query_string = raw_input("Enter Query: ")
    l = query_string.split('\'')[1::2]
    
    static_nodes=[]
    dynamic_nodes=[]
    for e in l:
        if(e!=''):
            e1="\'"+e+"\'"
            query_string=query_string.replace(e1,'')
            count=0;
            for d in dynamic_nodes_set:
                if((stemmer.stem(e)).lower() == (stemmer.stem(d)).lower()):
                    dynamic_nodes.append(e);
                    count=1;
                    break;
            if(count==0):
                static_nodes.append(e)

    query = query_string.split(' ')
    for keyword in query:
        if(keyword!=''):
            count=0;
            for d in dynamic_nodes_set:
                if((stemmer.stem(keyword)).lower() == (stemmer.stem(d)).lower() ):
                    dynamic_nodes.append(keyword);
                    count=1;
                    break;
            if(count==0):
                static_nodes.append(keyword)
    
    print static_nodes

    #reading the file containing dynamic nodes, the corresponding table names and
    #column names from the database
    dynamic_nodes_file = open(sys.argv[2],'r').read().split('\n')


    for i in xrange(0,len(dynamic_nodes)):
        for line in dynamic_nodes_file:
            temp = line.split(" - ")
            if((stemmer.stem(dynamic_nodes[i])).lower() == (stemmer.stem(temp[0])).lower()):
                dynamic_nodes[i]=temp[0];
                break;
    if('who' in static_nodes or 'Who' in static_nodes):
        dynamic_nodes.append('Name')

    print dynamic_nodes

    #store the table names and column names for each dynamci nodes
    table_name=[];
    column_name=[];
    for items in dynamic_nodes:
        for line in dynamic_nodes_file:
            temp = line.split(" - ")
            if(items == temp[0]):
                table_name.append(temp[1])
                if(len(temp) ==3):
                    column_name.append(temp[2])
                else:
                    column_name.append(' ');
                break;
    print table_name;
    print column_name;

    temp = set();

    for item in table_name:
        temp.add(item);

    #Write the MATCH section
    dict={};
    count=1;
    temp1=[];
    for item in temp:
        if(count==1):
            dict[item]="n1"
            temp1.append(item)
            s1 = "MATCH(n1:"+item+")"
        else:
            dict[item]="n"+str(count)
            temp1.append(item)
            s1 += ",(n"+str(count)+":"+item+")"
        count=count+1;
    print s1
    print temp1

    #Write the WHERE section
    flag=0;
    if(len(temp)>1):
        s1+=" WHERE ";
        flag=1;

    for i in xrange(1,len(temp1)):
        if(i>1):
            s1+=" AND "
        s1=WHERE_portion(temp1[0],temp1[i],s1,dict,dynamic_nodes);
    print s1;

    for i in xrange(0,len(column_name)):
        if(column_name[i] != ' ' and column_name[i] != dynamic_nodes[i]):
            if flag==0:
                flag=1;
                s1+=" WHERE "
            elif(i>0 or flag==1):
                s1+=" AND "
            s1+= dict[table_name[i]]+"."+column_name[i]+" = \'"+dynamic_nodes[i]+"\'"

    print s1

    #write the RETURN section
    s1+=" RETURN "
    already=0;
    if 'many' in static_nodes or 'count' in static_nodes or 'number' in static_nodes or 'numbers' in static_nodes:
        alrdy=0
        for i in xrange(0,len(dynamic_nodes)):
            if(column_name[i] == dynamic_nodes[i]):
                alrdy=1;
        for i in xrange(0,len(dynamic_nodes)):
            if(column_name[i] != dynamic_nodes[i] and alrdy==0):
                if(already>0):
                    s1+=","
                s1+=" COUNT(*) "
                already=1;
                break;
            elif(column_name[i] == dynamic_nodes[i]):
                if(already>0):
                    s1+=","
                s1+= dict[table_name[i]]+"."+dynamic_nodes[i]
                already=1;
    else:
        for i in xrange(0,len(dynamic_nodes)):
            if(column_name[i] == dynamic_nodes[i]):
                if(already>0):
                    s1+=","
                s1+= dict[table_name[i]]+"."+dynamic_nodes[i]
                already=1;



    print s1

    if 'maximum' in static_nodes or 'minimum' in static_nodes or 'order' in static_nodes :
        s1+=" ORDER BY toInt("
        if 'maximum' in static_nodes:
            keyword = 'maximum'
        elif 'minimum' in static_nodes:
            keyword = 'minimum'
        else:
            keyword ='order'
        befor_keyowrd, keyword, after_keyword = query_string.partition(keyword)


        for item in after_keyword.split(' '):
            b=0;
            for item1 in dynamic_nodes:
                if((stemmer.stem(item1)).lower() == (stemmer.stem(item)).lower()):
                    order_by =item1;
                    order_by_table_name = table_name[dynamic_nodes.index(item1)]
                    b=1;
                    break;
            if(b==1):
                break;
    
        s1+=dict[order_by_table_name]+"."+order_by+")"
        
        if 'maximum' in static_nodes:
            s1+=" DESC LIMIT 1"
        if 'minimum' in static_nodes:
            s1+= " LIMIT 1"
    
    print s1
    results=graph.cypher.execute(s1);
    print results


#function to generate the join condition between multiple tables
def WHERE_portion(item1,item2,s1,dict,dynamic_nodes):
    if(item1=='Users' or item1=='Answers'):
        s1+=dict[item1]+".uid = "
    else:
        s1+=dict[item1]+".QuestionedBy = "
    
    if(item2=='Users' or item2=='Answers'):
        s1+=dict[item2]+".uid "
    else:
        s1+=dict[item2]+".QuestionedBy"
    return s1;

if __name__=="__main__":
    main()
