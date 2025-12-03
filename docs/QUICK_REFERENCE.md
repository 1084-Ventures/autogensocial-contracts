# Quick Reference Guide

## Installation

```bash
pip install autogensocial-contracts
```

## Import Models

```python
from autogensocial_contracts import Brand, Post, PostPlan, SocialAccount
```

## Generate CRUD Operations

### Python

```python
from autogensocial_contracts.generators import CRUDGenerator

generator = CRUDGenerator()
operations = generator.generate_all_operations("brand", output_format="python")
```

### TypeScript

```python
operations = generator.generate_all_operations("post", output_format="typescript")
```

### SQL

```python
ddl = generator.generate_create_operation("brand", output_format="sql")
```

## Generate API Clients

### Python Client

```python
from autogensocial_contracts.generators import ClientGenerator

generator = ClientGenerator()
client = generator.generate_client("content-api", output_format="python")
```

### TypeScript Client

```python
client = generator.generate_client("publisher", output_format="typescript")
```

## Validate Contracts

### Validate Schemas

```python
from autogensocial_contracts.generators import SchemaValidator

validator = SchemaValidator()
is_valid, issues = validator.validate_schema("brand")
```

### Validate OpenAPI Specs

```python
from autogensocial_contracts.generators import OpenAPIValidator

validator = OpenAPIValidator()
is_valid, issues = validator.validate_spec("content-api")
```

## CLI Usage

### Generate CRUD Operations

```bash
# Generate all operations
python3 scripts/codegen.py crud brand python --output brand_crud.py

# Generate specific operation
python3 scripts/codegen.py crud post typescript --operation create

# Generate SQL DDL
python3 scripts/codegen.py crud brand sql --operation create
```

### Generate API Client

```bash
# Python client
python3 scripts/codegen.py client content-api python --output client.py

# TypeScript client
python3 scripts/codegen.py client publisher typescript --output client.ts
```

### Validate Contracts

```bash
# Validate all schemas
python3 scripts/codegen.py validate-schema --all

# Validate specific schema
python3 scripts/codegen.py validate-schema brand

# Validate all OpenAPI specs
python3 scripts/codegen.py validate-openapi --all

# Validate specific spec
python3 scripts/codegen.py validate-openapi content-api
```

## Demo Scripts

Run comprehensive demonstrations:

```bash
# See all features in action
python3 scripts/demo_generators.py

# Real-world usage examples
python3 scripts/usage_examples.py
```

## Common Use Cases

### 1. Building a FastAPI Backend

```python
from fastapi import FastAPI
from autogensocial_contracts import Brand, Post

app = FastAPI()

@app.post("/brands")
async def create_brand(brand: Brand):
    # Brand is automatically validated
    return brand
```

### 2. Creating Test Data

```python
from autogensocial_contracts import Brand, SocialAccount

test_brand = Brand(
    id="test-1",
    name="Test Brand",
    description="A test brand"
)

test_account = SocialAccount(
    platform="twitter",
    handle="testbrand"
)
```

### 3. Loading Schemas for Validation

```python
from autogensocial_contracts.schemas import load_schema

brand_schema = load_schema("brand")
# Use with jsonschema, ajv, or other validators
```

### 4. Loading OpenAPI Specs

```python
from autogensocial_contracts.openapi import load_openapi_spec

content_api = load_openapi_spec("content-api")
# Use with FastAPI, Flask-RESTX, etc.
```

## File Structure

```
autogensocial_contracts/
├── models/           # Pydantic models
├── schemas/          # JSON schemas
├── openapi/          # OpenAPI specs
└── generators/       # Code generators
    ├── crud_generator.py
    ├── client_generator.py
    └── validator.py
```

## Need Help?

- See `README.md` for overview
- See `USAGE.md` for detailed usage guide
- Run `python3 scripts/demo_generators.py` for examples
- Run `python3 scripts/usage_examples.py` for real-world scenarios
