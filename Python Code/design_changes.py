"""
SUMMARY:
Initiates design changes of a user-specified type at a user-specified point in
time for a design problem. NOTE: Currently set up specifically for the SenYang
bulk carrier design problem.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from get_constraints import getConstraints, getInequalities
from calc_rules import calcRules
from output_success import checkOutput
from vars_def import X
import numpy as np
import sympy as sp


"""
CLASS
"""
class changeDesign:
    
    def __init__(self, Discips, Input_Rules, Output_Rules):
        """
        Parameters
        ----------
        Discips : List of dictionaries
            Information pertaining to each discipline
        Input_Rules : List
            Current list of design space rules that each discipline needs to 
            abide by
        Output_Rules : List
            Current list of objectice space rules that each discipline needs to
            adhere to
        """
        self.D = Discips
        self.In_Rules = Input_Rules
        self.Out_Rules = Output_Rules
        return
    
    
    # Addition or subtraction of any input variables for a discipline
    def Inputs(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Changes to the analyses used to calculate output points from input points
    def Analyses(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Addition or subtraction of any output variables for a discipline
    def Outputs(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    def Reqs(self):
        """
        Description
        -----------
        Establish new objective space requirements that need to be satisfied.

        Returns
        -------
        Discips : List of dictionaries
            Same information pertaining to each discipline
        Input_Rules : List
            Same list of design space rules that each discipline needs to abide
            by
        Output_Rules : List
            New list of objectice space rules that each discipline needs to
            adhere to
        """
        
        # Create sympy design and output variables
        x = sp.symbols('x1:7') # L, T, D, C_B, B, V
        y = sp.symbols('y1:4') # F_n, GM, DW
        
        # Adjust the list of output rules - ~50% FEASIBLE SPACE REDUCTION!
        output_rules = [y[0] <= 0.292, y[1] - 0.092*X(x[4],4) >= 0.0, 
                        sp.And(y[2] >= 94000, y[2] <= 190000),
                        y[2] - (X(x[1],1)/0.45)**(1.0/0.31) >= 0.0]
        
        # Assign new output rules to the problem
        self.Out_Rules = output_rules
        
        # Return the discipline and rule information for the problem
        return self.D, self.In_Rules, self.Out_Rules
    
    
    def reevaluatePoints(self):
        """
        Description
        -----------
        Reevaluate the pass-fail amounts of all the previously explored design
        points and update the results for the requirements change(s).

        Returns
        -------
        Discips : List of dictionaries
            New information pertaining to each discipline
        """
        
        # Loop through each discipline
        for discip in self.D:
            
            # Remove all of the pass-fail amount data (and create design and
            ### output variable keys in eliminated key)
            discip['pass?'] = []
            discip['out_ineqs'] = {}
            discip['Fail_Amount'] = np.array([], dtype=float)
            discip['Pass_Amount'] = np.array([], dtype=float)
            if 'eliminated' in discip:
                discip['eliminated']['pass?'] = []
                discip['eliminated']['out_ineqs'] = {}
                discip['eliminated']['Fail_Amount'] = np.array([], dtype=float)
                discip['eliminated']['Pass_Amount'] = np.array([], dtype=float)
                discip['eliminated']['ins'] = discip['ins']
                discip['eliminated']['outs'] = discip['outs']
                
            # Determine current output value rules for the discipline to meet
            output_rules = getConstraints(discip['outs'] + discip['ins'], 
                                          self.Out_Rules)
            
            # Gather any new inequalities of relevance to the discipline
            discip = getInequalities(discip, output_rules, 'out_ineqs')
            
            # Add inequality to eliminated key if it exists
            if 'eliminated' in discip:
                discip['eliminated'] = getInequalities(discip['eliminated'], 
                    output_rules, 'out_ineqs')
            
            # Calculate lhs of output rule inequality for each point
            discip['out_ineqs'] = calcRules(discip, 'out_ineqs', 'tested_outs',
                                            'outs', 'tested_ins', 'ins')
            if 'eliminated' in discip:
                discip['eliminated']['out_ineqs'] = \
                    calcRules(discip['eliminated'], 'out_ineqs', 'tested_outs', 
                              'outs', 'tested_ins', 'ins')
            
            # Check whether the output points pass or fail
            outchk1 = checkOutput(discip, output_rules)
            discip = outchk1.basicCheck()
            if 'eliminated' in discip:
                outchk2 = checkOutput(discip['eliminated'])
                discip['eliminated'] = outchk2.basicCheck()
            
            # Determine the extent to which points pass and fail
            discip = outchk1.rmsFail()
            if 'eliminated' in discip:
                discip['eliminated'] = outchk2.rmsFail()
        
        # Return the update information for each discipline
        return self.D

