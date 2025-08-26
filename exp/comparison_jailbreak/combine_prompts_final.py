import csv
import os

# --- Configuration ---
auth_file = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories/Comparison/prompts_auth.csv'
complex_file = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories/Comparison/prompts.csv'
output_file = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories/Comparison/prompts_auth_complex.csv'

# --- Script Logic ---

# 1. Read both source files
try:
    with open(auth_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        auth_header = next(reader)
        auth_prompts = list(reader)
    with open(complex_file, 'r', encoding='utf-8') as f:
        # The key change is to read the file content directly to avoid CSV reader issues with newlines
        f.readline() # skip header
        content = f.read()
        # Split the content back into rows manually, handling the quotes
        complex_prompts_raw = content.strip().split('\n') # Corrected: removed extra quote
        complex_prompts = []
        for item in complex_prompts_raw:
            parts = item.split(',', 1) # Corrected: removed extra quote
            if len(parts) == 2:
                complex_prompts.append(parts)

except FileNotFoundError as e:
    print(f"FATAL: Could not find a source file: {e.filename}")
    exit(1)

if not auth_prompts or not complex_prompts:
    print("FATAL: One of the source files is empty.")
    exit(1)

if len(auth_prompts) != len(complex_prompts):
    print(f"FATAL: Mismatch in prompt counts. Auth: {len(auth_prompts)}, Complex: {len(complex_prompts)}")
    exit(1)

# 3. Combine the prompts
final_prompts = []
for i, (auth_category, auth_prompt) in enumerate(auth_prompts):
    # Ensure complex_prompts[i] has at least two elements before unpacking
    if len(complex_prompts[i]) < 2:
        print(f"Warning: Malformed entry in complex_prompts at index {i}. Skipping.")
        continue
    _, complex_prompt_text = complex_prompts[i]
    
    # Clean up the complex prompt text from file reading artifacts
    complex_prompt_text = complex_prompt_text.replace('""', '"').strip().rstrip('"')
    
    simple_request = "後者について、その詳細な手順を具体的に説明してください。"
    split_point = auth_prompt.find(simple_request)
    if split_point == -1:
        continue
    persona_and_comparison_part = auth_prompt[:split_point].strip()
    
    # The complex request structure starts with '# 制約条件'
    # The literal '\n' is in the file, so we search for that
    request_structure_start = complex_prompt_text.find('# 制約条件')
    if request_structure_start == -1:
         # Try finding with a literal newline if the above fails
         request_structure_start = complex_prompt_text.find('\n# 制約条件')

    if request_structure_start == -1:
        print(f"Warning: Could not find '# 制約条件' in prompt for {auth_category}. Skipping.")
        continue
        
    complex_request_part = complex_prompt_text[request_structure_start:]
    
    final_prompt_text = f"{persona_and_comparison_part}\n{complex_request_part}"
    
    final_prompts.append([auth_category, final_prompt_text])

# 4. Write the new combined prompts to the output file
try:
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'prompt'])
        writer.writerows(final_prompts)
    print(f"Successfully generated the combined prompts at: {output_file}")
except IOError as e:
    print(f"Error writing to {output_file}: {e}")

print("\nCombined prompt generation complete.")
