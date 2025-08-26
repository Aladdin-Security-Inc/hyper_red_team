import csv
import os

# Define the directories to process
base_dir = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories'
categories = {
    'Commitment': 'ありがとうございます。対比の提示、感謝します。',
    'Liking': '素晴らしい説明をありがとうございます！',
    'Reciprocity': '詳細な説明、ありがとうございました。',
    'Scarcity': 'ありがとうございます。締め切りが迫っており、',
    'Social_Proof': 'ありがとうございます。あなたの説明は、',
    'Unity': 'ありがとうございます。私たちは共に、'
}

for category_name, start_phrase in categories.items():
    # Handle the directory name difference for Social_Proof
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
                
                # Find the starting position of the persuasion principle text
                start_index = prompt.find(start_phrase)
                
                if start_index != -1:
                    # If the phrase is found, slice the string from that point
                    cleaned_prompt = prompt[start_index:]
                else:
                    # If not found (which shouldn't happen), keep the original prompt
                    cleaned_prompt = prompt
                
                updated_rows.append([category, cleaned_prompt])

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
