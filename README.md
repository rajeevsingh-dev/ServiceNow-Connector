# ServiceNow PDF Document Manager

A Python application to upload PDF policy documents to ServiceNow and view their content.

## Overview

This sample demonstrates how to:
- Upload PDF files to ServiceNow as knowledge article attachments
- List and view PDF documents from your ServiceNow instance
- Extract and display PDF text content

## Prerequisites

- Python 3.7+
- ServiceNow instance with Knowledge Management enabled
- ServiceNow admin credentials

## Quick Start

### 1. Setup ServiceNow Instance
If you don't have a ServiceNow instance, follow the setup guide:
[ServiceNow-Setup.md](ServiceNow-Setup.md)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file with your ServiceNow credentials:
```
SERVICENOW_INSTANCE_URL=https://your-instance.service-now.com
SERVICENOW_USERNAME=your-username
SERVICENOW_PASSWORD=your-password
```

### 4. Upload PDF Documents
Place your PDF files in the `Policy/` folder and run:
```bash
python servicenow_upload_pdfs_new.py
```

### 5. View PDF Documents
List and read PDF content from ServiceNow:
```bash
python servicenow_getallpolicydocuments.py
```

## Files Structure

- `servicenow_upload_pdfs_new.py` - Upload PDFs to ServiceNow
- `servicenow_getallpolicydocuments.py` - List and view PDF documents
- `Policy/` - Folder containing PDF files to upload
- `.env` - ServiceNow credentials (create this file)

## Features

- ✅ Upload PDF files as ServiceNow knowledge article attachments
- ✅ Create knowledge articles with metadata
- ✅ List all PDF documents in your ServiceNow instance
- ✅ Extract and display PDF text content
- ✅ Support for multiple PDF formats

## Troubleshooting

- Ensure your ServiceNow instance has Knowledge Management enabled
- Verify your credentials have admin permissions
- Check that PDF files are valid and readable
