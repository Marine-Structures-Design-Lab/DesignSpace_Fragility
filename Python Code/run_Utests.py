"""
DESCRIPTION:
Runs all of the unit test files and emails the results to the email address
established in GitHub workflow.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import os
import unittest
import requests
from io import StringIO

"""
SCRIPT
"""
# Get API key, sender and receiver email from environment variables
api_key = os.getenv('API_KEY')
sender_email = os.getenv('SENDER_EMAIL')
to_email = os.getenv('RECEIVER_EMAIL')

# Get all test files
test_files = [file for file in os.listdir('.') if file.startswith('Utest_') \
              and file.endswith('.py')]

# Initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add tests to the suite
for test in test_files:
    # Extract the module name from the file name
    module_name = test[:-3]
    suite.addTests(loader.loadTestsFromName(module_name))

# Prepare an object to capture the test runner's output
stream = StringIO()
runner = unittest.TextTestRunner(stream=stream)

# Run the tests
result = runner.run(suite)

# Send the results via email
email_content = {
    'sender': {'name': 'Unit Tester', 'email': sender_email},
    'to': [{'email': to_email}],
    'subject': 'Unit Test Results',
    'textContent': stream.getvalue(),
}

headers = {
    'accept': 'application/json',
    'api-key': api_key,
    'content-type': 'application/json',
}

response = requests.post(
    'https://api.sendinblue.com/v3/smtp/email',
    headers=headers,
    json=email_content,
)

# Check the response status
if response.status_code == 201:
    print('Email sent successfully!')
else:
    print('Failed to send email. Status code:', response.status_code)
    print('Response:', response.text)
