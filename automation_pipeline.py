#!/usr/bin/env python3
"""
Style System Automation Pipeline

This script automates the complete workflow:
1. Runs class-classifier.py to extract and classify CSS classes
2. Automatically passes the output to style-creation.py to create AEM policies
3. Provides comprehensive logging and error handling
"""

import json
import subprocess
import sys
import os
from datetime import datetime

def log_message(message, level="INFO"):
    """Log messages with timestamp and level"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    log_message(f"Starting {description}...")
    
    try:
        # Run the script and capture output
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        log_message(f" {description} completed successfully")
        
        # Print script output if any
        if result.stdout:
            log_message(f"Output from {script_name}:")
            print(result.stdout)
            
        return True
        
    except subprocess.CalledProcessError as e:
        log_message(f"Error running {script_name}: {e}", "ERROR")
        if e.stdout:
            log_message(f"Script output: {e.stdout}", "ERROR")
        if e.stderr:
            log_message(f"Script error: {e.stderr}", "ERROR")
        return False
    
    except FileNotFoundError:
        log_message(f" Script {script_name} not found", "ERROR")
        return False
    
    except Exception as e:
        log_message(f" Unexpected error running {script_name}: {str(e)}", "ERROR")
        return False

def verify_files():
    """Verify that required files exist"""
    required_files = [
        "class-calssifier.py",
        "style-creation.py",
        "css-class-index-expanded.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        log_message(f" Missing required files: {', '.join(missing_files)}", "ERROR")
        return False
    
    log_message(" All required files found")
    return True

def verify_output_files():
    """Verify that output files were created"""
    output_files = [
        "classified_result.json",
        "policy-creation.json"
    ]
    
    for file in output_files:
        if os.path.exists(file):
            log_message(f" Output file created: {file}")
            # Show file size
            size = os.path.getsize(file)
            log_message(f"  File size: {size} bytes")
        else:
            log_message(f"✗ Expected output file not found: {file}", "WARNING")

def main():
    """Main automation pipeline"""
    log_message("=" * 60)
    log_message("STYLE SYSTEM AUTOMATION PIPELINE STARTED")
    log_message("=" * 60)
    
    # Step 1: Verify required files exist
    if not verify_files():
        log_message("Pipeline aborted due to missing files", "ERROR")
        sys.exit(1)
    
    # Step 2: Run class classifier
    log_message("STEP 1: Running CSS Class Classification")
    log_message("-" * 40)
    
    if not run_script("class-calssifier.py", "CSS Class Classification"):
        log_message("Pipeline aborted: Class classification failed", "ERROR")
        sys.exit(1)
    
    # Step 3: Verify intermediate output
    if not os.path.exists("policy-creation.json"):
        log_message("policy-creation.json not created by classifier", "ERROR")
        log_message("Pipeline aborted: Missing intermediate output", "ERROR")
        sys.exit(1)
    
    log_message("Intermediate files created successfully")
    
    # Step 4: Run style creation
    log_message("STEP 2: Creating AEM Style Policies")
    log_message("-" * 40)
    
    if not run_script("style-creation.py", "AEM Style Policy Creation"):
        log_message("Pipeline aborted: Style creation failed", "ERROR")
        sys.exit(1)
    
    # Step 5: Verify all outputs
    log_message("STEP 3: Verifying Output Files")
    log_message("-" * 40)
    verify_output_files()
    
    # Step 6: Summary
    log_message("\n" + "=" * 60)
    log_message("AUTOMATION PIPELINE COMPLETED SUCCESSFULLY!")
    log_message("=" * 60)
    
    log_message("Summary of generated files:")
    log_message("• classified_result.json - Raw classification results")
    log_message("• policy-creation.json - Formatted style groups for AEM")
    log_message("• AEM policies have been sent to the configured endpoint")
    
    log_message("\nNext steps:")
    log_message("1. Review the generated policy-creation.json file")
    log_message("2. Check AEM for the updated style policies")
    log_message("3. Test the styles in AEM authoring environment")

if __name__ == "__main__":
    main()
