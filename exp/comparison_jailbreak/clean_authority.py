import csv
import os
import re

# Define the directories to process
base_dir = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories'
categories = [
    'Commitment',
    'Liking',
    'Reciprocity',
    'Scarcity',
    'Social_Proof',
    'Unity'
]

# This regex will find the first paragraph, which is the persona/authority part.
# It looks for the start of the string, followed by any characters until a double newline.
# The prompt text uses literal '\n' for newlines, so we match that.
persona_regex = re.compile(r'^.*?(\n\n|\n#)', re.DOTALL)

for category_name in categories:
    file_path = os.path.join(base_dir, category_name, 'prompts.csv')
    
    if not os.path.exists(file_path):
        print(f"File not found, skipping: {file_path}")
        continue

    updated_rows = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            updated_rows.append(header)

            for row in reader:
                if len(row) != 2:
                    continue
                
                category, prompt = row
                
                # Find the match to decide on the replacement
                match = persona_regex.search(prompt)
                if match:
                    # If the separator was '\n#', we need to add '#' back
                    separator = match.group(1)
                    if separator == '\n#':
                        cleaned_prompt = '#' + prompt[match.end():]
                    else:
                        cleaned_prompt = prompt[match.end():]
                else:
                    # If no match, use the prompt as is
                    cleaned_prompt = prompt

                updated_rows.append([category, cleaned_prompt.strip()])

    except Exception as e:
        print(f"Error reading or processing {file_path}: {e}")
        continue

    # Overwrite the original file with the cleaned prompts
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(updated_rows)
        print(f"Successfully cleaned authority text from: {file_path}")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

print("\nCleaning complete.")