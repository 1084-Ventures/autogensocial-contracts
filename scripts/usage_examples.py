"""
Real-world usage examples for autogensocial-contracts package.

This file demonstrates how to use the package in actual development scenarios.
"""

# ============================================================================
# Example 1: Using Pydantic Models for Data Validation
# ============================================================================

from autogensocial_contracts import Brand, Post, PostPlan, SocialAccount
from pydantic import ValidationError

# Create a brand with proper validation
try:
    brand = Brand(
        id="brand-001",
        name="TechCorp",
        description="A leading technology company",
        voice={
            "tone": ["professional", "innovative", "friendly"],
            "style": "Clear and concise, avoiding jargon"
        }
    )
    print(f"✓ Created brand: {brand.name}")
except ValidationError as e:
    print(f"✗ Validation error: {e}")

# Create a social account
social_account = SocialAccount(
    platform="twitter",
    handle="techcorp",
    displayName="TechCorp Official",
    isActive=True
)
print(f"✓ Created social account: @{social_account.handle}")

# Create a post
post = Post(
    id="post-001",
    brandId="brand-001",
    platform="twitter",
    content={
        "mainCopy": "Excited to announce our new product launch! 🚀",
        "hashtags": ["#TechCorp", "#Innovation", "#ProductLaunch"]
    },
    status="draft"
)
print(f"✓ Created post for {post.platform}")


# ============================================================================
# Example 2: Generating CRUD Operations for Backend Development
# ============================================================================

from autogensocial_contracts.generators import CRUDGenerator

# Initialize the generator
crud_gen = CRUDGenerator()

# Generate Python async CRUD operations for Brand
print("\n--- Generating Python CRUD Operations ---")
brand_operations = crud_gen.generate_all_operations("brand", output_format="python")

# Save to file for use in your backend
with open("/tmp/brand_crud.py", "w") as f:
    f.write("from typing import Optional, List\n")
    f.write("from sqlalchemy.ext.asyncio import AsyncSession\n")
    f.write("from sqlalchemy import select\n\n")
    f.write(brand_operations['create'])
    f.write("\n\n")
    f.write(brand_operations['read'])
    f.write("\n\n")
    f.write(brand_operations['update'])
    f.write("\n\n")
    f.write(brand_operations['delete'])

print("✓ Generated brand_crud.py with all CRUD operations")

# Generate SQL DDL for database setup
sql_ddl = crud_gen.generate_create_operation("brand", output_format="sql")
with open("/tmp/brand_schema.sql", "w") as f:
    f.write(sql_ddl)
print("✓ Generated brand_schema.sql")

# Generate TypeScript CRUD for frontend
ts_operations = crud_gen.generate_all_operations("post", output_format="typescript")
with open("/tmp/post_api.ts", "w") as f:
    f.write("// Auto-generated Post API functions\n\n")
    for op_name, op_code in ts_operations.items():
        f.write(f"// {op_name.upper()} Operation\n")
        f.write(op_code)
        f.write("\n\n")
print("✓ Generated post_api.ts with TypeScript functions")


# ============================================================================
# Example 3: Generating API Clients
# ============================================================================

from autogensocial_contracts.generators import ClientGenerator

client_gen = ClientGenerator()

# Generate Python API client for Content API
print("\n--- Generating API Clients ---")
python_client = client_gen.generate_client("content-api", output_format="python")

with open("/tmp/content_api_client.py", "w") as f:
    f.write(python_client)
print("✓ Generated content_api_client.py")

# Generate TypeScript API client for Publisher API
ts_client = client_gen.generate_client("publisher", output_format="typescript")

with open("/tmp/publisher_client.ts", "w") as f:
    f.write(ts_client)
print("✓ Generated publisher_client.ts")


# ============================================================================
# Example 4: Validating Schemas and OpenAPI Specs
# ============================================================================

from autogensocial_contracts.generators import SchemaValidator, OpenAPIValidator

print("\n--- Validating Schemas ---")

# Validate all JSON schemas
schema_validator = SchemaValidator()
schema_results = schema_validator.validate_all_schemas()

for schema_name, (is_valid, issues) in schema_results.items():
    status = "✓" if is_valid else "✗"
    print(f"{status} {schema_name}: {'VALID' if is_valid else 'INVALID'}")
    if issues:
        for issue in issues:
            print(f"    - {issue}")

