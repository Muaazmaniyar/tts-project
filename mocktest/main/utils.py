import csv
import os
from django.conf import settings

def get_questions_from_csv():
    questions = []
    # Hardcode your single course file here
    file_path = os.path.join(settings.BASE_DIR, 'Courses', 'math.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError("CSV file for course not found.")
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append({
                'question_text': row['question_text'],
                'option1': row['option1'],
                'option2': row['option2'],
                'option3': row['option3'],
                'option4': row['option4'],
                'correct_option': row['correct_option']
            })
    
    return questions
