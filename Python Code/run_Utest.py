"""
Execute all of the unittest files beginning with 'Utest_'.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import os
import subprocess

"""
SCRIPT
"""
# Get the current working directory
directory = os.getcwd()

# Get a list of all the test files
test_files = [f for f in os.listdir(directory) if f.startswith('Utest_') and \
              f.endswith('.py')]

results = {}

# Execute each test file
for test_file in test_files:
    result = subprocess.run(['python', os.path.join(directory, test_file)], \
                            capture_output=True, text=True)
    # Check if the test passed or failed
    if 'Error' in result.stdout or 'Fail' in result.stdout or 'AssertionError'\
        in result.stderr:
        status = 'FAILED'
    else:
        status = 'OK'
    results[test_file] = {'status': status, 'output': result.stdout + '\n' + \
                          result.stderr}

# Save the results to a text file
# This will save the results in the same directory as this script
with open('test_results.txt', 'w') as f:
    for test_file, result in results.items():
        f.write(
            f'Results for {test_file} '
            f'({result["status"]}): \n'
            f'{result["output"]}\n\n'
        )
