# Reattempt cleaning the newly uploaded file by removing lines with mismatched columns.
file_path = 'ALL_mix_data/data_cleaning_process/cleaned_data5_withhand.csv'
output_file_path = 'ALL_mix_data/data_cleaning_process/cleaned_data_6.csv'

try:
    # Detect mismatched rows
    valid_rows = []
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        header = file.readline()  # Read the header
        expected_columns = len(header.split(','))  # Count expected columns based on the header
        
        # Check each row
        for line in file:
            if len(line.split(',')) == expected_columns:
                valid_rows.append(line)
    
    # Save cleaned data
    with open(output_file_path, 'w', encoding='ISO-8859-1') as output_file:
        output_file.write(header)  # Write the header first
        output_file.writelines(valid_rows)  # Write only valid rows

    clean_status = f"File cleaned successfully and saved to: {output_file_path}"
except Exception as e:
    clean_status = f"Error during cleaning: {str(e)}"

clean_status

