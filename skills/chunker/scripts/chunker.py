#!/usr/bin/env python3
import argparse
import os
import json
from pathlib import Path

class Chunker:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def log(self, message):
        print(f"[CHUNKER] {message}")

    def chunk_file(self, file_path, chunk_size_kb, output_dir=None):
        file_path = Path(file_path)
        if not file_path.exists():
            self.log(f"Error: {file_path} does not exist.")
            return

        chunk_size = chunk_size_kb * 1024
        if output_dir is None:
            output_dir = file_path.parent / f"{file_path.name}_chunks"
        else:
            output_dir = Path(output_dir)

        if not self.dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        self.log(f"Chunking {file_path} into {chunk_size_kb}KB segments...")
        
        manifest = {
            "original_filename": file_path.name,
            "chunk_size_kb": chunk_size_kb,
            "chunks": []
        }

        with open(file_path, 'rb') as f:
            chunk_num = 0
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                
                chunk_name = f"{file_path.name}.part{chunk_num:03}"
                chunk_path = output_dir / chunk_name
                
                if not self.dry_run:
                    with open(chunk_path, 'wb') as cf:
                        cf.write(data)
                
                manifest["chunks"].append(chunk_name)
                chunk_num += 1

        if not self.dry_run:
            with open(output_dir / "manifest.json", 'w') as mf:
                json.dump(manifest, mf, indent=2)
            self.log(f"Created {len(manifest['chunks'])} chunks in {output_dir}")
        else:
            self.log(f"[DRY RUN] Would create {len(manifest['chunks'])} chunks in {output_dir}")

    def unchunk_file(self, chunk_dir, output_file=None):
        chunk_dir = Path(chunk_dir)
        manifest_path = chunk_dir / "manifest.json"
        
        if not manifest_path.exists():
            self.log(f"Error: Manifest not found in {chunk_dir}")
            return

        with open(manifest_path, 'r') as mf:
            manifest = json.load(mf)

        if output_file is None:
            output_file = chunk_dir.parent / f"restored_{manifest['original_filename']}"
        else:
            output_file = Path(output_file)

        self.log(f"Reconstructing {manifest['original_filename']} from {len(manifest['chunks'])} chunks...")

        if not self.dry_run:
            with open(output_file, 'wb') as f:
                for chunk_name in manifest['chunks']:
                    chunk_path = chunk_dir / chunk_name
                    if not chunk_path.exists():
                        self.log(f"Error: Missing chunk {chunk_name}")
                        return
                    with open(chunk_path, 'rb') as cf:
                        f.write(cf.read())
            self.log(f"Successfully reconstructed file at {output_file}")
        else:
            self.log(f"[DRY RUN] Would reconstruct file at {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Large File Chunker/Unchunker")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Chunk command
    chunk_parser = subparsers.add_parser("chunk", help="Split a file into chunks")
    chunk_parser.add_argument("file", help="File to split")
    chunk_parser.add_argument("--size", type=int, default=512, help="Chunk size in KB (default: 512)")
    chunk_parser.add_argument("--out", help="Output directory for chunks")

    # Unchunk command
    unchunk_parser = subparsers.add_parser("unchunk", help="Merge chunks back into a file")
    unchunk_parser.add_argument("dir", help="Directory containing chunks and manifest.json")
    unchunk_parser.add_argument("--out", help="Path for the reconstructed file")

    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run")

    args = parser.parse_args()
    chunker = Chunker(dry_run=args.dry_run)

    if args.command == "chunk":
        chunker.chunk_file(args.file, args.size, args.out)
    elif args.command == "unchunk":
        chunker.unchunk_file(args.dir, args.out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
