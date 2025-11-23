# GitHub Packages Publishing

## Setup

1. Create a Personal Access Token (PAT) with `write:packages` permission
2. Configure authentication

## Publishing to GitHub Packages

### Update pyproject.toml for GitHub Packages

Add repository URL to your pyproject.toml:

```toml
[project.urls]
Repository = "https://github.com/1084-Ventures/autogensocial-contracts"
"Package Repository" = "https://pypi.org/simple/"
```

### Build and Publish

```bash
# Build the package
python3 -m build

# Upload to GitHub Packages
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

For GitHub Packages specifically:
```bash
# Configure .pypirc for GitHub Packages
cat > ~/.pypirc << EOF
[distutils]
index-servers = github

[github]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <your-github-token>
EOF

# Upload to GitHub Packages
python3 -m twine upload --repository github dist/*
```

## Installing from GitHub Packages

### In requirements.txt
```
# For public packages
autogensocial-contracts==0.1.0

# For private GitHub packages, you may need:
--extra-index-url https://pypi.org/simple/
autogensocial-contracts==0.1.0
```

### With authentication (if private)
```bash
pip install autogensocial-contracts==0.1.0 --index-url https://pypi.org/simple/
```

## For Azure Functions deployment

In your `requirements.txt`:
```
autogensocial-contracts==0.1.0
```

Azure Functions will automatically install this during deployment if it's available on PyPI or configured package repositories.