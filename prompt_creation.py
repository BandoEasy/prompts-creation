import json
import os

# Global paths to your files
Data_path = "/Users/it/Desktop/Parsing json/data_questions_section.json"
PDF_in_JSON_directory = "/Users/it/Desktop/js"

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

def create_result_strings(data_value, questions, matching_sections, filename):
    """
    Constructs the result strings for each matching section.
    :param data_value: The 'data' field from the first file.
    :param questions: A list of questions from the first file.
    :param matching_sections: A list of tuples containing (section_name, section_content).
    :param filename: The name of the file being processed.
    :return: A list of formatted result strings, one for each matching section, including the file source and section name.
    """
    questions_str = ', '.join(questions)  # Join questions into a single string
    result_strings = []

    for section_name, section_content in matching_sections:
        result_string = f"{data_value}: {questions_str} in \n\tsection '{section_name}' \n\t(source: {filename}):\n {section_content}\n"
        result_strings.append(result_string)

    return result_strings

def process_files(file1_data, file2_data, filename):
    """
    Processes the data from the two files and returns a dictionary that groups the strings by the 'data' field in file 1.
    :param file1_data: Data from the first JSON file.
    :param file2_data: Data from the second JSON file.
    :param filename: The name of the file being processed (to include in the result strings).
    :return: A dictionary with 'data' as keys and lists of strings as values.
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

        # Formulate the result strings
        result_strings = create_result_strings(data_value, questions, matching_sections, filename)

        # Group the result strings by the 'data' field
        if data_value in grouped_results:
            grouped_results[data_value].extend(result_strings)
        else:
            grouped_results[data_value] = result_strings

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

            # Merge the results into the combined results
            for data_value, result_strings in results.items():
                if data_value in combined_results:
                    combined_results[data_value].extend(result_strings)
                else:
                    combined_results[data_value] = result_strings

    return combined_results

def main():
    # Load data from the first file
    try:
        file1_data = load_file(Data_path)
    except Exception as e:
        print(f"Error loading data file: {e}")
        return

    # Process multiple JSON files from the specified directory
    grouped_results = process_multiple_files(file1_data, PDF_in_JSON_directory)

    # Print the grouped results
    if not grouped_results:
        print("No results to display.")
    else:
        for data_value, result_strings in grouped_results.items():
            print(f"{data_value}:")
            for result_string in result_strings:
                print(f"  - {result_string}")
            print()  # Add a newline for better readability

if __name__ == "__main__":
    main()
