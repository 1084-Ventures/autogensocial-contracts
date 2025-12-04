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

## Code Generation

The package now includes powerful code generation utilities to help you build CRUD operations and API clients from your schemas.

### Generating CRUD Operations

```python
from autogensocial_contracts.generators import CRUDGenerator

# Initialize the generator
generator = CRUDGenerator()

# Generate Python CRUD operations
operations = generator.generate_all_operations("brand", output_format="python")
print(operations['create'])  # CREATE operation
print(operations['read'])    # READ operation
print(operations['update'])  # UPDATE operation
print(operations['delete'])  # DELETE operation

# Generate TypeScript CRUD operations
ts_operations = generator.generate_all_operations("post", output_format="typescript")
print(ts_operations['create'])

# Generate SQL DDL
sql_ddl = generator.generate_create_operation("brand", output_format="sql")
print(sql_ddl)
```

### Generating API Clients

```python
from autogensocial_contracts.generators import ClientGenerator

# Initialize the generator
generator = ClientGenerator()

# Generate Python API client
python_client = generator.generate_client("content-api", output_format="python")
print(python_client)

# Generate TypeScript API client
ts_client = generator.generate_client("publisher", output_format="typescript")
print(ts_client)

# Generate with custom class name
custom_client = generator.generate_client(
    "content-api",
    output_format="python",
    class_name="MyCustomAPIClient"
)
```

### Validating Schemas and OpenAPI Specs

```python
from autogensocial_contracts.generators import SchemaValidator, OpenAPIValidator

# Validate JSON schemas
schema_validator = SchemaValidator()
is_valid, issues = schema_validator.validate_schema("brand")
if not is_valid:
    print("Schema issues:", issues)

# Validate all schemas
results = schema_validator.validate_all_schemas()
for schema_name, (is_valid, issues) in results.items():
    print(f"{schema_name}: {'✓' if is_valid else '✗'}")

# Check schema consistency
is_consistent, differences = schema_validator.check_schema_consistency(
    "brand", "post", "id"
)

# Validate OpenAPI specifications
openapi_validator = OpenAPIValidator()
is_valid, issues = openapi_validator.validate_spec("content-api")

# Check schema references
all_valid, invalid_refs = openapi_validator.check_schema_refs("content-api")
```

### Running the Demo

See all code generation features in action:

```bash
python3 scripts/demo_generators.py
```

## Package Structure

- `autogensocial_contracts.models` - Pydantic models generated from JSON schemas
- `autogensocial_contracts.schemas` - JSON schema utilities and files
- `autogensocial_contracts.openapi` - OpenAPI specification utilities and files
- `autogensocial_contracts.generators` - Code generation utilities
  - `CRUDGenerator` - Generate CRUD operations from schemas
  - `ClientGenerator` - Generate API clients from OpenAPI specs
  - `SchemaValidator` - Validate JSON schemas
  - `OpenAPIValidator` - Validate OpenAPI specifications