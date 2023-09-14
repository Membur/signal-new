import csv

# Read the CSV data
data = []
with open('symbols.csv', mode='r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    for row in csvreader:
        data.append(row)

# Sort the data alphabetically by ticker (the first column)
sorted_data = sorted(data, key=lambda x: x[0])

# Write the sorted data to a new CSV file
with open('sorted_symbols.csv', mode='w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)  # Write the header
    csvwriter.writerows(sorted_data)  # Write the sorted data
