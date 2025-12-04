# AutoGenSocial Contracts

API contracts and data schemas for the AutoGenSocial platform - an AI-powered social media automation and content management system.

## 📋 Overview

This repository contains the contract specifications for the AutoGenSocial platform, including:

- **JSON Schemas**: Data models for brands, post plans, and posts
- **OpenAPI Specifications**: REST API definitions for all microservices
- **Pydantic Models**: Auto-generated Python models from JSON schemas
- **Code Generators**: Utilities to generate CRUD operations and API clients
- **Validators**: Tools to ensure schema and API consistency
- **Documentation**: Integration guides and best practices

These contracts serve as the source of truth for all services in the AutoGenSocial ecosystem, ensuring consistent data structures and API interfaces across all components.

## ✨ Key Features

- 🔄 **Auto-generate CRUD Operations**: Generate database operations in Python, TypeScript, or SQL from JSON schemas
- 🌐 **Auto-generate API Clients**: Create type-safe API clients from OpenAPI specifications
- ✅ **Schema Validation**: Validate JSON schemas and OpenAPI specs for consistency
- 📦 **Exportable Package**: Install as a Python package for use in other projects
- 🎨 **Multiple Output Formats**: Support for Python, TypeScript, and SQL generation

## 🏗️ Repository Structure

```
autogensocial-contracts/
├── autogensocial_contracts/
│   ├── models/           # Pydantic models (auto-generated)
│   │   ├── brand.py      # Brand model
│   │   ├── post.py       # Post model
│   │   ├── postPlan.py   # PostPlan model
│   │   └── socialAccount.py  # SocialAccount model
│   ├── schemas/          # JSON Schema definitions
│   │   ├── brand.json    # Brand configuration schema
│   │   ├── postPlan.json # Content planning schema
│   │   ├── post.json     # Social media post schema
│   │   └── socialAccount.json  # Social account schema
│   ├── openapi/          # OpenAPI 3.0 specifications
│   │   ├── content-api.yaml    # Content management API
│   │   ├── image-composer.yaml # Image generation API
│   │   └── publisher.yaml      # Publishing API
│   └── generators/       # Code generation utilities
│       ├── crud_generator.py   # CRUD operation generator
│       ├── client_generator.py # API client generator
│       └── validator.py        # Schema/OpenAPI validator
├── scripts/              # Utility scripts
│   ├── generate_models.py      # Regenerate Pydantic models
│   └── demo_generators.py      # Demo code generation
├── tests/                # Test suite
└── docs/                 # Additional documentation
```

## 🎯 Purpose

The AutoGenSocial platform automates social media content creation, planning, and publishing across multiple platforms. This contracts repository:

1. **Defines Data Models**: Standardizes how brands, content plans, and posts are structured
2. **Specifies APIs**: Documents all service endpoints, request/response formats, and authentication
3. **Generates Boilerplate**: Auto-generates CRUD operations and API clients to speed up development
4. **Validates Contracts**: Ensures schemas and APIs are consistent and follow best practices
5. **Enables Integration**: Provides clear contracts for clients and services to integrate with the platform
6. **Facilitates Development**: Enables parallel development of frontend and backend services
7. **Ensures Consistency**: Maintains data integrity across distributed microservices

## 📊 Schemas

### Brand Schema (`schemas/brand.json`)

Defines brand configuration including:
- Brand identity and description
- Voice and tone guidelines
- Target audience demographics
- Visual identity (colors, logos, fonts)
- Connected social media accounts
- Content posting guidelines

### Post Plan Schema (`schemas/postPlan.json`)

Defines content planning and campaigns:
- Campaign objectives and goals
- Content themes and keywords
- Publishing schedule and frequency
- Platform targeting
- Content mix distribution
- Approval workflows

### Post Schema (`schemas/post.json`)

Defines individual social media posts:
- Post content and media
- Platform-specific metadata
- Scheduling information
- Engagement metrics
- Approval status
- AI generation metadata

## 🔌 APIs

### Content API (`openapi/content-api.yaml`)

Manages brands, post plans, and content generation:

- **Base URL**: `https://api.autogensocial.com/v1`
- **Authentication**: Bearer JWT tokens
- **Key Endpoints**:
  - `GET/POST /brands` - Brand management
  - `GET/POST /post-plans` - Content planning
  - `GET/POST /posts` - Post management
  - `POST /content/generate` - AI content generation

### Image Composer API (`openapi/image-composer.yaml`)

Handles AI-powered image generation:

- **Base URL**: `https://images.autogensocial.com/v1`
- **Authentication**: Bearer JWT tokens
- **Key Endpoints**:
  - `POST /generate` - Generate single image
  - `POST /generate/batch` - Batch image generation
  - `POST /images/{id}/variations` - Generate variations
  - `GET/POST /templates` - Template management
  - `POST /assets` - Upload custom assets

