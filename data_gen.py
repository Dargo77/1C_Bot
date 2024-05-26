import json
import random

questions = {}

for i in range(1, 101):
    question = f"Вопрос {i}"
    answers = [f"Вариант ответа {i}-{j}" for j in range(1, 5)]
    correct_answer = random.choice(answers)

    questions[question] = {
        "ответы": answers,
        "правильный ответ": correct_answer
    }

json_data = json.dumps(questions, indent=4, ensure_ascii=False)

with open("questions.json", "w", encoding="utf-8") as file:
    file.write(json_data)

print("Файл 'questions.json' успешно создан с 100 случайными вопросами и ответами.")
