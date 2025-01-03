"""
SUMMARY:
Takes the calculated output values and assesses whether or not they meet the
current set of constraints/rules.  If they do not meet the rules, then it
assesses the extent to which this failure occurs.  If they do meet the rules,
then it assesses the extent to which failure has been avoided.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_start import outputStart
import numpy as np
import sympy as sp
import copy
import math

"""
SECONDARY FUNCTION
"""
def outputDiff(rule, i, d):
    """
    Description
    -----------
    A recursive function that calls itself until the rule being passed to it is
    a sympy inequality rather than an And or Or relational so that the
    normalized difference of a point to the base inequality can be calculated
    and evaluated further if it rests within a sympy relational before being
    returned for the root-mean square difference equation or minimum selection.
    
    Parameters
    ----------
    rule : Sympy relational or inequality
        The current rule for which an output point's failure or success
        difference is calculated
    i : Integer
        Index of the current design point
    d : Dictionary
        The particular discipline from which output information is being 
        gathered and stored
    
    Returns
    -------
    np.nanmin, np.nanmax, diff, ndiff : Float
        The failure difference of a point to the current rule whether that
        difference is a single value associated with an inequality (diff,
        ndiff), a list of inequalities (np.nanmin, np.nanmax), or not a number
        (np.nan)
    """
    
    # Check if rule is an Or or And relational
    if isinstance(rule, sp.Or) or isinstance(rule, sp.And):
        
        # Create a numpy zero array for the length of the arguments
        diff_vector = np.zeros(len(rule.args))
        
        # Loop through each argument of the rule
        for arg in rule.args:
            
            # Call the function again and assign its value to vector
            diff_vector[rule.args.index(arg)] = outputDiff(arg, i, d)
        
        # Check if rule is Or relational
        if isinstance(rule, sp.Or):
            
            # Return proper min or max value depending on pass/fail of point
            if d['pass?'][i] == False: return np.nanmin(diff_vector)
            elif any(isinstance(arg, sp.Or) for arg in rule.args):
                return np.nanmin(diff_vector)
            elif any(isinstance(arg, sp.And) for arg in rule.args):
                return np.nanmin(diff_vector)
            else: return np.nanmax(diff_vector)
        
        # Always return minimum value greater than 0.0 for And relational
        else:
            
            # Create a mask for values greater than 0.0
            mask = diff_vector > 0.0
            
            # Avoid error with all values being false in mask
            if np.all(~mask):
                return 0.0
            
            # Apply mask and return minimum value
            return np.nanmin(diff_vector[mask])
    
    # Perform following commands if rule is not an Or or And relational
    else:
        
        # Make a copy of the inequality
        rule_copy = copy.deepcopy(rule)
        
        # Gather free symbols of the inequality
        symbs = rule.free_symbols
        
        # Loop through each free symbol
        for symb in symbs:
            
            # Get index in the discipline of the free symbol and substitute
            # point value into free symbol of inequality
            if str(symb) in str(d['outs']):
                ind = d.get('outs').index(symb)
                rule_copy = rule_copy.subs(symb, d['tested_outs'][i, ind])
            else:
                ind = d.get('ins').index(symb)
                rule_copy = rule_copy.subs(symb, d['tested_ins'][i, ind])
        
        # Return 0.0 if inequality is true but point is failing...as difference
        ### should not contribute to fail amount
        if rule_copy and d['pass?'][i] == False:
            return 0.0
        
        # Return nan if inequality is not true but point is passing...as
        ### difference should not contribute to pass amount
        elif ~rule_copy and d['pass?'][i] == True:
            return np.nan
        
        # Perform following commands if rule copy is true and point is passing
        ### or if rule copy is false and point is failing
        else:
            
            # Determine difference between lhs and rhs of rule
            diff = abs(d['out_ineqs'][rule][i] - rule.rhs)
            
            # Determine range of values seen by the calculated rule
            range_array = d['out_ineqs'][rule]
            if 'eliminated' in d:
                range_array = np.concatenate((range_array, 
                    d['eliminated']['out_ineqs'][rule]), axis=0)
            
            # Check if calculated rule values have a range of 0.0
            if math.isclose(np.ptp(range_array), 0.0):
                
                # Return the non-normalized difference
                return diff
            
            # Normalize difference w/range of all values seen by rule
            ndiff = diff / np.ptp(range_array)
                
            # Return normalized absolute difference of lhs and rhs
            return ndiff


"""
CLASS
"""
class checkOutput:
    
    def __init__(self,discip,output_rules):
        """
        Parameters
        ----------
        discip : Dictionary
            Contains various key-value pairs associated with the current 
            details of the particular discipline
        output_rules : List of symbolic inequalities
            A condensed list of rules that will dictate whether the output
            values of the particular discipline pass or fail
        """
        self.d = discip
        self.outr = output_rules
        return
    
    
    def basicCheck(self):
        """
        Description
        -----------
        Checks whether the output values pass or fail the current set of output
        rules and adds this information to the discipline's dictionary of
        information.
        
        Parameters
        ----------
        None.

        Returns
        -------
        self.d : Dictionary
            The same dictionary now updated with new boolean values indicating
            passing or failing based on the corresponding output values
        """
        
        # Initial definitions to make code more readable
        start = outputStart(self.d, 'pass?')
        tested_outs = self.d['tested_outs']
        tested_ins = self.d['tested_ins']
        
        # Loop through each NEW design point in the output space
        for i in range(start, tested_outs.shape[0]):
            
            # Make a copy of the output rules
            rules_copy = copy.deepcopy(self.outr)
            
            # Loop through each output rule
            for j in range(0,len(self.outr)):
                
                # Loop through each output variable of the discipline
                for k in self.d['outs']:
                    
                    # Substitute output value for the variable in rule
                    rules_copy[j] = rules_copy[j].subs(k,
                        tested_outs[i, self.d['outs'].index(k)])
                
                # Loop through each input variable of the discipline
                for k in self.d['ins']:
                    
                    # Substitute input value for the variable in rule
                    rules_copy[j] = rules_copy[j].subs(k,
                        tested_ins[i, self.d['ins'].index(k)])
                    
            # Append boolean value to the proper dictionary key
            self.d['pass?'].append(all(rules_copy))
            
        # Return new dictionary with boolean values
        return self.d
    
    
    def rmsFail(self):
        """
        Description
        -----------
        When a point is failing at least one requirement, it calculates the 
        normalized root mean square difference of calculated output points to
        each relevant rule of the discipline.  When a point is not failing any
        requirments, it determines the minimum difference of calculated output
        points to threshold of rule relevant to the discipline.  Returns the
        "Fail_Amount" or "Pass_Amount" as part of a numpy vector in each
        discipline's dictionary.
        
        Parameters
        ----------
        None.

        Returns
        -------
        self.d : Dictionary
            The same dictionary now updated with new failure and pass amounts 
            for all of the output points that have been calculated thus far
        """
        
        # Initial definitions to make code more readable
        start = outputStart(self.d, 'Fail_Amount')
        pass_ = self.d['pass?']
        
        # Loop through each NEW design point
        for i in range(start,len(pass_)):
            
            # Initialize a numpy vector the same length as the rules
            tv_diff = np.zeros(len(self.outr))
            
            # Loop through each output rule
            for rule in self.outr:
                
                # Determine normalized difference of point to rule's threshold
                tv_diff[self.outr.index(rule)] = \
                    outputDiff(rule, i, self.d)
            
            # Check if point is already passing
            if pass_[i] == True:
                
                # Append 0.0 to the failure amount vector
                self.d['Fail_Amount'] = np.append(self.d['Fail_Amount'], 0.0)
                
                # Calculate minimum difference for set of relevant output rules
                min_d = np.nanmin(tv_diff)
                
                # Append min difference value to the pass amount vector
                self.d['Pass_Amount'] = np.append(self.d['Pass_Amount'], min_d)
                
            # Perform the following commands if the point is not passing
            else:
                
                # Append 0.0 to the pass amount vector
                self.d['Pass_Amount'] = np.append(self.d['Pass_Amount'], 0.0)
                
                # Calculate the NRMSD for the set of relevant output rules
                nrmsd = np.sqrt(np.sum(np.square(tv_diff))/len(tv_diff))
                
                # Append the NRMSD value to the failure amount vector
                self.d['Fail_Amount'] = np.append(self.d['Fail_Amount'], nrmsd)
                
        # Return updated dictionary with normalized failure amounts
        return self.d
    