---
name: qwen-to-gemini-converter
description: |
  Master skill for transforming Alibaba Qwen-Coder skills (2026 standard) into Gemini CLI skills.
  Triggers: "convert qwen skill", "migrate alibaba skill", "scaffold gemini skill from qwen".
allowed_tools:
  - run_shell_command
  - read_file
  - write_file
  - list_directory
metadata:
  version: "1.0.0"
  target_platform: "Gemini CLI"
  source_platform: "Qwen-Coder"
  tool_path: "./qwen-to-gem_cli.py"
---

# Qwen to Gemini Conversion Playbook

This skill automates the migration of local-first Qwen-Coder skills into the Gemini CLI ecosystem. Qwen-Coder skills often focus on specific neural "Experts" and "Trajectories," which this kit translates into Gemini-compatible metadata and instructions.

## Conversion Philosophy
1. **Expert Preservation**: Qwen's Mixture-of-Experts (MoE) routing preferences are preserved in the `metadata.qwen_legacy` block to inform future model routing in Gemini.
2. **Context Migration**: Replaces the local-centric `QWEN.md` references with repo-wide `GEMINI.md` standards.
3. **Trajectory Normalization**: Converts Qwen's "Trajectory Phases" into Gemini's "Execution Steps" for better readability.

## Reference Materials
- **[BEJSON_CRASH_COURSE.md](./BEJSON_CRASH_COURSE.md)**: Essential guide for understanding the structured mapping files.
- **[conversion_map.bejson](./conversion_map.bejson)**: The technical Rosetta Stone for Qwen-to-Gemini transformations.

## Usage Instructions

### 1. Initial Assessment
Check for `.qwen/` metadata folders or trajectory files that might contain local state.
```bash
ls -a <path_to_qwen_skill>
```

### 2. Full Conversion
Run the conversion pipeline to morph the manifest, patch the instructions, and clean internal Qwen metadata.
```bash
python3 qwen-to-gem_cli.py convert-all <path_to_qwen_skill>
```

### 3. Verification
Verify that `tools` has been renamed to `allowed_tools` and that `expert_routing_preference` is correctly nested.
```bash
head -n 20 <path_to_qwen_skill>/SKILL.md
```

## AI Assistance Requirement
Qwen-Coder often uses specialized SDK calls for local sub-agent spawning. If the skill contains complex `SubAgent` class logic, use this prompt:
> "I am migrating a Qwen-Coder SubAgent logic to Gemini A2A. Here is the Qwen SDK code: [PASTE CODE]. Convert this to a standalone Gemini script that uses `argparse` and the standard Gemini Agent Skills format."

## Tool Documentation: `qwen-to-gem_cli.py`
Automates the following:
- `morph-manifest`: Renames `tools` to `allowed_tools` and moves MoE keys to metadata.
- `patch-context`: `QWEN.md` -> `GEMINI.md`.
- `clean-dirs`: Removes `.qwen/` metadata folders.
