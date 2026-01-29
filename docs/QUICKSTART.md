# JsonSchemaCodeGen Quick Start Guide

## Copyright and Legal Notice

**Copyright © 2025-2030, All Rights Reserved**  
**Ashutosh Sinha**  
**Email: ajsinha@gmail.com**

This document and the associated software architecture are proprietary and confidential. Unauthorized copying, distribution, modification, or use of this document or the software system it describes is strictly prohibited without explicit written permission from the copyright holder.

**Patent Pending:** Certain architectural patterns and implementations described in this document may be subject to patent applications.

---

## Table of Contents

1. [Installation](#installation)
2. [5-Minute Quick Start](#5-minute-quick-start)
3. [Core Concepts](#core-concepts)
4. [Common Tasks](#common-tasks)
5. [CLI Reference](#cli-reference)
6. [Configuration Options](#configuration-options)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone or extract the package
cd jsonschemacodegen

# Basic installation
pip install .

# With all optional features
pip install .[all]
```

### Optional Dependencies

| Feature | Install Command | Description |
|---------|----------------|-------------|
| Faker | `pip install .[faker]` | Realistic sample data generation |
| Pydantic | `pip install .[pydantic]` | Pydantic model support |
| Requests | `pip install .[requests]` | Remote schema fetching |
| JsonSchema | `pip install .[jsonschema]` | Enhanced validation |
| All | `pip install .[all]` | All optional features |
| Development | `pip install .[dev]` | Testing and linting tools |

### Verify Installation

```bash
python -m jsonschemacodegen --version
# Output: jsonschemacodegen 1.0.0
```

---

## 5-Minute Quick Start

### Step 1: Import

```python
from jsonschemacodegen import SchemaProcessor
```

### Step 2: Define Schema

```python
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
```

### Step 3: Create Processor

```python
processor = SchemaProcessor(schema, root_class_name="User")
```

### Step 4: Generate What You Need

```python
# Generate Python dataclass code
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

### Step 5: Save Output

```python
from jsonschemacodegen.utils import save_code

save_code(code, "models/user.py")
```

---

## Core Concepts

### Schema Processing Pipeline

```
JSON Schema → Parse → Analyze → Generate → Output
     ↓          ↓        ↓          ↓         ↓
  Input    SchemaInfo  Types   Code/Data   Files
```

### Main Components

| Component | Purpose |
|-----------|---------|
| `SchemaProcessor` | Main entry point - unified API |
| `SchemaParser` | Parse schema structure |
| `TypeMapper` | Map JSON types to Python |
| `CodeGenerator` | Generate Python code |
| `SampleGenerator` | Generate test data |
| `SchemaValidator` | Validate schemas and data |

### SchemaProcessor Methods

```python
processor = SchemaProcessor(schema, root_class_name="MyClass")

# Parsing
info = processor.parse()              # → SchemaInfo

# Validation
processor.validate_schema()           # → ValidationResult
processor.validate_data(data)         # → ValidationResult

# Code Generation
processor.generate_code()             # → str (dataclass)
processor.generate_code("pydantic")   # → str (pydantic)
processor.generate_pydantic_models()  # → str (pydantic)

# Sample Data
processor.generate_samples(count=5)   # → List[Dict]

# Dynamic Classes
processor.generate_classes()          # → Type (runtime class)
```

---

## Common Tasks

### Load Schema from File

```python
from jsonschemacodegen.utils import load_schema

schema = load_schema("path/to/schema.json")
processor = SchemaProcessor(schema)
```

### Load Multiple Schemas

```python
from jsonschemacodegen.utils import load_schemas_from_directory

schemas = load_schemas_from_directory("schemas/", recursive=True)
for path, schema in schemas.items():
    print(f"Loaded: {path}")
```

### Generate Code with Custom Class Name

```python
processor = SchemaProcessor(schema, root_class_name="Customer")
code = processor.generate_code()
# Output includes: class Customer:
```

### Handle Complex Schemas with $ref

```python
schema = {
    "type": "object",
    "definitions": {
        "Address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"}
            }
        }
    },
    "properties": {
        "name": {"type": "string"},
        "address": {"$ref": "#/definitions/Address"}
    }
}

processor = SchemaProcessor(schema)
code = processor.generate_code()  # Handles $ref automatically
```

### Generate Realistic Test Data

```python
# With Faker (install: pip install faker)
processor = SchemaProcessor(schema)
samples = processor.generate_samples(count=10, use_faker=True)

# Without Faker
samples = processor.generate_samples(count=10, use_faker=False)
```

### Validate Data

```python
processor = SchemaProcessor(schema)

data = {"name": "John", "email": "invalid-email"}
result = processor.validate_data(data)

if not result.is_valid:
    for issue in result.issues:
        print(f"[{issue.severity}] {issue.path}: {issue.message}")
```

### Generate Pydantic Models

```python
processor = SchemaProcessor(schema, root_class_name="Product")
pydantic_code = processor.generate_pydantic_models()
print(pydantic_code)

# Output:
# from pydantic import BaseModel, Field
# 
# class Product(BaseModel):
#     name: str = Field(...)
#     price: float = Field(..., ge=0)
```

### Save Generated Code

```python
from jsonschemacodegen.utils import save_code

code = processor.generate_code()
save_code(code, "output/models.py")
```

### Parse Schema Information

```python
processor = SchemaProcessor(schema)
info = processor.parse()

print(f"Title: {info.title}")
print(f"Properties: {len(info.properties)}")
print(f"Required: {info.required}")

for name, prop in info.properties.items():
    print(f"  {name}: types={[t.value for t in prop.types]}, required={prop.required}")
```

---

## CLI Reference

### Generate Code

```bash
# Generate Python dataclass
python -m jsonschemacodegen generate schema.json -o models.py

# Generate Pydantic model
python -m jsonschemacodegen generate schema.json -s pydantic -o models.py

# Custom class name
python -m jsonschemacodegen generate schema.json -c Customer -o customer.py
```

### Generate Sample Data

```bash
# Generate 1 sample (default)
python -m jsonschemacodegen samples schema.json

# Generate multiple samples
python -m jsonschemacodegen samples schema.json -n 10 -o samples.json

# Without Faker
python -m jsonschemacodegen samples schema.json --no-faker
```

### Validate

```bash
# Validate schema itself
python -m jsonschemacodegen validate schema.json

# Validate data against schema
python -m jsonschemacodegen validate schema.json -d data.json
```

### Show Schema Info

```bash
python -m jsonschemacodegen info schema.json
```

### Interactive Mode

```bash
python -m jsonschemacodegen interactive

# Commands:
# > load schema.json
# > classes
# > samples 5
# > validate data.json
# > info
# > exit
```

### Help

```bash
python -m jsonschemacodegen --help
python -m jsonschemacodegen generate --help
```

---

## Configuration Options

### SchemaProcessor Options

```python
processor = SchemaProcessor(
    schema,                    # Required: JSON Schema dict
    root_class_name="Root",    # Name for the root class
    resolve_refs=True,         # Resolve $ref references
    use_faker=True,            # Use Faker for sample data
)
```

### Code Generation Styles

| Style | Description | Output |
|-------|-------------|--------|
| `dataclass` | Python dataclasses (default) | `@dataclass` classes |
| `pydantic` | Pydantic v2 models | `BaseModel` classes |
| `standard` | Plain Python classes | Regular classes |

### Sample Generation Options

```python
samples = processor.generate_samples(
    count=5,                   # Number of samples
    use_faker=True,            # Use Faker for realistic data
    include_optional=0.7,      # 70% chance to include optional fields
)
```

---

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'jsonschemacodegen'
```
**Solution**: Install the package with `pip install .`

**Issue: Faker not available**
```
Warning: Faker not available, using basic random data
```
**Solution**: Install Faker with `pip install faker`

**Issue: Schema file not found**
```
FileNotFoundError: Schema file not found: schema.json
```
**Solution**: Check the file path is correct and the file exists

**Issue: Invalid JSON in schema**
```
json.JSONDecodeError: Expecting property name
```
**Solution**: Validate your JSON syntax (missing quotes, trailing commas)

**Issue: Circular reference error**
```
Warning: Circular reference detected: #/definitions/Node
```
**Solution**: This is handled automatically, but check your schema for unintended cycles

### Getting Help

1. Check the [Examples Guide](EXAMPLES.md) for working examples
2. Review the [Architecture Guide](ARCHITECTURE.md) for detailed documentation
3. Run the demo: `python main.py`
4. Contact: ajsinha@gmail.com

---

## Next Steps

1. **Explore Examples**: Check `examples/schemas/` for 22+ real-world schemas
2. **Run Demo**: Execute `python main.py` to see all features
3. **Read Architecture**: See `docs/ARCHITECTURE.md` for deep dive
4. **Browse Examples Guide**: See `docs/EXAMPLES.md` for schema explanations

---

## Quick Reference Card

```python
# Import
from jsonschemacodegen import SchemaProcessor
from jsonschemacodegen.utils import load_schema, save_code

# Load
schema = load_schema("schema.json")

# Process
processor = SchemaProcessor(schema, root_class_name="MyModel")

# Generate
code = processor.generate_code()           # Dataclass
pydantic = processor.generate_pydantic_models()  # Pydantic
samples = processor.generate_samples(5)    # Test data

# Validate
result = processor.validate_data(data)
if not result.is_valid:
    print(result.issues)

# Save
save_code(code, "output/models.py")
```

```bash
# CLI
python -m jsonschemacodegen generate schema.json -o models.py
python -m jsonschemacodegen samples schema.json -n 10
python -m jsonschemacodegen validate schema.json -d data.json
python -m jsonschemacodegen info schema.json
python -m jsonschemacodegen interactive
```

---

**Copyright © 2025-2030, Ashutosh Sinha. All Rights Reserved.**
