#!/usr/bin/env python3
"""
Example script demonstrating code generation capabilities.

This script shows how to use the generators module to:
1. Generate CRUD operations from JSON schemas
2. Generate API clients from OpenAPI specifications
3. Validate schemas and OpenAPI specs
"""

from autogensocial_contracts.generators import (
    CRUDGenerator,
    ClientGenerator,
    SchemaValidator,
    OpenAPIValidator,
)


def demo_crud_generation():
    """Demonstrate CRUD operation generation."""
    print("=" * 70)
    print("CRUD OPERATION GENERATION")
    print("=" * 70)
    
    generator = CRUDGenerator()
    
    # Generate Python CRUD operations for Brand
    print("\n--- Python CRUD Operations for Brand ---\n")
    operations = generator.generate_all_operations("brand", output_format="python")
    
    print("CREATE Operation:")
    print(operations['create'][:200] + "...")
    
    print("\nREAD Operation:")
    print(operations['read'][:200] + "...")
    
    # Generate TypeScript CRUD operations for Post
    print("\n--- TypeScript CRUD Operations for Post ---\n")
    operations = generator.generate_all_operations("post", output_format="typescript")
    
    print("CREATE Operation:")
    print(operations['create'])
    
    # Generate SQL DDL for PostPlan
    print("\n--- SQL CREATE TABLE for PostPlan ---\n")
    sql_create = generator.generate_create_operation("postPlan", output_format="sql")
    print(sql_create)


def demo_client_generation():
    """Demonstrate API client generation."""
    print("\n" + "=" * 70)
    print("API CLIENT GENERATION")
    print("=" * 70)
    
    generator = ClientGenerator()
    
    # Generate Python client for Content API
    print("\n--- Python Client for Content API ---\n")
    python_client = generator.generate_client("content-api", output_format="python")
    print(python_client[:500] + "...")
    
    # Generate TypeScript client for Publisher API
    print("\n--- TypeScript Client for Publisher API ---\n")
    ts_client = generator.generate_client("publisher", output_format="typescript")
    print(ts_client[:500] + "...")


def demo_validation():
    """Demonstrate schema and OpenAPI validation."""
    print("\n" + "=" * 70)
    print("SCHEMA AND OPENAPI VALIDATION")
    print("=" * 70)
    
    # Validate JSON schemas
    print("\n--- Validating JSON Schemas ---\n")
    schema_validator = SchemaValidator()
    results = schema_validator.validate_all_schemas()
    
    for schema_name, (is_valid, issues) in results.items():
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{schema_name}: {status}")
        if issues:
            for issue in issues:
                print(f"  - {issue}")
    
    # Check schema consistency
    print("\n--- Checking Schema Consistency ---\n")
    is_consistent, differences = schema_validator.check_schema_consistency(
        "brand", "post", "id"
    )
    consistency_status = "✓ CONSISTENT" if is_consistent else "✗ INCONSISTENT"
    print(f"'id' field across Brand and Post schemas: {consistency_status}")
    if differences:
        for diff in differences:
            print(f"  - {diff}")
    
    # Validate OpenAPI specs
    print("\n--- Validating OpenAPI Specifications ---\n")
    openapi_validator = OpenAPIValidator()
    results = openapi_validator.validate_all_specs()
    
    for spec_name, (is_valid, issues) in results.items():
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{spec_name}: {status}")
        if issues:
            for issue in issues:
                print(f"  - {issue}")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  AutoGenSocial Contracts - Code Generation Demo".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    demo_crud_generation()
    demo_client_generation()
    demo_validation()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nFor more information, see:")
    print("  - README.md for package overview")
    print("  - USAGE.md for usage examples")
    print("  - autogensocial_contracts/generators/ for generator modules")
    print()


if __name__ == "__main__":
    main()
