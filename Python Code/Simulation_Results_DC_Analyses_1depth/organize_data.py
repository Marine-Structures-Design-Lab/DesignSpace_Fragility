"""
SUMMARY:
Extract average data from each test case that tracks the total space remaining,
feasible space remaining, and feasible-to-total space remaining in each
discipline over the elapsed project timeline.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import pickle

"""
TERTIARY FUNCTIONS
"""
def universalContribution(Discips, index, ind_discip):
    """
    Description
    -----------
    Determine the fraction of possible feasible solutions for a design point in
    interdependent discipline's when it is passing in the main discipline.

    Parameters
    ----------
    Discips : Dictionary
        All of the information pertaining to each discipline
    index : Integer
        Row of the discretized design point in the original design space
    ind_discip : Integer
        Main discipline of a design point

    Returns
    -------
    Float
        Fraction of potential feasible designs remaining in interdependent
        disciplines for a design point
    """
    
    # Initialize numerator and denominator values for fraction
    numerator = 0
    denominator = 0
    
    # Loop through each interdependent discipline
    for i, discip in enumerate(Discips):
        
        # Skip to next discipline if the same discipline as the design point
        if i == ind_discip: continue

        # Convert list to a numpy array
        discip_pass_array = np.array(discip['pass?'])

        # Determine indices in interdependent discipline that share an input
        # design variable with main discipline
        var_inter = [discip['ins'].index(var) \
                     for var in Discips[ind_discip]['ins'] \
                     if var in discip['ins']]
        
        # Loop through each interdependent variable index
        for j in var_inter:
            
            # Determine index of variable in main discipline matching 
            # interdependent variable discipline
            var_main = Discips[ind_discip]['ins'].index(discip['ins'][j])
            
            # Find interdependent design point indices with interdependent 
            # design point variable value matching main discipline design point 
            # variable value
            mask = np.isclose(Discips[i]['tested_ins'][:, j], 
                Discips[ind_discip]['tested_ins'][index, var_main])
            
            # Add to the numerator for number of times that interdependent
            # discipline's pass? value is True
            numerator += np.sum(discip_pass_array[mask])
            
            # Add to the denominator for each masked index
            denominator += np.sum(mask)
    
    # Return the fraction of universal feasibility
    return numerator / denominator if denominator > 0 else 0


"""
SECONDARY FUNCTIONS
"""
def sharedIndices(larger_array, smaller_array):
    """
    Description
    -----------
    Finds the indices in the original space remaining array that still exist in
    the reduced space remaining array.

    Parameters
    ----------
    larger_array : Numpy array
        Original space remaining array
    smaller_array : Numpy array
        Reduced space remaining array

    Returns
    -------
    indices : List of integers
        Indices in the larger numpy array with matching data points to the
        smaller numpy array
    """
    
    # Initialize an empty list to store indices
    indices = []
    
    # Iterate over each row in the smaller array
    for row in smaller_array:
        
        # Find the index in the larger array where the row matches
        index = np.where((larger_array == row).all(axis=1))[0][0]
        
        # Append that index to the list of indices
        indices.append(index)
    
    # Return the list of indices
    return indices


def countBooleans(index_list, Discips, ind_discip):
    """
    Description
    -----------
    Counts the remaining number of passing data points for the reduced design
    space.  For each passing point, also counts that point's 'universal'
    feasibility contribution based on fraction of passing points remaining in
    other interdependent disciplines for its particular value.

    Parameters
    ----------
    index_list : List of integers
        Indices of the original design space that still remain
    Discips : Dictionary
        All of the information pertaining to each discipline
    ind_discip : Integer
        Main discipline of a design point

    Returns
    -------
    true_count : Integer
        Remaining number of passing data points in the reduced design space
    true_count_all : Float
        Total sum of the fraction of potential feasible designs remaining
        within interdependent discipline's for each design point remaining
        in the main discipline's reduced design space
    """
    
    # Initialize counter for discipline's True values
    true_count = 0
    
    # Initialize counter for universal True values
    true_count_all = 0
    
    # Loop through the index list to find the corresponding boolean values
    for index in index_list:
        
        # Check if the data point at the particular index is passing
        if Discips[ind_discip]['pass?'][index]:
            
            # Add 1 to the discipline's True values counter
            true_count += 1
            
            # Add 0 or 1 to the universal True values counter
            true_count_all += universalContribution(Discips, index, ind_discip)
            
    # Return the sum of the true count and the universal true count
    return true_count, true_count_all


"""
MAIN FUNCTIONS
"""
def createTimeData(test_case_name):
    """
    Description
    -----------
    Determine all of the times that data was collected for a test case by
    consulting the console output files.

    Parameters
    ----------
    test_case_name : String
        Name of the particular test case that was run

    Returns
    -------
    set_of_times : Set
        All of the time iterations when data was gathered
    """
    
    # Change the time sets below based on the experiments run
    set_of_times = {0, 120, 206, 276, 324, 357, 386, 407, 426, 438, 449, 459,
                    468, 477, 485, 493, 501, 509, 517, 525, 533, 541, 549, 557,
                    565, 573, 581, 589, 597, 600}
    
    # Return the set of times
    return set_of_times


def fillSpaceRemaining(test_case, set_of_times, Discips):
    """
    Description
    -----------
    Goes through all of the runs for a test case and organizes the total and
    feasible space remaining such that there are data points for every time
    iteration.

    Parameters
    ----------
    test_case : Dictionary
        Contains elapsed space remaining data for each run of a test case
    set_of_times : Set
        All of the time iterations when data was gathered
    Discips : Dictionary
        Contains information relevant to each discipline of the design problem

    Returns
    -------
    space_rem : Dictionary
        Tracks the total space remaining for each run of a test case over the
        elapsed iterations
    feas_rem : Dictionary
        Tracks the feasible space remaining for each run of a test case over
        the elapsed iterations
    ufeas_rem : Dictionary
        Tracks the universal feasible space remaining for each run of a test
        case over the elapsed iterations
    """
    
    # Create a list of the times and sort them in ascending order
    list_of_times = sorted(list(set_of_times))
    
    # Initialize an empty dictionary for space remaining data
    space_rem = {}
    
    # Initialize an empty dictionary for percentage of feasible space data
    feas_rem = {}
    
    # Initialize an empty dictionary for universal feasible space data
    ufeas_rem = {}
    
    # Loop through each run of the test case
    for run_name, discips in test_case.items():
        
        # Initialize empty dictionaries for the run
        space_rem[run_name] = {}
        feas_rem[run_name] = {}
        ufeas_rem[run_name] = {}
        
        # Loop through each discipline of the run
        for ind_discip, list_discip in enumerate(discips):
            
            # Create a name for the discipline based on the index of the data
            discip_name = f"Discipline_{ind_discip + 1}"
            
            # Initialize empty dictionaries for the discipline
            space_rem[run_name][discip_name] = {}
            feas_rem[run_name][discip_name] = {}
            ufeas_rem[run_name][discip_name] = {}
            
            # Loop through each value in the list of times
            for time in list_of_times:
                
                # Assign time to a key for the dictionaries
                space_rem[run_name][discip_name][time] = []
                feas_rem[run_name][discip_name][time] = []
                ufeas_rem[run_name][discip_name][time] = []
            
            # Loop through each data point in the list
            for ind_data, dic_data in enumerate(list_discip):
                
                # Add size of the numpy array to the proper iteration list
                space_rem[run_name][discip_name][dic_data['iter']].append\
                    (len(dic_data['space_remaining']))
                
                # Determine shared indices between space remaining arrays
                matches = sharedIndices(Discips[ind_discip]['tested_ins'], 
                                        dic_data['space_remaining'])
                
                # Count and record True values for indices in both
                true_count, true_count_all = countBooleans(matches, Discips,
                                                           ind_discip)
                
                # Append first count to the feasible dictionary
                feas_rem[run_name][discip_name][dic_data['iter']].append\
                    (true_count)
                
                # Append second count to the universal feasible dictionary
                ufeas_rem[run_name][discip_name][dic_data['iter']].append\
                    (true_count_all)
            
            # Loop back through the list of times
            for ind_time, time in enumerate(list_of_times):
                
                # Check if space remaining list is empty
                if not space_rem[run_name][discip_name][time]:
                    
                    # Add minimum space remaining from one earlier time
                    space_rem[run_name][discip_name][time].append(min(\
                        space_rem[run_name][discip_name][list_of_times\
                        [ind_time-1]]))
                
                # Check if feasible space list is empty
                if not feas_rem[run_name][discip_name][time]:
                    
                    # Add minimum feasible count from one earlier time
                    feas_rem[run_name][discip_name][time].append(min(\
                        feas_rem[run_name][discip_name][list_of_times\
                        [ind_time-1]]))
                        
                # Check if universal feasible space list is empty
                if not ufeas_rem[run_name][discip_name][time]:
                    
                    # Add minimum feasible count from one earlier time
                    ufeas_rem[run_name][discip_name][time].append(min(\
                        ufeas_rem[run_name][discip_name][list_of_times\
                        [ind_time-1]]))
    
    # Return the dictionaries of filled in time information
    return space_rem, feas_rem, ufeas_rem


def findAverages(space_rem, feas_rem, ufeas_rem):
    """
    Description
    -----------
    Finds the average total space and feasible space remaining for each
    discipline, at each time stamp, of each test case, across all of the runs
    of that test case.

    Parameters
    ----------
    space_rem : Dictionary
        Tracks the total space remaining for each run of a test case over the
        elapsed iterations
    feas_rem : Dictionary
        Tracks the feasible space remaining for each run of a test case over
        the elapsed iterations
    ufeas_rem : Dictionary
        Tracks the universal feasible space remaining for each run of a test
        case over the elapsed iterations

    Returns
    -------
    average_rem : Dictionary
        Average total space remaining over elapsed project time
    average_feas : Dictionary
        Average feasible space remaining over elapsed project time
    average_ufeas : Dictionary
        Average universal feasible space remaining over elapsed project time
    """
    
    # Initialize an empty dictionary for average space remaining data
    average_rem = {}
    
    # Initialize an empty dictionary for average feasible count
    average_feas = {}
    
    # Initialize an empty dictionary for average universal feasbile count
    average_ufeas = {}
    
    # Loop through each discipline
    for discip_name, sr_dic in space_rem['Run_1'].items():
        
        # Initialize empty dictionaries for the discipline
        average_rem[discip_name] = {}
        average_feas[discip_name] = {}
        average_ufeas[discip_name] = {}

        # Loop through each time that space remaining data is accounted for
        for time, sr_set in sr_dic.items():
            
            # Initalize time keys for summation part of averaging
            average_rem[discip_name][time] = 0.0
            average_feas[discip_name][time] = 0.0
            average_ufeas[discip_name][time] = 0.0
    
    # Loop through each run of the test case
    for run_name, discips in space_rem.items():
        
        # Loop through each discipline of the run
        for discip_name, sr_dic in discips.items():
            
            # Loop through each time that space remaining data is accounted for
            for time, sr_lis in sr_dic.items():
                
                # Add midpoint of the space remaining to the proper summation
                average_rem[discip_name][time] += (min(sr_lis) + max(sr_lis))/2
            
            # Loop through each time that feasible space data is accounted for
            for time, fr_lis in feas_rem[run_name][discip_name].items():
                
                # Add midpoint of the space remaining to the proper summation
                average_feas[discip_name][time] += (min(fr_lis)+max(fr_lis))/2
            
            # Loop thru each time universal feasible space data accounted for
            for time, fr_lis in ufeas_rem[run_name][discip_name].items():
                
                # Add midpoint of the space remaining to the proper summation
                average_ufeas[discip_name][time] += (min(fr_lis)+max(fr_lis))/2
        
    # Loop through each discipline
    for discip_name, ar_dic in average_rem.items():
        
        # Loop through each time that space remaining data is accounted for
        for time in ar_dic.keys():
            
            # Divide summations by the number of test cases run
            average_rem[discip_name][time] = \
                average_rem[discip_name][time] / len(space_rem)
            average_feas[discip_name][time] = \
                average_feas[discip_name][time] / len(space_rem)
            average_ufeas[discip_name][time] = \
                average_ufeas[discip_name][time] / len(space_rem)
            
    # Return the data for the average space remaining at each time
    return average_rem, average_feas, average_ufeas


def findPercentages(average_rem, average_feas, average_ufeas):
    """
    Description
    -----------
    Converts the average total space remaining and average feasible space
    remaining into percentages, while also calculating the percentage of 
    average feasible space remaining to average total space remaining.

    Parameters
    ----------
    average_rem : Dictionary
        Average total space remaining over elapsed project time
    average_feas : Dictionary
        Average feasible space remaining over elapsed project time
    average_ufeas : Dictionary
        Average universal feasible space remaining over elapsed project time

    Returns
    -------
    percent_rem : Dictionary
        Average percentage of total space remaining
    percent_feas1 : Dictionary
        Average percentage of feasible space to total space remaining
    percent_feas2 : Dictionary
        Average percentage of feasible space remaining
    percent_ufeas1 : Dictionary
        Average universal percentage of feasible space to total space remaining
    percent_ufeas2 : Dictionary
        Average universal percentage of feasible space remaining
    """
    
    # Initialize an empty dictionary for percent of space remaining data
    percent_rem = {}
    
    # Initialize first empty dictionary for percent of feasible space
    percent_feas1 = {}
    
    # Initialize second empty dictionary for percent of feasible space
    percent_feas2 = {}
    
    # Initialize first empty dictionary for percent of universal feasible space
    percent_ufeas1 = {}
    
    # Initialize second empty dictionary for percent universal feasible space
    percent_ufeas2 = {}
    
    # Loop through each discipline
    for discip_name, ar_dic in average_rem.items():
        
        # Initialize empty dictionaries for the discipline
        percent_rem[discip_name] = {}
        percent_feas1[discip_name] = {}
        percent_feas2[discip_name] = {}
        percent_ufeas1[discip_name] = {}
        percent_ufeas2[discip_name] = {}
        
        # Loop through each time that average remaining is accounted for
        for time, ar in ar_dic.items():
            
            # Compute the percentage of the average space remaining
            percent_rem[discip_name][time] = ar / ar_dic[0] * 100
            
            # Compute percentage of average feasible space in remaining space
            percent_feas1[discip_name][time] = average_feas[discip_name][time]\
                / ar * 100
            
            # Compute percentage of average feasible space in original space
            percent_feas2[discip_name][time] = average_feas[discip_name][time]\
                / ar_dic[0] * 100
            
            # Compute percent of average universal feasible space in remaining
            percent_ufeas1[discip_name][time] = \
                average_ufeas[discip_name][time] / ar * 100
            
            # Compute percent of average universal feasible space in original
            percent_ufeas2[discip_name][time] = \
                average_ufeas[discip_name][time] / ar_dic[0] * 100
    
    # Return the percentage of the average space remaining
    return percent_rem, percent_feas1, percent_feas2, percent_ufeas1, \
        percent_ufeas2


"""
SCRIPT
"""
# Ensure this script is only run when it is being executed directly
if __name__ == "__main__":
    
    # Upload saved data
    with open('Discips.pkl', 'rb') as f:
        Discips = pickle.load(f)
    with open('Test_Case_1.pkl', 'rb') as f:
        Test_Case_1 = pickle.load(f)
    with open('Test_Case_2.pkl', 'rb') as f:
        Test_Case_2 = pickle.load(f)
    with open('Test_Case_3.pkl', 'rb') as f:
        Test_Case_3 = pickle.load(f)
    
    # Identify the test cases whose data will be assessed
    test_case_names = ['Test_Case_1', 'Test_Case_2', 'Test_Case_3']
    
    # Initialize a dictionaries for data pertinent to each discipline
    all_disciplines_data = {
        'Discipline_1': {},
        'Discipline_2': {},
        'Discipline_3': {}
        }
    # Initialize a dictionary for data pertinent to each discipline
    feas1_disciplines_data = {
        'Discipline_1': {},
        'Discipline_2': {},
        'Discipline_3': {}
        }
    # Initialize a dictionary for data pertinent to each discipline
    feas2_disciplines_data = {
        'Discipline_1': {},
        'Discipline_2': {},
        'Discipline_3': {}
        }
    # Initialize a dictionary for data pertinent to each discipline
    ufeas1_disciplines_data = {
        'Discipline_1': {},
        'Discipline_2': {},
        'Discipline_3': {}
        }
    # Initialize a dictionary for data pertinent to each discipline
    ufeas2_disciplines_data = {
        'Discipline_1': {},
        'Discipline_2': {},
        'Discipline_3': {}
        }
    
    # Loop through each test case / name
    for test_case_name in test_case_names:
        
        # Retrieve variable whose name matches the string
        test_case = globals()[test_case_name]
        
        # Determine all of the times when data was recorded
        set_of_times = createTimeData(test_case_name)
        
        # Determine space remaining at each of those times for each test run
        space_rem, feas_rem, ufeas_rem = fillSpaceRemaining(test_case, 
            set_of_times, Discips)
        
        # Determine average space remaining at each time over all of the runs
        average_rem, average_feas, average_ufeas = findAverages(space_rem, 
            feas_rem, ufeas_rem)
        
        # Convert averages into percentages
        percent_rem, percent_feas1, percent_feas2, percent_ufeas1, \
            percent_ufeas2 = findPercentages(average_rem, average_feas, 
            average_ufeas)
        
        # Loop through disciplines
        for discip_name in all_disciplines_data.keys():
            
            # Add results to new key within dictionaries
            all_disciplines_data[discip_name][test_case_name] = \
                percent_rem[discip_name]
            feas1_disciplines_data[discip_name][test_case_name] = \
                percent_feas1[discip_name]
            feas2_disciplines_data[discip_name][test_case_name] = \
                percent_feas2[discip_name]
            ufeas1_disciplines_data[discip_name][test_case_name] = \
                percent_ufeas1[discip_name]
            ufeas2_disciplines_data[discip_name][test_case_name] = \
                percent_ufeas2[discip_name]
    
    # Save the new data
    with open('all_disciplines.pkl', 'wb') as f:
        pickle.dump(all_disciplines_data, f)
    with open('feas1_disciplines.pkl', 'wb') as f:
        pickle.dump(feas1_disciplines_data, f)
    with open('feas2_disciplines.pkl', 'wb') as f:
        pickle.dump(feas2_disciplines_data, f)
    with open('ufeas1_disciplines.pkl', 'wb') as f:
        pickle.dump(ufeas1_disciplines_data, f)
    with open('ufeas2_disciplines.pkl', 'wb') as f:
        pickle.dump(ufeas2_disciplines_data, f)
