# README: JSON Parsing for Fine-Tuning ChatGPT Model

## Overview

This project processes JSON files to extract specific sections of text and format them into prompts that can be used for fine-tuning a GPT-based model (like ChatGPT). The extracted data includes questions, relevant sections of text, and metadata such as the file source and section names. The formatted output is intended for use in creating training data to improve the performance of a fine-tuned language model.

### Key Components:

- **JSON Input Files**:
  - **File 1 (`data_questions_section.json`)**: This file contains a list of data entries, each of which includes a `data` field, a list of `questions`, and a list of `Possible sections`. The `Possible sections` are the section names we expect to find in the second set of JSON files.
  - **Multiple PDF JSON Files**: These files represent converted PDF documents. Each file contains a `sections` object where different sections of the document are labeled and stored.

- **Output**: The script outputs a collection of formatted strings that can be used as training data prompts. Each string consists of a data field, questions, a section name, and text extracted from the PDF JSON files, along with the filename of the source.

## Purpose

The primary purpose of this script is to generate high-quality prompt-response data for fine-tuning a language model like ChatGPT. The output strings from this project are designed to be prompts in the form of questions with contextually relevant text from various documents. This allows for fine-tuning the model to improve its ability to answer specific questions based on real-world documents.

## Code Structure

### 1. `load_file(file_path)`

This function loads a JSON file from a specified path and returns its content as a Python dictionary.

### 2. `get_matching_sections_contents(possible_sections, sections)`

- **Input**: A list of possible section names from the first JSON file and a dictionary of sections from the PDF JSON file.
- **Output**: A list of tuples containing both section names and section content that match the section names listed in `possible_sections`.
- **Purpose**: To identify and extract relevant sections from the second JSON file that match the section names specified in the first file.

### 3. `create_result_strings(data_value, questions, matching_sections, filename)`

- **Input**: 
  - `data_value`: The `data` field from the first JSON file.
  - `questions`: A list of questions related to that data.
  - `matching_sections`: A list of tuples of section names and their content from the second JSON file.
  - `filename`: The name of the PDF JSON file from which the section was extracted.
- **Output**: A list of formatted strings, each containing the `data_value`, `questions`, `section_name`, `section_content`, and the `filename`.
- **Purpose**: To generate the formatted prompt strings that will be used as training data for fine-tuning the model.

### 4. `process_files(file1_data, file2_data, filename)`

- **Input**: 
  - `file1_data`: Content from the first JSON file.
  - `file2_data`: Content from a PDF JSON file.
  - `filename`: The name of the PDF JSON file.
- **Output**: A dictionary of grouped results, where the keys are the `data` field and the values are lists of formatted prompt strings.
- **Purpose**: To process a pair of JSON files (one from each source) and extract the relevant information for prompt creation.

### 5. `process_multiple_files(file1_data, json_directory)`

- **Input**: 
  - `file1_data`: Content from the first JSON file.
  - `json_directory`: The directory containing multiple PDF JSON files.
- **Output**: A dictionary of combined results from all the processed PDF JSON files.
- **Purpose**: To process multiple JSON files from a directory, combine their results, and return the final set of formatted prompts for fine-tuning.

### 6. `main()`

- The main function that orchestrates the entire process:
  1. Loads the first JSON file.
  2. Processes multiple PDF JSON files from the specified directory.
  3. Prints the formatted prompt strings that can be used for fine-tuning.

## Output Format

The script generates strings in the following format:

```
<data_value>: <questions> in section '<section_name>' (source: <filename>):
<section_content>
```

### Example:

```text
Customer Support: What are the available channels of support? in section 'Support Channels' (source: support_document_001.json):
The available channels for customer support include phone, email, and live chat. These services are available 24/7.
```

## Usage

### Prerequisites

- Python 3.x
- JSON files structured as described above.

### Running the Script

1. Set the correct paths for the `Data_path` (for `data_questions_section.json`) and `PDF_in_JSON_directory` (for the directory containing your JSON files) in the script.
2. Run the script by executing:

   ```bash
   python script_name.py
   ```

3. The script will process all JSON files in the specified directory and print the formatted strings to the console.

### Customization

- You can modify the structure of the formatted strings in the `create_result_strings` function based on the specific format required for fine-tuning your model.
- The script is designed to handle multiple files and errors gracefully, but you can further enhance it with logging or output redirection if needed.

## Contribution

Feel free to submit issues or pull requests to improve this project or add more features like support for additional file formats, enhanced error handling, or more customizable prompt formats.

## License

This project is licensed under the MIT License.

---

This README provides an overview of the project's purpose, code structure, and instructions for usage. It is designed for developers looking to generate training data for fine-tuning GPT models based on custom document sets.
