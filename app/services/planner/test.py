import json
from planner_validator import validate_presentation

# Load the JSON presentation file
with open("app/services/planner/dummy_valid.json", "r") as f:
    presentation_data = json.load(f)

# Validate
result = validate_presentation(presentation_data)

# Print the results
print(json.dumps(result, indent=2))
