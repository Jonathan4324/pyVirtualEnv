import csv

# Input and output file paths
input_file = "ALL_mix_data/data_CP_Walmart/cleaned_data5_withhand.csv"
output_file = "cleaned_data5_without_image_and_description.csv"

# Columns to remove
columns_to_remove = ["image_url", "short_description"]

try:
    # Read the input file and process
    with open(input_file, mode='r', encoding="ISO-8859-1") as infile:
        reader = csv.DictReader(infile)
        # Create a new list of fieldnames without the columns to remove
        fieldnames = [field for field in reader.fieldnames if field not in columns_to_remove]
        
        # Write to the output file
        with open(output_file, mode='w', encoding="ISO-8859-1", newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                # Remove unwanted columns
                filtered_row = {key: value for key, value in row.items() if key in fieldnames}
                writer.writerow(filtered_row)

    print(f"Cleaned CSV saved to: {output_file}")
except Exception as e:
    print(f"Error processing file: {e}")