### Publisher API (`openapi/publisher.yaml`)

Manages publishing and scheduling across platforms:

- **Base URL**: `https://publisher.autogensocial.com/v1`
- **Authentication**: Bearer JWT tokens
- **Key Endpoints**:
  - `POST /publish` - Publish immediately
  - `POST /schedule` - Schedule future posts
  - `GET /schedules` - List scheduled posts
  - `POST /platforms/connect` - Connect social accounts
  - `GET /analytics/posts/{id}` - Retrieve post analytics

## 📝 Versioning Strategy

This repository follows **Semantic Versioning (SemVer)** principles:

### Version Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes to schemas or APIs (e.g., removing required fields, changing data types)
- **MINOR**: Backward-compatible additions (e.g., new optional fields, new endpoints)
- **PATCH**: Backward-compatible fixes (e.g., documentation updates, clarifications)

### API Versioning

APIs use **URL-based versioning**:
- Current version: `/v1`
- Future versions: `/v2`, `/v3`, etc.

### Schema Versioning

Schemas include version information in their `$id` field:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://autogensocial.com/schemas/brand.json",
  "title": "Brand"
}
```

### Breaking Changes

When introducing breaking changes:
1. Increment the MAJOR version
2. Create a new API version (e.g., `/v2`)
3. Maintain the previous version for at least 6 months
4. Provide migration guides in the `docs/` folder
5. Tag the release in Git with the version number

## 🚀 Code Generation

The package includes powerful code generation utilities to accelerate development:

### Generate CRUD Operations

```python
from autogensocial_contracts.generators import CRUDGenerator

generator = CRUDGenerator()

# Generate Python CRUD operations
operations = generator.generate_all_operations("brand", output_format="python")
print(operations['create'])  # async def create_brand(...)
print(operations['read'])    # async def get_brand(...) + list_brands(...)
print(operations['update'])  # async def update_brand(...)
print(operations['delete'])  # async def delete_brand(...)

# Generate TypeScript CRUD operations
ts_ops = generator.generate_all_operations("post", output_format="typescript")

# Generate SQL DDL
sql = generator.generate_create_operation("brand", output_format="sql")
```

### Generate API Clients

```python
from autogensocial_contracts.generators import ClientGenerator

generator = ClientGenerator()

# Generate Python API client with async/await
client_code = generator.generate_client("content-api", output_format="python")
# Output: class ContentAPIClient with async methods

# Generate TypeScript API client
ts_client = generator.generate_client("publisher", output_format="typescript")
# Output: export class PublisherAPIClient with async methods
```

### Validate Schemas and APIs

```python
from autogensocial_contracts.generators import SchemaValidator, OpenAPIValidator

# Validate all schemas
schema_validator = SchemaValidator()
results = schema_validator.validate_all_schemas()

# Validate all OpenAPI specs
openapi_validator = OpenAPIValidator()
results = openapi_validator.validate_all_specs()

