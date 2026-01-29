#!/usr/bin/env python3
"""
JsonSchemaCodeGen - Main Demonstration Script

Copyright © 2025-2030, All Rights Reserved
Ashutosh Sinha
Email: ajsinha@gmail.com

LEGAL NOTICE:
This software is proprietary and confidential. Unauthorized copying,
distribution, modification, or use is strictly prohibited without
explicit written permission from the copyright holder.

Patent Pending: Certain implementations may be subject to patent applications.

This script demonstrates all the key features of JsonSchemaCodeGen.
"""

import json
import os
import sys
from pathlib import Path

# Add package to path for direct execution
sys.path.insert(0, str(Path(__file__).parent))

from jsonschemacodegen import (
    SchemaProcessor,
    generate_code,
    generate_samples,
    generate_pydantic_models,
    __version__,
)
from jsonschemacodegen.utils import load_schema


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_subheader(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---\n")


def demo_basic_usage():
    """Demonstrate basic schema processing."""
    print_header("BASIC USAGE DEMONSTRATION")
    
    # Simple schema
    schema = {
        "type": "object",
        "title": "Person",
        "description": "A simple person record",
        "properties": {
            "id": {"type": "string", "format": "uuid"},
            "name": {"type": "string", "minLength": 1, "maxLength": 100},
            "email": {"type": "string", "format": "email"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
            "isActive": {"type": "boolean", "default": True}
        },
        "required": ["id", "name", "email"]
    }
    
    print_subheader("Input Schema")
    print(json.dumps(schema, indent=2))
    
    # Create processor
    processor = SchemaProcessor(schema, root_class_name="Person")
    
    # Parse schema
    print_subheader("Parsed Schema Info")
    info = processor.parse()
    print(f"Title: {info.title}")
    print(f"Description: {info.description}")
    print(f"Properties: {len(info.properties)}")
    for name, prop in info.properties.items():
        req = " (required)" if prop.required else ""
        print(f"  - {name}: {[t.value for t in prop.types]}{req}")
    
    # Generate code
    print_subheader("Generated Python Dataclass")
    code = processor.generate_code()
    print(code)
    
    # Generate samples
    print_subheader("Generated Sample Data")
    samples = processor.generate_samples(count=3)
    for i, sample in enumerate(samples, 1):
        print(f"Sample {i}:")
        print(json.dumps(sample, indent=2, default=str))
        print()


def demo_complex_schema():
    """Demonstrate complex schema with nested objects."""
    print_header("COMPLEX SCHEMA DEMONSTRATION")
    
    schema = {
        "type": "object",
        "title": "Order",
        "definitions": {
            "Address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "country": {"type": "string"}
                },
                "required": ["street", "city", "country"]
            },
            "LineItem": {
                "type": "object",
                "properties": {
                    "productId": {"type": "string"},
                    "name": {"type": "string"},
                    "quantity": {"type": "integer", "minimum": 1},
                    "price": {"type": "number", "minimum": 0}
                },
                "required": ["productId", "quantity", "price"]
            }
        },
        "properties": {
            "orderId": {"type": "string", "format": "uuid"},
            "customer": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                },
                "required": ["name", "email"]
            },
            "items": {
                "type": "array",
                "items": {"$ref": "#/definitions/LineItem"},
                "minItems": 1
            },
            "shippingAddress": {"$ref": "#/definitions/Address"},
            "status": {
                "type": "string",
                "enum": ["pending", "processing", "shipped", "delivered"]
            },
            "total": {"type": "number"},
            "createdAt": {"type": "string", "format": "date-time"}
        },
        "required": ["orderId", "customer", "items", "status"]
    }
    
    processor = SchemaProcessor(schema, root_class_name="Order")
    
    # Show parsed info
    print_subheader("Schema Structure")
    info = processor.parse()
    print(f"Title: {info.title}")
    print(f"Definitions: {list(info.definitions.keys())}")
    print(f"Properties: {list(info.properties.keys())}")
    
    # Generate code
    print_subheader("Generated Code")
    code = processor.generate_code()
    print(code)
    
    # Generate sample
    print_subheader("Generated Sample Order")
    sample = processor.generate_samples(count=1)[0]
    print(json.dumps(sample, indent=2, default=str))


