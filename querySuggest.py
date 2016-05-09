import sys
# run command - python querySuggest.py <Cypher_dict> <dynamic_nodes_table_file.txt>
def main():
    user_query = raw_input("Enter your query: ").lower().split(' ')
    static_file = open(sys.argv[1],'r').read().split('\n')[:-1] # static nodes file
    dynamic_file = open(sys.argv[2],'r').read().split('\n')[:-1] # dynamic nodes file
    static_dict = {}
    dynamic_dict = {}
    # store the static pattens in a dict
    for line in static_file:
        temp = line.split("-")
        #remove trailing spaces and convert to lower case
        static_node = temp[0].rstrip().lower()
        cpattern = temp[1].rstrip().lower()
        static_dict[static_node]=cpattern
    #store the dynamic nodes or all words that appear in the database in a dict
    for lined in dynamic_file:
        tempd = lined.split("-")
        dynamic_node = tempd[0].rstrip().lower()
        dynamic_table = tempd[1].strip().lower()
        dynamic_dict[dynamic_node] = dynamic_table

    print dynamic_dict
    # tree of all static nodes, obtained from schema and the keywords in the templates we are interested in
    tree = {'all': set(['questions', 'answers', 'users']), 'questions': set(['title','have follows', 'have answersCount', 'did','answeredBy']), 'did': set(['users']) , 'answeredBy': set(['users']), 'users': set(['name', 'level', 'points', 'bestAnswerCount', 'questionsCount', 'answersCount']), 'answers' : set(['answerOf', 'answeredBy', 'has upVotes', 'has downVotes', 'ratings', 'commentsCount' , 'bestOrNot'])}
    
    """
    visited = set()
    stack = ['start']
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(tree[vertex] - visited)
        print visited
        print stack
    """
    # Storing all the words to be suggested in a list
    suggest = []
    suggest = user_query
    suggest_tail = ['']

    # process each word entered by user and make suggestions based on different conditions
    exit = 0
    while(exit == 0 ):
        suggest = user_query
        last_word = user_query[-1]
        n=0
        suggest_list = []
        suggest_tail = ['']
        for patterns in static_dict.keys():
            if last_word ==  patterns.split(' ')[0]:
                 #if patterns not in suggest: suggest.append(patterns)
                suggest_tail.append(patterns.split(' ')[1])
        
       # if the last word appears as one of the keys in the tree, print its children
        if last_word in tree.keys():
            #suggest.append(last_word)
            for child in tree[last_word]:
                if child not in suggest_tail : suggest_tail.append(child)
                if child in tree.keys():
                    for grand_child in tree[child]:
                        suggest_tail.append(child+" "+grand_child)

        # if last word is of or for, look at the second last word in the query
        if last_word == "of" or last_word == "for":
            if len(user_query) > 1:
                for k,v in tree.iteritems():
                    if user_query[-2] in v: 
                        suggest_tail.append(k)
        
        #if last word appears in the dynamic dict, store its parent and append its children to suggest_tail
        if last_word in dynamic_dict.keys():
            if dynamic_dict[last_word] in tree.keys():
                for child in tree[dynamic_dict[last_word]]:
                    if child not in suggest_tail : suggest_tail.append(child)
                    if child in tree.keys():
                        for grand_child in tree[child]:
                            suggest_tail.append(child+" "+grand_child)
                                    
        # print the list of suggestions thus collected
        for tail in suggest_tail:
            n=n+1
            for item in suggest:
                print item,
            print tail+" "+str(n)
            suggest_list.append(' '.join(suggest)+" "+tail)
            
        # An interactive interface to get input and make suggestions to the user
        user_choice = raw_input("Type your pick or type 0 to enter another query: ")
        try:
            uc = int(user_choice)
        except ValueError:
            print "Wrong option. Exiting ..."
            exit = 1
            break

        if uc <= n and uc !=0 :
            print "Your pick is "+str(uc)+" "+suggest_list[uc-1]
            exit = 1
        elif uc == 0:
            user_query = raw_input("Enter another query or type exit: ").split(' ')
            if user_query[0] == "exit" : exit = 1
        else :
            print "Wrong option. Exiting ... "
            exit = 1
       

if __name__ == "__main__":
    main()    
