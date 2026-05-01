#!/usr/bin/env python3
import argparse
import os
import re
import yaml
from pathlib import Path

class ClaudeToGeminiConverter:
    def __init__(self, skill_path, dry_run=False):
        self.skill_path = Path(skill_path)
        self.dry_run = dry_run
        self.skill_md_path = self.skill_path / "SKILL.md"

    def log(self, message):
        print(f"[CLAUDE-CONVERTER] {message}")

    def normalize_yaml(self):
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
        if 'allowed-tools' in data:
            data['allowed_tools'] = data.pop('allowed-tools')
        
        if 'metadata' not in data:
            data['metadata'] = {}
        
        # Move Claude-specific keys to metadata
        claude_keys = ['invocation-policy', 'model-preference']
        for key in claude_keys:
            if key in data:
                data['metadata'][key] = data.pop(key)
        
        # Ensure mcpServers exists for the extractor to use later
        if 'mcpServers' not in data:
            data['mcpServers'] = []

        new_yaml = yaml.dump(data, sort_keys=False)
        new_content = f"---\n{new_yaml}---\n{body_content}"

        if not self.dry_run:
            with open(self.skill_md_path, 'w') as f:
                f.write(new_content)
            self.log("Normalized YAML keys in SKILL.md")
        else:
            self.log("[DRY RUN] Would normalize YAML keys in SKILL.md")

    def patch_context(self):
        if not self.skill_md_path.exists():
            return

        with open(self.skill_md_path, 'r') as f:
            content = f.read()

        # Context swaps
        replacements = [
            (r'CLAUDE\.md', r'GEMINI.md'),
            (r'Claude Code', r'Gemini CLI'),
            (r'Anthropic', r'Google'),
            (r'Claude 4\.7 Opus', r'Gemini 2.5 Pro'),
        ]

        new_content = content
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, new_content)

        if not self.dry_run:
            with open(self.skill_md_path, 'w') as f:
                f.write(new_content)
            self.log("Patched context references in SKILL.md")
        else:
            self.log("[DRY RUN] Would patch context references in SKILL.md")

    def extract_mcp(self):
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return

        discovered_servers = set()
        # Scan for FastMCP instantiations
        for script_file in scripts_dir.glob("*.[tp]y"): # .ts, .py (simplified to py for this python tool's detection)
            # Actually we should also check .ts if possible, but we'll stick to py/js/ts text scanning
            pass
        
        for ext in ["*.py", "*.ts", "*.js"]:
            for script_file in scripts_dir.glob(ext):
                with open(script_file, 'r', errors='ignore') as f:
                    content = f.read()
                    # Look for new FastMCP("ServerName") or FastMCP("ServerName")
                    matches = re.findall(r'FastMCP\([\'"](.+?)[\'"]\)', content)
                    for m in matches:
                        discovered_servers.add(m)

        if not discovered_servers:
            return

        self.log(f"Discovered MCP Servers: {list(discovered_servers)}")

        # Inject into YAML
        with open(self.skill_md_path, 'r') as f:
            content = f.read()
        
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            data = yaml.safe_load(match.group(1))
            body = content[match.end():]
            
            if 'mcpServers' not in data:
                data['mcpServers'] = []
            
            for s in discovered_servers:
                if s not in data['mcpServers']:
                    data['mcpServers'].append(s)
            
            new_yaml = yaml.dump(data, sort_keys=False)
            new_content = f"---\n{new_yaml}---\n{body}"

            if not self.dry_run:
                with open(self.skill_md_path, 'w') as f:
                    f.write(new_content)
                self.log(f"Injected {len(discovered_servers)} MCP servers into SKILL.md")

    def convert_all(self):
        self.log(f"Starting Claude-to-Gemini conversion for: {self.skill_path}")
        self.normalize_yaml()
        self.patch_context()
        self.extract_mcp()
        self.log("Conversion complete.")

def main():
    parser = argparse.ArgumentParser(description="Claude-to-Gemini Skill Converter")
    parser.add_argument("command", choices=["normalize-yaml", "patch-context", "extract-mcp", "convert-all"])
    parser.add_argument("skill_path", help="Path to the Claude skill directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run")

    args = parser.parse_args()
    converter = ClaudeToGeminiConverter(args.skill_path, dry_run=args.dry_run)

    if args.command == "normalize-yaml":
        converter.normalize_yaml()
    elif args.command == "patch-context":
        converter.patch_context()
    elif args.command == "extract-mcp":
        converter.extract_mcp()
    elif args.command == "convert-all":
        converter.convert_all()

if __name__ == "__main__":
    main()
