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
import requests
import subprocess
from datetime import datetime

"""
SCRIPT FOR RUNNING TESTS
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

"""
SCRIPT FOR SENDING EMAIL
"""
# Sendinblue API details
api_key = os.environ['API_KEY']
sender_email = os.environ['SENDER_EMAIL']
recipient_email = os.environ['RECIPIENT_EMAIL']

# Email details
subject = 'Unit Testing Results'
current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Prepare the results content
text_content = f'Here are the results of all the unit test files as of {current_datetime}:\n\n'
for test_file, result in results.items():
    text_content += (
        f'Results for {test_file} '
        f'({result["status"]}): \n'
        f'{result["output"]}\n\n'
    )

# Prepare the data for the API request
data = {
    'sender': {
        'name': sender_email,
        'email': sender_email
    },
    'to': [
        {
            'email': recipient_email
        }
    ],
    'subject': subject,
    'textContent': text_content,
}

# Send the email using Sendinblue API
headers = {'api-key': api_key}
response = requests.post('https://api.sendinblue.com/v3/smtp/email', json=data, headers=headers)

# Check the response status
if response.status_code == 201:
    print('Email sent successfully!')
else:
    print('Failed to send email. Status code:', response.status_code)
    print('Response:', response.text)
