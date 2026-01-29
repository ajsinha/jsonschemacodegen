# JsonSchemaCodeGen Architecture Guide

## Copyright and Legal Notice

**Copyright © 2025-2030, All Rights Reserved**  
**Ashutosh Sinha**  
**Email: ajsinha@gmail.com**

This document and the associated software architecture are proprietary and confidential. Unauthorized copying, distribution, modification, or use of this document or the software system it describes is strictly prohibited without explicit written permission from the copyright holder.

**Patent Pending:** Certain architectural patterns and implementations described in this document may be subject to patent applications.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [Module Architecture](#module-architecture)
4. [Core Components](#core-components)
5. [Generator Components](#generator-components)
6. [Data Flow](#data-flow)
7. [Extension Points](#extension-points)
8. [Design Patterns Used](#design-patterns-used)
9. [Performance Considerations](#performance-considerations)
10. [Security Considerations](#security-considerations)

---

## System Overview

JsonSchemaCodeGen is designed as a modular, extensible system for processing JSON Schema documents and generating various outputs including Python code, sample data, and validation reports.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        JsonSchemaCodeGen                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    SchemaProcessor                            │   │
│  │                   (Main Entry Point)                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│          ┌───────────────────┼───────────────────┐                  │
│          ▼                   ▼                   ▼                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │
│  │     Core     │   │  Generators  │   │    Models    │            │
│  ├──────────────┤   ├──────────────┤   ├──────────────┤            │
│  │ • Resolver   │   │ • Code       │   │ • Base       │            │
│  │ • Parser     │   │ • Sample     │   │ • Registry   │            │
│  │ • TypeMapper │   │ • Class      │   │              │            │
│  │ • Validator  │   │ • Pydantic   │   │              │            │
│  └──────────────┘   └──────────────┘   └──────────────┘            │
│          │                   │                   │                  │
│          └───────────────────┼───────────────────┘                  │
│                              ▼                                       │
│                      ┌──────────────┐                               │
│                      │   Utilities  │                               │
│                      ├──────────────┤                               │
│                      │ • File I/O   │                               │
│                      │ • JSON Utils │                               │
│                      │ • Naming     │                               │
│                      └──────────────┘                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Architecture Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- **Core**: Schema understanding and analysis
- **Generators**: Output production
- **Models**: Data structures
- **Utils**: Cross-cutting concerns

### 2. Dependency Injection
Components receive their dependencies through constructors, making them testable and configurable.

### 3. Open/Closed Principle
The system is open for extension (new generators, validators) but closed for modification of core behavior.

### 4. Fail-Safe Defaults
All components have sensible defaults and graceful degradation when optional dependencies are unavailable.

### 5. Immutability Where Possible
Schema data and parsed information are treated as immutable to prevent side effects.

---

## Module Architecture

### Package Structure

```
jsonschemacodegen/
├── __init__.py              # Public API exports
├── __main__.py              # CLI entry point
├── cli.py                   # CLI implementation
│
├── core/                    # Core processing modules
│   ├── __init__.py
│   ├── reference_resolver.py
│   ├── schema_parser.py
│   ├── schema_processor.py
│   ├── type_mapper.py
│   └── validator.py
│
├── generators/              # Output generators
│   ├── __init__.py
│   ├── class_generator.py
│   ├── code_generator.py
│   ├── pydantic_generator.py
│   └── sample_generator.py
│
├── models/                  # Data models
│   ├── __init__.py
│   └── base.py
│
└── utils/                   # Utility functions
    ├── __init__.py
    ├── file_utils.py
    ├── json_utils.py
    └── naming.py
```

### Module Dependencies

```
                    ┌─────────────┐
                    │    utils    │
                    └─────────────┘
                          ▲
            ┌─────────────┼─────────────┐
            │             │             │
    ┌───────┴───────┐     │     ┌───────┴───────┐
    │    models     │     │     │   generators  │
    └───────────────┘     │     └───────────────┘
            ▲             │             ▲
            │             │             │
            └─────────────┼─────────────┘
                          │
                    ┌─────┴─────┐
                    │    core   │
                    └───────────┘
                          ▲
                          │
                    ┌─────┴─────┐
                    │  __init__ │
                    └───────────┘
```

---

## Core Components

### 1. ReferenceResolver (`core/reference_resolver.py`)

**Purpose**: Resolves `$ref` references in JSON Schema documents.

**Key Classes**:
- `ReferenceResolver`: Main resolver class
- `SchemaRegistry`: Manages multiple related schemas

**Capabilities**:
- Local references (`#/definitions/Name`)
- File-based references (`./other-schema.json`)
- Remote HTTP/HTTPS references
- Circular reference detection
- Caching for performance

**Architecture**:
```
┌─────────────────────────────────────────┐
│          ReferenceResolver              │
├─────────────────────────────────────────┤
│ - schema: Dict                          │
│ - registry: SchemaRegistry              │
│ - resolved_cache: Dict                  │
│ - resolution_stack: Set (cycle detect)  │
├─────────────────────────────────────────┤
│ + resolve(ref: str) → Dict              │
│ + resolve_all() → Dict                  │
│ + register_schema(uri, schema)          │
└─────────────────────────────────────────┘
```

### 2. SchemaParser (`core/schema_parser.py`)

**Purpose**: Parses JSON Schema into structured Python objects.

**Key Classes**:
- `SchemaParser`: Main parser class
- `SchemaInfo`: Parsed schema information (dataclass)
- `PropertyInfo`: Property metadata (dataclass)

**Capabilities**:
- Type extraction (including union types)
- Constraint parsing
- Composition handling (allOf, anyOf, oneOf)
- Conditional schema support (if/then/else)
- Definition extraction

**Architecture**:
```
┌─────────────────────────────────────────┐
│            SchemaParser                 │
├─────────────────────────────────────────┤
│ - schema: Dict                          │
│ - resolver: ReferenceResolver           │
├─────────────────────────────────────────┤
│ + parse() → SchemaInfo                  │
│ + parse_property(name, schema)          │
│ + merge_schemas(schemas: List)          │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│            SchemaInfo                   │
├─────────────────────────────────────────┤
│ + title: Optional[str]                  │
│ + description: Optional[str]            │
│ + types: List[SchemaType]               │
│ + properties: Dict[str, PropertyInfo]   │
│ + definitions: Dict[str, SchemaInfo]    │
│ + required: List[str]                   │
│ + constraints: Dict                     │
│ + all_of/any_of/one_of: List           │
└─────────────────────────────────────────┘
```

### 3. TypeMapper (`core/type_mapper.py`)

**Purpose**: Maps JSON Schema types to Python types.

**Key Classes**:
- `TypeMapper`: Main mapper class
- `TypeMapping`: Mapping result (dataclass)

**Capabilities**:
- Primitive type mapping
- Format-specific types (email, uuid, datetime, etc.)
- Array and object handling
- Union types (anyOf, oneOf)
- Nullable type support
- Custom type registration

**Type Mapping Table**:
```
JSON Schema Type     Format          Python Type
─────────────────────────────────────────────────
string               -               str
string               email           str (EmailStr with Pydantic)
string               date-time       datetime
string               date            date
string               uuid            UUID
string               uri             str
string               ipv4            IPv4Address
string               ipv6            IPv6Address
integer              -               int
number               -               float (or Decimal)
boolean              -               bool
null                 -               None
array                -               List[T]
object               -               Dict or custom class
```

### 4. SchemaValidator (`core/validator.py`)

**Purpose**: Validates schemas and data against schemas.

**Key Classes**:
- `SchemaValidator`: Main validator class
- `ValidationResult`: Validation outcome (dataclass)
- `ValidationIssue`: Individual issue details (dataclass)

**Capabilities**:
- Schema structure validation
- Data validation against schema
- Detailed error reporting with paths
- Severity levels (error, warning, info)
- Custom validator support

### 5. SchemaProcessor (`core/schema_processor.py`)

**Purpose**: High-level unified API combining all core functionality.

**This is the main entry point for users.**

**Key Methods**:
```python
class SchemaProcessor:
    def __init__(schema, root_class_name="Root", resolve_refs=True, use_faker=True)
    
    def parse() -> SchemaInfo
    def validate_schema() -> ValidationResult
    def validate_data(data) -> ValidationResult
    def generate_code(style="dataclass") -> str
    def generate_pydantic_models() -> str
    def generate_samples(count=1) -> List[Dict]
    def generate_classes() -> Type
```

---

## Generator Components

### 1. CodeGenerator (`generators/code_generator.py`)

**Purpose**: Generates Python source code as strings.

**Output Formats**:
- Dataclasses (default)
- Standard classes
- TypedDict

**Features**:
- Complete module generation with imports
- Type hints
- Docstrings from schema descriptions
- Nested class support
- Serialization methods (to_dict, from_dict, to_json, from_json)

**Generated Code Structure**:
```python
"""
Generated by JsonSchemaCodeGen
Schema: User
Generated at: 2025-01-29T12:00:00
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

@dataclass
class User:
    """User account information."""
    
    id: UUID
    email: str
    name: str
    age: Optional[int] = None
    
    def to_dict(self) -> dict:
        ...
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        ...
```

### 2. PydanticGenerator (`generators/pydantic_generator.py`)

**Purpose**: Generates Pydantic v2 model code.

**Features**:
- Pydantic v2 syntax
- Field validators
- Constraint mapping
- Format-specific types
- ConfigDict configuration
- Alias support for JSON field names

**Generated Code Structure**:
```python
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True
    )
    
    id: str = Field(..., alias="id")
    email: str = Field(..., min_length=1)
    age: Optional[int] = Field(None, ge=0, le=150)
```

### 3. SampleGenerator (`generators/sample_generator.py`)

**Purpose**: Generates realistic sample JSON data.

**Features**:
- Faker integration for realistic data
- Constraint-aware generation
- Format-specific generators
- Custom generator registration
- Configurable optional field inclusion

**Data Generation Strategy**:
```
Format          Generator
─────────────────────────────────
email           faker.email()
uuid            uuid.uuid4()
date            faker.date()
date-time       faker.date_time_this_year()
uri             faker.url()
ipv4            faker.ipv4()
name            faker.name()
phone           faker.phone_number()
address         faker.address()
(default)       Random appropriate value
```

### 4. ClassGenerator (`generators/class_generator.py`)

**Purpose**: Dynamically creates Python classes at runtime.

**Features**:
- Runtime dataclass creation
- Proper field ordering
- Method generation
- Forward reference handling
- Model registry integration

---

## Data Flow

### Schema Processing Flow

```
Input Schema (JSON/Dict)
         │
         ▼
┌─────────────────────┐
│ ReferenceResolver   │──── Resolve $ref ────┐
└─────────────────────┘                      │
         │                                   │
         ▼                                   │
┌─────────────────────┐                      │
│   SchemaParser      │◄─────────────────────┘
└─────────────────────┘
         │
         ▼
    SchemaInfo
    (Parsed Data)
         │
         ├──────────────┬──────────────┬──────────────┐
         ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ CodeGen     │ │ PydanticGen │ │ SampleGen   │ │ Validator   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
   Python Code    Pydantic Code   Sample Data   Validation
                                                 Result
```

### Code Generation Flow

```
SchemaInfo
     │
     ▼
┌──────────────────┐
│  TypeMapper      │
│  (Map to Python) │
└──────────────────┘
     │
     ▼
TypeMapping[]
     │
     ▼
┌──────────────────┐
│  CodeGenerator   │
│  (Build AST)     │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│  Format & Output │
└──────────────────┘
     │
     ▼
Python Source Code
```

---

## Extension Points

### Adding a New Generator

1. Create a new file in `generators/`
2. Implement the generator class:

```python
class CustomGenerator:
    def __init__(self, schema: Dict[str, Any], **options):
        self.schema = schema
        self.parser = SchemaParser(schema)
        
    def generate(self) -> str:
        info = self.parser.parse()
        # Generate output
        return output
```

3. Register in `generators/__init__.py`
4. Add method to `SchemaProcessor`

### Adding Custom Type Mappings

```python
from jsonschemacodegen.core import TypeMapper

mapper = TypeMapper()
mapper.register_format_mapping(
    "phone",
    TypeMapping(
        python_type="PhoneNumber",
        imports={"from phonenumbers import PhoneNumber"},
        default="None"
    )
)
```

### Adding Custom Validators

```python
from jsonschemacodegen.core import SchemaValidator

validator = SchemaValidator()
validator.register_validator(
    "custom_rule",
    lambda schema, data, path: ValidationIssue(...) if invalid else None
)
```

---

## Design Patterns Used

### 1. Strategy Pattern
Different generators implement the same interface but produce different outputs.

### 2. Factory Pattern
`SchemaProcessor` acts as a factory for creating appropriate handlers.

### 3. Registry Pattern
`ModelRegistry` and `SchemaRegistry` manage collections of related objects.

### 4. Builder Pattern
Code generators build output incrementally.

### 5. Visitor Pattern
Schema traversal for validation and processing.

### 6. Decorator Pattern
Optional features (Faker, validation) wrap core functionality.

---

## Performance Considerations

### Caching
- Reference resolution results are cached
- Parsed schemas are cached within processor lifetime
- Type mappings are computed once

### Lazy Evaluation
- Definitions are parsed on-demand
- Remote schemas are fetched only when referenced

### Memory Management
- Large schemas processed incrementally
- Circular reference detection prevents infinite loops

### Recommendations
- Reuse `SchemaProcessor` instances when processing multiple data items
- Use `SchemaRegistry` for related schemas
- Enable caching for repeated operations

---

## Security Considerations

### Remote Schema Fetching
- HTTPS preferred over HTTP
- Timeout limits on remote requests
- Optional disable of remote fetching

### Input Validation
- Schema structure validated before processing
- Malformed JSON handled gracefully
- Path traversal prevented in file references

### Generated Code
- No `eval()` or `exec()` in generated code
- Proper escaping of string values
- Type-safe output

---

## Conclusion

JsonSchemaCodeGen's architecture is designed for:
- **Modularity**: Easy to understand and modify individual components
- **Extensibility**: Add new generators or validators without changing core
- **Reliability**: Comprehensive error handling and validation
- **Performance**: Caching and lazy evaluation for efficiency
- **Maintainability**: Clear separation of concerns and documentation

For implementation details, refer to the source code and inline documentation.

---

**Copyright © 2025-2030, Ashutosh Sinha. All Rights Reserved.**