# Check schema consistency
is_consistent, diffs = schema_validator.check_schema_consistency(
    "brand", "post", "id"
)
```

### Run the Demo

```bash
python3 scripts/demo_generators.py
```

This will demonstrate all code generation capabilities with actual output from your schemas and OpenAPI specs.

### Deprecation Policy

Features marked for deprecation:
1. Will be announced at least 3 months in advance
2. Will include migration path documentation
3. Will be supported for at least 6 months after deprecation notice
4. Will be removed only in MAJOR version updates

## 🚀 How to Use These Contracts

### For API Consumers (Frontend/Client Applications)

1. **Install the Package**: Get type-safe models and utilities
   ```bash
   pip install autogensocial-contracts
   ```

2. **Use Pydantic Models**: Import and use the pre-built models
   ```python
   from autogensocial_contracts import Brand, Post, PostPlan
   
   brand = Brand(id="123", name="My Brand")
   ```

3. **Generate Client SDK**: Use the built-in client generator
   ```python
   from autogensocial_contracts.generators import ClientGenerator
   
   generator = ClientGenerator()
   client_code = generator.generate_client("content-api", output_format="typescript")
   # Save to file and use in your frontend application
   ```

4. **Alternatively, use OpenAPI Generator**: Traditional approach
   ```bash
   # Example: Generate TypeScript client for Content API
   openapi-generator-cli generate \
     -i openapi/content-api.yaml \
     -g typescript-axios \
     -o ./generated/content-api-client
   ```

5. **Validate Requests**: Use Pydantic models to validate API requests
   ```python
   from autogensocial_contracts import Brand
   from pydantic import ValidationError
   
   try:
       brand = Brand(**request_data)
   except ValidationError as e:
       print("Invalid brand data:", e)
   ```

### For API Providers (Backend Services)

1. **Install the Package**: Get models and CRUD generators
   ```bash
   pip install autogensocial-contracts
   ```

2. **Use Pydantic Models**: Leverage auto-generated models for validation
   ```python
   from autogensocial_contracts import Brand, Post
   from pydantic import ValidationError
   
   # Automatically validates incoming data
   brand = Brand(**request_json)
   ```

3. **Generate CRUD Operations**: Use built-in generators to create database operations
   ```python
   from autogensocial_contracts.generators import CRUDGenerator
   
   generator = CRUDGenerator()
   
   # Generate Python async CRUD operations for SQLAlchemy
   crud_code = generator.generate_all_operations("brand", output_format="python")
   
   # Or generate SQL DDL
   sql_ddl = generator.generate_create_operation("brand", output_format="sql")
   ```

4. **Validate Incoming Data**: Use the schema validator
   ```python
   from autogensocial_contracts.generators import SchemaValidator
   
   validator = SchemaValidator()
   is_valid, issues = validator.validate_schema("brand")
   ```

5. **Auto-generate Documentation**: Use Swagger UI or ReDoc with OpenAPI specs
   ```python
   from autogensocial_contracts.openapi import load_openapi_spec
   
   spec = load_openapi_spec("content-api")
   # Pass to FastAPI, Flask-RESTX, etc.
   ```

### For Testing

1. **Use Pydantic Models**: Create test data easily
   ```python
   from autogensocial_contracts import Brand, Post
   
   test_brand = Brand(id="test-1", name="Test Brand")
   test_post = Post(
       id="post-1",
       brandId="test-1",
       platform="twitter",
       content={"mainCopy": "Test post"},
       status="draft"
   )
   ```

2. **Schema Validation**: Validate test data against JSON schemas
   ```python
   from autogensocial_contracts.generators import SchemaValidator
   
   validator = SchemaValidator()
   is_valid, issues = validator.validate_schema("brand")
   ```

3. **Contract Testing**: Ensure API responses match OpenAPI specifications
   ```python
   from autogensocial_contracts.generators import OpenAPIValidator
   
   validator = OpenAPIValidator()
   is_valid, issues = validator.validate_spec("content-api")
   ```

4. **Mock Servers**: Generate mock servers from OpenAPI specs for testing
   ```bash
   # Example: Run a mock server with Prism
   prism mock openapi/content-api.yaml
   ```

### For Documentation

1. **Interactive Docs**: Use Swagger UI or ReDoc to render interactive documentation
   ```bash
   # Serve with Swagger UI
   npx @redocly/openapi-cli preview-docs openapi/content-api.yaml
   ```
2. **API Reference**: Include OpenAPI specs in developer documentation
3. **Code Examples**: Generate code examples in multiple languages from specs

## 🛠️ Development Workflow

### Making Changes

1. **Clone the repository**
   ```bash
   git clone https://github.com/1084-Ventures/autogensocial-contracts.git
   cd autogensocial-contracts
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/add-new-field
   ```

3. **Make changes to schemas or OpenAPI specs**
   - Edit JSON schema files in `schemas/`
   - Update OpenAPI YAML files in `openapi/`

4. **Validate your changes**
   ```bash
   # Validate JSON schemas
   ajv validate -s schemas/brand.json -d examples/brand-example.json
   
   # Validate OpenAPI specs
   npx @redocly/openapi-cli lint openapi/content-api.yaml
   ```

5. **Update version numbers** (if needed)
   - Update API version in OpenAPI `info.version`
   - Tag release after merging

6. **Submit a pull request**

### Validation Tools

Recommended tools for validating contracts:

- **JSON Schema**: [AJV](https://ajv.js.org/) - Fast JSON validator
- **OpenAPI**: [@redocly/openapi-cli](https://redocly.com/docs/cli/) - OpenAPI linter and validator
- **API Testing**: [Prism](https://stoplight.io/open-source/prism) - Mock server and validator

## 🔐 Security

- All APIs use **Bearer token authentication** (JWT)
- Sensitive data should never be committed to this repository
- API keys and credentials must be managed through environment variables
- Follow OAuth 2.0 for platform integrations (Twitter, Facebook, etc.)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Follow existing schema and API design patterns
2. Maintain backward compatibility when possible
3. Document all changes in pull request descriptions
4. Validate all changes before submitting
5. Add examples for new fields or endpoints

## 📄 License

See [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or issues:
- **Email**: support@autogensocial.com
- **Issues**: [GitHub Issues](https://github.com/1084-Ventures/autogensocial-contracts/issues)

## 🗺️ Roadmap

Future additions to this repository:

- [ ] AsyncAPI specifications for event-driven communication
- [ ] GraphQL schema definitions
- [ ] Additional platform integrations (Pinterest, Snapchat)
- [ ] Webhook event schemas
- [ ] Example request/response payloads
- [ ] Integration test suites