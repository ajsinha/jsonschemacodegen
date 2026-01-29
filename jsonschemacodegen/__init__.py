"""
JsonSchemaCodeGen - Commercial Grade JSON Schema to Python Code Generator
=========================================================================

Copyright © 2025-2030, All Rights Reserved
Ashutosh Sinha
Email: ajsinha@gmail.com

LEGAL NOTICE:
This software is proprietary and confidential. Unauthorized copying,
distribution, modification, or use is strictly prohibited without
explicit written permission from the copyright holder. This software
is provided "as is" without warranty of any kind, either expressed or implied.

Patent Pending: Certain architectural patterns and implementations
described herein may be subject to patent applications.

=========================================================================

A comprehensive library for working with JSON Schema in Python:
- Generate Python classes from JSON Schema
- Generate sample JSON data from schemas
- Handle complex schemas with $ref, allOf, anyOf, oneOf
- Support for remote and local schema references
- Pydantic model generation
- Full JSON Schema Draft-07 support

Usage:
    from jsonschemacodegen import SchemaProcessor, generate_classes, generate_samples

    # Quick start
    processor = SchemaProcessor(schema)
    classes = processor.generate_classes()
    samples = processor.generate_samples(count=5)

Author: JsonSchemaCodeGen Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "JsonSchemaCodeGen Team"

from .core.schema_parser import SchemaParser
from .core.reference_resolver import ReferenceResolver
from .core.type_mapper import TypeMapper
from .core.validator import SchemaValidator

from .generators.sample_generator import SampleGenerator, generate_samples
from .generators.class_generator import ClassGenerator, generate_classes
from .generators.code_generator import CodeGenerator, generate_code
from .generators.pydantic_generator import PydanticGenerator, generate_pydantic_models

from .models.base import BaseModel, JsonSerializable

from .core.schema_processor import SchemaProcessor

__all__ = [
    # Version
    "__version__",
    
    # Core
    "SchemaParser",
    "ReferenceResolver", 
    "TypeMapper",
    "SchemaValidator",
    "SchemaProcessor",
    
    # Generators
    "SampleGenerator",
    "ClassGenerator",
    "CodeGenerator",
    "PydanticGenerator",
    
    # Convenience functions
    "generate_samples",
    "generate_classes",
    "generate_code",
    "generate_pydantic_models",
    
    # Models
    "BaseModel",
    "JsonSerializable",
]
