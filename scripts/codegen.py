#!/usr/bin/env python3
"""
Command-line interface for autogensocial-contracts code generators.

Usage:
    python3 scripts/codegen.py crud brand python
    python3 scripts/codegen.py client content-api typescript
    python3 scripts/codegen.py validate --all
"""

import argparse
import sys
from pathlib import Path

from autogensocial_contracts.generators import (
    CRUDGenerator,
    ClientGenerator,
    SchemaValidator,
    OpenAPIValidator,
)


def generate_crud(args):
    """Generate CRUD operations."""
    generator = CRUDGenerator()
    
    if args.operation == "all":
        operations = generator.generate_all_operations(args.schema, args.format)
        
        if args.output:
            output_file = Path(args.output)
            with open(output_file, 'w') as f:
                for op_name, op_code in operations.items():
                    f.write(f"# {op_name.upper()} Operation\n")
                    f.write(op_code)
                    f.write("\n\n")
            print(f"✓ Generated CRUD operations to {output_file}")
        else:
            for op_name, op_code in operations.items():
                print(f"\n{'=' * 70}")
                print(f"{op_name.upper()} Operation")
                print('=' * 70)
                print(op_code)
    else:
        if args.operation == "create":
            code = generator.generate_create_operation(args.schema, args.format)
        elif args.operation == "read":
            code = generator.generate_read_operation(args.schema, args.format)
        elif args.operation == "update":
            code = generator.generate_update_operation(args.schema, args.format)
        elif args.operation == "delete":
            code = generator.generate_delete_operation(args.schema, args.format)
        else:
            print(f"Unknown operation: {args.operation}")
            return 1
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(code)
            print(f"✓ Generated {args.operation} operation to {args.output}")
        else:
            print(code)
    
    return 0


def generate_client(args):
    """Generate API client."""
    generator = ClientGenerator()
    
    code = generator.generate_client(
        args.spec,
        output_format=args.format,
        class_name=args.class_name
    )
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(code)
        print(f"✓ Generated API client to {args.output}")
    else:
        print(code)
    
    return 0


def validate_schemas(args):
    """Validate JSON schemas."""
    validator = SchemaValidator()
    
    if args.all:
        results = validator.validate_all_schemas()
        
        print("Schema Validation Results:")
        print("=" * 70)
        
        all_valid = True
        for schema_name, (is_valid, issues) in results.items():
            status = "✓ VALID" if is_valid else "✗ INVALID"
            print(f"\n{schema_name}: {status}")
            if issues:
                all_valid = False
                for issue in issues:
                    print(f"  - {issue}")
        
        return 0 if all_valid else 1
    else:
        is_valid, issues = validator.validate_schema(args.schema)
        
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{args.schema}: {status}")
        
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  - {issue}")
        
        return 0 if is_valid else 1


def validate_openapi(args):
    """Validate OpenAPI specifications."""
    validator = OpenAPIValidator()
    
    if args.all:
        results = validator.validate_all_specs()
        
        print("OpenAPI Validation Results:")
        print("=" * 70)
        
        all_valid = True
        for spec_name, (is_valid, issues) in results.items():
            status = "✓ VALID" if is_valid else "✗ INVALID"
            print(f"\n{spec_name}: {status}")
            if issues:
                all_valid = False
                for issue in issues:
                    print(f"  - {issue}")
        
        return 0 if all_valid else 1
    else:
        is_valid, issues = validator.validate_spec(args.spec)
        
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{args.spec}: {status}")
        
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  - {issue}")
        
        return 0 if is_valid else 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Code generation utilities for autogensocial-contracts"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # CRUD generator
    crud_parser = subparsers.add_parser("crud", help="Generate CRUD operations")
    crud_parser.add_argument("schema", help="Schema name (e.g., brand, post)")
    crud_parser.add_argument(
        "format",
        choices=["python", "typescript", "sql"],
        help="Output format"
    )
    crud_parser.add_argument(
        "--operation",
        choices=["all", "create", "read", "update", "delete"],
        default="all",
        help="Operation to generate (default: all)"
    )
    crud_parser.add_argument(
        "--output", "-o",
        help="Output file path (prints to stdout if not specified)"
    )
    
    # Client generator
    client_parser = subparsers.add_parser("client", help="Generate API client")
    client_parser.add_argument("spec", help="OpenAPI spec name (e.g., content-api)")
    client_parser.add_argument(
        "format",
        choices=["python", "typescript"],
        help="Output format"
    )
    client_parser.add_argument(
        "--class-name",
        help="Custom class name for the client"
    )
    client_parser.add_argument(
        "--output", "-o",
        help="Output file path (prints to stdout if not specified)"
    )
    
    # Schema validator
    schema_parser = subparsers.add_parser("validate-schema", help="Validate JSON schemas")
    schema_parser.add_argument(
        "schema",
        nargs="?",
        help="Schema name to validate (omit to validate all)"
    )
    schema_parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all schemas"
    )
    
    # OpenAPI validator
    openapi_parser = subparsers.add_parser("validate-openapi", help="Validate OpenAPI specs")
    openapi_parser.add_argument(
        "spec",
        nargs="?",
        help="OpenAPI spec name to validate (omit to validate all)"
    )
    openapi_parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all OpenAPI specs"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "crud":
            return generate_crud(args)
        elif args.command == "client":
            return generate_client(args)
        elif args.command == "validate-schema":
            return validate_schemas(args)
        elif args.command == "validate-openapi":
            return validate_openapi(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
