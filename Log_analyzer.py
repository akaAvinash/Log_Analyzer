import os
import re

# Ask the user for the log directory path
log_directory = input("Enter the log directory path: ")

# Check if the log directory is valid
if not os.path.isdir(log_directory):
    print("Invalid log directory path!")
else:
    # Ask the user for keywords to search
    keywords = input("Enter the keywords to search (separated by commas): ").split(',')

    # Ask the user for the log file name and path
    log_file_name = input("Enter the name of the log file: ")
    log_file_path = os.path.join(log_directory, log_file_name)

    # Check if the log file exists
    if not os.path.isfile(log_file_path):
        print("Log file not found!")
    else:
        # Perform log analysis on the file
        with open(log_file_path, "r") as log_file:
            # Read all lines of the log file
            log_lines = log_file.readlines()

        # Process each log entry and store matching lines and their reasons
        matching_lines = []
        for line in log_lines:
            # Strip leading and trailing whitespace
            line = line.strip()

            # Check if the log entry contains the specified keywords
            if any(keyword in line.lower() for keyword in keywords):
                # Check if the line mentions the reason for crashes or failures
                if "reason" in line.lower():
                    matching_lines.append(line)
                else:
                    # Check if the line contains keywords enclosed in brackets or parentheses
                    for keyword in keywords:
                        pattern = rf"[\(\[].*?{re.escape(keyword)}.*?[\)\]]"
                        if re.search(pattern, line, re.IGNORECASE):
                            matching_lines.append(line)
                            break


        # Extract the type of crash from the line
        crash_type = re.findall(r'\b(crash|fail|error|exception)\b', line, re.IGNORECASE)
        if crash_type:
            if 'crash' in keywords:
                match = re.search(rf"CrashType:(.*)", line, re.IGNORECASE)
                if match:
                    matching_lines.append("CrashType: " + match.group(1).strip())
            else:
                match = re.search(rf"{crash_type[0]}Type:(.*)", line, re.IGNORECASE)
                if match:
                    matching_lines.append(crash_type[0] + " Type: " + match.group(1).strip())
    


        # Create a new file to store the analyzed log lines
        analyzed_log_file_path = os.path.splitext(log_file_path)[0] + "_analyzed.txt"

        with open(analyzed_log_file_path, "w") as analyzed_log_file:
            # Write the matching log lines to the analyzed log file
            analyzed_log_file.write("\n".join(matching_lines))

        print("Log analysis completed!")
        print("Analyzed log saved as:", analyzed_log_file_path)
