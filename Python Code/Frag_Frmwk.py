# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 18:28:57 2023

@author: Joseph B. Van Houten (joeyvan@umich.edu)

This is going to act as a script file for the assessment of design space
fragility.  For now, this script file is only going to focus on comparing the
fragility of a design space for any proposed space reduction to the fragility
of the design space without that reduction to quantify reduction risk, so
project time and/or budget does not need to be incorporated yet.  Reduction
risks do not yet need to be put into the scope of project time/budget remaining
to try to determine what exactly is a high-risk reduction.  Nor does the
program need to focus on guiding any further exploration or condensing of
the size of the proposed reduction to alleviate some of that risk.


[Further Description]
"""

"""
ELEMENTS WITHIN SCRIPT FILE:

1) User needs to input characteristics for particular aspects of the problem
    - Symbols (?) for all of the design variables involved
    - Acceptable bounds for each variable (input or output)

2) User needs to gather information
    - The exact locations of each discipline's design space that have been
      sampled at a particular point in time
    - The areas of each design space that the design manager wants to reduce
      at a particular point in time
      -- Individual variable reductions (i.e. x1 < 5) will impact every design
         space that contains that variable
      -- Shared variable reductions (i.e. x1 + x2 < 5) will impact every design
         space that contains all of the variables involved

3) The program will need to establish information to be able to run simulations
    - The exact equations and/or marine design programs used to sample areas
      of each discipline's design space

"""

"""
ELEMENTS OUTSIDE OF SCRIPT FILE:
    
1) Calls to mathematical functions (or actual marine program functions)

"""

"""
CHRONOLOGICAL COMMANDS OF SCRIPT FILE:
    
1) Calculate entropy levels of each discipline's design space without any
   space reductions
    - What entropy types?
    - How should the entropy characterize the space?
        -- A single all-encompassing entropy value for each space
        -- Entropy contour map
        -- Entropy value assigned to each individual point based on what is
           around it (perceived boundaries and other points)

2) Introduce perturubations
    - Potentially move points to other test points?
    - Potentially more points to perceived feasible or dominated boundaries?
    - Should start simple to test out the entropy metrics by just randomly
      moving a boundary and/or randomly moving each point a specified distance
      away from its current location
      
3) Calculate new entropy level's of each discipline's design space without any
   space reductions
   
4) Calculate difference between new and original entropy levels of each
   discipline
   
5) Introduce the space reduction(s)
    - One at a time or all at once or some other sort of combination?
    
6) Repeat steps 1-4 with the reduced design space
    
7) Compare the entropy level differences before of step 4 before and after
   introducing the proposed space reduction(s)

"""

"""
WHERE TO FOCUS RESEARCH ATTENTION:

1) How to use entropy to calculate uncertainty associated with perceptions of a
   sampled design space


"""








"""
SCRIPT
"""

# -------------Automated Exploration & Space Reduction Proposition-------------

# ALL OF THE CODE FOR ANALYZING DATA AND PROPOSING REDUCTIONS BEFORE
# INCORPORATING ANY SORT OF A FRAGILITY FRAMEWORK --> This section and the last
# section will actually probably be better off in a "Script" file that is bound
# to call the fragility framework...a level up so to say



# -----------------------------Fragility Framework-----------------------------


# Gather all the proposed space reductions for that point in time into a list

# Loop through each proposed reduction in the list

    # Determine disciplines that are involved for the particular reduction
    ### If it is a proposed reduction for a single variable (i.e. eliminate all
    ### designs for x1 that are less than 5), then every discipline containing
    ### that variable are involved in the reduction.  If it is a proposed
    ### reduction involving multiple variables (i.e. eliminate all designs
    ### where the sum of x1 and x2 are less than 5), then every discipline
    ### containing ALL off the variables are involved in the reduction.
    
    # Record the disciplines involved in each particular reduction
    
# Stop looping through each proposed reduction in the list

# Loop through each discipline of the problem

    # Reflect on the specific reductions that affect the particular discipline
    
    # If the discipline is not involved in any proposed reduction, then
    # continue to the next discipline of the for loop
    
    # Calculate the entropy of the particular discipline's remaining design
    # space before factoring in any of its proposed reductions
    ### 1) Need to figure out exactly how the entropy is going to look.  I will
    ###    likely start out with some sort of Shannon Entropy, but I need to
    ###    determine exactly how that gets calculated for a design space having
    ###    many design variables.  I also need to figure out exactly how I want
    ###    the entropy to characterize the design space.  Do I want a single
    ###    entropy value encompassing the entire design space?  Do I want some
    ###    sort of an entropy contour map tracking levels of design space
    ###    entropy between the minimum and maximum amounts of the design space?
    ###    Do I want to attach a particular entropy value to each discrete
    ###    point in the design space based on the outcomes of the design space
    ###    sampled in that point's vicinity/the perceived feasible/dominated
    ###    boundaries?
    ### 2) This entropy calculation will probably involve some sort of function
    ###    call to an entropy calculator.  That function will require the
    ###    following information: COME BACK AND MOVE THESE BULLET POINTS!
    ###        - If the entropy is only concerned with the feasibility of the
    ###          specific discipline (as it is in this stage of the code), then
    ###          the locations of the discrete points tested, the pass/fail
    ###          success of each point tested, the current extreme bounds of
    ###          the design space (?)
    ###        - If the entropy is also concerned with the dominance of the
    ###          specific discipline, then the entropy calculating function
    ###          will also need pass/fail success of points and/or perceived
    ###          feasible regions of disciplines with interdependent spaces
    ###        - If the entropy is also concerned with the preferences of the
    ###          specific discipline, then the entropy calculating function
    ###          will also need information on the extent to which each tested
    ###          design point of the particular discipline is passing/failing
    
    # Perturb the data of the particular discipline's remaining design space
    # before factoring in any of its proposed reductions
    




# -------Comparison of Design Results with & without Fragility Framework-------





