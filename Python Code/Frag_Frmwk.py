"""
DESCRIPTION:
This is going to act as a function/class(?) for the assessment of design space
fragility.  For now, this function is only going to focus on comparing the
fragility of a design space for any proposed space reduction to the fragility
of the design space without that reduction to quantify reduction risk, so
project time and/or budget does not need to be incorporated here.  Reduction
risks do not yet need to be put into the scope of project time/budget remaining
to try to determine what exactly is a high-risk reduction.  Nor does the
function need to focus on guiding any further exploration or condensing of the
size of the proposed reduction to alleviate some of that risk.

This function will receive input on all of the proposed space reductions at a
particular point in time, the discipline's involved in a problem, the variables
that are associated with each discipline, the points that have been tested in
each discipline's design space, the resulting output points, the requirements
each variable need to meet, and (eventually?) the preferences for each design
variable as a whole (i.e. speed needs to be at least 40 knots, but we want the
vessel to go as fast as possible).

This function will produce entropy results, fragility results, and reduction
risk results.  The entropy results will likely be tabular because of the
possibility of those design spaces to have more than three-dimensions.  But
another function can be created with these entropy results that fixes certain
values of a discipline and returns two- or three-dimensional entropy figures.
There will be fragility values returned for each possible combination of space
reductions at a particular moment in time so they can be compared against each
other.  And there will be some sort of risk value returned based on carrying
out all of the proposed reductions at once versus not carrying any of them out.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
COMMANDS
"""

# -------------Automated Exploration & Space Reduction Proposition-------------
# SBD PROBLEM SCRIPT?

# ALL OF THE CODE FOR ANALYZING DATA AND PROPOSING REDUCTIONS BEFORE
# INCORPORATING ANY SORT OF A FRAGILITY FRAMEWORK --> This section will
# actually probably be better off in a "Script" file that is bound to call the
# fragility framework file.  But I can make arbitrary reduction proposals to
# just test out the framework before incorporating it into an actual SBD
# process.



# -----------------------------Fragility Framework-----------------------------
# FUNCTION CONTAINING CLASSES WITH OTHER FUNCTIONS?

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
    # space before factoring in any proposed reductions --> Test out different
    # function call(s) within an entropy-calculating class
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
    # before factoring in any of its proposed reductions --> Test out different
    # function call(s) within a perturbation class
    ### There is a spectrum of ideas on how perturbations could be introduced.
    ### The simplest strategy would be to create move boundaries and points a
    ### set distance away and/or introduce new requirements/points based on
    ### what would be reasonable for the specific design problem.  But this
    ### requires the designer to create an all-encompassing list of possible
    ### design changes that may occur when running the fragility framework.  A
    ### more reasonable strategy may be to suppose worst-case scenarios or
    ### scenarios of points possibly moving to other points or perceived bounds
    ### in their immediate vicinity and observing perhaps how the distances
    ### differ between the output and input spaces for those moves.  Another
    ### strategy may be to suppose that each point has a bubble around it of
    ### possible locations to where the points could change, and then to
    ### observe how that bubble fits in together with all of the bubbles of the
    ### other surrounding points.  This is likely the kind of direction the
    ### perturbations aspect of the fragility framework will take, but for now,
    ### it will likely be easiest and straightforward to test out random
    ### shifts in points and boundaries while we get a grasp on how the entropy
    ### metrics and characterization of the space will look.
    
    # Calculate the entropy of the particular discipline's remaining design
    # space before factoring in any of its proposed reductions but after
    # introducing the perturbations --> Test out different function call(s)
    # within the sample entropy-calculating class
    
    # Determine the difference in the particular discipline's entropy levels
    # before introducing the perturbations as compared to after introducing
    # the perturbations --> Test out different function call(s) within an
    # entropy-comparing class
    ### This may be an interesting step and may be dependent on exactly how
    ### entropy is used to classify a design space.  If a design space is given
    ### one value that describes the entire space, it could be as simple as one
    ### difference calculation.  However, if an entropy contour map is used, or
    ### if each test point is given an entropy value to hold onto but then all
    ### of those points move, this difference "calculation" will become more
    ### involved.
    
# Stop looping through each discipline of the problem

