#!/usr/bin/env python
"""
ServiceNow PDF Document Uploader
A script to upload PDF files from a Policy folder to ServiceNow as knowledge article attachments
"""

import os
import glob
import json
import base64
from dotenv import load_dotenv
import requests
import time
import sys

# Ensure output is not buffered (helps with seeing output in some terminal environments)
sys.stdout.reconfigure(line_buffering=True)  # For Python 3.7+

# Load environment variables from .env file
load_dotenv()

# ServiceNow connection settings
INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")

# Check for missing environment variables
missing_vars = []
if not INSTANCE_URL:
    missing_vars.append("SERVICENOW_INSTANCE_URL")
if not USERNAME:
    missing_vars.append("SERVICENOW_USERNAME")
if not PASSWORD:
    missing_vars.append("SERVICENOW_PASSWORD")

if missing_vars:
    print(f"Error: The following environment variables are required but missing: {', '.join(missing_vars)}")
    print("Please create a .env file with these variables or set them in your environment.")
    print("Example .env file content:")
    print("SERVICENOW_INSTANCE_URL=https://[your-instance].service-now.com")
    print("SERVICENOW_USERNAME=your-username")
    print("SERVICENOW_PASSWORD=your-password")
    exit(1)

# Ensure instance URL has no trailing slash
INSTANCE_URL = INSTANCE_URL.rstrip('/')

# Constants
POLICY_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Policy")
KB_BASE_CATEGORY = "0aa3ffa7db7c030064dd36cb7c96197f"  # General category, you may need to update this

class ServiceNowUploader:
    """Class to handle uploading PDFs to ServiceNow"""
    
    def __init__(self):
        """Initialize the uploader"""
        self.auth = requests.auth.HTTPBasicAuth(USERNAME, PASSWORD)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        print(f"Initialized ServiceNow uploader for: {INSTANCE_URL}", flush=True)
    
    def create_knowledge_article(self, title, content, category=KB_BASE_CATEGORY):
        """Create a new knowledge article
        
        Args:
            title: Article title
            content: Article content
            category: KB category sys_id
            
        Returns:
            sys_id of created article or None if failed
        """
        url = f"{INSTANCE_URL}/api/now/table/kb_knowledge"
        
        data = {
            "short_description": title,
            "text": content,
            "kb_category": category,
            "workflow_state": "draft"  # Start as draft
        }
        
        try:
            response = requests.post(
                url, 
                auth=self.auth,
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                article_id = result['result']['sys_id']
                print(f"Created knowledge article: {title} (ID: {article_id})", flush=True)
                return article_id
            else:
                print(f"Error creating article: HTTP {response.status_code}", flush=True)
                print(f"Response: {response.text}", flush=True)
                return None
                
        except Exception as e:
            print(f"Exception creating article: {e}", flush=True)
            return None
    
    def publish_article(self, article_id):
        """Publish a draft knowledge article
        
        Args:
            article_id: sys_id of the article to publish
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{INSTANCE_URL}/api/now/table/kb_knowledge/{article_id}"
        
        data = {
            "workflow_state": "published"
        }
        
        try:
            response = requests.patch(
                url, 
                auth=self.auth,
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                print(f"Published article ID: {article_id}", flush=True)
                return True
            else:
                print(f"Error publishing article: HTTP {response.status_code}", flush=True)
                print(f"Response: {response.text}", flush=True)
                return False
                
        except Exception as e:
            print(f"Exception publishing article: {e}", flush=True)
            return False
    
    def upload_attachment(self, table_name, table_sys_id, file_path):
        """Upload a file as an attachment
        
        Args:
            table_name: Name of the table (e.g., kb_knowledge)
            table_sys_id: sys_id of the record
            file_path: Path to the file to upload
            
        Returns:
            sys_id of created attachment or None if failed
        """
        file_name = os.path.basename(file_path)
        
        try:
            url = f"{INSTANCE_URL}/api/now/attachment/file"
            print(f"Uploading attachment to: {url}", flush=True)
            with open(file_path, 'rb') as file_data:
                files = {
                    'file': (file_name, file_data, 'application/pdf')
                }
                data = {
                    'table_name': table_name,
                    'table_sys_id': table_sys_id
                }
                print(f"Data being sent: table_name={table_name}, table_sys_id={table_sys_id}", flush=True)
                print("Sending attachment request...", flush=True)
                response = requests.post(
                    url,
                    auth=self.auth,
                    data=data,
                    files=files
                )
            if response.status_code == 201:
                result = response.json()
                attachment_id = result['result']['sys_id']
                print(f"Uploaded attachment: {file_name} (ID: {attachment_id})", flush=True)
                return attachment_id
            else:
                print(f"Error uploading attachment: HTTP {response.status_code}", flush=True)
                print(f"Response: {response.text}", flush=True)
                return None
        except Exception as e:
            print(f"Exception uploading attachment: {e}", flush=True)
            return None

def main():
    """Main function to upload PDFs to ServiceNow"""
    print("\n===== ServiceNow PDF Document Uploader =====", flush=True)
    print(f"Instance: {INSTANCE_URL}", flush=True)
    print(f"Username: {USERNAME}", flush=True)
    print(f"Policy Folder: {POLICY_FOLDER}", flush=True)
    
    # Find PDF files in the Policy folder
    pdf_files = glob.glob(os.path.join(POLICY_FOLDER, "*.pdf"))
    
    if not pdf_files:
        print(f"\nNo PDF files found in folder: {POLICY_FOLDER}", flush=True)
        return
    
    print(f"\nFound {len(pdf_files)} PDF files to upload.\n", flush=True)
    
    uploader = ServiceNowUploader()
    
    # Process each PDF file
    for pdf_file in pdf_files:
        file_name = os.path.basename(pdf_file)
        file_base_name = os.path.splitext(file_name)[0]
        
        # Create article title and content from file name
        article_title = f"Policy Document: {file_base_name.replace('_', ' ')}"
        article_content = f"""
        <h2>Policy Document</h2>
        <p>This is an automatically uploaded policy document.</p>
        <p>File: {file_name}</p>
        <p>Upload Date: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Please see the attached PDF for complete information.</p>
        """
        
        print(f"\n--- Processing: {file_name} ---", flush=True)
        
        # Step 1: Create knowledge article
        article_id = uploader.create_knowledge_article(article_title, article_content)
        if not article_id:
            print(f"Failed to create article for {file_name}, skipping...", flush=True)
            continue
        
        # Step 2: Upload PDF as attachment
        attachment_id = uploader.upload_attachment("kb_knowledge", article_id, pdf_file)
        if not attachment_id:
            print(f"Failed to upload attachment for {file_name}", flush=True)
            continue
        
        # Step 3: Publish the article
        success = uploader.publish_article(article_id)
        if success:
            article_url = f"{INSTANCE_URL}/kb_view.do?sysparm_article={article_id}"
            print(f"Successfully published article with attachment", flush=True)
            print(f"Article URL: {article_url}", flush=True)
    
    print("\n===== Upload Process Complete =====", flush=True)
    print("Check your ServiceNow instance for the uploaded documents", flush=True)

if __name__ == "__main__":
    main()
