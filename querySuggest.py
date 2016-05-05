import sys

def main():
    user_query = raw_input("Type the query: ").split(' ')
    static_file = open(sys.argv[1],'r').read().split('\n')[:-1]
    static_dict = {}
    # store the static pattens in a dict
    for line in static_file:
        temp = line.split("-")
        #static_list = temp[0].split(' ')
        static_node = temp[0]
        cpattern = temp[1]
        static_dict[static_node]=cpattern

    # tree of all static nodes, obtained from schema and templates we are interested in
    tree = {'all': set(['questions', 'answers', 'users']), 'questions': set(['have title','have follows', 'have answersCount', 'questionedBy','answeredBy']), 'questionedBy': set(['users']) , 'answeredBy': set(['users']), 'users': set(['name', 'level', 'points', 'bestAnswerCount', 'questionsCount', 'answeresCount']), 'answers' : set(['answerOf', 'answeredBy', 'has upVotes', 'has downVotes', 'ratings', 'commentsCount' , 'bestOrNot'])}
    
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
    suggest = []
    suggest_tail = []
    for word in user_query:
        for patterns in static_dict.keys():
            if word in patterns.split(' '): 
                #print patterns
                if patterns not in suggest: suggest.append(patterns)
        if word in tree.keys():
            #print word
            suggest.append(word)
            for child in tree[word]:
                #print child,
                if child not in suggest_tail: suggest_tail.append(child)

    for tail in suggest_tail:
        for item in suggest:
            print item,
        print tail

if __name__ == "__main__":
    main()    
