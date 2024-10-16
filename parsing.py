import json

Data_path = "/Users/it/Desktop/Parsing json/data_questions_section.json"
PDF_in_JSON_path = " "

def load_file(file_path):
    """Loads a JSON file from the specified path."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_matching_sections_contents(possible_sections, sections):
    """
    Returns the content of matching sections from the second file based on the possible sections as a list.

    :param possible_sections: A list of section names from the first file.
    :param sections: The 'sections' object from the second file.
    :return: A list of matching section contents.
    """
    matching_sections = []

    for section in possible_sections:
        if section in sections:
            # Append the content of the section to the list
            matching_sections.append(sections[section])

    return matching_sections

def create_result_strings(data_value, questions, matching_sections):
        """
        Constructs the result strings for each matching section.

        :param data_value: The 'data' field from the first file.
        :param questions: A list of questions from the first file.
        :param matching_sections: A list of matching section contents.
        :return: A list of formatted result strings, one for each matching section.
        """
        questions_str = ', '.join(questions)  # Join questions into a single string
        result_strings = []

        for section_content in matching_sections:
            result_string = f"{data_value}: {questions_str} in the following text: {section_content}"
            result_strings.append(result_string)

        return result_strings


def process_files(file1_data, file2_data):
    """
    Processes the data from the two files and returns a dictionary that groups the strings by the 'data' field in file 1.

    :param file1_data: Data from the first JSON file.
    :param file2_data: Data from the second JSON file.
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
        result_strings = create_result_strings(data_value, questions, matching_sections)

        # Group the result strings by the 'data' field
        if data_value in grouped_results:
            grouped_results[data_value].extend(result_strings)
        else:
            grouped_results[data_value] = result_strings

    return grouped_results

def main():
    # Paths to your files
    file1_path = 'file1.json'
    file2_path = 'file2.json'

    # Load data from both files
    file1_data = load_file(file1_path)
    file2_data = load_file(file2_path)

    # Process and generate grouped output
    grouped_results = process_files(file1_data, file2_data)

    # Print the grouped results
    for data_value, result_strings in grouped_results.items():
        print(f"{data_value}:")
        for result_string in result_strings:
            print(f"  - {result_string}")
        print()  # Add a newline for better readability

# Call the main function to execute the program
if __name__ == "__main__":
    main()

