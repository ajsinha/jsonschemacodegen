# JsonSchemaCodeGen v1.0.0

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        JsonSchemaCodeGen v1.0.0                              ║
║                                                                              ║
║            Commercial Grade JSON Schema to Python Code Generator             ║
║                                                                              ║
║                  Copyright © 2025-2030, All Rights Reserved                  ║
║                      Ashutosh Sinha (ajsinha@gmail.com)                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Copyright and Legal Notice

**Copyright © 2025-2030, All Rights Reserved**  
**Ashutosh Sinha**  
**Email: ajsinha@gmail.com**

### Legal Notice

This document and the associated software architecture are proprietary and confidential. Unauthorized copying, distribution, modification, or use of this document or the software system it describes is strictly prohibited without explicit written permission from the copyright holder.

This document is provided "as is" without warranty of any kind, either expressed or implied. The copyright holder shall not be liable for any damages arising from the use of this document or the software system it describes.

**Patent Pending:** Certain architectural patterns and implementations described in this document may be subject to patent applications.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [API Reference](#api-reference)
- [CLI Usage](#cli-usage)
- [Example Schemas](#example-schemas)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Support](#support)

---

## Overview

**JsonSchemaCodeGen** is a comprehensive, commercial-grade Python library for working with JSON Schema. It provides powerful, production-ready tools for:

- 🔧 **Schema Parsing**: Parse and analyze JSON Schema documents with full Draft-07 support
- 💻 **Code Generation**: Generate Python dataclasses, Pydantic v2 models, and more
- 📊 **Sample Data Generation**: Create realistic test data with Faker integration
- ✅ **Validation**: Validate schemas and data with detailed error reporting
- 🔗 **Reference Resolution**: Handle complex `$ref` references including remote schemas

### Why JsonSchemaCodeGen?

| Feature | JsonSchemaCodeGen | Others |
|---------|-------------------|--------|
| Full Draft-07 Support | ✅ | Partial |
| Pydantic v2 Generation | ✅ | Limited |
| Realistic Sample Data | ✅ Faker Integration | Basic |
| Remote Schema Resolution | ✅ HTTP/HTTPS | Local only |
| Circular Reference Handling | ✅ Intelligent | Errors |
| Commercial Grade | ✅ Production Ready | Experimental |

---

## Key Features

### Code Generation

| Output Format | Description |
|---------------|-------------|
| **Python Dataclasses** | Modern Python dataclasses with type hints |
| **Pydantic v2 Models** | Full Pydantic v2 support with validators |
| **Standard Classes** | Traditional Python classes |

### Schema Support

- ✅ All JSON Schema Draft-07 keywords
- ✅ Composition: `allOf`, `anyOf`, `oneOf`, `not`
- ✅ Conditionals: `if`/`then`/`else`
- ✅ References: local, file, remote HTTP/HTTPS
- ✅ Definitions: `definitions`, `$defs`
- ✅ All format specifiers: uuid, email, date-time, uri, ipv4, ipv6, etc.
- ✅ All constraints: min/max, patterns, enums, required fields

### Sample Data Generation

- 🎭 **Faker Integration**: Realistic names, emails, addresses, etc.
- 📏 **Constraint-Aware**: Respects min/max, patterns, formats
- 🔄 **Configurable**: Optional field inclusion probability
- 🎯 **Format-Specific**: Proper UUID, email, datetime generation

### Validation

- 📋 Schema structure validation
- 📊 Data validation against schema
- 📍 Detailed error paths
- ⚠️ Severity levels (error, warning, info)
- 🔌 Custom validator support

---

## Installation

### From Source

```bash
cd jsonschemacodegen
pip install .
```

### With Optional Dependencies

```bash
# All features
pip install .[all]

# Specific features
pip install .[faker]      # Realistic sample data
pip install .[pydantic]   # Pydantic model generation
pip install .[requests]   # Remote schema fetching
pip install .[jsonschema] # Enhanced validation

# Development
pip install .[dev]        # Testing and linting
```

### Verify Installation

```bash
python -m jsonschemacodegen --version
```

---

## Quick Start

### Basic Usage

```python
from jsonschemacodegen import SchemaProcessor

# Define schema
schema = {
    "type": "object",
    "title": "User",
    "properties": {
        "id": {"type": "string", "format": "uuid"},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["id", "name", "email"]
}

# Create processor
processor = SchemaProcessor(schema, root_class_name="User")

# Generate Python dataclass
code = processor.generate_code()
print(code)

# Generate Pydantic model
pydantic_code = processor.generate_pydantic_models()
print(pydantic_code)

# Generate sample data
samples = processor.generate_samples(count=3)
for sample in samples:
    print(sample)

# Validate data
data = {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "John", "email": "john@example.com"}
result = processor.validate_data(data)
print(f"Valid: {result.is_valid}")
```

### Load from File

```python
from jsonschemacodegen import SchemaProcessor
from jsonschemacodegen.utils import load_schema, save_code

# Load schema
schema = load_schema("examples/schemas/02_product.json")

# Process
processor = SchemaProcessor(schema)
code = processor.generate_code()

# Save
save_code(code, "output/product.py")
```

### Command Line

```bash
# Generate code
python -m jsonschemacodegen generate schema.json -o models.py

# Generate Pydantic
python -m jsonschemacodegen generate schema.json -s pydantic -o models.py

# Generate samples
python -m jsonschemacodegen samples schema.json -n 10 -o samples.json

# Validate
python -m jsonschemacodegen validate schema.json -d data.json
```

For complete quick start guide, see [docs/QUICKSTART.md](docs/QUICKSTART.md).

---

## Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](docs/QUICKSTART.md) | Get started in 5 minutes |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture and design |
| [EXAMPLES.md](docs/EXAMPLES.md) | Detailed guide to all 22+ example schemas |
| [LICENSE](LICENSE) | Proprietary license terms |

### Run the Demo

```bash
python main.py
```

This demonstrates all key features with working examples.

---

## API Reference

### SchemaProcessor (Main Entry Point)

```python
from jsonschemacodegen import SchemaProcessor

processor = SchemaProcessor(
    schema,                    # JSON Schema dictionary
    root_class_name="Root",    # Name for root class
    resolve_refs=True,         # Resolve $ref references
    use_faker=True             # Use Faker for samples
)

# Methods
info = processor.parse()                    # → SchemaInfo
result = processor.validate_schema()        # → ValidationResult
result = processor.validate_data(data)      # → ValidationResult
code = processor.generate_code()            # → str
code = processor.generate_pydantic_models() # → str
samples = processor.generate_samples(n)     # → List[Dict]
cls = processor.generate_classes()          # → Type
```

### Convenience Functions

```python
from jsonschemacodegen import (
    generate_code,
    generate_samples,
    generate_pydantic_models,
    validate_schema,
    validate_data
)

# Quick generation
code = generate_code(schema, class_name="MyClass")
samples = generate_samples(schema, count=5)
pydantic = generate_pydantic_models(schema)

# Quick validation
is_valid = validate_data(data, schema)
```

### Utility Functions

```python
from jsonschemacodegen.utils import (
    load_schema,
    save_schema,
    save_code,
    load_schemas_from_directory
)

# Load/save
schema = load_schema("schema.json")
save_schema(schema, "output.json")
save_code(code, "models.py")

# Batch load
schemas = load_schemas_from_directory("schemas/", recursive=True)
```

### Core Components

```python
from jsonschemacodegen.core import (
    SchemaParser,
    ReferenceResolver,
    TypeMapper,
    SchemaValidator
)

# Individual component usage
parser = SchemaParser(schema)
info = parser.parse()

resolver = ReferenceResolver(schema)
resolved = resolver.resolve_all()

mapper = TypeMapper()
mapping = mapper.map_schema(schema)

validator = SchemaValidator()
result = validator.validate_data(data, schema)
```

### Generator Components

```python
from jsonschemacodegen.generators import (
    CodeGenerator,
    SampleGenerator,
    PydanticGenerator,
    ClassGenerator
)

# Code generation
gen = CodeGenerator(schema, class_name="MyClass")
code = gen.generate()

# Sample generation
sample_gen = SampleGenerator(schema)
sample = sample_gen.generate()

# Pydantic generation
pydantic_gen = PydanticGenerator(schema)
code = pydantic_gen.generate()
```

---

## CLI Usage

### Commands

| Command | Description |
|---------|-------------|
| `generate` | Generate Python code from schema |
| `samples` | Generate sample JSON data |
| `validate` | Validate schema or data |
| `info` | Display schema information |
| `interactive` | Start interactive mode |

### Generate Command

```bash
python -m jsonschemacodegen generate <schema> [options]

Options:
  -o, --output FILE      Output file path
  -c, --class-name NAME  Root class name (default: Root)
  -s, --style STYLE      Code style: dataclass, pydantic (default: dataclass)
```

### Samples Command

```bash
python -m jsonschemacodegen samples <schema> [options]

Options:
  -n, --count N          Number of samples (default: 1)
  -o, --output FILE      Output file path
  --no-faker             Disable Faker
```

### Validate Command

```bash
python -m jsonschemacodegen validate <schema> [options]

Options:
  -d, --data FILE        JSON data file to validate
```

### Interactive Mode

```bash
python -m jsonschemacodegen interactive

Commands:
  load <file>            Load a schema
  classes                Generate Python classes
  samples [n]            Generate n samples
  validate <file>        Validate data file
  info                   Show schema info
  exit                   Exit
```

---

## Example Schemas

JsonSchemaCodeGen includes **22+ comprehensive example schemas** demonstrating real-world use cases:

### Basic Schemas (01-04)
| Schema | Description |
|--------|-------------|
| `01_user.json` | User account with preferences and roles |
| `02_product.json` | E-commerce product with variants |
| `03_order.json` | Order with line items and shipping |
| `04_api_response.json` | Standard API response wrapper |

### Content & Communication (05-10)
| Schema | Description |
|--------|-------------|
| `05_blog_post.json` | Blog post with nested comments |
| `06_config.json` | Application configuration |
| `07_invoice.json` | Business invoice |
| `08_event.json` | Calendar event with recurrence |
| `09_workflow.json` | Automation workflow |
| `10_notification.json` | Multi-channel notification |

### Industry-Specific (11-15)
| Schema | Description |
|--------|-------------|
| `11_healthcare_patient.json` | FHIR-style patient record |
| `12_iot_device.json` | IoT device with telemetry |
| `13_graphql_schema.json` | GraphQL schema definition |
| `14_kubernetes_deployment.json` | K8s deployment spec |
| `15_financial_transaction.json` | Transaction with compliance |

### Technical & DevOps (16-22)
| Schema | Description |
|--------|-------------|
| `16_media_library.json` | Digital media asset |
| `17_survey.json` | Survey with questions |
| `18_cicd_pipeline.json` | CI/CD pipeline |
| `19_ml_model.json` | ML model registry |
| `20_api_gateway.json` | API gateway config |
| `21_game_entity.json` | Game entity (ECS style) |
| `22_openapi_spec.json` | OpenAPI specification |

For detailed explanations of each schema, see [docs/EXAMPLES.md](docs/EXAMPLES.md).

---

## Project Structure

```
jsonschemacodegen/
├── jsonschemacodegen/           # Main package
│   ├── __init__.py              # Public API exports
│   ├── __main__.py              # CLI entry point
│   ├── cli.py                   # CLI implementation
│   ├── core/                    # Core processing
│   │   ├── reference_resolver.py    # $ref resolution
│   │   ├── schema_parser.py         # Schema parsing
│   │   ├── schema_processor.py      # Main processor
│   │   ├── type_mapper.py           # Type mapping
│   │   └── validator.py             # Validation
│   ├── generators/              # Code generators
│   │   ├── class_generator.py       # Dynamic classes
│   │   ├── code_generator.py        # Python code
│   │   ├── pydantic_generator.py    # Pydantic models
│   │   └── sample_generator.py      # Sample data
│   ├── models/                  # Data models
│   │   └── base.py                  # Base classes
│   └── utils/                   # Utilities
│       ├── file_utils.py            # File I/O
│       ├── json_utils.py            # JSON helpers
│       └── naming.py                # Naming conventions
├── examples/
│   └── schemas/                 # 22+ example schemas
│       ├── 01_user.json
│       ├── ...
│       └── definitions/         # Shared definitions
├── tests/                       # Test suite
├── docs/                        # Documentation
│   ├── QUICKSTART.md
│   ├── ARCHITECTURE.md
│   └── EXAMPLES.md
├── main.py                      # Demo script
├── setup.py                     # Package setup
├── pyproject.toml               # Modern packaging
├── LICENSE                      # Proprietary license
└── README.md                    # This file
```

---

## Dependencies

### Required
- **Python 3.8+**
- No required external dependencies (pure Python core)

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| faker | ≥18.0.0 | Realistic sample data |
| requests | ≥2.28.0 | Remote schema fetching |
| jsonschema | ≥4.17.0 | Enhanced validation |
| pydantic | ≥2.0.0 | Pydantic model support |

### Development

| Package | Purpose |
|---------|---------|
| pytest | Testing |
| pytest-cov | Coverage |
| black | Formatting |
| isort | Import sorting |
| mypy | Type checking |
| flake8 | Linting |

---

## Support

For support, licensing inquiries, or bug reports:

**Ashutosh Sinha**  
**Email: ajsinha@gmail.com**

---

## License

This software is proprietary and confidential. See [LICENSE](LICENSE) for full terms.

**Copyright © 2025-2030, All Rights Reserved**  
**Ashutosh Sinha**

**Patent Pending:** Certain architectural patterns and implementations may be subject to patent applications.
