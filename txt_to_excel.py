import pandas as pd
import re

# Read the text file
with open('questions.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove separator and header lines
rows = []
for line in lines:
    # Skip lines that are just separators or empty
    if re.match(r'^\s*\|[- ]+\|', line) or line.strip() == '':
        continue
    # Remove leading/trailing whitespace and split by '|'
    parts = [col.strip() for col in line.strip().strip('|').split('|')]
    if len(parts) == 3:
        rows.append(parts)

# Create DataFrame and write to Excel
if rows:
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.to_excel('questions.xlsx', index=False)
    print('questions.xlsx has been created from questions.txt.')
else:
    print('No valid data found in questions.txt.')
