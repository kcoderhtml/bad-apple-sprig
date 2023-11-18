#!/bin/bash

# Default values
input_dir=""
output_dir=""
remove_original=false

# Function to print usage
print_usage() {
  echo "Usage: $0 -i <input_directory> -o <output_directory> [-r]"
  echo "Options:"
  echo "  -i <input_directory>    Input directory containing images"
  echo "  -o <output_directory>   Output directory for converted images"
  echo "  -r                      Remove original files after conversion (optional)"
  exit 1
}

# Function to display a progress bar
progress_bar() {
  local progress current total width filename

  # Assign values to variables
  current=$1
  total=$2
  width=50
  filename=$3

  # Calculate progress
  progress=$((current * 100 / total))

  # Display the progress bar and file name
  printf "[%-*s] %d%% - %s\r" "$width" "$(printf '=%.0s' $(seq 1 $((width * progress / 100))))" "$progress" "$filename"
}

# Parse command line options
while getopts ":i:o:r" opt; do
  case $opt in
    i)
      input_dir="$OPTARG"
      ;;
    o)
      output_dir="$OPTARG"
      ;;
    r)
      remove_original=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      print_usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      print_usage
      ;;
  esac
done

# Check if required options are provided
if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
  echo "Error: Input and output directories are required."
  print_usage
fi

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Find all JPEG and PNG files in the input directory
file_list=($(find "$input_dir" -type f \( -iname \*.jpg -o -iname \*.jpeg -o -iname \*.png \)))
total_files=${#file_list[@]}

# Process each file
for ((i = 0; i < total_files; i++)); do
  file="${file_list[i]}"
  # Get the file name without extension
  filename=$(basename "$file" | sed 's/\.[^\.]*$//')

  # Convert the image to black and white BMP and resize to 24x18 pixels
  convert "$file" -colorspace Gray -resize 24x18 -depth 1 "$output_dir/$filename.bmp"

  # Optional: If you want to remove the original file after conversion
  if [ "$remove_original" = true ]; then
    rm "$file"
  fi

  # Display the progress bar with the file name
  progress_bar "$((i + 1))" "$total_files" "$filename"
done

echo -e "\nConversion complete."
