#!/usr/bin/env python3
import argparse
import json
import yaml
import sys
from pathlib import Path

class GeminiSkillValidator:
    def __init__(self, schema_path):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        self.fields = {f['field_name']: f for f in self._parse_fields()}

    def _parse_fields(self):
        field_defs = []
        headers = self.schema['Fields']
        for row in self.schema['Values']:
            field_defs.append(dict(zip([h['name'] for h in headers], row)))
        return field_defs

    def validate_type(self, val, expected_type):
        if expected_type == "string": return isinstance(val, str)
        if expected_type == "boolean": return isinstance(val, bool)
        if expected_type == "array": return isinstance(val, list)
        if expected_type == "object": return isinstance(val, dict)
        if expected_type == "integer": return isinstance(val, int)
        return True

    def validate(self, skill_dir):
        skill_dir = Path(skill_dir)
        skill_md = skill_dir / "SKILL.md"
        
        if not skill_md.exists():
            print(f"FAILED: SKILL.md not found in {skill_dir}")
            return False

        with open(skill_md, 'r') as f:
            content = f.read()

        import re
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            print(f"FAILED: No YAML frontmatter in {skill_md}")
            return False

        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            print(f"FAILED: YAML parsing error: {e}")
            return False

        errors = []
        # Check required fields and types
        for name, info in self.fields.items():
            required = info.get('required', False)
            expected_type = info.get('type')
            
            if required and name not in data:
                errors.append(f"Missing required field: '{name}'")
            elif name in data and expected_type:
                if not self.validate_type(data[name], expected_type):
                    errors.append(f"Invalid type for '{name}': Expected {expected_type}, got {type(data[name]).__name__}")
            
        # Check for deprecated fields
        if 'capabilities' in data:
            errors.append("Deprecated field found: 'capabilities'. Use 'allowed_tools' instead.")

        # Check directory structure
        required_dirs = ["scripts"]
        for d in required_dirs:
            if not (skill_dir / d).exists():
                errors.append(f"Missing recommended directory: '{d}/'")

        if errors:
            print(f"Validation FAILED for {data.get('name', 'unnamed')}:")
            for err in errors:
                print(f"  - {err}")
            return False
        
        print(f"SUCCESS: Skill '{data.get('name')}' is valid for Gemini CLI.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Gemini Skill Validator v1.1")
    parser.add_argument("skill_path", help="Path to the Gemini skill directory")
    parser.add_argument("--schema", help="Path to the BEJSON schema")
    
    args = parser.parse_args()
    
    # Default schema path logic
    schema_path = args.schema
    if not schema_path:
        # Try to find it in references/ relative to the script
        potential_path = Path(__file__).parent.parent / "references" / "gemini_skill_schema.bejson"
        if potential_path.exists():
            schema_path = str(potential_path)
        else:
            print("Error: Schema path not provided and not found in default location.")
            sys.exit(1)

    validator = GeminiSkillValidator(schema_path)
    if not validator.validate(args.skill_path):
        sys.exit(1)

if __name__ == "__main__":
    main()
