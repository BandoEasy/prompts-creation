import json
import os

# Global paths to your files
Data_path = "/Users/it/Desktop/Parsing json/data_questions_section.json"
PDF_in_JSON_directory = "/Users/it/Desktop/js"
Output_JSON_path = "/Users/it/Desktop/Parsing json/output_data_grouped.json"  # Path to save the grouped result JSON

def load_file(file_path):
    """Loads a JSON file from the specified path."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_matching_sections_contents(possible_sections, sections):
    """
    Returns the content of matching sections from the second file based on the possible sections as a list.
    :param possible_sections: A list of section names from the first file.
    :param sections: The 'sections' object from the second file.
    :return: A list of tuples (section_name, section_content) for matching sections.
    """
    matching_sections = []
    for section in possible_sections:
        if section in sections:
            # Append the section name and content as a tuple to the list
            matching_sections.append((section, sections[section]))
    return matching_sections

def create_json_objects(questions, matching_sections, filename):
    """
    Constructs a list of JSON objects for each matching section.
    :param questions: A list of questions from the first file.
    :param matching_sections: A list of tuples containing (section_name, section_content).
    :param filename: The name of the file being processed.
    :return: A list of JSON objects for each matching section, excluding 'data_value'.
    """
    json_objects = []

    for section_name, section_content in matching_sections:
        json_object = {
            "questions": questions,
            "section_name": section_name,
            "section_content": section_content,
            "source_filename": filename
        }
        json_objects.append(json_object)

    return json_objects

def process_files(file1_data, file2_data, filename):
    """
    Processes the data from the two files and returns a dictionary that groups the JSON objects by the 'data' field in file 1.
    :param file1_data: Data from the first JSON file.
    :param file2_data: Data from the second JSON file.
    :param filename: The name of the file being processed (to include in the JSON objects).
    :return: A dictionary with 'data' as keys and lists of JSON objects as values.
    """
    sections = file2_data.get("sections", {})  # Get sections from file 2
    grouped_results = {}  # Dictionary to group results by the 'data' field

    # Iterate over entries in file 1
    for entry in file1_data:
        data_value = entry.get("data", "")
        questions = entry.get("questions", [])
        possible_sections = entry.get("Possible sections", [])

        # Get all matching sections based on the possible sections
        matching_sections = get_matching_sections_contents(possible_sections, sections)

        # Formulate the JSON objects
        result_json_objects = create_json_objects(questions, matching_sections, filename)

        # Group the result JSON objects by the 'data' field
        if data_value in grouped_results:
            grouped_results[data_value].extend(result_json_objects)
        else:
            grouped_results[data_value] = result_json_objects

    return grouped_results

def process_multiple_files(file1_data, json_directory):
    """
    Processes multiple JSON files in the specified directory along with the data from the first file.
    :param file1_data: Data from the first JSON file.
    :param json_directory: Directory containing PDF JSON files to process.
    :return: A dictionary that groups results from all processed files.
    """
    combined_results = {}

    # Ensure that the directory exists and contains files
    if not os.path.exists(json_directory):
        print(f"Directory {json_directory} does not exist.")
        return combined_results

    if not os.listdir(json_directory):
        print(f"No files found in {json_directory}.")
        return combined_results

    # Loop through all files in the directory
    for filename in os.listdir(json_directory):
        if filename.endswith(".json"):  # Process only JSON files
            file_path = os.path.join(json_directory, filename)
            print(f"Processing file: {file_path}")

            # Load the second file (PDF in JSON format)
            try:
                file2_data = load_file(file_path)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue

            # Process the files and get grouped results, passing the filename
            results = process_files(file1_data, file2_data, filename)

            # Merge the results into the combined results, grouped by data_value
            for data_value, result_json_objects in results.items():
                if data_value in combined_results:
                    combined_results[data_value].extend(result_json_objects)
                else:
                    combined_results[data_value] = result_json_objects

    return combined_results

def save_results_to_json(result_data, output_path):
    """
    Saves the processed results to a JSON file.
    :param result_data: The final processed data to be saved.
    :param output_path: The path where the result JSON file will be saved.
    """
    try:
        with open(output_path, 'w') as outfile:
            json.dump(result_data, outfile, indent=4)
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"Error saving results to {output_path}: {e}")

def main():
    # Load data from the first file
    try:
        file1_data = load_file(Data_path)
    except Exception as e:
        print(f"Error loading data file: {e}")
        return

    # Process multiple JSON files from the specified directory
    grouped_results = process_multiple_files(file1_data, PDF_in_JSON_directory)

    # Save the grouped results to a new JSON file
    if not grouped_results:
        print("No results to display.")
    else:
        save_results_to_json(grouped_results, Output_JSON_path)

if __name__ == "__main__":
    main()
