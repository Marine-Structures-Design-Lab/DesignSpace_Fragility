"""
SUMMARY:
Takes the calculated output values and assesses whether or not they meet the
current set of constraints/rules.  If they do not meet the rules, then it
provides the opportunity to assess the extent to which this failure occurs.

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
import warnings

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
    returned for the root-mean square difference equation
    
    Parameters
    ----------
    rule : Sympy relational or inequality
        The current rule for which an output point's failure difference is
        calculated
    i : Integer
        Index of the current design point
    d : Dictionary
        The particular discipline from which output information is being 
        gathered and stored

    Returns
    -------
    np.nanmin, np.nanmax, np.nan, diff, ndiff : Float or nan
        The failure difference of a point to the current rule whether that
        difference is a single value associated with an inequality (diff,
        ndiff), a list of inequalities (np.nanmin, np.nanmax), or nan because
        the point is not failing
    """
    
    # Check if rule is an Or or And relational
    if isinstance(rule, sp.Or) or isinstance(rule, sp.And):
        
        # Create a numpy zero array for the length of the arguments
        diff_vector = np.zeros(len(rule.args))
        
        # Loop through each argument of the rule
        for arg in rule.args:
            
            # Call the function again and assign its value to vector
            diff_vector[rule.args.index(arg)] = outputDiff(arg,i, d)
        
        # Turn off the warning messages for an all NaN matrix/vector
        warnings.filterwarnings\
            ('ignore', 'All-NaN (slice|axis) encountered')
        
        # Return min of difference array for each point of Or rule
        if isinstance(rule, sp.Or): return np.nanmin(diff_vector)
        
        # Return max of difference array for each point of And rule
        else: return np.nanmax(diff_vector)
    
    # Perform following commands if rule is not an Or or And relational
    else:
        
        # Make a copy of the inequality
        rule_copy = copy.deepcopy(rule)
        
        # Gather free symbols of the inequality
        symbs = rule.free_symbols
        
        # Loop through each free symbol
        for symb in symbs:
            
            # Get index in the discipline's outputs of the free symbol
            ind = d['outs'].index(symb)
            
            # Substitute output value into free symbol of rule copy
            rule_copy = rule_copy.subs(symb, d['tested_outs'][i,ind])
        
        # Check if the rule copy is true
        if rule_copy:
            
            # Return not a number
            return np.nan
        
        # Perform the following commands if the rule copy is not true
        else:
            
            # Determine difference between lhs and rhs of rule
            diff = abs(d['out_ineqs'][rule][i] - rule.rhs)
            
            # Check if calculated rule values have a range of 0.0
            if math.isclose(np.ptp(d['out_ineqs'][rule]), 0.0):
                
                # Return the non-normalized difference
                return diff
            
            # Normalize difference w/range of all values seen by rule
            ndiff = diff / np.ptp(d['out_ineqs'][rule])
                
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
        information
        
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
        
        # Loop through each NEW design point in the output space
        for i in range(start, tested_outs.shape[0]):
            
            # Make a copy of the output rules
            rules_copy = copy.deepcopy(self.outr)
            
            # Loop through each output rule
            for j in range(0,len(self.outr)):
                
                # Loop through each output variable of the discipline
                for k in self.d['outs']:
                    
                    # Substitute output value for the variable in rule
                    rules_copy[j] = rules_copy[j].subs(k,\
                        tested_outs[i,self.d['outs'].index(k)])
                    
            # Append boolean value to the proper dictionary key
            self.d['pass?'].append(all(rules_copy))
            
        # Return new dictionary with boolean values
        return self.d
    
    
    def rmsFail(self):
        """
        Description
        -----------
        Calculates the normalized root mean square difference of calculated
        output points to each relevant rule of the discipline and returns those
        values as part of a numpy vector in the discipline's "Fail_Amount" key
        
        Parameters
        ----------
        None.

        Returns
        -------
        self.d : Dictionary
            The same dictionary now updated with new failure amounts for all of
            the output points that have been calculated thus far
        """
        
        # Initial definitions to make code more readable
        start = outputStart(self.d, 'Fail_Amount')
        pass_ = self.d['pass?']
        
        # Loop through each NEW design point
        for i in range(start,len(pass_)):
            
            # Check if point is already passing
            if pass_[i] == True:
                
                # Append 0.0 to the failure amount vector
                self.d['Fail_Amount'] = np.append(self.d['Fail_Amount'], 0.0)
            
            # Perform the following commands if the point is not passing
            else:
                
                # Initialize a numpy vector the same length as the rules
                tv_diff = np.zeros(len(self.outr))
                
                # Loop through each output rule
                for rule in self.outr:
                    
                    # Determine the normalized difference that point fails rule
                    tv_diff[self.outr.index(rule)] = \
                        outputDiff(rule, i, self.d)
                
                # Identify any instances of not a number
                nan_mask = np.isnan(tv_diff)
                
                # Replace any instance of not a number with 0.0
                tv_diff[nan_mask] = 0.0
                
                # Calculate the NRMSD for the set of relevant output rules
                nrmsd = np.sqrt(np.sum(np.square(tv_diff))/len(tv_diff))
                
                # Append the NRMSD value to the failure amount vector
                self.d['Fail_Amount'] = np.append(self.d['Fail_Amount'],nrmsd)
                
        # Return updated dictionary with normalized failure amounts
        return self.d
    
