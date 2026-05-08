# Gemini Skill Toolkit

**Version 1.0.0 · AI Agent Engineering · Multi-Platform Interoperability**

The **Gemini Skill Toolkit** is an advanced, industrial-grade suite of tools designed for the creation, validation, and cross-platform migration of AI agent skills. Built specifically for Elton Boehnen's **Gemini CLI** ecosystem, it enables developers to build high-performance, modular skills that are fully compliant with the **2026 Engineering Mandates**.

## Author Information
- **Name:** Elton Boehnen
- **Email:** [boehnenelton2024@gmail.com](mailto:boehnenelton2024@gmail.com)
- **GitHub:** [https://github.com/boehnenelton/](https://github.com/boehnenelton/)
- **Website:** [https://boehnenelton2024.pages.dev](https://boehnenelton2024.pages.dev)

## Core Utility Arsenal
The toolkit is organized into specialized functional zones:

### 1. Master Skill Converter
The flagship orchestration tool for porting AI capabilities between major ecosystems:
- **`detect_platform.py`**: Cryptographically-sound marker detection for Claude, Codex, and Qwen skills.
- **Conversion Kits**: Specialized logic for transforming proprietary manifests into standardized `SKILL.md` frontmatter.
- **Interoperability Bridge**: Leverages `conversion_map.bejson` to enforce positional integrity during the translation process.

### 2. Validation Engine (`validator.py`)
A rigorous QA tool that verifies skills against Elton Boehnen's authoritative **Gemini Skill Schema**:
- **Type Safety**: Enforces strict data types (string, boolean, array, object, integer) for all manifest fields.
- **Structural Auditing**: Ensures required directory hierarchies (e.g., `scripts/`) and mandatory fields are present.
- **Nomenclature Checks**: Identifies deprecated fields (like `capabilities`) and enforces 2026-standard key names (`allowed_tools`).

### 3. Integrated Skills
The repository serves as a live development environment, including:
- **`chunker`**: A BEJSON-native project serialization skill.
- **`mock_codex_skill`**: A sandbox environment for testing translation and validation patterns.

## Technical Specifications
- **Language:** Python 3.10+
- **Data Compliance:** BEJSON 104a (Schema), MFDB v1.3.1 (Workspace)
- **Configuration:** YAML Frontmatter + Markdown Body
- **Standards:** Strictly compliant with Elton Boehnen's **Modular AI Certification (Level 3)**.

## Usage Guide
### Validating a Local Skill
```bash
python3 skills/master-skill-converter/scripts/validator.py ./path_to_my_skill
```
### Converting a Legacy Claude Skill
```bash
python3 cli-tools/claude-to-gem_cli.py ./path_to_claude_skill
```

## License
Created and maintained by Elton Boehnen. All rights reserved.
