import json
import requests
import os
import sys

# Load configuration
def load_config():
    """Load configuration from config.json"""
    try:
        with open("config.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("ERROR: config.json not found. Please ensure the configuration file exists.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in config.json: {str(e)}")
        sys.exit(1)

config = load_config()

# AEM Configuration
url = config["aem"]["url"]
headers = config["aem"]["headers"]

# Load style groups from policy-creation.json file
policy_file_path = config["files"]["policy_output"]

try:
    with open(policy_file_path, "r") as file:
        style_groups_data = json.load(file)
    
    # Convert the loaded data back to JSON string for the API payload
    style_groups = json.dumps(style_groups_data)
    print(style_groups)
    print(f"Successfully loaded style groups from {policy_file_path}")
    
except FileNotFoundError:
    print(f"Error: {policy_file_path} not found. Please ensure the file exists in the project directory.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format in {policy_file_path}")
    exit(1)
except Exception as e:
    print(f"Error loading {policy_file_path}: ")
    exit(1)
 
# Policy creation configuration
policy_creation_config = config["scripts"]["policy_creation"]
payload = {
    'scriptPath': policy_creation_config["scriptPath"],
    'component': policy_creation_config["component"],
    'siteName': policy_creation_config["siteName"],
    'styleGroups': style_groups
}

print(f"Sending style policies to AEM endpoint: {url}")
print(f"Component: {policy_creation_config['component']}")
print(f"Site: {policy_creation_config['siteName']}")

try:
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    resp = response.json()
    print("Style policies successfully sent to AEM")
    print("Response from AEM:")
    print(json.dumps(resp, indent=2))
    
except requests.exceptions.RequestException as e:
    print(f" Error sending request to AEM: {str(e)}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f" Error parsing AEM response: {str(e)}")
    print(f"Raw response: {response.text}")
    sys.exit(1)
except Exception as e:
    print(f" Unexpected error: {str(e)}")
    sys.exit(1)

print("Style creation process completed successfully!")
