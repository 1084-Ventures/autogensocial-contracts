# Direct Git Installation Guide

## Overview
Install the package directly from the GitHub repository without needing to publish to PyPI.

## Installation Methods

### Method 1: Install from Git URL

```bash
# Install latest from main branch
pip install git+https://github.com/1084-Ventures/autogensocial-contracts.git

# Install specific version/tag
pip install git+https://github.com/1084-Ventures/autogensocial-contracts.git@v0.1.0

# Install specific branch
pip install git+https://github.com/1084-Ventures/autogensocial-contracts.git@develop
```

### Method 2: requirements.txt format

```
# In your requirements.txt files

# Latest from main branch
git+https://github.com/1084-Ventures/autogensocial-contracts.git

# Specific version/tag
git+https://github.com/1084-Ventures/autogensocial-contracts.git@v0.1.0

# With egg name for clarity
git+https://github.com/1084-Ventures/autogensocial-contracts.git#egg=autogensocial-contracts
```

### Method 3: For Private Repositories (with authentication)

```bash
# Using personal access token
pip install git+https://<username>:<token>@github.com/1084-Ventures/autogensocial-contracts.git

# Using SSH (if SSH keys are configured)
pip install git+ssh://git@github.com/1084-Ventures/autogensocial-contracts.git
```

## Azure Functions Integration

### For Azure Functions (requirements.txt)
```
# Add this line to your Azure Functions requirements.txt
git+https://github.com/1084-Ventures/autogensocial-contracts.git@v0.1.0
```

### For Azure Container Instances or App Service
```dockerfile
# In Dockerfile
RUN pip install git+https://github.com/1084-Ventures/autogensocial-contracts.git@v0.1.0
```

## Version Management

### Create Git Tags for Releases
```bash
# Tag the current commit
git tag v0.1.0
git push origin v0.1.0

# Then install specific version
pip install git+https://github.com/1084-Ventures/autogensocial-contracts.git@v0.1.0
```

## Advantages of Git Installation
- ✅ No need to publish to PyPI
- ✅ Works with private repositories
- ✅ Version control through Git tags
- ✅ Direct access to latest changes
- ✅ Works in Azure Functions, Container Apps, etc.

## Authentication for Private Repos

### Option 1: Personal Access Token in Azure
Set environment variables in Azure Functions:
```
GITHUB_TOKEN=your_personal_access_token
```

Then use in requirements.txt:
```
git+https://${GITHUB_TOKEN}@github.com/1084-Ventures/autogensocial-contracts.git
```

### Option 2: Deploy Key (recommended for production)
1. Generate SSH key pair
2. Add public key as deploy key to repository
3. Use SSH URL in requirements.txt