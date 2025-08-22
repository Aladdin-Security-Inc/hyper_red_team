import os
import sys

# Add src directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loaders import convert_csv_to_coco_like, convert_problems_to_coco_like

def main():
    # --- Convert hunnypod datasets ---
    print("--- Converting hunnypod datasets ---")
    hunnypod_data_dir = "data/hunnypod"
    hunnypod_output_dir = "data/hunnypod"
    
    csv_files = [f for f in os.listdir(hunnypod_data_dir) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        csv_path = os.path.join(hunnypod_data_dir, csv_file)
        convert_csv_to_coco_like(csv_path, hunnypod_output_dir)

    # --- Convert tdd_sabotage_experiment datasets ---
    print("\n--- Converting tdd_sabotage_experiment datasets ---")
    problems_dir = "data/tdd_sabotage_experiment/problems"
    output_path = "data/tdd_sabotage_experiment/problems_coco.json"
    convert_problems_to_coco_like(problems_dir, output_path)


if __name__ == '__main__':
    main()