def demo_pydantic_generation():
    """Demonstrate Pydantic model generation."""
    print_header("PYDANTIC MODEL GENERATION")
    
    schema = {
        "type": "object",
        "title": "Product",
        "properties": {
            "id": {"type": "string", "format": "uuid"},
            "name": {"type": "string", "minLength": 1, "maxLength": 255},
            "description": {"type": "string"},
            "price": {"type": "number", "minimum": 0},
            "category": {"type": "string", "enum": ["electronics", "clothing", "food", "other"]},
            "tags": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "inStock": {"type": "boolean", "default": True},
            "createdAt": {"type": "string", "format": "date-time"}
        },
        "required": ["id", "name", "price", "category"]
    }
    
    processor = SchemaProcessor(schema, root_class_name="Product")
    
    print_subheader("Generated Pydantic Model")
    pydantic_code = processor.generate_pydantic_models()
    print(pydantic_code)
    
    print_subheader("Sample Product Data")
    sample = processor.generate_samples(count=1)[0]
    print(json.dumps(sample, indent=2, default=str))


def demo_validation():
    """Demonstrate validation capabilities."""
    print_header("VALIDATION DEMONSTRATION")
    
    schema = {
        "type": "object",
        "title": "User",
        "properties": {
            "username": {"type": "string", "minLength": 3, "maxLength": 20, "pattern": "^[a-z0-9_]+$"},
            "email": {"type": "string", "format": "email"},
            "age": {"type": "integer", "minimum": 18, "maximum": 120}
        },
        "required": ["username", "email"]
    }
    
    processor = SchemaProcessor(schema)
    
    # Valid data
    print_subheader("Validating Valid Data")
    valid_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "age": 30
    }
    print(f"Data: {json.dumps(valid_data)}")
    result = processor.validate_data(valid_data)
    print(f"Valid: {result.is_valid}")
    
    # Invalid data
    print_subheader("Validating Invalid Data")
    invalid_data = {
        "username": "JD",  # Too short, has uppercase
        "email": "not-an-email",
        "age": 15  # Below minimum
    }
    print(f"Data: {json.dumps(invalid_data)}")
    result = processor.validate_data(invalid_data)
    print(f"Valid: {result.is_valid}")
    if not result.is_valid:
        print("Issues:")
        for issue in result.issues:
            print(f"  - {issue.path}: {issue.message}")


def demo_file_schemas():
    """Demonstrate loading and processing file-based schemas."""
    print_header("FILE-BASED SCHEMA DEMONSTRATION")
    
    schema_dir = Path(__file__).parent / "examples" / "schemas"
    
    if not schema_dir.exists():
        print(f"Schema directory not found: {schema_dir}")
        return
    
    # List available schemas
    schemas = list(schema_dir.glob("*.json"))
    print(f"Found {len(schemas)} example schemas:\n")
    
    for schema_path in sorted(schemas)[:5]:
        print(f"  - {schema_path.name}")
    
    if len(schemas) > 5:
        print(f"  ... and {len(schemas) - 5} more")
    
    # Process first schema
    if schemas:
        print_subheader(f"Processing: {sorted(schemas)[0].name}")
        schema = load_schema(sorted(schemas)[0])
        processor = SchemaProcessor(schema)
        
        info = processor.parse()
        print(f"Title: {info.title or 'N/A'}")
        print(f"Properties: {len(info.properties)}")
        print(f"Definitions: {len(info.definitions)}")
        
        print_subheader("Sample Data")
        sample = processor.generate_samples(count=1)[0]
        sample_str = json.dumps(sample, indent=2, default=str)
        print(sample_str[:1000])
        if len(sample_str) > 1000:
            print("... (truncated)")


def main():
    """Run all demonstrations."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                     JsonSchemaCodeGen v{version}                      ║
║                                                                  ║
║  Commercial Grade JSON Schema to Python Code Generator           ║
║                                                                  ║
║  Copyright © 2025-2030, All Rights Reserved                      ║
║  Ashutosh Sinha (ajsinha@gmail.com)                              ║
╚══════════════════════════════════════════════════════════════════╝
""".format(version=__version__))
    
    print("This script demonstrates the key features of JsonSchemaCodeGen.\n")
    
    try:
        demo_basic_usage()
        demo_complex_schema()
        demo_pydantic_generation()
        demo_validation()
        demo_file_schemas()
        
        print_header("DEMONSTRATION COMPLETE")
        print("For more information, see the README.md file.")
        print("For CLI usage: python -m jsonschemacodegen --help")
        print("\nCopyright © 2025-2030, Ashutosh Sinha. All Rights Reserved.")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
