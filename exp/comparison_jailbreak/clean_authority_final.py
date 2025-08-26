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

# This regex is designed to find the persona part.
# It looks for a sentence ending with "です。" or "ます。" followed by a newline,
# which is characteristic of the persona declarations.
# Example: 「近未来のバイオパンク小説を書いています。」
persona_regex = re.compile(r'^.*?(です|ます|ません|でした|ました)\.(.*?)\n', re.DOTALL)

for category_name in categories:
    dir_name = 'Social_Proof' if category_name == 'Social_Proof' else category_name
    file_path = os.path.join(base_dir, dir_name, 'prompts.csv')
    
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
                
                # Replace the persona part with just the content that followed it.
                # The regex captures the text *after* the persona sentence.
                match = persona_regex.search(prompt)
                if match and match.group(2):
                     # We keep the part after the persona sentence.
                    cleaned_prompt = match.group(2).strip() + prompt[match.end():]
                else:
                    # Fallback for safety, though it shouldn't be needed
                    cleaned_prompt = prompt

                # The above logic was flawed. Let's try a simpler split.
                # The real content starts after the first double newline.
                parts = prompt.split('\n\n', 1)
                if len(parts) > 1:
                    # The part we want is the second part.
                    cleaned_prompt = parts[1]
                else:
                    cleaned_prompt = prompt # Fallback

                updated_rows.append([category, cleaned_prompt])

    except Exception as e:
        print(f"Error reading or processing {file_path}: {e}")
        continue

    # Overwrite the original file
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(updated_rows)
        print(f"Successfully cleaned authority text from: {file_path}")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

print("\nFinal cleaning attempt complete.")