# Check consistency of 'id' field across schemas
is_consistent, differences = schema_validator.check_schema_consistency(
    "brand", "post", "id"
)
print(f"\n{'✓' if is_consistent else '✗'} 'id' field consistency: {'CONSISTENT' if is_consistent else 'INCONSISTENT'}")

# Validate OpenAPI specifications
print("\n--- Validating OpenAPI Specs ---")
openapi_validator = OpenAPIValidator()
openapi_results = openapi_validator.validate_all_specs()

for spec_name, (is_valid, issues) in openapi_results.items():
    status = "✓" if is_valid else "✗"
    print(f"{status} {spec_name}: {'VALID' if is_valid else 'INVALID'}")
    if issues:
        for issue in issues[:3]:  # Show first 3 issues
            print(f"    - {issue}")


# ============================================================================
# Example 5: Using Generated Code in a FastAPI Application
# ============================================================================

print("\n--- Example: FastAPI Integration ---")

example_fastapi_code = '''
# app.py - FastAPI application using autogensocial-contracts

from fastapi import FastAPI, HTTPException
from autogensocial_contracts import Brand, Post, PostPlan
from autogensocial_contracts.openapi import load_openapi_spec
from typing import List

app = FastAPI(
    title="AutoGenSocial API",
    description="Social media content management API",
    version="1.0.0"
)

# In-memory storage (replace with database)
brands_db: dict[str, Brand] = {}

@app.post("/brands", response_model=Brand)
async def create_brand(brand: Brand):
    """Create a new brand."""
    if brand.id in brands_db:
        raise HTTPException(status_code=400, detail="Brand already exists")
    brands_db[brand.id] = brand
    return brand

@app.get("/brands/{brand_id}", response_model=Brand)
async def get_brand(brand_id: str):
    """Get a brand by ID."""
    if brand_id not in brands_db:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brands_db[brand_id]

@app.get("/brands", response_model=List[Brand])
async def list_brands():
    """List all brands."""
    return list(brands_db.values())

@app.put("/brands/{brand_id}", response_model=Brand)
async def update_brand(brand_id: str, brand: Brand):
    """Update a brand."""
    if brand_id not in brands_db:
        raise HTTPException(status_code=404, detail="Brand not found")
    brands_db[brand_id] = brand
    return brand

@app.delete("/brands/{brand_id}")
async def delete_brand(brand_id: str):
    """Delete a brand."""
    if brand_id not in brands_db:
        raise HTTPException(status_code=404, detail="Brand not found")
    del brands_db[brand_id]
    return {"status": "deleted"}

# Run with: uvicorn app:app --reload
'''

with open("/tmp/example_fastapi_app.py", "w") as f:
    f.write(example_fastapi_code)
print("✓ Generated example_fastapi_app.py")


# ============================================================================
# Example 6: Schema Introspection
# ============================================================================

print("\n--- Schema Introspection ---")

from autogensocial_contracts.schemas import load_schema, get_available_schemas

# Get all available schemas
available_schemas = get_available_schemas()
print(f"Available schemas: {', '.join(available_schemas)}")

# Examine Brand schema structure
brand_schema = load_schema("brand")
print(f"\nBrand schema properties:")
for prop_name, prop_def in brand_schema['properties'].items():
    prop_type = prop_def.get('type', 'unknown')
    description = prop_def.get('description', 'No description')
    required = '(required)' if prop_name in brand_schema.get('required', []) else ''
    print(f"  - {prop_name}: {prop_type} {required}")
    print(f"    {description}")


# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 70)
print("SUMMARY OF GENERATED FILES")
print("=" * 70)
print("""
✓ /tmp/brand_crud.py         - Python async CRUD operations for Brand
✓ /tmp/brand_schema.sql      - SQL DDL for Brand table
✓ /tmp/post_api.ts           - TypeScript API functions for Post
✓ /tmp/content_api_client.py - Python API client for Content API
✓ /tmp/publisher_client.ts   - TypeScript API client for Publisher API
✓ /tmp/example_fastapi_app.py - Example FastAPI application

These files can be used directly in your projects or as templates
for your own implementations.
""")
