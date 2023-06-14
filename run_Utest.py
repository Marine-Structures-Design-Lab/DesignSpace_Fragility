"""
Execute all of the unittest files beginning with 'Utest_' and email the results
in a text file.

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
import base64

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

# Save the results to a text file
attachment_filename = 'test_results.txt'
with open(attachment_filename, 'w') as f:
    for test_file, result in results.items():
        f.write(
            f'Results for {test_file} '
            f'({result["status"]}): \n'
            f'{result["output"]}\n\n'
        )

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

# Read attachment file content
with open(attachment_filename, 'r') as file:
    attachment_content = file.read()

# Encode attachment content as Base64
attachment_content_base64 = base64.b64encode(attachment_content.encode()).decode()

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
    'textContent': 'See attached file for the results.',
    'attachment': [
        {
            'name': attachment_filename,
            'content': attachment_content_base64
        }
    ]
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
