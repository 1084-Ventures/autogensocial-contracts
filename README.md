# AutoGenSocial Contracts

API contracts and data schemas for the AutoGenSocial platform - an AI-powered social media automation and content management system.

## 📋 Overview

This repository contains the contract specifications for the AutoGenSocial platform, including:

- **JSON Schemas**: Data models for brands, post plans, and posts
- **OpenAPI Specifications**: REST API definitions for all microservices
- **Prompts**: AI prompt templates for content generation
- **Documentation**: Integration guides and best practices

These contracts serve as the source of truth for all services in the AutoGenSocial ecosystem, ensuring consistent data structures and API interfaces across all components.

## 🏗️ Repository Structure

```
autogensocial-contracts/
├── schemas/              # JSON Schema definitions
│   ├── brand.json        # Brand configuration schema
│   ├── postPlan.json     # Content planning schema
│   └── post.json         # Social media post schema
├── openapi/              # OpenAPI 3.0 specifications
│   ├── content-api.yaml  # Content management API
│   ├── image-composer.yaml  # Image generation API
│   └── publisher.yaml    # Publishing and scheduling API
├── prompts/              # AI prompt templates
└── docs/                 # Additional documentation
```

## 🎯 Purpose

The AutoGenSocial platform automates social media content creation, planning, and publishing across multiple platforms. This contracts repository:

1. **Defines Data Models**: Standardizes how brands, content plans, and posts are structured
2. **Specifies APIs**: Documents all service endpoints, request/response formats, and authentication
3. **Enables Integration**: Provides clear contracts for clients and services to integrate with the platform
4. **Facilitates Development**: Enables parallel development of frontend and backend services
5. **Ensures Consistency**: Maintains data integrity across distributed microservices

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

### Deprecation Policy

Features marked for deprecation:
1. Will be announced at least 3 months in advance
2. Will include migration path documentation
3. Will be supported for at least 6 months after deprecation notice
4. Will be removed only in MAJOR version updates

## 🚀 How to Use These Contracts

### For API Consumers (Frontend/Client Applications)

1. **Review OpenAPI Specs**: Browse the OpenAPI specifications in the `openapi/` directory
2. **Generate Client SDKs**: Use tools like OpenAPI Generator to create client libraries
   ```bash
   # Example: Generate TypeScript client for Content API
   openapi-generator-cli generate \
     -i openapi/content-api.yaml \
     -g typescript-axios \
     -o ./generated/content-api-client
   ```
3. **Validate Requests**: Use the schemas to validate your API requests before sending
4. **Handle Responses**: Parse responses according to the defined schemas

### For API Providers (Backend Services)

1. **Implement Endpoints**: Build services that conform to the OpenAPI specifications
2. **Validate Data**: Use JSON schemas to validate incoming data
   ```javascript
   // Example: Validate brand data in Node.js
   const Ajv = require('ajv');
   const ajv = new Ajv();
   const schema = require('./schemas/brand.json');
   const validate = ajv.compile(schema);
   const valid = validate(brandData);
   ```
3. **Generate Server Stubs**: Use OpenAPI tools to generate server boilerplate
4. **Auto-generate Documentation**: Tools like Swagger UI can render interactive API docs

### For Testing

1. **Schema Validation**: Validate test data against JSON schemas
2. **Contract Testing**: Ensure API responses match OpenAPI specifications
3. **Mock Servers**: Generate mock servers from OpenAPI specs for testing
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