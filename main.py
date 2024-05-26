from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
from config import TOKEN

# Читаем JSON файл с вопросами
with open('questions.json', 'r', encoding='utf-8') as file:
    questions = json.load(file)

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Обработчик команды /start
@dp.message_handler(commands='start')
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=1)
    markup.add(types.KeyboardButton('Начать тестирование'))
    markup.add(types.KeyboardButton('Статистика'))

    await message.answer('Привет!', reply_markup=markup)


# Переменная для хранения данных о пользователе
user_data = {}


# Обработчик кнопки "Начать тестирование"
@dp.message_handler(lambda message: message.text == 'Начать тестирование')
async def start_exam(message: types.Message):
    # Инициализируем данные пользователя
    user_id = message.from_user.id
    user_data[user_id] = {
        'questions_count': 0,
        'score': 0
    }
    
    # Сбрасываем данные о прошлом тестирование
    user_data[user_id]['questions_count'] = 0
    user_data[user_id]['score'] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=1)
    markup.add(types.KeyboardButton('Начать тестирование'))
    await message.answer("Статистика сброшена. Начинаем новое тестирование!")
    await ask_question(message)


# Обработчик кнопки "Начать новое тестирование"
@dp.message_handler(lambda message: message.text == 'Начать новое тестирование')
async def start_exam(message: types.Message):
    # Инициализируем данные пользователя
    user_id = message.from_user.id
    user_data[user_id] = {
        'questions_count': 0,
        'score': 0
    }
    
    # Сбрасываем данные о прошлом тестирование
    user_data[user_id]['questions_count'] = 0
    user_data[user_id]['score'] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=1)
    markup.add(types.KeyboardButton('Начать новое тестирование'))
    await message.answer("Статистика сброшена. Начинаем новое тестирование!")
    await ask_question(message)


# Функция для отправки вопроса
async def ask_question(message: types.Message):
    user_id = message.from_user.id
    current_question_index = user_data[user_id]['questions_count']
    current_question = list(questions.keys())[current_question_index]
    answer_options = questions[current_question]['ответы']

    markup = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True, row_width=1)
    markup.add(*answer_options)
    markup.add(types.KeyboardButton('Статистика'))
    markup.add(types.KeyboardButton('Начать новое тестирование'))

    await message.answer(f"{current_question}", reply_markup=markup)


# Обработчик ответов на вопросы
@dp.message_handler(lambda message: message.text in questions[list(questions.keys())[user_data[message.from_user.id]['questions_count']]]['ответы'])
async def process_answer(message: types.Message):
    user_id = message.from_user.id
    current_question_index = user_data[user_id]['questions_count']
    current_question = list(questions.keys())[current_question_index]
    correct_answer = questions[current_question]['правильный ответ']
    user_answer = message.text

    # Проверяем ответ пользователя
    if user_answer == correct_answer:
        user_data[user_id]['score'] += 1
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

    # Переходим к следующему вопросу
    user_data[user_id]['questions_count'] += 1

    # Проверяем, если достигнут конец тестированиеа
    if user_data[user_id]['questions_count'] == len(questions):
        await show_statistics(message)
    else:
        await ask_question(message)


# Функция для вывода статистики
@dp.message_handler(lambda message: message.text.lower() == "статистика")
async def show_statistics(message: types.Message):
    user_id = message.from_user.id
    score = user_data[user_id]['score']
    questions_count = len(questions)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=1)
    markup.add(types.KeyboardButton('Начать новое тестирование'))

    await message.answer(f"Вы набрали {score} очков из {questions_count}", reply_markup=markup)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)