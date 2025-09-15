import os
import csv
from django.conf import settings
from main.models import Question, Subject

def load_questions_from_csv():
    fixtures_dir = os.path.join(settings.BASE_DIR, 'fixtures')

    if not os.path.exists(fixtures_dir):
        print(f"❌ Fixtures folder not found at {fixtures_dir}")
        return

    csv_files = [f for f in os.listdir(fixtures_dir) if f.lower().endswith('.csv')]

    if not csv_files:
        print(f"❌ No CSV files found in {fixtures_dir}")
        return

    for filename in csv_files:
        try:
            subject_name = os.path.splitext(filename)[0]
            subject, _ = Subject.objects.get_or_create(name=subject_name)

            print(f"📄 Loading file: {filename}...")

            file_path = os.path.join(fixtures_dir, filename)
            with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                reader.fieldnames = [f.strip().lower() for f in reader.fieldnames]

                count = 0
                for row in reader:
                    if not row.get('question'):
                        continue

                    
                    if Question.objects.filter(subject=subject, question_text=row['question']).exists():
                        continue

                    Question.objects.create(
                        subject=subject,
                        question_text=row['question'].strip(),
                        option1=row['option1'].strip(),
                        option2=row['option2'].strip(),
                        option3=row['option3'].strip(),
                        option4=row['option4'].strip(),
                        correct_answer=row['correct_answer'].strip(),
                    )
                    count += 1

            print(f"✅ Loaded {count} questions for subject '{subject_name}'.")

        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")

    print("🎉 All CSV files processed successfully.")
