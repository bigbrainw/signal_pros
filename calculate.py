import csv

def calculate_average(csv_file_path):
    total = 0
    count = 0

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if there is one

        for row in csv_reader:
            total += float(row[1])  # Convert the value to float and add to the total
            count += 1

    if count == 0:
        raise ValueError("The CSV file is empty or does not have any rows with data.")
    
    average = total / count
    return average

# Example usage
csv_file_path = 'alpha2.csv'
average_value = calculate_average(csv_file_path)
print(f"The average of the values in the second column is {average_value:.2f}")
