import pandas as pd

# Load the CSV file
file_path = 'compare.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Calculate the number of correct predictions
correct_predictions = (df['My prediction'] == df['Actual answer']).sum()

# Calculate the total number of predictions
total_predictions = len(df)

# Calculate the percentage of correct predictions
percentage_correct = (correct_predictions / total_predictions) * 100

print(f'Percentage of correct predictions: {percentage_correct:.2f}%')
