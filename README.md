# ServiceNow PDF Document Manager

A Python application to upload PDF policy documents to ServiceNow and view their content.

## Overview

This sample demonstrates how to:
- Upload PDF files to ServiceNow as knowledge article attachments
- List and view PDF documents from your ServiceNow instance
- Extract and display PDF text content

## ServiceNow Integration Approaches

ServiceNow offers several integration methods for different use cases:

1. **REST API** (used in this project) - [Official Docs](https://developer.servicenow.com/dev.do#!/reference/api/tokyo/rest/c_TableAPI)  
   Standard HTTP-based API for CRUD operations on ServiceNow records. Ideal for straightforward integrations and widely supported across programming languages. Requires minimal setup but proper authentication.

2. **MID Server** - [Official Docs](https://docs.servicenow.com/bundle/tokyo-servicenow-platform/page/product/mid-server/concept/mid-server-landing.html)  
   A Java application that runs on a server in your network to facilitate secure communications between ServiceNow and internal systems. Useful for accessing resources behind firewalls or when ServiceNow needs to interact with on-premises systems.

3. **Integration Hub** - [Official Docs](https://docs.servicenow.com/bundle/tokyo-servicenow-platform/page/administer/integrationhub/concept/integrationhub.html)  
   A no-code/low-code platform for building workflows that integrate with third-party systems. Features pre-built "spokes" (connectors) for common applications and services, allowing complex integrations without extensive coding.

4. **Microsoft Logic Apps with ServiceNow Connector** - [Microsoft Docs](https://learn.microsoft.com/en-us/connectors/service-now/)  
   Microsoft's cloud-based integration service that connects ServiceNow with other Azure services and third-party applications. Provides a visual designer for creating automated workflows with built-in connectors, triggers, and actions specific to ServiceNow.

### Our Implementation Approach

This project uses the **REST API approach** with:
- Basic authentication (username/password)
- Direct HTTP requests via the `requests` library for uploads
- Asynchronous HTTP requests via `aiohttp` for retrieving documents
- JSON for data exchange
- PDF content extraction using PyPDF2

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
Copy the `.env.example` file to `.env` and update with your ServiceNow credentials:
```bash
# Copy the example file
cp .env.example .env

# Edit the file with your editor
# For Windows: notepad .env
# For macOS/Linux: nano .env
```

Your `.env` file should contain:
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

- `servicenow_upload_pdfs_new.py` - Upload PDFs to ServiceNow (uses `requests` library)
- `servicenow_getallpolicydocuments.py` - List and view PDF documents (uses `aiohttp` for async operations)
- `extract_pdf_text.py` - Utility to extract text from PDF files
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
- Confirm your instance URL is correct and accessible 
- Check that your ServiceNow instance has the appropriate REST API endpoints enabled

## API Authentication

This project uses Basic Authentication for simplicity. In production environments, consider:

1. **OAuth 2.0** - More secure token-based authentication
2. **Service Account** - Using a dedicated integration user with limited permissions
3. **MID Server** - For secure integrations without exposing credentials
4. **Managed Identity** - If using Azure services like Logic Apps, leverage managed identities for secure, certificate-based authentication

## Purpose of this Repository

The primary purpose of this repository is to provide a starting point for developers who need to retrieve PDF documents and associated data from ServiceNow. It serves as a basic implementation that demonstrates the fundamental techniques for connecting to ServiceNow, uploading documents, and retrieving their content using Python.

## Future Enhancements

### Implement OAuth 2.0 with Service Principal Authentication

A key enhancement for production environments would be to replace basic authentication with OAuth 2.0 and Service Principal (Client ID/Secret) authentication:

1. **Create a ServiceNow OAuth Service Provider and Client Application**
   - Configure OAuth provider in ServiceNow
   - Create a client application to obtain client ID and secret

2. **User-Specific Policy Data Retrieval**
   - Implement user context-based filtering
   - Only retrieve policies relevant to the authenticated user
   - Leverage ServiceNow's role-based access control (RBAC)

3. **Benefits of this Enhancement**
   - Enhanced security (no storing username/passwords)
   - Support for token expiration and refresh
   - Fine-grained access control based on user identity
   - Compliance with modern security practices

This enhancement would make the integration more secure, maintainable, and suitable for enterprise environments where protecting sensitive policy documents is essential.

## Additional Resources

- [Microsoft ServiceNow Connector Documentation](https://learn.microsoft.com/en-us/connectors/service-now/)
- [ServiceNow REST API Documentation](https://developer.servicenow.com/dev.do#!/reference/api/sandiego/rest)
- [ServiceNow Table API Developer Guide](https://developer.servicenow.com/dev.do#!/reference/api/sandiego/rest/c_TableAPI)
