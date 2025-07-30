import json
import requests
from openai import OpenAI
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

# Script configuration
css_extraction_config = config["scripts"]["css_extraction"]
payload = {
    'scriptPath': css_extraction_config["scriptPath"],
    'component': css_extraction_config["component"],
    'siteName': css_extraction_config["siteName"],
    'cssAttrName': css_extraction_config["cssAttrName"]
}

files = []
 
response = requests.request("POST", url, headers=headers, data=payload, files=files)
 
resp = response.json()
print(resp)
 
# Load classification index from config
classification_file = config["files"]["classification_index"]
 
try:
    with open(classification_file, "r") as file:
        data = json.load(file)
    print(f"Successfully loaded classification index from {classification_file}")
except FileNotFoundError:
    print(f"ERROR: Classification file {classification_file} not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON in {classification_file}: {str(e)}")
    sys.exit(1)
 
def classify_items_by_category(item_list, categorized_dict, unknown_key="Not Known"):
 
    result = {}
 
    for item in item_list:
        found = False
        for category, values in categorized_dict.items():
            if item in values:
                if category not in result:
                    result[category] = []
                result[category].append(item)
                found = True
                break
        if not found:
            if unknown_key not in result:
                result[unknown_key] = []
            result[unknown_key].append(item)
 
    return result
 
 
resp_output_list = json.loads(resp["output"])
classified_result = classify_items_by_category(resp_output_list, data)
print(classified_result)
 
final_dict = json.dumps(classified_result, indent=2)
print(final_dict)



# Save classified results to file
classified_result_file = config["files"]["classified_result"]
with open(classified_result_file, "w") as outfile:
    outfile.write(final_dict)
print(f"Classified results saved to {classified_result_file}")

# Set up OpenAI client
openai_config = config["openai"]
api_key = openai_config["api_key_placeholder"]
if not api_key:
    print("WARNING: OPENAI_API_KEY environment variable not set.")
    print("Please set your OpenAI API key as an environment variable or update the script.")
    print("For security reasons, avoid hardcoding API keys in the script.")
    # Fallback to placeholder - user should replace this
    api_key = openai_config.get("api_key_placeholder", "your-openai-api-key-here")
    if api_key == "your-openai-api-key-here":
        print("ERROR: Please set a valid OpenAI API key.")
        sys.exit(1)

client = OpenAI(api_key=api_key)

prompt = """
Convert the following JSON data into its proper format, you will get this json data {final_dict}

The json should be structured as follows:
format:

    {
        "Group Name": [
            {"id": "unique-id", "label": "Human Readable Label", "className": "class-name"}
            .
            .

        ],
        "Another Group Name": [
            {"id": "unique-id", "label": "Human Readable Label", "className": "class-name"}
            .
            .
        ]
    }

example:
{
    "Utility Classes": [
        {"id": "label-required-field", "label": "Required Control Label", "className": "control-label-required"},
        {"id": "pointer-cursor", "label": "Pointer Cursor", "className": "cursor-pointer"}
    ],
    "Not Known": [
        {"id": "recommended-title", "label": "Recommended For You", "className": "recommended_for_me-title"}
    ]
}

instructions:
    1. id and label must Different from className, means meaning is same but text is different, there is no hyphen in labels
    2. id should be unique sparate with hyphen.
    3. label must be human-readable, not identical to className — no hyphens or underscores, capitalized words.
    4. please! do not modify className it should be same as name you are getting it from json, do not include any underscore in className.
    5. please do not add any extra text or comments, dont miss any object from json

"""

def generate_response(prompt, model=None):
    """Generate response using OpenAI API with configuration"""
    if model is None:
        model = openai_config["model"]
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are working as the JSON formatter who is mapping class names with its class id and label. Use this JSON: " + final_dict}, 
            {"role": "user", "content": prompt},
        ],
        temperature=openai_config["temperature"],
    )
    return response.choices[0].message.content


print("Generating formatted policy JSON using OpenAI...")
answer = generate_response(prompt)

# Save to policy creation file
policy_output_file = config["files"]["policy_output"]
with open(policy_output_file, "w") as outfile:
    outfile.write(answer)

print(f"Policy creation JSON saved to {policy_output_file}")
print("Classification and formatting completed successfully!")
