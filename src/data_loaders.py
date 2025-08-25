import pandas as pd
import json
import os

def convert_csv_to_coco_like(csv_path, output_dir):
    """
    Converts a CSV file with a 'prompt' column to a COCO-like JSON format.

    Args:
        csv_path (str): Path to the input CSV file.
        output_dir (str): Directory to save the output JSON file.
    """
    df = pd.read_csv(csv_path)

    images = []
    annotations = []
    categories = [{"id": 1, "name": "prompt", "supercategory": "text"}] # Example category

    for idx, row in df.iterrows():
        image_id = idx + 1
        prompt_text = row['prompt']

        images.append({
            "id": image_id,
            "file_name": f"prompt_{image_id}.txt", # Dummy file name
            "width": 0,
            "height": 0,
        })

        annotations.append({
            "id": idx + 1,
            "image_id": image_id,
            "category_id": 1,
            "caption": prompt_text, # Using caption field for the prompt
        })

    coco_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Output file name based on input csv
    base_name = os.path.basename(csv_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_dir, f"{file_name_without_ext}_coco.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully converted {csv_path} to {output_path}")

if __name__ == '__main__':
    # Example usage:
    # This part is for testing and won't be executed when imported.
    # You would typically call this function from another script.
    pass


def convert_problems_to_coco_like(problems_dir, output_path):
    """
    Converts a directory of Python problem files to a COCO-like JSON format.

    Args:
        problems_dir (str): Path to the directory containing .py files.
        output_path (str): Path to save the output JSON file.
    """
    images = []
    annotations = []
    categories = [{"id": 1, "name": "python_problem", "supercategory": "code"}]

    problem_files = [f for f in os.listdir(problems_dir) if f.endswith('.py') and f != '__init__.py']

    for idx, file_name in enumerate(problem_files):
        image_id = idx + 1
        file_path = os.path.join(problems_dir, file_name)

        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()

        images.append({
            "id": image_id,
            "file_name": file_name,
            "width": 0, # Not applicable for code
            "height": 0, # Not applicable for code
        })

        annotations.append({
            "id": idx + 1,
            "image_id": image_id,
            "category_id": 1,
            "code": code_content, # Custom field for the code content
        })

    coco_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully converted {problems_dir} to {output_path}")


def load_coco_data(json_path):
    """
    Loads data from a COCO-like JSON file.

    Args:
        json_path (str): Path to the COCO-like JSON file.

    Returns:
        dict: The loaded data.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Successfully loaded data from {json_path}")
    return data
