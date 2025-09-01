import csv, os
from django.conf import settings

def get_questions_from_csv():
    questions = []
    file_path = os.path.join(settings.BASE_DIR, 'myapp', 'fixtures', 'icd_part_a.csv')
    
    with open(file_path, newline='', encoding='cp1252') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append({
                'question_text': row['question'],
                'option1': row['option1'],
                'option2': row['option2'],
                'option3': row['option3'],
                'option4': row['option4'],
                'correct_option': row['correct_answer'],
            })
    return questions
