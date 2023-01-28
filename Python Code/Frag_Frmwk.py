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



