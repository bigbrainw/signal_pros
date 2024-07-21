import pandas as pd

def flip_values_in_true_label_columns(input_csv, output_csv):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Iterate through columns and flip values if column name contains 'True Label'
    for col in df.columns:
        if 'True Label' in col:
            df[col] = df[col].apply(lambda x: 1 if x == 0 else 0)
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

# Example usage
input_csv = 'answer.csv'  # Replace with your input file path
output_csv = 'correct_format.csv'  # Replace with your output file path
flip_values_in_true_label_columns(input_csv, output_csv)
