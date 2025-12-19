#!/usr/bin/env bash
# this is mostly vibe-coded
# Usage: ./remove_bg.sh input_folder output_folder

set -e

INPUT_DIR="$1"
OUTPUT_DIR="$2"

# Check arguments
if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "Usage: $0 <input_folder> <output_folder>"
  exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Process each PNG file
for file in "$INPUT_DIR"/*.png; do
  # Skip if no files match
  [ -e "$file" ] || continue

  filename=$(basename "$file")
  output="$OUTPUT_DIR/$filename"

  echo "Processing: $filename"

  convert "$file" \
    -fuzz 10% \
    -transparent white \
    "$output"
done

echo "Done."
