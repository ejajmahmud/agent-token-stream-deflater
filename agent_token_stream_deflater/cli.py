"""CLI for Token Stream Deflater."""
import argparse
from .core import TokenStreamDeflater, TokenStreamInflater

def main():
    parser = argparse.ArgumentParser(description="Agent Token Stream Deflater CLI")
    parser.add_argument("--demo", action="store_true", help="Run compression demo")
    args = parser.parse_args()

    deflater = TokenStreamDeflater()
    sample = "autonomous agent tool execution autonomous agent protocol response"
    compressed = deflater.compress_chunk(sample)
    print(f"Original size: {len(sample)} bytes -> Compressed: {len(compressed)} bytes")

    inflater = TokenStreamInflater()
    decompressed = inflater.decompress_chunk(compressed)
    print("Reconstituted text:", decompressed)

if __name__ == "__main__":
    main()
