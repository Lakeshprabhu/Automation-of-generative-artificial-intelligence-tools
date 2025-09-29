import csv

from openai import Chatgpt
import pandas





prompt = """You will be given a file with the following columns:
index, category, question, questiontype, answer, and insights.

Your task:

Answer the question only if the questiontype is "text-based".
If it is "NA" or "image-based", skip it (return an empty string).

If a row has questiontype = "reference", treat the question as supporting material — do not answer it.
Use it to help answer the text-based questions that appear below it, until the next reference appears or the section ends.

For each answered question, also generate a short explanation in the insights column describing the logic used to derive the answer.
If a reference was used, mention that in the insight.

Output Instructions:

Return only a JSON array of strings.

Each string corresponds positionally to a row in the input file.

For skipped rows (e.g. references, images, or NA), return an empty string ("") in that position.

Your response must be valid JSON — no comments, keys, or labels.

Example output for answer column:

json
Copy
Edit
["", "", "The capital of France is Paris.", "", "Photosynthesis converts light into energy.", ""]
Example output for insights column:

json
Copy
Edit
["", "", "Paris is the capital of France based on general knowledge.", "", "Derived from the provided reference on plant biology.", ""]
⚠️ Output must be a plain JSON array — nothing else. This is so it can be directly pasted into a column of the CSV.



"""

rows = []



with open(r"C:\Users\thang\Downloads\project by chatgpt - Sheet1 (1).csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# Convert to string for the prompt
csv_data = "\n".join([str(row) for row in rows])



communication = Chatgpt(prompt,"B",csv_data)

communication.get_response()

print(communication.get_response())