#!/usr/bin/env python
"""
ServiceNow PDF Document Lister and Reader
A script to list the top 10 PDF attachments across all ServiceNow knowledge articles
and display their content
"""

import os
import asyncio
import base64
import io
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Import required libraries
import aiohttp
import requests
try:
    # Try to import PyPDF2 for PDF processing
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    print("PyPDF2 not installed. PDF content extraction disabled.")
    print("Run 'pip install PyPDF2' to enable PDF extraction.")
    PDF_SUPPORT = False

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

class PolicyDocumentRetriever:
    """Simple class to retrieve policy documents from ServiceNow"""
    
    def __init__(self):
        """Initialize the retriever"""
        self.session = None
        
    async def get_session(self) -> aiohttp.ClientSession:
        """Create or get existing aiohttp session with auth"""
        if not self.session:
            auth = aiohttp.BasicAuth(USERNAME, PASSWORD)
            timeout = aiohttp.ClientTimeout(total=30)
            
            self.session = aiohttp.ClientSession(
                auth=auth,
                timeout=timeout,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            )
            print("Created ServiceNow API session")
        return self.session
    
    async def get_all_knowledge_articles(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all knowledge articles from ServiceNow"""
        session = await self.get_session()
        
        # Get all articles regardless of workflow state to find PDF attachments
        params = {
            'sysparm_fields': 'sys_id,number,short_description,text,category,sys_updated_on,workflow_state',
            'sysparm_limit': limit
        }
        
        url = f"{INSTANCE_URL}/api/now/table/kb_knowledge"
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get('result', [])
                    print(f"Retrieved {len(articles)} knowledge articles")
                    return articles
                else:
                    print(f"Error retrieving articles: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"Exception retrieving articles: {e}")
            return []
    
    async def get_article_attachments(self, article_id: str) -> List[Dict[str, Any]]:
        """Get attachments for a knowledge article"""
        session = await self.get_session()
        
        params = {
            'sysparm_query': f'table_name=kb_knowledge^table_sys_id={article_id}',
            'sysparm_fields': 'sys_id,file_name,content_type,size_bytes'
        }
        
        url = f"{INSTANCE_URL}/api/now/table/sys_attachment"
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    attachments = data.get('result', [])
                    print(f"Found {len(attachments)} attachments for article {article_id}")
                    return attachments
                else:
                    print(f"Error retrieving attachments: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"Exception retrieving attachments: {e}")
            return []
    
    async def download_attachment(self, attachment_id: str) -> Optional[bytes]:
        """Download an attachment by ID"""
        session = await self.get_session()
        
        url = f"{INSTANCE_URL}/api/now/attachment/{attachment_id}/file"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    print(f"Downloaded attachment {attachment_id}: {len(content)} bytes")
                    return content
                else:
                    print(f"Error downloading attachment: HTTP {response.status}")
                    return None
        except Exception as e:
            print(f"Exception downloading attachment: {e}")
            return None
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            print("Closed ServiceNow API session")


def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text content from a PDF"""
    if not PDF_SUPPORT:
        return "[PDF text extraction not available - install PyPDF2]"
    
    try:
        # Create a file-like object from bytes
        pdf_file = io.BytesIO(pdf_content)
        
        # Create PDF reader
        reader = PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return f"[PDF extraction error: {e}]"


async def collect_pdf_attachments(retriever: PolicyDocumentRetriever) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """Collect all PDF attachments across all articles
    
    Returns:
        List of tuples with (article_info, attachment_info)
    """
    all_pdf_attachments = []
    
    # Step 1: Get all knowledge articles
    print("\n1. Retrieving all knowledge articles...")
    articles = await retriever.get_all_knowledge_articles()
    
    if not articles:
        print("No articles found. Check your ServiceNow instance or credentials.")
        return []
    
    # Step 2: Find PDF attachments across all articles
    print("\n2. Searching for PDF attachments across all articles...")
    for article in articles:
        article_id = article.get('sys_id', '')
        title = article.get('short_description', 'Untitled')
        
        # Get attachments for this article
        attachments = await retriever.get_article_attachments(article_id)
        
        # Filter for PDF attachments only
        for attachment in attachments:
            attachment_id = attachment.get('sys_id', '')
            filename = attachment.get('file_name', '')
            content_type = attachment.get('content_type', '')
            
            # Only consider PDF files
            if content_type == 'application/pdf' or filename.lower().endswith('.pdf'):
                # Create a simplified article info dict to keep with attachment
                article_info = {
                    'sys_id': article_id,
                    'title': title,
                    'url': f"{INSTANCE_URL}/kb_view.do?sysparm_article={article_id}"
                }
                
                all_pdf_attachments.append((article_info, attachment))
                
    return all_pdf_attachments


async def main():
    """Main function"""
    print(f"\n===== ServiceNow Top 10 PDF Documents =====")
    print(f"Instance: {INSTANCE_URL}")
    print(f"Username: {USERNAME}")
    print(f"Authentication: {'Configured' if PASSWORD else 'Missing'}")
    
    retriever = PolicyDocumentRetriever()
    
    try:
        # Step 1: Collect all PDF attachments across all articles
        print("\nAttempting to connect to ServiceNow...")
        pdf_attachments = await collect_pdf_attachments(retriever)
        
        if not pdf_attachments:
            print("\nNo PDF attachments found across any articles.")
            print("\nPossible reasons:")
            print("1. No policy documents with PDF attachments exist in your ServiceNow instance")
            print("2. Knowledge Management may not be properly configured")
            print("3. Authentication or permission issues")
            print("\nTroubleshooting tips:")
            print("- Verify your ServiceNow credentials are correct")
            print("- Check that Knowledge Management is enabled in your instance")
            print("- Upload some PDF attachments to knowledge articles")
            return
        
        # Step 2: Process only the top 10 PDF attachments
        top_10_pdfs = pdf_attachments[:10]
        print(f"\nFound {len(pdf_attachments)} total PDF attachments")
        print(f"Processing top {len(top_10_pdfs)} PDF documents...\n")
        
        # Step 3: Download and display content for the top 10 PDFs
        for i, (article, attachment) in enumerate(top_10_pdfs):
            attachment_id = attachment.get('sys_id', '')
            filename = attachment.get('file_name', '')
            content_type = attachment.get('content_type', '')
            size = attachment.get('size_bytes', '0')
            
            print(f"\n--- PDF #{i+1}/{len(top_10_pdfs)} ---")
            print(f"Filename: {filename}")
            print(f"Size: {size} bytes")
            print(f"From Article: {article['title']}")
            print(f"Article URL: {article['url']}")
            
            # Download PDF content
            print(f"Downloading PDF content...")
            pdf_content = await retriever.download_attachment(attachment_id)
            
            if pdf_content:
                # Extract text from PDF
                pdf_text = extract_text_from_pdf(pdf_content)
                
                # Print PDF content
                print(f"\nPDF CONTENT:")
                print("-" * 40)
                
                # Print first 500 characters with more preview
                if len(pdf_text) > 500:
                    print(f"{pdf_text[:500]}...\n[Document continues - {len(pdf_text)} characters total]")
                else:
                    print(pdf_text)
                
                print("-" * 40)
            else:
                print("Failed to download PDF content")
        
        print(f"\n===== Top {len(top_10_pdfs)} PDF Documents Processed =====")
    
    except Exception as e:
        print(f"Error in main: {e}")
    
    finally:
        # Close session
        await retriever.close()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
