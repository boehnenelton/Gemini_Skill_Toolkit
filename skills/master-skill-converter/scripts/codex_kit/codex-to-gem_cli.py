#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import ast
import yaml
from pathlib import Path

class CodexToGeminiConverter:
    def __init__(self, skill_path, dry_run=False):
        self.skill_path = Path(skill_path)
        self.dry_run = dry_run
        self.skill_md_path = self.skill_path / "SKILL.md"

    def log(self, message):
        print(f"[CONVERTER] {message}")

    def morph_manifest(self):
        if not self.skill_md_path.exists():
            self.log("SKILL.md not found, skipping manifest morph.")
            return

        with open(self.skill_md_path, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            self.log("No frontmatter found in SKILL.md.")
            return

        yaml_content = match.group(1)
        body_content = content[match.end():]
        
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as exc:
            self.log(f"Error parsing YAML: {exc}")
            return

        # Transformation Logic
        new_data = {
            "name": data.get("name", "unnamed-skill"),
            "description": data.get("description", ""),
            "allowed_tools": data.get("capabilities", []),
            "metadata": data.get("metadata", {})
        }
        
        # Add Gemini specific defaults or mapped values
        if "compatibility" in data:
            new_data["metadata"]["original_compatibility"] = data["compatibility"]
        
        new_yaml = yaml.dump(new_data, sort_keys=False)
        new_content = f"---\n{new_yaml}---\n{body_content}"

        if not self.dry_run:
            with open(self.skill_md_path, 'w') as f:
                f.write(new_content)
            self.log("Successfully morphed manifest in SKILL.md")
        else:
            self.log("[DRY RUN] Would morph manifest in SKILL.md")

    def patch_prompt(self):
        if not self.skill_md_path.exists():
            return

        with open(self.skill_md_path, 'r') as f:
            content = f.read()

        # Regex replacements
        replacements = [
            (r'\$\.([a-zA-Z0-9_-]+)', r'/\1'), # $.command -> /command
            (r'OpenAI Codex', r'Gemini CLI'),
            (r'GPT-5\.5', r'Gemini 2.5 Pro'),
            (r'Aardvark Security', r'Gemini Safety Framework'),
            (r'openai\.yaml', r'GEMINI.md'),
        ]

        new_content = content
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, new_content)

        if not self.dry_run:
            with open(self.skill_md_path, 'w') as f:
                f.write(new_content)
            self.log("Successfully patched prompt instructions in SKILL.md")
        else:
            self.log("[DRY RUN] Would patch prompt instructions in SKILL.md")

    def shift_dirs(self):
        mapping = {
            "lib": "scripts",
            "bin": "scripts",
            "ref": "references"
        }

        for old, new in mapping.items():
            old_path = self.skill_path / old
            new_path = self.skill_path / new
            
            if old_path.exists() and old_path.is_dir():
                if not self.dry_run:
                    if new_path.exists():
                        # Merge contents
                        for item in old_path.iterdir():
                            shutil.move(str(item), str(new_path))
                        shutil.rmtree(old_path)
                    else:
                        old_path.rename(new_path)
                    self.log(f"Shifted {old}/ to {new}/")
                else:
                    self.log(f"[DRY RUN] Would shift {old}/ to {new}/")

        # Cleanup Codex specific files
        openai_yaml = self.skill_path / "agents" / "openai.yaml"
        if openai_yaml.exists():
            if not self.dry_run:
                openai_yaml.unlink()
                self.log("Removed agents/openai.yaml")
                # Remove agents dir if empty
                try:
                    os.rmdir(self.skill_path / "agents")
                except OSError:
                    pass
            else:
                self.log("[DRY RUN] Would remove agents/openai.yaml")

    def bridge_tools(self):
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return

        for py_file in scripts_dir.glob("*.py"):
            self.log(f"Processing tool: {py_file.name}")
            with open(py_file, 'r') as f:
                tree = ast.parse(f.read())

            modified = False
            new_body = []
            tool_functions = []

            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    # Check for @openai.tool()
                    is_tool = False
                    new_decorator_list = []
                    for decorator in node.decorator_list:
                        if (isinstance(decorator, ast.Call) and 
                            isinstance(decorator.func, ast.Attribute) and 
                            decorator.func.attr == 'tool' and 
                            isinstance(decorator.func.value, ast.Name) and 
                            decorator.func.value.id == 'openai'):
                            is_tool = True
                            modified = True
                        else:
                            new_decorator_list.append(decorator)
                    
                    if is_tool:
                        node.decorator_list = new_decorator_list
                        tool_functions.append(node.name)
                
                new_body.append(node)

            if modified:
                # Add argparse bridge at the end
                bridge_code = self._generate_bridge(tool_functions)
                bridge_ast = ast.parse(bridge_code)
                new_body.extend(bridge_ast.body)
                tree.body = new_body

                if not self.dry_run:
                    try:
                        new_source = ast.unparse(tree)
                    except AttributeError:
                        self.log("ast.unparse not available, skipping AST write. (Requires Python 3.9+)")
                        continue
                    
                    with open(py_file, 'w') as f:
                        f.write(new_source)
                    self.log(f"Bridged tool logic in {py_file.name}")
                else:
                    self.log(f"[DRY RUN] Would bridge tool logic in {py_file.name}")

    def _generate_bridge(self, func_names):
        if not func_names: return ""
        # Simplified bridge for the first tool found
        name = func_names[0]
        return f"""
if __name__ == "__main__":
    import argparse
    import json
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--args', type=str, help='JSON string of arguments')
    args = parser.parse_args()
    try:
        kwargs = json.loads(args.args) if args.args else {{}}
        result = {name}(**kwargs)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error executing {name}: {{e}}", file=sys.stderr)
        sys.exit(1)
"""

    def convert_all(self):
        self.log(f"Starting conversion for: {self.skill_path}")
        self.morph_manifest()
        self.patch_prompt()
        self.shift_dirs()
        self.bridge_tools()
        self.log("Conversion complete.")

def main():
    parser = argparse.ArgumentParser(description="Codex-to-Gemini Skill Converter")
    parser.add_argument("command", choices=["morph-manifest", "patch-prompt", "shift-dirs", "bridge-tools", "convert-all"])
    parser.add_argument("skill_path", help="Path to the Codex skill directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without modifying files")

    args = parser.parse_args()
    converter = CodexToGeminiConverter(args.skill_path, dry_run=args.dry_run)

    if args.command == "morph-manifest":
        converter.morph_manifest()
    elif args.command == "patch-prompt":
        converter.patch_prompt()
    elif args.command == "shift-dirs":
        converter.shift_dirs()
    elif args.command == "bridge-tools":
        converter.bridge_tools()
    elif args.command == "convert-all":
        converter.convert_all()

if __name__ == "__main__":
    main()
