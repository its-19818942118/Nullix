#!/usr/bin/env bash

# Cycle through all .sh, .zsh, .zshrc, .py, .md, .conf, .kvconfig, .svg, .css, .dcol, .theme, .json, .jsonc, .lst, .t1, .t2 and .t3 files in the current directory and all its subdirectories
find . \( -name "*.sh" -o -name "*.zsh" -o -name "*.zshrc" -o -name "*.py" -o -name "*.md" -o -name "*.conf" -o -name "*.kvconfig" -o -name "*.svg" -o -name "*.css" -o -name "*.dcol" -o -name "*.theme" -o -name "*.json" -o -name "*.jsonc" -o -name "*.lst" -o -name "*.t1" -o -name "*.t2" -o -name "*.t3" \) -type f | while read -r file; do
    # CR (Carriage Return) removal and overwrite
    tr -d '\r' <"$file" >temp_file && mv temp_file "$file"

    # Files with the extension .sh, .zsh, .zshrc and .py have the executable permission
    if [[ "${file##*.}" = "sh" || "${file##*.}" = "zsh" || "${file##*.}" = "zshrc" || "${file##*.}" = "py" ]]; then
        chmod +x "$file"
        echo "Set executable permission: $file"
    fi

    echo "Processed: $file"
done

echo "All given files have been processed."