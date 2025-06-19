# ServiceNow PDF Document Manager

A Python application to upload PDF policy documents to ServiceNow and view their content.

## Overview

This sample demonstrates how to:
- Upload PDF files to ServiceNow as knowledge article attachments
- List and view PDF documents from your ServiceNow instance
- Extract and display PDF text content

## ServiceNow Integration Approaches

There are several ways to connect and integrate with ServiceNow:

1. **REST API** (used in this project)
   - Simple HTTP requests using basic authentication
   - Best for straightforward operations and quick implementations
   - Allows CRUD operations on ServiceNow tables and attachments

2. **SOAP Web Services**
   - XML-based protocol for more complex integrations
   - Good for enterprise integration scenarios
   - Requires WSDL understanding but provides strong typing

3. **ServiceNow API Client Libraries**
   - Official libraries for languages like JavaScript, Java, etc.
   - Streamlined API interactions with built-in authentication handling
   - Not available for all languages

4. **MID Server**
   - For secure integrations between ServiceNow and internal systems
   - Runs as an agent within your network
   - Handles data flow between ServiceNow and internal resources

5. **Integration Hub**
   - No-code/low-code integration platform from ServiceNow
   - Pre-built connectors for many third-party systems
   - Requires additional licensing

6. **Microsoft Logic Apps with ServiceNow Connector**
   - No-code/low-code integration via [Microsoft Logic Apps ServiceNow Connector](https://learn.microsoft.com/en-us/connectors/service-now/)
   - Visual workflow designer for building automated processes
   - Easy integration with other Microsoft and third-party services
   - Built-in connectors for common ServiceNow operations

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
