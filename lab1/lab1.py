# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain, pretty_goal_tree
from data import *
import pprint

pp = pprint.PrettyPrinter(indent=1)
pprint = pp.pprint

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

# Fill this in with your rule
transitive_rule = IF( AND('(?x) beats (?y)', '(?y) beats (?z)' ), THEN( '(?x) beats (?z)' ))

# You can test your rule by uncommenting these pretty print statements
#  and observing the results printed to your screen after executing lab1.py
# pprint(forward_chain([transitive_rule], abc_data))
# pprint(forward_chain([transitive_rule], poker_data))
# pprint(forward_chain([transitive_rule], minecraft_data))


#### Part 3: Family Relations #########################################

# Define your rules here. We've given you an example rule whose lead you can follow:
# friend_rule = IF( AND("person (?x)", "person (?y)"), THEN ("friend (?x) (?y)", "friend (?y) (?x)") )
identity_rule = IF('person (?x)', THEN('self (?x) (?x)'))
child_rule = IF('parent (?x) (?y)', THEN('child (?y) (?x)'))
sibling_rule = IF(AND('parent (?x) (?y)', 'parent (?x) (?z)', NOT('self (?y) (?z)')), THEN('sibling (?y) (?z)'))
grandparent_rule = IF( AND('parent (?x) (?y)', 'parent (?y) (?z)'), THEN('grandparent (?x) (?z)', 'grandchild (?z) (?x)'))
cousin_rule = IF(AND('parent (?w) (?x)', 'parent (?y) (?z)', 'sibling (?w) (?y)'), THEN('cousin (?x) (?z)','cousin (?z) (?x)'))

# Add your rules to this list:
family_rules = [ identity_rule, child_rule, sibling_rule, grandparent_rule, cousin_rule ]

# Uncomment this to test your data on the Simpsons family:
# pprint(forward_chain(family_rules, simpsons_data, verbose=False))

# These smaller datasets might be helpful for debugging:
# pprint(forward_chain(family_rules, sibling_test_data, verbose=True))
# pprint(forward_chain(family_rules, grandparent_test_data, verbose=True))

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
# pprint(black_family_cousins)


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """
    hyp = OR([hypothesis])
    for rule in rules:
        # for consequent in rule.consequent():
            m = match(rule.consequent(),hypothesis)
            if m is not None:
                # good_consequent = populate(consequents, m)
                antecedents = rule.antecedent()
                if isinstance(antecedents, str):
                    antecedents = [antecedents]
                antecedent = [backchain_to_goal_tree(rules, populate(a, m)) for a in antecedents]
                if isinstance(antecedents, OR):
                    hyp.append(OR(antecedent))
                else:
                    hyp.append(AND(antecedent))
    return simplify(hyp)

# Uncomment this to test out your backward chainer:
pretty_goal_tree(backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin'))


#### Survey #########################################

NAME = "Monica Mladenik"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = None
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
print("(Doing forward chaining. This may take a minute.)")
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
