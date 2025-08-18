import os
import csv
import re
import argparse

def parse_markdown_to_csv(directory):
    """
    Parses a review.md file within a given directory and converts it into a
    prompts.csv file.
    """
    md_file_path = os.path.join(directory, 'review.md')
    csv_file_path = os.path.join(directory, 'prompts.csv')
    base_category = os.path.basename(os.path.normpath(directory))

    if not os.path.exists(md_file_path):
        print(f"Error: '{md_file_path}' not found.")
        return

    print(f"Reading from '{md_file_path}'...")

    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content into sections for each variation
    variations = re.split(r'\n---\n', content)
    
    parsed_data = []

    for i, var in enumerate(variations):
        if not var.strip() or 'Jailbreak Variations for:' in var:
            continue

        try:
            # Extract persona from the main heading
            persona_match = re.search(r'## Variation \d+: The (.*?) Persona', var)
            if not persona_match:
                print(f"Warning: Could not find persona for variation {i+1}. Skipping.")
                continue
            persona = persona_match.group(1).strip()
            
            category = f"{base_category} - {persona}"

            # Extract content for each step
            initial_prompt = re.search(r'### 段階1: 初期プロンプト \(initial_prompt\)\s*>\s*(.*?)\s*###', var, re.DOTALL).group(1).strip()
            step1_response = re.search(r'### 段階1.5: 想定されるモデルの応答 \(step1_response_content\)\s*(.*?)\s*###', var, re.DOTALL).group(1).strip()
            step2_prompt = re.search(r'### 段階2: 追撃プロンプト \(step2_prompt\)\s*>\s*(.*?)\s*$', var, re.DOTALL).group(1).strip()

            parsed_data.append([category, initial_prompt, step1_response, step2_prompt])
        except AttributeError:
            print(f"Warning: Could not parse variation {i+1} completely. Check formatting. Skipping.")
            continue

    if not parsed_data:
        print("No data was parsed. CSV file will not be created.")
        return

    # Write the data to a CSV file
    print(f"Writing {len(parsed_data)} records to '{csv_file_path}'...")
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["category", "initial_prompt", "step1_response_content", "step2_prompt"])
            writer.writerows(parsed_data)
        print("Conversion successful.")
    except IOError as e:
        print(f"Error writing to file: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a review.md file to a prompts.csv file.')
    parser.add_argument('directory', type=str, help='The directory containing the review.md file.')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
    else:
        parse_markdown_to_csv(args.directory)
