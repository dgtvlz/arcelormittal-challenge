#!/bin/bash

while IFS= read -r line; do
    trimmed_line=$(echo "$line" | xargs)
    paths+=( "$trimmed_line" )
done < "available_files.txt"

#paths=(
#"data/2023/11/27/09027.json"
#"data/2023/11/27/09029.json"
#"data/2023/11/27/09043.json"
#"data/2023/11/27/09034.json"
#"data/2023/11/27/09050.json"
#)

total_paths=${#paths[@]}

for ((i=0; i<${total_paths}; i++)); do
    path="${paths[$i]}"
    python3 "src/client.py" "$path"
    echo "Progress: $(( (i + 1) * 100 / total_paths ))%"
done