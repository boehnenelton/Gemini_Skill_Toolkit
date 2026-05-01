#!/usr/bin/env python3
import sys
from pathlib import Path

def detect_platform(skill_path):
    path = Path(skill_path)
    
    # Platform markers
    markers = {
        "Claude": ["CLAUDE.md", "claude_config.json"],
        "Codex": ["agents/openai.yaml", "codex.yaml"],
        "Qwen": ["QWEN.md", "qwen_config.json"]
    }
    
    # Check for markers
    for platform, files in markers.items():
        for f in files:
            if (path / f).exists():
                return platform
                
    # Check content of SKILL.md if it exists
    skill_md = path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        if "allowed-tools" in content: return "Claude"
        if "$." in content: return "Codex"
        if "expert_routing_preference" in content: return "Qwen"
        
    return "Unknown"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: detect_platform.py <skill_path>")
        sys.exit(1)
        
    platform = detect_platform(sys.argv[1])
    print(platform)
