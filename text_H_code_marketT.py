
# Retry the process of identifying problematic rows and saving valid data and logs.
file_path = 'ALL_mix_data/data_CP_Walmart/cleaned_data5_withhand.csv'
log_file_path = 'problematic_rows_log_retry.txt'
cleaned_file_path = 'Newcleaned_data_6.csv'

try:
    problematic_rows = []
    valid_rows = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        header = file.readline()  # Read the header
        expected_columns = len(header.split(','))  # Count expected columns based on the header

        # Check each row
        for line_number, line in enumerate(file, start=2):  # Start at line 2 for rows after the header
            if len(line.split(',')) == expected_columns:
                valid_rows.append(line)
            else:
                problematic_rows.append((line_number, line))

    # Log problematic rows
    with open(log_file_path, 'w', encoding='ISO-8859-1') as log_file:
        log_file.write("Problematic Rows Log\n")
        log_file.write("Line Number\tRow Content\n")
        for row in problematic_rows:
            log_file.write(f"{row[0]}\t{row[1]}")

    # Save valid rows
    with open(cleaned_file_path, 'w', encoding='ISO-8859-1') as cleaned_file:
        cleaned_file.write(header)  # Write the header first
        cleaned_file.writelines(valid_rows)  # Write only valid rows

    log_status_retry = (
        f"Valid rows saved to: {cleaned_file_path}\n"
        f"Problematic rows logged to: {log_file_path}\n"
        f"Total problematic rows: {len(problematic_rows)}"
    )
except Exception as e:
    log_status_retry = f"Error during retry logging: {str(e)}"

log_status_retry
