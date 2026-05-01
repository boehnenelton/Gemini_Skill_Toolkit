---
name: claude-to-gemini-converter
description: |
  Master skill for transforming Anthropic Claude Code skills (2026 standard) into Gemini CLI skills.
  Triggers: "convert claude skill", "migrate anthropic skill", "scaffold gemini skill from claude".
allowed_tools:
  - run_shell_command
  - read_file
  - write_file
  - list_directory
metadata:
  version: "1.0.0"
  target_platform: "Gemini CLI"
  source_platform: "Claude Code"
  tool_path: "./claude-to-gem_cli.py"
---

# Claude to Gemini Conversion Playbook

This skill manages the transition from Anthropic's Claude Code ecosystem to the Google Gemini CLI. While both platforms share the Agent Skills Open Standard and MCP, subtle syntactical differences exist that this kit automates.

## Conversion Strategy
1. **Structural Alignment**: Claude's directory structure is already compatible; the focus is on YAML and context references.
2. **MCP Continuity**: Claude's FastMCP servers are natively supported by Gemini. This tool automatically discovers and registers them.
3. **Context Mapping**: Swaps `CLAUDE.md` logic for `GEMINI.md`.

## Reference Materials
- **[BEJSON_CRASH_COURSE.md](./BEJSON_CRASH_COURSE.md)**: Essential guide for understanding the structured mapping files.
- **[conversion_map.bejson](./conversion_map.bejson)**: The technical Rosetta Stone for Claude-to-Gemini transformations.

## Usage Instructions

### 1. Initial Assessment
Review the Claude skill for any "Routines" or Anthropic-specific ephemeral configurations.
```bash
ls -R <path_to_claude_skill>
```

### 2. Full Conversion
Execute the pipeline to normalize YAML, patch context, and extract MCP servers.
```bash
python3 claude-to-gem_cli.py convert-all <path_to_claude_skill>
```

### 3. Verification
Verify that the `mcpServers` list in the new `SKILL.md` matches the servers found in `scripts/`.
```bash
grep "mcpServers" <path_to_claude_skill>/SKILL.md
```

## AI Assistance Requirement
If the conversion tool logs an error or if the skill relies on "Claude Routines," utilize the following prompt with Gemini:
> "I am converting a Claude Routine to a Gemini Subagent. Here is the Claude Routine logic: [PASTE LOGIC]. Rewrite this as a Gemini `AGENT.md` configuration."

## Tool Documentation: `claude-to-gem_cli.py`
This tool automates the "boring" parts of the migration:
- `normalize-yaml`: `allowed-tools` -> `allowed_tools`.
- `patch-context`: `CLAUDE.md` -> `GEMINI.md`.
- `extract-mcp`: Scans for `FastMCP` and updates the YAML frontmatter.
