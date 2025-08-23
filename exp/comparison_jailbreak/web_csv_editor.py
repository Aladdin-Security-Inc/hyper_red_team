#!/usr/bin/env python3
import pandas as pd
import os
import sys
from flask import Flask, render_template_string, request, jsonify

# --- Configuration ---
# The absolute path to the CSV file you want to edit.
CSV_FILE_PATH = "/Users/kooimai/Programming/hyper_red_team/exp/comparison_jailbreak/Top_Threats/prompts.csv"
# --- End of Configuration ---

# Initialize the Flask application
app = Flask(__name__)

# --- HTML, CSS, and JavaScript Template (Embedded in a Python string) ---
# This single string contains all the frontend code.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Editor</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 0; background-color: #f8f9fa; color: #212529; }
        header { background-color: #343a40; color: white; padding: 1rem; text-align: center; }
        .container { max-width: 1200px; margin: 20px auto; padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .controls { text-align: right; margin-bottom: 20px; }
        button { background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        #status { margin-right: 15px; font-style: italic; color: #6c757d; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th, td { border: 1px solid #dee2e6; padding: 12px; text-align: left; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; cursor: pointer; }
        th { background-color: #f2f2f2; }
        td:hover { background-color: #e9ecef; }
        .modal-bg { display: none; position: fixed; z-index: 1; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.5); }
        .modal-content { background-color: #fefefe; margin: 5% auto; padding: 20px; border: 1px solid #888; width: 80%; max-width: 800px; border-radius: 8px; display: flex; flex-direction: column; }
        .modal-header { padding-bottom: 10px; border-bottom: 1px solid #ccc; }
        .modal-body { flex-grow: 1; display: flex; flex-direction: column; padding: 10px 0; }
        #editor-textarea { width: 100%; flex-grow: 1; min-height: 400px; font-family: monospace; font-size: 14px; line-height: 1.5; border: 1px solid #ccc; border-radius: 4px; padding: 10px; resize: vertical; }
        .modal-footer { padding-top: 10px; text-align: right; }
        .close-btn { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <header>
        <h1>CSV Editor</h1>
        <p>File: {{ file_path }}</p>
    </header>
    <div class="container">
        <div class="controls">
            <span id="status">Ready</span>
            <button id="save-btn">Save Changes to File</button>
        </div>
        <div style="overflow-x: auto;">
            <table>
                <thead>
                    <tr>
                        <th>Row</th>
                        {% for header in headers %}
                            <th>{{ header }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in data %}
                    <tr data-row-index="{{ loop.index0 }}">
                        <td>{{ loop.index0 }}</td>
                        {% for cell in row %}
                            <td data-col-index="{{ loop.index0 }}">{{ cell }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- The Modal -->
    <div id="editor-modal" class="modal-bg">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close-btn">&times;</span>
                <h2 id="modal-title">Edit Cell</h2>
            </div>
            <div class="modal-body">
                <textarea id="editor-textarea"></textarea>
            </div>
            <div class="modal-footer">
                <button id="modal-save-btn">Update Cell</button>
            </div>
        </div>
    </div>

    <script>
        // Client-side data store
        let tableData = {{ data|tojson }};
        const headers = {{ headers|tojson }};
        let currentRow, currentCol;

        const modal = document.getElementById('editor-modal');
        const statusEl = document.getElementById('status');

        // Open modal and populate with data
        document.querySelector('table').addEventListener('click', (e) => {
            if (e.target.tagName === 'TD') {
                currentRow = e.target.parentElement.dataset.rowIndex;
                currentCol = e.target.dataset.colIndex;
                
                document.getElementById('modal-title').innerText = `Editing Row ${currentRow}, Column "${headers[currentCol]}"`;
                document.getElementById('editor-textarea').value = tableData[currentRow][currentCol];
                modal.style.display = 'block';
            }
        });

        // Close modal
        document.querySelector('.close-btn').onclick = () => { modal.style.display = 'none'; };
        window.onclick = (e) => { if (e.target == modal) { modal.style.display = 'none'; } };

        // Save changes from modal to client-side store
        document.getElementById('modal-save-btn').onclick = () => {
            const newContent = document.getElementById('editor-textarea').value;
            tableData[currentRow][currentCol] = newContent;
            
            // Update the table cell visually
            const cell = document.querySelector(`tr[data-row-index='${currentRow}'] td[data-col-index='${currentCol}']`);
            cell.innerText = newContent;
            
            modal.style.display = 'none';
            statusEl.innerText = 'Unsaved changes';
        };

        // Save all changes back to the server
        document.getElementById('save-btn').onclick = async () => {
            statusEl.innerText = 'Saving...';
            try {
                const response = await fetch('/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: tableData })
                });
                const result = await response.json();
                if (result.success) {
                    statusEl.innerText = 'Saved successfully!';
                } else {
                    statusEl.innerText = `Error: ${result.error}`;
                }
            } catch (error) {
                statusEl.innerText = `Error: ${error}`;
            }
        };
    </script>
</body>
</html>
"""

def load_data(file_path):
    """Loads data from the CSV file."""
    try:
        df = pd.read_csv(file_path, quotechar='"', engine='python')
        return df.fillna('')
    except FileNotFoundError:
        print(f"FATAL ERROR: The file was not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"FATAL ERROR: An error occurred while reading the CSV: {e}", file=sys.stderr)
        sys.exit(1)

def save_data(df, file_path):
    """Saves the DataFrame back to the CSV file."""
    df.to_csv(file_path, index=False, quotechar='"', quoting=1) # csv.QUOTE_ALL

@app.route('/')
def index():
    """Main route to display the editor."""
    df = load_data(CSV_FILE_PATH)
    headers = df.columns.tolist()
    data = df.values.tolist()
    return render_template_string(HTML_TEMPLATE, headers=headers, data=data, file_path=CSV_FILE_PATH)

@app.route('/save', methods=['POST'])
def save():
    """API endpoint to save the data."""
    try:
        incoming_data = request.json['data']
        df = pd.DataFrame(incoming_data, columns=load_data(CSV_FILE_PATH).columns)
        save_data(df, CSV_FILE_PATH)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("--- Starting Web CSV Editor ---")
    print(f"Editing file: {CSV_FILE_PATH}")
    print("Open your web browser and go to: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server.")
    app.run(debug=True)
