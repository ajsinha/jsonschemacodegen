# JsonSchemaCodeGen Examples Guide

## Copyright and Legal Notice

**Copyright © 2025-2030, All Rights Reserved**  
**Ashutosh Sinha**  
**Email: ajsinha@gmail.com**

This document and the associated software architecture are proprietary and confidential. Unauthorized copying, distribution, modification, or use of this document or the software system it describes is strictly prohibited without explicit written permission from the copyright holder.

**Patent Pending:** Certain architectural patterns and implementations described in this document may be subject to patent applications.

---

## Table of Contents

1. [Overview](#overview)
2. [Schema Categories](#schema-categories)
3. [Basic Schemas (01-04)](#basic-schemas-01-04)
4. [Content & Communication (05-10)](#content--communication-05-10)
5. [Industry-Specific (11-15)](#industry-specific-11-15)
6. [Technical & DevOps (16-22)](#technical--devops-16-22)
7. [Common Definitions](#common-definitions)
8. [Using the Examples](#using-the-examples)
9. [Best Practices Demonstrated](#best-practices-demonstrated)

---

## Overview

JsonSchemaCodeGen includes **22+ comprehensive example schemas** covering a wide range of real-world use cases. These schemas demonstrate:

- Various JSON Schema features (types, formats, constraints)
- Complex nested structures
- Reference patterns (`$ref`)
- Composition (allOf, anyOf, oneOf)
- Real-world data modeling patterns

### Location

All example schemas are located in:
```
examples/schemas/
├── 01_user.json
├── 02_product.json
├── ...
├── 22_openapi_spec.json
└── definitions/
    └── common.json
```

---

## Schema Categories

| Category | Schemas | Description |
|----------|---------|-------------|
| **Basic** | 01-04 | Common application entities |
| **Content** | 05-10 | Content management & communication |
| **Industry** | 11-15 | Healthcare, IoT, Finance |
| **Technical** | 16-22 | DevOps, ML, Gaming, APIs |

---

## Basic Schemas (01-04)

### 01_user.json - User Account

**Purpose**: User account management with preferences and roles.

**Key Features Demonstrated**:
- Enum types for roles and status
- Nested preferences object
- Format validators (email, uuid)
- Pattern validation for usernames

**Schema Structure**:
```json
{
  "title": "User",
  "type": "object",
  "definitions": {
    "UserRole": { "enum": ["admin", "moderator", "user", "guest"] },
    "UserStatus": { "enum": ["active", "inactive", "suspended", "pending"] },
    "UserPreferences": { ... }
  },
  "properties": {
    "id": { "format": "uuid" },
    "email": { "format": "email" },
    "username": { "minLength": 3, "maxLength": 30 },
    "role": { "$ref": "#/definitions/UserRole" },
    "preferences": { "$ref": "#/definitions/UserPreferences" }
  }
}
```

**Usage Example**:
```python
from jsonschemacodegen import SchemaProcessor
from jsonschemacodegen.utils import load_schema

schema = load_schema("examples/schemas/01_user.json")
processor = SchemaProcessor(schema, root_class_name="User")

# Generate code
print(processor.generate_code())

# Generate sample user
sample = processor.generate_samples(count=1)[0]
# Output: {'id': 'a1b2c3d4-...', 'email': 'john@example.com', 'username': 'john_doe', ...}
```

---

### 02_product.json - E-commerce Product

**Purpose**: Product catalog with variants, pricing, and categories.

**Key Features Demonstrated**:
- Recursive references (Category → parent Category)
- Complex nested structures (variants with inventory)
- Array of objects
- Price as structured object (amount + currency)

**Key Definitions**:
- `Price`: Amount in cents + currency code
- `Variant`: SKU, price, inventory, attributes
- `Category`: Hierarchical product categories

**Relationships**:
```
Product
├── categories[] → Category (with parent reference)
├── variants[] → Variant
│   └── price → Price
└── images[]
```

---

### 03_order.json - E-commerce Order

**Purpose**: Complete order with line items, addresses, payments, and shipments.

**Key Features Demonstrated**:
- Multiple address types (shipping, billing)
- Line items with product references
- Payment and shipment tracking
- Discount structures

**Key Definitions**:
- `Address`: Shipping/billing address
- `LineItem`: Product, quantity, price, discount
- `Discount`: Percentage or fixed amount
- `Payment`: Method, status, transaction details
- `Shipment`: Carrier, tracking, delivery status

**Complexity**: This schema demonstrates a complete e-commerce transaction flow.

---

### 04_api_response.json - API Response Wrapper

**Purpose**: Standardized API response format with errors and pagination.

**Key Features Demonstrated**:
- Generic wrapper pattern
- Error object structure
- Pagination metadata
- Request tracing (requestId)

**Structure**:
```json
{
  "success": true,
  "data": { ... },
  "errors": [],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "totalItems": 100,
    "totalPages": 5
  },
  "meta": {
    "requestId": "uuid",
    "timestamp": "2025-01-29T12:00:00Z"
  }
}
```

**Use Case**: Wrap any API response for consistent client handling.

---

## Content & Communication (05-10)

### 05_blog_post.json - Blog Post with Comments

**Purpose**: Blog content management with nested comments.

**Key Features Demonstrated**:
- Self-referencing comments (replies)
- Multiple authors (coAuthors)
- Content format options (markdown, html, plain)
- Tag system

**Comment Threading**:
```
Comment
├── author → Author
├── content
├── replies[] → Comment (recursive)
└── likes
```

---

### 06_config.json - Application Configuration

**Purpose**: Comprehensive application configuration schema.

**Key Features Demonstrated**:
- Environment-specific settings
- Database connection configuration
- Cache configuration with drivers
- Security settings (JWT, CORS, rate limiting)
- Feature flags

**Sections**:
- `app`: Name, version, environment, debug mode
- `server`: Host, port, workers
- `database`: Connection pool, SSL, timeout
- `cache`: Redis/Memcached configuration
- `logging`: Level, format, outputs
- `security`: JWT, CORS, rate limiting

---

### 07_invoice.json - Business Invoice

**Purpose**: Professional invoice with line items and payment terms.

**Key Features Demonstrated**:
- Contact with nested address
- Line item calculations
- Tax handling
- Payment terms with due dates

**Business Logic**:
```
Invoice
├── from → Contact (seller)
├── to → Contact (buyer)
├── items[] → InvoiceItem
│   ├── quantity × unitPrice
│   ├── discount
│   └── taxRate
├── subtotal, taxTotal, discountTotal, total
└── paymentTerms
```

---

### 08_event.json - Calendar Event

**Purpose**: Calendar event with recurrence rules and attendees.

**Key Features Demonstrated**:
- RRULE-style recurrence patterns
- Attendee status tracking
- Virtual meeting support
- Reminder configuration

**Recurrence Pattern**:
```json
{
  "frequency": "weekly",
  "interval": 1,
  "daysOfWeek": ["MO", "WE", "FR"],
  "until": "2025-12-31",
  "exceptions": ["2025-07-04"]
}
```

---

### 09_workflow.json - Automation Workflow

**Purpose**: Workflow automation with steps, conditions, and triggers.

**Key Features Demonstrated**:
- Step-based execution flow
- Conditional branching
- Retry policies
- Multiple trigger types

**Workflow Structure**:
```
Workflow
├── triggers[] (manual, schedule, webhook, event)
├── steps[]
│   ├── action (http, email, script, database)
│   ├── condition (branching logic)
│   ├── onSuccess / onFailure
│   └── retryPolicy
└── variables
```

---

### 10_notification.json - Multi-Channel Notification

**Purpose**: Notification system supporting multiple delivery channels.

**Key Features Demonstrated**:
- Channel-specific configuration (oneOf)
- Template system with variables
- Recipient preferences
- Scheduling and expiration

**Supported Channels**:
- Email (with attachments, CC, BCC)
- SMS (Twilio, Nexmo, AWS SNS)
- Push notifications
- In-app notifications
- Slack
- Webhooks

---

## Industry-Specific (11-15)

### 11_healthcare_patient.json - Healthcare Patient Record

**Purpose**: FHIR-inspired patient record structure.

**Key Features Demonstrated**:
- Multiple identifiers (MRN, SSN, etc.)
- Structured name components
- Contact points with ranking
- Insurance information
- Emergency contacts

**Healthcare Standards**:
- Name structure (given[], family, prefix, suffix)
- Contact system types (phone, email, fax)
- Address use types (home, work, billing)

---

### 12_iot_device.json - IoT Device

**Purpose**: IoT device management with telemetry and commands.

**Key Features Demonstrated**:
- Telemetry data structure
- Command/control patterns
- Firmware management
- Network configuration
- Alert system

**Telemetry Data**:
```json
{
  "timestamp": "2025-01-29T12:00:00Z",
  "temperature": 23.5,
  "humidity": 45,
  "battery": 87,
  "signal": -65
}
```

---

### 13_graphql_schema.json - GraphQL Schema Definition

**Purpose**: Represent GraphQL schema as JSON for tooling.

**Key Features Demonstrated**:
- Type definitions with kinds
- Field definitions with arguments
- Type references (nullable, list, non-null)
- Directive support

**GraphQL Type Mapping**:
```
TypeDef
├── name, kind (OBJECT, INPUT, INTERFACE, UNION, ENUM, SCALAR)
├── fields[] → FieldDef
│   ├── type → TypeRef (kind, name, ofType)
│   └── args[] → Argument
├── interfaces[]
└── directives[]
```

---

### 14_kubernetes_deployment.json - Kubernetes Deployment

**Purpose**: Kubernetes Deployment resource specification.

**Key Features Demonstrated**:
- K8s resource structure (apiVersion, kind, metadata, spec)
- Container specifications
- Environment variables (direct and from secrets/configmaps)
- Probes (liveness, readiness)
- Resource limits

**Container Configuration**:
```json
{
  "name": "app",
  "image": "myapp:1.0",
  "ports": [{ "containerPort": 8080 }],
  "resources": {
    "limits": { "cpu": "500m", "memory": "512Mi" },
    "requests": { "cpu": "250m", "memory": "256Mi" }
  },
  "livenessProbe": { "httpGet": { "path": "/health", "port": 8080 } }
}
```

---

### 15_financial_transaction.json - Financial Transaction

**Purpose**: Financial transaction with compliance and audit trail.

**Key Features Demonstrated**:
- Money as structured type (amount + currency)
- Account information with institutions
- Compliance checks (AML, KYC, sanctions)
- Audit trail entries

**Compliance Structure**:
```
Transaction
├── source → Account
├── destination → Account
├── amount → Money
├── compliance[]
│   ├── type (aml, kyc, sanctions, fraud)
│   ├── status (pending, passed, failed, review)
│   └── score, flags
└── auditTrail[]
```

---

## Technical & DevOps (16-22)

### 16_media_library.json - Digital Media Asset

**Purpose**: Media asset management with variants and metadata.

**Key Features Demonstrated**:
- Multiple media variants (quality levels)
- Rich metadata (EXIF, camera info)
- Transcription support
- Access control

**Media Variants**:
```
MediaAsset
├── type (image, video, audio, document)
├── variants[]
│   ├── quality (original, high, medium, low, thumbnail)
│   ├── format, dimensions, duration
│   └── bitrate, fileSize
├── metadata (title, artist, location, camera)
└── transcripts[] (for audio/video)
```

---

### 17_survey.json - Survey with Questions

**Purpose**: Survey builder with question types and logic.

**Key Features Demonstrated**:
- Multiple question types
- Validation rules
- Conditional logic (show/hide based on answers)
- Response collection

**Question Types**:
- text, textarea, number, date
- single_choice, multiple_choice
- rating, matrix, ranking
- file_upload

---

### 18_cicd_pipeline.json - CI/CD Pipeline

**Purpose**: CI/CD pipeline definition (Azure DevOps style).

**Key Features Demonstrated**:
- Multi-stage pipelines
- Job dependencies
- Matrix strategies
- Trigger configuration
- Container jobs

**Pipeline Structure**:
```
Pipeline
├── trigger (branches, paths, tags)
├── schedules[] (cron expressions)
├── resources (repositories, containers)
├── variables[]
└── stages[]
    └── jobs[]
        └── steps[]
```

---

### 19_ml_model.json - ML Model Registry

**Purpose**: Machine learning model registry and deployment tracking.

**Key Features Demonstrated**:
- Model versioning
- Metrics tracking
- Dataset references
- Deployment management

**Model Lifecycle**:
```
MLModel
├── versions[]
│   ├── artifacts[] (model, weights, config)
│   ├── metrics (accuracy, precision, recall, F1)
│   ├── parameters
│   └── trainingData → Dataset
├── deployments[]
│   ├── environment (dev, staging, prod)
│   ├── endpoint, replicas
│   └── resources (cpu, memory, gpu)
└── inputSchema, outputSchema
```

---

### 20_api_gateway.json - API Gateway Configuration

**Purpose**: API gateway routing and policy configuration.

**Key Features Demonstrated**:
- Route definitions with backends
- Authentication methods
- Rate limiting
- Request/response transformation
- CORS configuration

**Route Configuration**:
```json
{
  "path": "/api/users",
  "methods": ["GET", "POST"],
  "backend": {
    "type": "http",
    "url": "http://user-service:8080",
    "timeout": 30000,
    "circuitBreaker": { "threshold": 5, "timeout": 60000 }
  },
  "authentication": { "type": "jwt" },
  "rateLimit": { "requests": 100, "period": "minute" }
}
```

---

### 21_game_entity.json - Game Entity

**Purpose**: Game entity with components (Unity/ECS style).

**Key Features Demonstrated**:
- Transform (position, rotation, scale)
- Component-based architecture
- Physics (colliders, rigid body)
- Animation system
- Recursive children (scene hierarchy)

**Entity Structure**:
```
GameEntity
├── transform (position, rotation, scale)
├── components[]
├── colliders[] (box, sphere, capsule, mesh)
├── rigidBody (mass, drag, gravity)
├── renderer (mesh, materials, shadows)
├── scripts[] (class, parameters)
├── animation (controller, clips)
└── children[] → GameEntity (recursive)
```

---

### 22_openapi_spec.json - OpenAPI Specification

**Purpose**: Simplified OpenAPI 3.0 schema representation.

**Key Features Demonstrated**:
- API metadata (info, servers)
- Path definitions with operations
- Parameter types (query, header, path, cookie)
- Request/response bodies
- Security schemes

**OpenAPI Structure**:
```
OpenAPISpec
├── openapi: "3.0.0"
├── info (title, version, contact, license)
├── servers[]
├── paths
│   └── /endpoint → PathItem
│       └── get/post/put/delete → Operation
│           ├── parameters[]
│           ├── requestBody
│           └── responses
├── components (schemas, responses, securitySchemes)
└── security[], tags[]
```

---

## Common Definitions

### definitions/common.json

**Purpose**: Reusable type definitions for cross-schema references.

**Included Definitions**:
- `UUID`: String with uuid format
- `Email`: String with email format
- `PhoneNumber`: E.164 format pattern
- `ISO8601DateTime`: Date-time format
- `ISO8601Date`: Date format
- `URL`: URI format
- `Currency`: ISO 4217 currency codes
- `Money`: Amount + currency object
- `Address`: Full postal address
- `GeoLocation`: Latitude, longitude, altitude
- `Pagination`: Page, perPage, totals
- `AuditInfo`: Created/updated timestamps and users

**Usage**:
```json
{
  "properties": {
    "location": { "$ref": "definitions/common.json#/definitions/GeoLocation" },
    "price": { "$ref": "definitions/common.json#/definitions/Money" }
  }
}
```

---

## Using the Examples

### Loading and Processing

```python
from jsonschemacodegen import SchemaProcessor
from jsonschemacodegen.utils import load_schema, load_schemas_from_directory

# Load single schema
schema = load_schema("examples/schemas/02_product.json")
processor = SchemaProcessor(schema)

# Load all schemas from directory
all_schemas = load_schemas_from_directory("examples/schemas/")
for path, schema in all_schemas.items():
    print(f"Processing: {path}")
    processor = SchemaProcessor(schema)
    code = processor.generate_code()
```

### Generating Code for All Examples

```python
import os
from pathlib import Path
from jsonschemacodegen import SchemaProcessor
from jsonschemacodegen.utils import load_schema, save_code

schema_dir = Path("examples/schemas")
output_dir = Path("generated")
output_dir.mkdir(exist_ok=True)

for schema_file in schema_dir.glob("*.json"):
    schema = load_schema(schema_file)
    title = schema.get("title", schema_file.stem)
    
    processor = SchemaProcessor(schema, root_class_name=title)
    
    # Generate Python dataclass
    code = processor.generate_code()
    save_code(code, output_dir / f"{schema_file.stem}.py")
    
    # Generate Pydantic model
    pydantic_code = processor.generate_pydantic_models()
    save_code(pydantic_code, output_dir / f"{schema_file.stem}_pydantic.py")
    
    print(f"Generated: {title}")
```

### Generating Test Data

```python
from jsonschemacodegen import SchemaProcessor
from jsonschemacodegen.utils import load_schema
import json

schema = load_schema("examples/schemas/03_order.json")
processor = SchemaProcessor(schema)

# Generate 10 sample orders
orders = processor.generate_samples(count=10)

# Save to file
with open("test_orders.json", "w") as f:
    json.dump(orders, f, indent=2, default=str)
```

---

## Best Practices Demonstrated

### 1. Use Definitions for Reusability
All schemas define reusable types in `definitions` section.

### 2. Meaningful Titles and Descriptions
Every schema and property has descriptive metadata.

### 3. Appropriate Constraints
- String: minLength, maxLength, pattern, format
- Number: minimum, maximum, multipleOf
- Array: minItems, maxItems, uniqueItems
- Object: required, additionalProperties

### 4. Enum for Fixed Values
Status fields, types, and categories use enums.

### 5. Format Specifiers
Proper use of format for semantic validation:
- uuid, email, date-time, uri, ipv4, ipv6

### 6. Composition for Complex Types
Use of allOf for inheritance-like patterns.

### 7. Optional vs Required
Clear distinction between mandatory and optional fields.

---

## Summary

These 22+ example schemas provide comprehensive coverage of:

| Aspect | Examples |
|--------|----------|
| Basic CRUD | User, Product, Order |
| Content Management | Blog, Media, Survey |
| Configuration | App Config, API Gateway |
| Industry Standards | Healthcare (FHIR-like), Finance |
| DevOps | K8s, CI/CD, ML Ops |
| API Design | REST Response, OpenAPI, GraphQL |
| Gaming | Entity-Component System |
| IoT | Device Management, Telemetry |

Use these schemas as:
- **Learning resources** for JSON Schema features
- **Templates** for your own schemas
- **Test cases** for JsonSchemaCodeGen
- **Reference implementations** for common patterns

---

**Copyright © 2025-2030, Ashutosh Sinha. All Rights Reserved.**
