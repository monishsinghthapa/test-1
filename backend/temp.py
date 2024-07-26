import re

# Example text
text = "The year 2023 is coming soon."

# Regex pattern to match a year (1000-2999)
pattern = r"\b(1[0-9]{3}|2[0-9]{3})\b"

# Using re.findall() to extract all matched years from the text
matched_years = re.findall(pattern, text)

print(matched_years)  # Output: ['2023']
