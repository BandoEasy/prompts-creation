# JSON Parsing and Grouping for Fine-Tuning Data

This project processes and extracts information from multiple JSON files, and groups relevant sections based on predefined questions. The grouped data is then saved in a structured JSON format, which can be used for various purposes such as fine-tuning AI models like GPT or for other data analysis tasks.

## Features

- **Parsing JSON Files**: The project takes in a directory of JSON files (representing PDF documents) and another JSON file containing questions and data categories.
- **Section Matching**: For each `data_value` (such as a category), it matches sections from the PDF JSON files based on predefined possible sections.
- **Grouping and Formatting**: The extracted data (including questions, sections, and metadata) is grouped by the `data_value`, formatted into JSON objects, and saved as a new JSON file.
- **Easy Integration**: The output JSON is formatted to be easily consumed by downstream tasks, such as model fine-tuning or other processing.

## Input Data

There are two main types of input files:

1. **Questions JSON (`data_questions_section.json`)**:
    - Contains a list of questions and their corresponding `data_value`.
    - Specifies which sections of the PDF documents to look for.
    - Example structure:
      ```json
      [
        {
          "data": "Funding Options",
          "questions": [
            "What types of funding are available?",
            "What is the interest rate?"
          ],
          "Possible sections": [
            "Funding Process",
            "Interest Rate"
          ]
        }
      ]
      ```

2. **PDF JSON Files**:
    - These represent the contents of PDF documents, converted to JSON.
    - Contains sections of text that will be extracted and matched to the `data_value` and questions.
    - Example structure:
      ```json
      {
        "sections": {
          "Funding Process": "The process of funding is ...",
          "Interest Rate": "The interest rate is 3%..."
        }
      }
      ```

## Output Data

The result of this project is a single JSON file where data is grouped by `data_value`. The JSON file is structured like this:

```json
{
    "Funding Options": [
        {
            "questions": [
                "What types of funding are available?",
                "What is the interest rate?"
            ],
            "section_name": "Funding Process",
            "section_content": "The process of funding is ...",
            "source_filename": "funding_document_001.json"
        },
        {
            "questions": [
                "What types of funding are available?",
                "What is the interest rate?"
            ],
            "section_name": "Interest Rate",
            "section_content": "The interest rate is 3%...",
            "source_filename": "funding_document_002.json"
        }
    ]
}
```

## Prerequisites

To use this project, you'll need the following:

- Python 3.x
- JSON files for both:
  - A file containing questions and section details (`data_questions_section.json`)
  - A directory of JSON files representing PDF documents.

## How It Works

1. **Loading Files**: The script loads the main JSON file containing the questions (`data_questions_section.json`) and iterates over multiple PDF JSON files in the specified directory.
2. **Section Matching**: It checks each file for sections that match the `Possible sections` from the questions file.
3. **JSON Object Creation**: For each matching section, a JSON object is created that contains:
   - The `questions`
   - The `section_name`
   - The `section_content`
   - The `source_filename` of the document from which the section was extracted.
4. **Grouping**: The JSON objects are grouped by the `data_value` and saved to a new JSON file.
5. **Saving Results**: The final grouped JSON is saved to a specified output path.

## How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```

2. **Prepare Your Data**:
   - Place the questions file (`data_questions_section.json`) in the appropriate directory.
   - Ensure you have a directory containing the PDF JSON files you want to process.

3. **Modify the Paths**:
   - In the script, modify the following paths to point to your files:
     - `Data_path`: Path to the questions JSON file.
     - `PDF_in_JSON_directory`: Path to the directory containing the PDF JSON files.
     - `Output_JSON_path`: Path where you want to save the final output.

4. **Run the Script**:
   ```bash
   python script_name.py
   ```

5. **Check the Output**:
   - Once the script has completed, the grouped results will be saved in the file specified by `Output_JSON_path`.

## Code Overview

### Functions

- **`load_file(file_path)`**:
  - Loads a JSON file from the specified path and returns its content.
  
- **`get_matching_sections_contents(possible_sections, sections)`**:
  - Checks for section matches between the `possible_sections` from the questions JSON file and the `sections` in a PDF JSON file. Returns the matching sections.

- **`create_json_objects(questions, matching_sections, filename)`**:
  - Creates JSON objects for each matched section, including `questions`, `section_name`, `section_content`, and `source_filename`.

- **`process_files(file1_data, file2_data, filename)`**:
  - For each entry in the questions JSON, it looks for matching sections in the PDF JSON files and creates the corresponding JSON objects. These objects are grouped by the `data_value`.

- **`process_multiple_files(file1_data, json_directory)`**:
  - Iterates through the directory of PDF JSON files, processing each file and grouping the results by the `data_value`.

- **`save_results_to_json(result_data, output_path)`**:
  - Saves the final grouped JSON data to the specified output file.

### Example Execution

```python
# Load data from the first file
file1_data = load_file(Data_path)

# Process multiple JSON files from the specified directory
grouped_results = process_multiple_files(file1_data, PDF_in_JSON_directory)

# Save the grouped results to a new JSON file
save_results_to_json(grouped_results, Output_JSON_path)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

## Contact

For questions or support, feel free to open an issue in this repository.

---

This README file should provide a comprehensive guide for using the project. You can expand on it with more details if necessary, such as providing troubleshooting steps or adding more examples. Let me know if you need anything else!
