---
name: codex-to-gemini-converter
description: |
  Master skill for transforming OpenAI Codex skills (2026 standard) into Gemini CLI skills.
  Triggers: "convert codex skill", "migrate openai skill", "scaffold gemini skill from codex".
allowed_tools:
  - run_shell_command
  - read_file
  - write_file
  - list_directory
metadata:
  version: "1.0.0"
  target_platform: "Gemini CLI"
  source_platform: "OpenAI Codex"
  tool_path: "./codex-to-gem_cli.py"
---

# Codex to Gemini Conversion Playbook

This skill automates the migration of legacy or current OpenAI Codex (2026) skills into the Gemini CLI ecosystem. It utilizes the `codex-to-gem_cli.py` Python utility to handle structural, manifest, and tool-level transformations.

## Conversion Philosophy
1. **Safety First**: Always run with `--dry-run` initially to verify planned changes.
2. **Context Preservation**: Retain original compatibility notes and metadata in the `metadata` block.
3. **Surgical Patching**: Only replace brand-specific terms (OpenAI, GPT-5.5) and command syntax (`$.` -> `/`).

## Reference Materials
- **[BEJSON_CRASH_COURSE.md](./BEJSON_CRASH_COURSE.md)**: Essential guide for understanding the structured mapping files.
- **[conversion_map.bejson](./conversion_map.bejson)**: The technical Rosetta Stone for Codex-to-Gemini transformations.

## Usage Instructions

### 1. Initial Assessment
List the contents of the target Codex skill to ensure it follows the standard structure (`SKILL.md`, `lib/`, `agents/`).
```bash
ls -R <path_to_codex_skill>
```

### 2. Full Conversion
Run the master conversion command. This will morph the manifest, patch the prompt instructions, shift directories, and bridge Python tools.
```bash
python3 codex-to-gem_cli.py convert-all <path_to_codex_skill>
```

### 3. Granular Execution
If specific parts of the skill need manual oversight, use the subcommands:
- `morph-manifest`: Only update `SKILL.md` frontmatter.
- `patch-prompt`: Only replace text/syntax in `SKILL.md` body.
- `shift-dirs`: Only reorganize the folder structure.
- `bridge-tools`: Only convert `@openai.tool()` Python scripts.

## Post-Conversion Checklist
- [ ] Verify `SKILL.md` YAML is valid.
- [ ] Ensure all scripts in `scripts/` are executable.
- [ ] Test the bridged tools using `python3 scripts/tool_name.py --args '{"key": "value"}'`.
- [ ] Update the `allowed_tools` list in the new `SKILL.md` if additional Gemini-native tools are needed.

## Tool Documentation: `codex-to-gem_cli.py`
The underlying tool handles the "heavy lifting" of AST manipulation and regex patching. It requires `pyyaml` and Python 3.9+.

### Arguments:
- `command`: The specific conversion step to run.
- `skill_path`: The directory of the skill to be converted.
- `--dry-run`: (Optional) Log actions without modifying the filesystem.
