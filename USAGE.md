# Installation and Usage Guide

## Installation

### From Source (Development)

1. Clone the repository:
```bash
git clone https://github.com/1084-Ventures/autogensocial-contracts.git
cd autogensocial-contracts
```

2. Install in development mode:
```bash
python3 -m pip install --user --break-system-packages -e .
```

### From PyPI (When Published)
```bash
pip install autogensocial-contracts
```

## Usage

### Basic Model Usage

```python
from autogensocial_contracts import Brand, Post, PostPlan, SocialAccount

# Create a brand
brand = Brand(
    id="my-brand-123",
    name="My Company",
    description="A technology company focused on innovation"
)

# Create a social account
account = SocialAccount(
    id="social-123",
    platform="twitter",
    username="mycompany",
    brand_id="my-brand-123"
)

# Create a post plan
plan = PostPlan(
    id="plan-456",
    brand_id="my-brand-123",
    title="Product Launch Announcement",
    objective="Announce new product launch"
)
```

### Loading JSON Schemas

```python
from autogensocial_contracts.schemas import load_schema, get_available_schemas

# See all available schemas
schemas = get_available_schemas()
print("Available schemas:", schemas)

# Load a specific schema
brand_schema = load_schema("brand")
print("Brand schema:", brand_schema)
```

### Loading OpenAPI Specifications

```python
from autogensocial_contracts.openapi import load_openapi_spec, get_available_specs

# See all available API specs
specs = get_available_specs()
print("Available specs:", specs)

# Load a specific API specification
content_api = load_openapi_spec("content-api")
print("Content API title:", content_api.get("info", {}).get("title"))
```

## Development

### Regenerating Models

After updating JSON schemas, regenerate the Python models:

```bash
python3 scripts/generate_models.py
```

### Building the Package

```bash
python3 -m build
```

### Publishing to PyPI

```bash
python3 -m twine upload dist/*
```

## Package Structure

- `autogensocial_contracts.models` - Pydantic models generated from JSON schemas
- `autogensocial_contracts.schemas` - JSON schema utilities and files
- `autogensocial_contracts.openapi` - OpenAPI specification utilities and files