# Loop through each possible combination of space reductions in the list - 
# excluding the possible combination of no space reductions considered because
# there would be no fragility comparison to be made for that case
### This part of the code may involve some sort of decision to make it more
### concise.  Let's say 4 reductions are proposed at a particular moment in
### time.  While eventually, the decision may be made to just assess the
### resulting fragility that each of these proposed reductions have on a design
### space individually or as a whole, it makes sense to also test out all of
### the possible intermediate combinations of these reductions.  For example,
### maybe we find out that when looking at each reduction individually, those
### reductions do not have a huge affect on the fragility of any of the design
### spaces.  But when we look at them altogether, we see a huge impact on the
### fragility of each, or particular, design spaces.  This may make us want to
### break down the possible combinations further.  There may be a noticeable
### difference in the impact on a discipline's fragility when the 1st and 2nd
### proposed reductions are looked at together compared to when the 1st and 4th
### reductions are looked at together.  Until we have gathered some entropic
### data from this, the best option is likely to look at every possible
### combination of space reductions proposed at a particular moment in time.
### If 4 reductions are proposed at that particular moment, this would mean
### having 15 different combinations to look at (where combinations are
### different than permutations because order does not matter, and there is no
### set length of the number of reductions that have to be in a combination).
### Those combinations would look as such - 1, 2, 3, 4, 1&2, 1&3, 1&4, 2&3,
### 2&4, 3&4, 1&2&3, 1&2&4, 1&3&4, 2&3&4, 1&2&3&4.

    # Reflect on the discipline(s) affected by the particular combination of
    # space reductions and compile into a list
    
    # Loop through each discipline affected by the particular combination of
    # space reductions in the list
    ### All of the commands in this for loop should be done in the same manner
    ### as they were done above for consistency of results
    
        # Calculate the entropy of the particular discipline's remaining design
        # space after factoring in all proposed reductions of the particular
        # combination
        
        # Perturb the data of the particular discipline's remaining design
        # space after factoring in all proposed reductions of the particular
        # combination
        
        # Calculate the entropy of the particular discipline's remaining design
        # space after factoring in all proposed reductions of the particular
        # combination and after introducing the perturbations
        
        # Determine the difference in the particular discipline's entropy
        # levels before introducing the perturbations as compared to after
        # introducing the perturbations
    
    # Stop looking through each discipline affected by the particular
    # combination of space reductions in the list

# Stop looping through each possible combination of space reductions in the
# list


# ALL OF THE CODE FOR ANALYZING HOW THE DESIGN SPACES WITHOUT ANY OF THE
# PROPOSED SPACE REDUCTIONS HANDLE THE PERTURBATIONS COMPARED TO HOW THE DESIGN
# SPACES WITH EACH POSSIBLE COMBINATION OF THE PROPOSED SPACE REDUCTIONS HANDLE
# THE PERTURBATIONS TO DETERMINE HOW FRAGILE EACH OF THOSE POSSIBLE
# COMBINATIONS OF SPACE REDUCTIONS WOULD END UP MAKING EACH DESIGN SPACE.
# QUANTIFY THE RISK OF THE PROPOSED SPACE REDUCTIONS IN REFERENCE TO ITSELF.
# SAVE COMPARISONS OF RISK TO PROJECT TIME AND/OR BUDGET FOR NEXT SECTION.






# -------Next Steps for Design Manager to Make Based on Risk Assessment--------
# SEPARATE FUNCTION CALL?

# Compare the risk to the project time remaining to either suggest not making
# the proposed reduction at that point in time (step 1), condensing the
# reduction to reduce the risk (step 2), and guiding where further exploration
# should take place to gather more information before committing to the
# reduction (step 3)





# -------------Automated Exploration & Space Reduction Continuation------------
# BACK TO SBD PROBLEM SCRIPT?

# JUMP BACK INTO THE SCRIPT FILE THAT IS USED TO ANALYZE THE SET-BASED DESIGN
# PROBLEM OF CONCERN, EXPLORE THE SPACE, AND PROPOSE REDUCTIONS.  EVENTUALLY
# THIS SCRIPT WILL BE USED TO TEST A SBD PROCESS WITH THE FRAGILITY FRAMEWORK
# AGAINST ONE THAT DOES NOT USE IT, AND WE WILL OBSERVE HOW EFFECTIVE A SBD
# PROCESS IS WITH THE FRAMEWORK COMPARED TO WITHOUT THE FRAMEWORK.  AS THE
# EXPLORATION AND REDUCTION PROCESS CONTINUES, WE WILL HAVE EXPERIMENTS WITH
# THE FRAMEWORK WHEN IT PLANS FOR POSSIBLE DESIGN CHANGES BUT NO DESIGN CHANGES
# ACTUALLY OCCUR, AS WELL AS EXPERIMENTS THAT ACTUALLY INTRODUCE RANDOM DESIGN
# CHANGES AND RUN A BUNCH OF MONTE CARLO BASED EXPERIMENTS WITH THESE RANDOM
# DESIGN CHANGES THAT POP UP.


















# --How can all of this be similarly applied to an Iterative Design Process?---

# See design notebook dated 1/27/23 for current notes/ideas on this...



