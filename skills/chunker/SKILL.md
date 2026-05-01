---
name: file-chunker
description: |
  Specialized skill for splitting large files into smaller chunks and merging them back.
  Triggers: "chunk file", "split large file", "merge chunks", "reconstruct file from parts".
allowed_tools:
  - run_shell_command
  - list_directory
metadata:
  version: "1.0.0"
  tool_path: "./scripts/chunker.py"
---

# File Chunker & Unchunker Playbook

This skill provides a robust utility for managing files that are too large for standard context windows or need to be processed in segments. It uses a manifest-based system to ensure data integrity during reconstruction.

## Procedures

### 1. Chunking a File
Split a large file into smaller pieces. By default, it creates chunks of 512KB.
```bash
python3 scripts/chunker.py chunk <path_to_large_file> --size <size_in_kb>
```
*A new directory named `<filename>_chunks/` will be created containing the parts and a `manifest.json`.*

### 2. Unchunking (Reconstructing) a File
Merge parts back into the original file using the manifest.
```bash
python3 scripts/chunker.py unchunk <path_to_chunks_directory>
```
*The reconstructed file will be saved as `restored_<original_filename>` in the parent directory of the chunks.*

## Best Practices
- **Manifest Integrity**: Never delete or modify the `manifest.json` file inside the chunks directory; it is required for reconstruction.
- **Verification**: Always verify the size/hash of the reconstructed file against the original if possible.
- **Context Management**: Use this skill when a file is >500KB to ensure the Gemini CLI can process it effectively.
