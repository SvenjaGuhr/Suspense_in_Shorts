import nltk
import glob
import os
import csv

# Ensure required NLTK models are downloaded
nltk.download('punkt')

from nltk.tokenize import sent_tokenize

# === CONFIGURATION ===
input_pattern = '/Users/your_path/Suspense/*.txt'
output_folder = '/Users/your_path/Suspense/for_annotation/'

# === PROCESS EACH TXT FILE ===
for txt_file in glob.glob(input_pattern):
    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Sentence splitting with NLTK
    sentences = sent_tokenize(text)

    # Prepare output CSV path
    base_name = os.path.basename(txt_file)
    csv_name = os.path.splitext(base_name)[0] + "_sentences.csv"
    output_path = os.path.join(output_folder, csv_name)

    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sentence_ID", "Sentence", "reader_suspense_level (0 = default; 1-5)", "character_anxiety_level (0 = default; 1-5)", "character", "suspense/anxiety-evoking_element", "arising_questions (optional)", "question_answered_in_Sentence_ID"])
        for i, sent in enumerate(sentences, start=1):
            writer.writerow([i, sent, "", "", ""])

    print(f"✅ {len(sentences)} sentences written to {output_path}")
