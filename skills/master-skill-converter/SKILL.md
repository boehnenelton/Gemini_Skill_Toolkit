---
name: master-skill-converter
description: |
  The unified entry point for converting skills from Codex, Claude Code, and Qwen-Coder into the Gemini CLI standard.
  Triggers: "convert any skill", "start conversion toolkit", "identify skill platform".
allowed_tools:
  - run_shell_command
  - list_directory
  - read_file
metadata:
  version: "1.1.0"
  toolkit_root: "/storage/emulated/0/dev/strategy/deep_research_2026/reports/cli_converter"
---

# Universal AI Skill Conversion Toolkit (v1.1)

This toolkit migrates specialized AI skills from Codex, Claude Code, and Qwen-Coder into the Gemini CLI standard.

## Toolkit Structure
- **`scripts/`**: Core logic including platform detection and validation.
- **`references/`**: Technical mapping data and schema definitions.
- **`scripts/claude_kit/`**, **`scripts/codex_kit/`**, **`scripts/qwen_kit/`**: Specialist transformation scripts.

## Universal Conversion Workflow

### Step 1: Platform Identification
Run the detector to identify the source platform.
```bash
python3 scripts/detect_platform.py <path_to_target_skill>
```

### Step 2: Invoke Specialist Kit
Run the appropriate converter based on the detection result.
```bash
# Example for Claude
python3 scripts/claude_kit/claude-to-gem_cli.py convert-all <path_to_skill>
```

### Step 3: Validation
Enforce the **Gemini Agent Skills Open Standard** using the enhanced validator.
```bash
python3 scripts/validator.py <path_to_converted_skill>
```

## Progressive Disclosure References
- **[BEJSON_CRASH_COURSE.md](references/BEJSON_CRASH_COURSE.md)**: Logic behind the mapping format.
- **[conversion_map.bejson](references/conversion_map.bejson)**: The master Rosetta Stone.
- **[gemini_skill_schema.bejson](references/gemini_skill_schema.bejson)**: The formal validation schema.

## Best Practices
- **Lean Context**: Use references only when necessary.
- **Validation First**: Never install a skill without running the validator.
- **Agentic Output**: Scripts are optimized for LLM readability.
