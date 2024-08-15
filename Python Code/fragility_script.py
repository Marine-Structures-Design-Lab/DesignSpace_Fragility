"""
SUMMARY:
Contains methods for performing either a probabilistic fragility model (PFM) or
entropic fragility model (EFM) assessment depending on the model chosen by the
user in the main script file.  Goes on to quantify and assess the risk relative
to an adaptive threshold that can be slightly manipulated as well.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from windfall_regret import evalCompProb, calcWindRegret, quantRisk, plotWindRegret
from entropy_tracker import prepEntropy, evalEntropy
from fragility_check import checkFragility
import copy


"""
CLASS
"""
class fragilityCommands:
    
    def __init__(self, Discips_fragility, irules_fragility, pf_combos,
                 pf_fragility, pf_std_fragility, passfail, passfail_std):
        """
        Parameters
        ----------
        Discips_fragility : Dictionary
            All information pertaining to each discipline at the beginning of
            the newest space reduction cycle
        irules_fragility : List
            Sympy and/or relationals detailing all of the new space reduction
            rules of the current space reduction cycle
        pf_combos : Dictionary
            Each discipline's pass-fail predictions for each design space of
            each new rule combination being considered
        pf_fragility : List
            Each discipline's pass-fail predictions for the non-reduced design
            space at the beginning of the space reduction cycle
        pf_std_fragility : List
            Each discipline's pass-fail standard deviations for the non-reduced
            design space at the beginning of the space reduction cycle
        passfail : List of dictionaries
            History of each discipline's pass-fail predictions up to a certain
            point in time
        passfail_std : List of dictionaries
            History of each discipline's pass-fail standard deviatiokns up to a
            certain point in time
        """
        self.Df = Discips_fragility
        self.irf = irules_fragility
        self.pf_combos = pf_combos
        self.pf_frag = pf_fragility
        self.pf_std_frag = pf_std_fragility
        self.pf = passfail
        self.pf_std = passfail_std
        return
    
    
    def PFM(self):
        """
        Description
        -----------
        Performs the necessary commands to evaluate each design space's
        fragility with the probabilistic fragility model approach.

        Returns
        -------
        wr : Dictionary
            Windfall and regret data for each discretized point remaining in
            the non-reduced, reduced, and leftover design spaces of each 
            discipline for all of the rules proposed in the current time stamp
        run_wind : Dictionary
            Fraction of windfall potential in remaining design spaces for all
            of the rules proposed in the current time stamp
        run_reg : Dictionary
            Fraction of regret potential in remaining design spaces for all of
            the rules proposed in the current time stamp
        ris : Dictionary
            Added potentials for regret and windfall accompanying a set of
            input rule(s) for the current timestamp
        """
        
        # Calculate complementary probabilities of feasibility
        prob_feas = evalCompProb(self.pf_frag, self.pf_std_frag)
        
        # Calculate windfall and regret for remaining design spaces
        wr, run_wind, run_reg = calcWindRegret\
            (self.irf, self.Df, self.pf_combos, prob_feas, self.pf_frag)
        
        # Quantify risk or potential of space reduction -- VARIABLE COMBOS!!
        ### Positive value means pot. regret or windfall ADDED
        ### Negative value means pot. regret or windfall REDUCED
        ris = quantRisk(self.Df, run_wind, run_reg, wr)
        
        # Return the probability-based fragility results
        return wr, run_wind, run_reg, ris
    
    
    def EFM(self):
        """
        Description
        -----------
        Performs the necessary commands to evaluate each design space's
        fragility with the entropic fragility model approach.

        Returns
        -------
        wr : Dictionary
            Windfall and regret data for each discretized point remaining in
            the non-reduced, reduced, and leftover design spaces of each 
            discipline for all of the rules proposed in the current time stamp
        run_wind : Dictionary
            Fraction of windfall potential in remaining design spaces for all
            of the rules proposed in the current time stamp
        run_reg : Dictionary
            Fraction of regret potential in remaining design spaces for all of
            the rules proposed in the current time stamp
        ris : Dictionary
            Added potentials for regret and windfall accompanying a set of
            input rule(s) for the current timestamp
        """
        
        # Organize the history of recorded pass-fail data in non-reduced space
        passfail_frag, passfail_std_frag = prepEntropy(self.pf, self.Df, 
                                                       self.pf_std)
        
        # Evaluate the TVE throughout remaining design spaces
        TVE = evalEntropy(passfail_frag, passfail_std_frag)
        
        # Calculate windfall and regret for remaining design spaces
        wr, run_wind, run_reg = calcWindRegret\
            (self.irf, self.Df, self.pf_combos, TVE, self.pf_frag)
        
        # Quantify risk or potential of space reduction -- VARIABLE COMBOS!!
        ### Positive value means pot. regret or windfall ADDED
        ### Negative value means pot. regret or windfall REDUCED
        ris = quantRisk(self.Df, run_wind, run_reg, wr)
        
        # Return the entropy-based fragility results
        return wr, run_wind, run_reg, ris
    
    
    def assessRisk(self, ris, iters, iters_max, exp_parameters, irules_new, 
                   fragility_shift, banned_rules, windreg, wr, 
                   running_windfall, run_wind, running_regret, run_reg, risk):
        """
        Description
        -----------
        Assesses whether or not any design spaces are too fragile for the
        current set of input rule(s) being proposed in combination with any
        rules accepted already and then organizes rules and accompanying data
        that went into making the decision.

        Parameters
        ----------
        ris : Dictionary
            Added potentials for regret and windfall accompanying a set of
            input rule(s) for the current timestamp
        iters : Integer
            Amount of time that has been spent exploring design spaces already
        iters_max : Integer
            Total time allotted to explore design spaces
        exp_parameters : Numpy array
            Various exponential function parameters dictating minimum space
            reduction pace for each discipline
        irules_new : List
            Sympy relationals dictating the newest set of space reduction rules
            being considered
        fragility_shift : Float
            Amount to either translate the exponential function (basicCheck) or
            set as a weighted coefficient (basicCheck2) for manipulating the
            fragility threshold via the design manager
        banned_rules : Set
            Sympy relationals detailing the input rule(s) no longer being
            considered for the current round of space reductions
        windreg : List of dictionaries
            Contains the complete history of gathered windfall and regret data
            for each discipline's design space
        wr : Dictionary
            Contains gathered windfall and regret data for each discipline's
            design space at the current time stamp
        running_windfall : List of dictionaries
            Contains the complete history of gathered windfall totals for each
            discipline's design space
        run_wind : Dictionary
            Contains gathered windfall totals for each discipline's design
            space at the current time stamp
        running_regret : List of dictionaries
            Contains the complete history of gathered regret totals for each
            discipline's design space
        run_reg : Dictionary
            Contains gathered regret totals for each discipline's design space
            at the current time stamp
        risk : List of dictionaries
            Contains the complete history of gathered risk data for each
            discipline

        Returns
        -------
        banned_rules : Set
            Updated sympy relationals detailing the input rule(s) no longer
            being considered for the current round of space reductions
        windreg : List of dictionaries
            Updated history of gathered windfall and regret data for each
            discipline's design space
        running_windfall : List of dictionaries
            Updated history of gathered windfall totals for each discipline's
            design space
        running_regret : List of dictionaries
            Updated history of gathered regret totals for each discipline's
            design space
        risk : List of dictionaries
            Updated history of gathered risk data for each discipline
        irules_new : List
            Updated list of sympy relationals dictating the newest set of space
            reduction rule(s) being considered
        irules_fragility : List
            Updated list of sympy and/or relationals detailing all of the new
            space reduction rules of the current space reduction cycle
        break_loop : Boolean
            Flag for whether or not the current cycle of fragility assessments
            should be broken
        """
        
        # Initialize a fragility check object
        fragile = checkFragility(ris, self.Df)
        
        # Execute fragility assessment
        net_wr = fragile.basicCheck2(iters, iters_max, exp_parameters, 
                                    fragility_shift)
        
        # Print results of fragility assessment
        print(f"Fragility assessment: {net_wr}")
        
        # Indicate that the fragility loop should not be broken
        break_loop = False

        # Check if ANY rule combos do not lead to fragile space
        if any(dic["fragile"] == False for dic in net_wr.values()):
            
            # Select rule combination to move forward with and add
            # to banned rule set
            final_combo, banned_rules = \
                fragile.newCombo(net_wr, banned_rules)
            
            # Append all findings to the list of dictionaries
            windreg.append(copy.deepcopy\
                ({final_combo: wr[final_combo]}))
            running_windfall.append(copy.deepcopy\
                ({final_combo: run_wind[final_combo]}))
            running_regret.append(copy.deepcopy\
                ({final_combo: run_reg[final_combo]}))
            risk.append(copy.deepcopy\
                ({final_combo: ris[final_combo]}))
            
            # Plot the potential for windfall and regret throughout each 
            # discipline's design space for the final combo
            # plotWindRegret(self.Df, self.irf, {final_combo: wr[final_combo]})
                
            # Append time to the dictionaries
            windreg[-1]['time'] = iters
            running_windfall[-1]['time'] = iters
            running_regret[-1]['time'] = iters
            risk[-1]['time'] = iters
            
            # Reassign NEW input rules as the items in the final combo
            irules_new = list(set(final_combo) ^ set(self.irf))
            
            # Add new input rules to the list of the current time stamp
            self.irf += irules_new
            
            # Indicate that the fragility loop should be broken
            break_loop = True
        
        # Return the documented fragility results
        return banned_rules, windreg, running_windfall, running_regret, risk, \
            irules_new, self.irf, break_loop
