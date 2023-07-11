#!/usr/bin env python 2.7
"""
Localize
Iterates the axioms in a ProverX object and replaces one of its variables with a constant
"""

__authors__ = "Afonso Bras Sousa, Manuel Madelino, Henrique Duarte"
__maintainer__ = "Afonso Bras Sousa"
__email__ = "ab.sousa@campus.fct.unl.pt"
__version__ = 0.1

import copy
import re

"""
getVars
Finds variables in an axiom (started with u-z)
Ignores functions and duplicates
"""
def getVars(axiom):
    variables = re.findall(r"[u-z]\w*", axiom)  # find variables
    formulas = re.findall(r"([u-z]\w*)\(", axiom)  # find functions
    variables = [i for i in variables if i not in formulas]  # remove functions from list
    return set(variables)  # removes duplicates


"""
localize variable
Replaces a variable in an axiom with a constant
"""
def localizeVar(axiom, var, const_name):
    # print "DEBUG REPLACE %s in %s" % (var, axiom)
    newaxiom = "L(%s) <-> " % const_name
    newaxiom += re.sub(r"\b%s\b" % var, const_name, axiom)
    # print "DEBUG %s" % newaxiom
    return newaxiom


"""
replace axiom
Replaces an axiom within a ProverX object with another axiom
"""
def replaceAxiom(obj, oldAxiom, newAxiom):
    newObj = copy.deepcopy(obj)
    newObj.axioms.remove(oldAxiom)
    newObj.axioms.append(newAxiom)
    return newObj


"""
Localize
Iterates the axioms in a ProverX object and replaces one of its variables with a constant
Ignores axioms in the ignore list
"""
def localize(obj, goal, ignore_list=[]):
    result = []
    obj.goals.replace(goal) # replace original goals with our localize goal
    for axiom in obj.axioms:
        if axiom in ignore_list: continue # ignore axioms in ignore_list
        vars = getVars(axiom)
        for var in vars:
            # print "DEBUG %s" % var
            newAxiom = localizeVar(axiom, var, CONSTANT) # replace a variable with a constant
            newObj = replaceAxiom(obj, axiom, newAxiom) # replace the original axiom with our localized axiom
            newObj = newObj.find_both() # check for proof
            if newObj.proofs.found:
                result.append(newObj)
    return result

"""
Main function
"""

CONSTANT = "cLOCAL"  # set name of constant

example = Proverx('abelian.in') # load a proverX file
result = localize(example, "L(a) -> L(a').") # returns list of proverX objects where the specified goal proof was found -- in this case for L(a) -> L(a')

# Printing all the valid proverX objects:
for index, item in enumerate(result):
    print "=== Localized result #%d ===" % index
    print 'Axioms'
    print item.axioms
    
    print "Proofs found:"
    print item.find_proofs()
    print ""
    
    # Shows the proof
    # print p.proofs

# Testing ignore list

result = localize(example, "L(a) -> L(a').", ["1 * x = x"]) # the axiom 1 * x = x will be ignored

# Printing all the valid proverX objects:
for index, item in enumerate(result):
    print "=== Localized result #%d ===" % index
    print 'Axioms'
    print item.axioms
    
    print "Proofs found:"
    print item.find_proofs()
    print ""
    
    # Shows the proof
    # print p.proofs
