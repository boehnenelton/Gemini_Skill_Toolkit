#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import yaml
from pathlib import Path

class QwenToGeminiConverter:
    def __init__(self, skill_path, dry_run=False):
        self.skill_path = Path(skill_path)
        self.dry_run = dry_run
        self.skill_md_path = self.skill_path / "SKILL.md"

    def log(self, message):
        print(f"[QWEN-CONVERTER] {message}")

    def morph_manifest(self):
        if not self.skill_md_path.exists():
            self.log("SKILL.md not found.")
            return

        with open(self.skill_md_path, 'r') as f:
            content = f.read()

        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            self.log("No frontmatter found.")
            return

        yaml_content = match.group(1)
        body_content = content[match.end():]
        
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as exc:
            self.log(f"Error parsing YAML: {exc}")
            return

        # Normalization logic
        if 'tools' in data:
            data['allowed_tools'] = data.pop('tools')
        
        if 'metadata' not in data:
            data['metadata'] = {}
        
        # Capture Qwen-specific routing keys
        qwen_keys = ['model_hint', 'expert_routing_preference', 'trajectory_version']
        qwen_legacy = {}
        for key in qwen_keys:
            if key in data:
                qwen_legacy[key] = data.pop(key)
        
        if qwen_legacy:
            data['metadata']['qwen_legacy'] = qwen_legacy

        new_yaml = yaml.dump(data, sort_keys=False)
        new_content = f"---\n{new_yaml}---\n{body_content}"

        if not self.dry_run:
            with open(self.skill_md_path, 'w') as f:
                f.write(new_content)
            self.log("Morphed Qwen manifest in SKILL.md")
        else:
            self.log("[DRY RUN] Would morph Qwen manifest in SKILL.md")

    def patch_context(self):
        if not self.skill_md_path.exists():
            return

        with open(self.skill_md_path, 'r') as f:
            content = f.read()

        # Context swaps
        replacements = [
            (r'QWEN\.md', r'GEMINI.md'),
            (r'Qwen-Coder', r'Gemini CLI'),
            (r'QwenClient', r'GeminiClient'),
            (r'Alibaba', r'Google'),
            (r'Trajectory Phase', r'Execution Step'),
        ]

        new_content = content
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, new_content)

        if not self.dry_run:
            with open(self.skill_md_path, 'w') as f:
                f.write(new_content)
            self.log("Patched Qwen context references in SKILL.md")
        else:
            self.log("[DRY RUN] Would patch Qwen context references in SKILL.md")

    def clean_dirs(self):
        # Remove .qwen directories if they exist in the skill root
        qwen_internal = self.skill_path / ".qwen"
        if qwen_internal.exists() and qwen_internal.is_dir():
            if not self.dry_run:
                shutil.rmtree(qwen_internal)
                self.log("Removed .qwen/ internal metadata.")
            else:
                self.log("[DRY RUN] Would remove .qwen/ internal metadata.")

    def convert_all(self):
        self.log(f"Starting Qwen-to-Gemini conversion for: {self.skill_path}")
        self.morph_manifest()
        self.patch_context()
        self.clean_dirs()
        self.log("Conversion complete.")

def main():
    parser = argparse.ArgumentParser(description="Qwen-to-Gemini Skill Converter")
    parser.add_argument("command", choices=["morph-manifest", "patch-context", "clean-dirs", "convert-all"])
    parser.add_argument("skill_path", help="Path to the Qwen skill directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run")

    args = parser.parse_args()
    converter = QwenToGeminiConverter(args.skill_path, dry_run=args.dry_run)

    if args.command == "morph-manifest":
        converter.morph_manifest()
    elif args.command == "patch-context":
        converter.patch_context()
    elif args.command == "clean-dirs":
        converter.clean_dirs()
    elif args.command == "convert-all":
        converter.convert_all()

if __name__ == "__main__":
    main()
