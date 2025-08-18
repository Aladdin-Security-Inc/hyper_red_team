import os
import csv
import argparse
import re

def convert_csv_to_markdown(directory):
    """
    Parses a prompts.csv file within a given directory and converts it into a
    review_generated.md file.
    """
    csv_file_path = os.path.join(directory, 'prompts.csv')
    md_file_path = os.path.join(directory, 'review_generated.md')
    base_category = os.path.basename(os.path.normpath(directory))

    if not os.path.exists(csv_file_path):
        print(f"Error: '{csv_file_path}' not found.")
        return

    print(f"Reading from '{csv_file_path}'...")

    rows = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            for row in reader:
                rows.append(row)
    except (IOError, StopIteration) as e:
        print(f"Error reading CSV file: {e}")
        return

    if not rows:
        print("No data found in CSV. Markdown file will not be created.")
        return

    # Start building the markdown content
    md_content = f"# Jailbreak Variations for: {base_category}\n\n"
    md_content += "This file was automatically generated from prompts.csv.\n\n"

    for i, row in enumerate(rows):
        try:
            category, initial_prompt, step1_response, step2_prompt = row
            
            # Extract persona from category like "Poisons - Novelist"
            persona_match = re.search(r' - (.*)$', category)
            persona = persona_match.group(1).strip() if persona_match else f"Variation {i+1}"

            md_content += "---\n\n"
            md_content += f"## Variation {i+1}: The {persona} Persona\n\n"
            
            md_content += "### 段階1: 初期プロンプト (initial_prompt)\n"
            md_content += f"> {initial_prompt}\n\n"
            
            md_content += "### 段階1.5: 想定されるモデルの応答 (step1_response_content)\n"
            md_content += f"{step1_response}\n\n"
            
            md_content += "### 段階2: 追撃プロンプト (step2_prompt)\n"
            md_content += f"> {step2_prompt}\n\n"

        except ValueError:
            print(f"Warning: Skipping row {i+1} due to incorrect number of columns.")
            continue

    # Write the markdown content to a file
    print(f"Writing {len(rows)} records to '{md_file_path}'...")
    try:
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print("Conversion successful.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a prompts.csv file to a review_generated.md file.')
    parser.add_argument('directory', type=str, help='The directory containing the prompts.csv file.')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
    else:
        convert_csv_to_markdown(args.directory)
