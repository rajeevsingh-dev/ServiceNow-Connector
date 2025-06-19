# ServiceNow Setup Guide

This guide will help you create a ServiceNow account, set up an instance, and configure it for use with the PDF Document Manager.

## 1. Create ServiceNow Account

### Step 1: Sign Up for ServiceNow
1. Go to [ServiceNow Developer Portal](https://developer.servicenow.com/)
2. Click **"Sign Up"** or **"Get Started"**
3. Fill in your information:
   - Email address
   - Password
   - Company name
   - Country/Region
4. Accept the terms and conditions
5. Click **"Create Account"**

### Step 2: Verify Your Email
1. Check your email for verification link
2. Click the verification link to activate your account
3. Log in to the ServiceNow Developer Portal

## 2. Create a ServiceNow Instance

### Step 1: Request a Personal Developer Instance
1. Log in to [ServiceNow Developer Portal](https://developer.servicenow.com/)
2. Navigate to **"Manage"** → **"Instance"**
3. Click **"Request Instance"**
4. Select **"Personal Developer Instance"**
5. Choose your preferred release (latest recommended)
6. Click **"Request"**

### Step 2: Wait for Instance Creation
- Instance creation takes 5-15 minutes
- You'll receive an email when it's ready
- Your instance URL will be: `https://[your-instance-id].service-now.com`

### Step 3: Access Your Instance
1. Click the instance URL from your email
2. Log in with your ServiceNow credentials
3. You'll be redirected to your admin interface

## 3. Understanding the ServiceNow Admin Interface

### Main Navigation
- **All** - Search for any application or module
- **System Definition** - Configure system settings
- **System Applications** - Manage applications
- **User Administration** - Manage users and roles
- **Knowledge** - Manage knowledge base (what we need)

### Key Areas for PDF Management

#### Knowledge Management
1. **Navigate to**: `Knowledge` → `Knowledge Base`
2. **Purpose**: Create and manage knowledge articles with PDF attachments
3. **Key Features**:
   - Create knowledge articles
   - Upload PDF attachments
   - Manage categories
   - Control access permissions

#### User Administration
1. **Navigate to**: `User Administration` → `Users`
2. **Purpose**: Manage user accounts and permissions
3. **Key Features**:
   - Create API users
   - Assign roles and permissions
   - Manage user access

#### System Definition
1. **Navigate to**: `System Definition` → `Tables`
2. **Purpose**: View and understand data structure
3. **Key Tables**:
   - `kb_knowledge` - Knowledge articles
   - `sys_attachment` - File attachments
   - `kb_category` - Article categories

## 4. Configure Knowledge Management

### Step 1: Enable Knowledge Management
1. Navigate to **Knowledge** → **Knowledge Base**
2. If prompted, enable Knowledge Management
3. Follow the setup wizard if needed

### Step 2: Create Knowledge Categories
1. Navigate to **Knowledge** → **Categories**
2. Click **"New"** to create categories:
   - **Policy Documents**
   - **HR Policies**
   - **Company Guidelines**
3. Set appropriate permissions and workflow states

### Step 3: Configure User Permissions
1. Navigate to **User Administration** → **Users**
2. Find your user account
3. Ensure you have these roles:
   - `knowledge_admin`
   - `attachment_admin`
   - `web_service_admin`

## 5. Test Your Setup

### Step 1: Create a Test Knowledge Article
1. Navigate to **Knowledge** → **Knowledge Base**
2. Click **"New"** → **"Article"**
3. Fill in the details:
   - **Title**: "Test Policy Document"
   - **Category**: Select a category you created
   - **Article**: Add some test content
4. Click **"Submit"**

### Step 2: Upload a Test PDF
1. In your test article, click **"Attachments"**
2. Click **"Attach File"**
3. Upload a PDF file
4. Save the article

### Step 3: Verify API Access
Test that your instance is accessible via API:
```bash
curl -u "your-username:your-password" \
  "https://your-instance.service-now.com/api/now/table/kb_knowledge?sysparm_limit=5"
```

## 6. Get Your Instance Information

### Required Information for the App
You'll need these details for the `.env` file:

1. **Instance URL**: `https://[your-instance-id].service-now.com`
2. **Username**: Your ServiceNow username
3. **Password**: Your ServiceNow password

### Example .env File
```
SERVICENOW_INSTANCE_URL=https://dev123456.service-now.com
SERVICENOW_USERNAME=admin
SERVICENOW_PASSWORD=your-password
```

## 7. Common Issues and Solutions

### Issue: "Knowledge Management not available"
**Solution**: 
- Ensure you have the Knowledge Management plugin enabled
- Contact ServiceNow support if needed

### Issue: "Permission denied" errors
**Solution**:
- Verify your user has admin roles
- Check that Knowledge Management is properly configured
- Ensure your user has attachment permissions

### Issue: "Instance not accessible"
**Solution**:
- Verify your instance URL is correct
- Check that your instance is active (not suspended)
- Ensure your credentials are correct

## 8. Next Steps

Once your ServiceNow instance is set up:

1. **Configure your `.env` file** with your instance details
2. **Place PDF files** in the `Policy/` folder
3. **Run the upload script**: `python servicenow_upload_pdfs_new.py`
4. **View your documents**: `python servicenow_getallpolicydocuments.py`

## Support Resources

- [ServiceNow Developer Documentation](https://developer.servicenow.com/)
- [ServiceNow Community](https://community.servicenow.com/)
- [Knowledge Management Documentation](https://docs.servicenow.com/bundle/rome-knowledge-management/page/product/knowledge-management/concept/c_KnowledgeManagement.html)
