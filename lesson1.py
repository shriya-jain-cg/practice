import pandas as pd
from datetime import datetime

# Read the login log file
log_path = r"c:/Users/shriyjai/Downloads/Login_log.txt"
with open(log_path, "r") as f:
    lines = f.readlines()

def parse_line(line):
    # Example: "username | role | created_at | expires_at"
    parts = [p.strip() for p in line.strip().split('|')]
    if len(parts) < 4 or parts[0] == "username":
        return None
    username = parts[0]
    created_at_str = parts[2]
    expires_at_str = parts[3]
    try:
        created_at = pd.to_datetime(created_at_str)
        expires_at = pd.to_datetime(expires_at_str)
    except Exception:
        return None
    return {"username": username, "created_at": created_at, "expires_at": expires_at}

records = [parse_line(line) for line in lines]
records = [r for r in records if r is not None]
df = pd.DataFrame(records)

# Calculate session duration in seconds
df['session_seconds'] = (df['expires_at'] - df['created_at']).dt.total_seconds()

# Add week_start and week_end columns
# Week starts on Monday (isoweekday=1)
df['week_start'] = df['created_at'].dt.to_period('W').apply(lambda r: r.start_time.date())
df['week_end'] = df['created_at'].dt.to_period('W').apply(lambda r: r.end_time.date())

# Group by username, week_start, week_end and count logins
weekly_logins = df.groupby(['username', 'week_start', 'week_end']).size().reset_index(name='login_count')

# Save the weekly login count report to an Excel file
excel_output_path = r"c:/Users/shriyjai/Downloads/weekly_login_count_report.xlsx"
weekly_logins[['username', 'week_start', 'week_end', 'login_count']].to_excel(excel_output_path, index=False)

print("Weekly login count by user:")
print(weekly_logins[['username', 'week_start', 'week_end', 'login_count']])
print(f"Report saved to: {excel_output_path}")

# Read the token log file, skipping the header and separator lines
log_path = r"c:/Users/shriyjai/Downloads/token_log.txt"
with open(log_path, "r") as f:
    lines = f.readlines()

# Remove header and separator lines
data_lines = [line for line in lines if not (line.strip().startswith('username') or set(line.strip()) == set('-+|'))]

# Parse each line into columns
records = []
for line in data_lines:
    parts = [p.strip() for p in line.strip().split('|')]
    if len(parts) < 5:
        continue
    username = parts[0]
    tokens_used = int(parts[2]) if parts[2] else 0
    usage_percentage = float(parts[3]) if parts[3] else 0.0
    records.append({
        'username': username,
        'tokens_used': tokens_used,
        'usage_percentage': usage_percentage
    })

df_tokens = pd.DataFrame(records)

# Merge token usage info into weekly login count report
weekly_logins = weekly_logins.merge(df_tokens, on='username', how='left')

# Save the merged report to Excel
excel_output_path = r"c:/Users/shriyjai/Downloads/weekly_login_count_report.xlsx"
weekly_logins[['username', 'week_start', 'week_end', 'login_count', 'tokens_used', 'usage_percentage']].to_excel(excel_output_path, index=False)

print("Weekly login count by user with token usage:")
print(weekly_logins[['username', 'week_start', 'week_end', 'login_count', 'tokens_used', 'usage_percentage']])
print(f"Report saved to: {excel_output_path}")