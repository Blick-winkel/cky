# -*- coding: utf-8 -*-
"""
Kathryn Nichols
Stefan Behr
LING 571
Project 1

This program reads in a context free grammar at
arg 1 and outputs the grammar in Chomsky Normal
Form to the file at arg 2. Comments and empty
lines are eliminated.

"""

import sys

i = 1               # tracks names of new rules
rule_map = {}       # stores rules
output = ''         # stores output

# Returns a list of terminals and their
# indices in the given rule
def find_terminals(rule):
    terminals = []
    indices = []
    j = 0
    for item in rule:
        if item[0] == "'":
            terminals.append(item)
            indices.append(j)
        j += 1
    
    return terminals, indices

# Returns a string representation
# of the given rule
def stringify(rule):
    string = rule[0] + ' ->'
    for item in rule[1:]:
        string += ' ' + item
    string += '\n'
    
    return string

# Adds a rule to the dictionary of rules
def add_rule(rule):
    
    global rule_map
    
    if rule[0] not in rule_map:
        rule_map[rule[0]] = []
    rule_map[rule[0]].append(rule[1:])

# Replaces the terminals in the given
# rule with new nonterminals. Adds
# new rules to the output, returns
# altered rule
def replace_terminals(rule, terminals, indices):
    
    global output
    global i
    
    for j in range(len(indices)):
        new_node = 'X' + str(i)
        i += 1
        rule[indices[j]] = new_node
        output += stringify([new_node] + [terminals[j]])
    
    return rule

# Replaces first two elements in given
# rule with a new nonterminal. Adds
# new rule to the output, returns
# altered rule
def replace_long(rule):
    
    global output
    global i
    
    new_node = 'X' + str(i)
    i += 1
    output += stringify([new_node] + rule[1:3])
    rule = [rule[0]] + [new_node] + rule[3:]
    
    return rule

# Reads in CFG file, converts to Chomsky
# Normal Form and outputs to file
def main():
    
    global output
    
    reserves = []
    
    with open(sys.argv[1]) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            line = line.strip()
            
            # do not process commented or empty lines
            if line != '' and line[0] != '#':
                line = line.split('->')
                lhs = line[0].strip()
                rhs = line[1:][0].strip().split('|')
                
                for item in rhs:
                    rule = [lhs] + item.split()
                    skip = False
                    
                    # reserve unit productions for the end
                    if len(rule) == 2 and rule[1][0] != "'":
                        reserves.append(rule)
                        skip = True
                    
                    # not a terminal
                    elif len(rule) > 2:
                        
                        # find hybrid rules
                        terminals, indices = find_terminals(rule)
                        if len(terminals) > 0:
                            rule = replace_terminals(rule, terminals, indices)
                            
                        # convert long productions
                        while len(rule) > 3:
                            rule = replace_long(rule)
                    
                    add_rule(rule)
                    
                    if not skip:
                        output += stringify(rule)   # output final rule
    
    
    # convert unit productions 
    while len(reserves) > 0:
        rule = reserves.pop()
        if rule[1] in rule_map:
            for item in rule_map[rule[1]]:
                new_rule = [rule[0]] + item
                #print new_rule
                if len(new_rule) > 2 or new_rule[1][0] == "'":
                    output += stringify(new_rule)
                else:
                    reserves.append(new_rule)
                add_rule(new_rule)
    
    with open(sys.argv[2], 'w') as f:
        f.write(output)

main()
            