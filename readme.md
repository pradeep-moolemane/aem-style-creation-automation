# Style System Automation

A Python-based automation tool for classifying and organizing CSS classes from Adobe Experience Manager (AEM) components into structured style groups for the AEM Style System.

## Overview

This project automates the process of extracting CSS classes from AEM components, classifying them into meaningful categories, and generating structured JSON files that can be used to create AEM Style System policies. It integrates with AEM's Groovy Console API and uses OpenAI's GPT models to intelligently format the classified results.

## Features

- **AEM Integration**: Connects to AEM instances via Groovy Console API to extract CSS classes from components
- **Intelligent Classification**: Categorizes CSS classes into predefined groups (Utility Classes, Button Styles, Layout & Containers, etc.)
- **AI-Powered Formatting**: Uses OpenAI GPT-4 to transform classified results into properly structured JSON with human-readable labels
- **Automated Workflow**: End-to-end automation from CSS extraction to policy-ready JSON generation

## Project Structure

```
style-system-automation/
├── automation_pipeline.py       # Master automation script (runs everything)
├── run_automation.bat          # Windows batch file for easy execution
├── config.json                 # Configuration file for all settings
├── class-classifier.py         # CSS extraction and classification script
├── style-creation.py           # AEM policy creation script
├── css-class-index-expanded.json # Master classification index
├── classified_result.json      # Raw classification results (generated)
├── policy-creation.json        # Final formatted output for AEM policies (generated)
├── prompt/
│   └── prompt.txt              # AI prompt template for CSS classification
├── source-css/                # Directory for source CSS files
└── README.md                  # This file
```

## Prerequisites

- Python 3.7+
- Required Python packages:
  - `requests`
  - `openai`
  - `json` (built-in)
- Access to AEM instance with Groovy Console
- OpenAI API key

## Installation

1. Clone or download this repository
2. Create virtual env -> python -m venv venv
3. Activate -> venv\Scripts\activate.bat  
4. Install required Python packages:
   ```bash
   pip install requests openai
   ```
5. Set up your OpenAI API key in the script or as an environment variable

## Configuration

All configuration is managed through the `config.json` file. Update the following sections as needed:

### AEM Connection Setup

Update the AEM connection details in `config.json`:

```json
{
  "aem": {
    "url": "https://your-aem-instance.com/bin/groovyconsole/post.json",
    "headers": {
      "Authorization": "Basic your-base64-encoded-credentials",
      "Cookie": "cq-authoring-mode=TOUCH"
    }
  }
}
```

### Script Configuration

Configure the Groovy scripts and component paths:

```json
{
  "scripts": {
    "css_extraction": {
      "scriptPath": "/var/groovyconsole/scripts/getCssClasses.groovy",
      "component": "your-component-path",
      "siteName": "your-site-name",
      "cssAttrName": "class"
    },
    "policy_creation": {
      "scriptPath": "/var/groovyconsole/scripts/updatePolicies.groovy",
      "component": "your-component-path",
      "siteName": "your-site-name"
    }
  }
}
```

### File Paths

File paths are configured in the config file:

```json
{
  "files": {
    "classification_index": "css-class-index-expanded.json",
    "classified_result": "classified_result.json",
    "policy_output": "policy-creation.json"
  }
}
```

### OpenAI Configuration

Set up OpenAI settings (use environment variable for API key):

```json
{
  "openai": {
    "model": "gpt-4-turbo",
    "temperature": 0.7,
    "api_key_placeholder": "your-openai-api-key-here"
  }
}
```

**Important**: Set your OpenAI API key as an environment variable:
```bash
set OPENAI_API_KEY=your-actual-api-key-here
```

## Usage

### Quick Start (Automated Pipeline)

1. **Set up your OpenAI API key** as an environment variable:
   ```bash
   set OPENAI_API_KEY=your-api-key-here
   ```

2. **Run the complete automation pipeline**:
   
   **Option A: Using the batch file (Windows)**
   ```bash
   run_automation.bat
   ```
   
   **Option B: Using Python directly**
   ```bash
   python automation_pipeline.py
   ```

3. **Review Results**: The automation will generate:
   - `classified_result.json`: Raw classification results
   - `policy-creation.json`: Formatted results ready for AEM Style System policies
   - AEM policies will be automatically sent to your configured endpoint

### Manual Step-by-Step Execution

If you prefer to run the scripts individually:

1. **Prepare Classification Index**: Ensure your `css-class-index-expanded.json` contains all the CSS class categories.

2. **Run Classification**:
   ```bash
   python class-calssifier.py
   ```

3. **Run Policy Creation**:
   ```bash
   python style-creation.py
   ```

## Classification Categories

The system organizes CSS classes into the following categories:

- **Animation & States**: Visibility, hover, active states
- **COPE Core Components**: ISI, Search, Images, Accordion, etc.
- **Wegovy Branding**: Brand-specific styles and components
- **Button Styles**: Primary, secondary, and specialized button variants
- **Card Variants**: Different card layouts and styles
- **Color Themes**: Color-based styling options
- **Component Sizes**: Size variations (small, medium, large)
- **Form Elements**: Input fields, checkboxes, form controls
- **Grid & Columns**: Layout and column structures
- **Layout & Containers**: Wrapper and container classes
- **Modal & Overlay Styles**: Modal dialogs and overlays
- **Navigation Styles**: Menu and navigation components
- **Text Alignment**: Text positioning utilities
- **Typography Styles**: Font and text styling
- **Utility Classes**: General-purpose utility classes

## Output Format

The final output (`policy-creation.json`) follows this structure:

```json
{
  "Category Name": [
    {
      "id": "unique-identifier",
      "label": "Human Readable Label",
      "className": "actual-css-class-name"
    }
  ]
}
```

## AI Prompt Engineering

The system uses a carefully crafted prompt (stored in `prompt/prompt.txt`) to guide the AI in:

1. Analyzing CSS files and extracting class names
2. Identifying semantic meaning from class names
3. Grouping classes into logical AEM Style System categories
4. Generating human-friendly labels for author use

## Workflow

1. **CSS Extraction**: Script calls AEM Groovy Console API to extract CSS classes from specified components
2. **Classification**: Classes are categorized using the predefined classification index
3. **AI Processing**: OpenAI GPT-4 formats the results into structured JSON with proper IDs and labels
4. **Output Generation**: Final JSON files are created for use in AEM Style System policies

## Error Handling

The script includes basic error handling for:
- API connection issues
- File I/O operations
- JSON parsing errors

## Contributing

When contributing to this project:

1. Ensure all file paths are properly configured
2. Test with your AEM instance before submitting changes
3. Update the classification index as needed for new CSS patterns
4. Maintain the existing JSON structure for compatibility

## Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- Use environment variables for sensitive configuration
- Ensure AEM credentials are properly secured
- Review the generated output before using in production

## License

This project is intended for internal use at Infogain for automating AEM Style System creation.

## Support

For issues or questions regarding this automation tool, please contact the development team or create an issue in the project repository.
