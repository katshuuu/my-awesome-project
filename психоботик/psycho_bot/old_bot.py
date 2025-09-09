import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    ContextTypes, ConversationHandler, filters
)
from config import BOT_TOKEN, AVAILABLE_TESTS, CHOOSING_TEST, IN_TEST, TEST_COMPLETED
from database import user_db
from tests.lusher import LusherTest
from tests.rorschach import RorschachTest
from tests.love_language import LoveLanguageTest
from tests.temperament import TemperamentTest
from tests.zodiac import ZodiacTest

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальные переменные для хранения состояния тестов
user_tests = {}

# Клавиатура с тестами
tests_keyboard = [
    [AVAILABLE_TESTS['lusher'], AVAILABLE_TESTS['rorschach']],
    [AVAILABLE_TESTS['love_language'], AVAILABLE_TESTS['temperament']],
    [AVAILABLE_TESTS['zodiac'], AVAILABLE_TESTS['personality']],
    ['📊 Моя статистика', '❌ Отмена']
]
reply_markup = ReplyKeyboardMarkup(tests_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the bot")
    
    # Добавляем пользователя в базу
    user_db.add_user(user.id, user.username, user.first_name)
    
    welcome_text = (
        "🧠 Добро пожаловать в бот психологических тестов!\n\n"
        "Здесь вы можете пройти различные психологические тесты "
        "и получить персональный анализ результатов.\n\n"
        "Выберите тест из меню ниже:"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    return CHOOSING_TEST

async def choose_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора теста"""
    user_choice = update.message.text
    user_id = update.message.from_user.id
    
    # Проверяем выбранный тест
    test_name = None
    for key, value in AVAILABLE_TESTS.items():
        if user_choice == value:
            test_name = key
            break
    if test_name == 'love_language':
        user_tests[user_id] = LoveLanguageTest()
    elif test_name == 'temperament':
        user_tests[user_id] = TemperamentTest()
    elif test_name == 'zodiac':
        user_tests[user_id] = ZodiacTest()
    elif test_name == 'rorschach':
        user_tests[user_id] = RorschachTest()
        test = user_tests[user_id]
        question = test.get_current_question()
        
        # Используем специальный метод для отправки с изображением
        if hasattr(test, 'send_question') and callable(getattr(test, 'send_question')):
            await test.send_question(update, context, question)
        else:
            await update.message.reply_text(question["text"])
        
        return IN_TEST
    # ... остальная логика выбора тестов
    
    if user_choice == '📊 Моя статистика':
        stats = user_db.get_user_stats(user_id)
        if stats:
            response = (
                f"📊 Ваша статистика:\n\n"
                f"👤 Имя: {stats['first_name']}\n"
                f"✅ Пройдено тестов: {stats['tests_completed']}\n"
                f"📅 Зарегистрирован: {stats['registration_date'][:10]}\n\n"
                f"Последние тесты:\n"
            )
            for test in stats['test_history'][-3:]:
                response += f"• {test['test_name']} - {test['date'][:10]}\n"
        else:
            response = "Статистика не найдена."
        
        await update.message.reply_text(response, reply_markup=reply_markup)
        return CHOOSING_TEST
    
    if test_name:
        # Инициализируем выбранный тест
        if test_name == 'lusher':
            user_tests[user_id] = LusherTest()
        elif test_name == 'rorschach':
            user_tests[user_id] = RorschachTest()
        else:
            # Для других тестов можно добавить аналогично
            await update.message.reply_text(
                "Этот тест в разработке 🛠️",
                reply_markup=reply_markup
            )
            return CHOOSING_TEST
        
        # Получаем первый вопрос
        test = user_tests[user_id]
        question = test.get_current_question()
        
        if question:
            if question['type'] == 'color_choice':
                # Создаем клавиатуру с цветами
                color_keys = [[color['emoji'] for color in question['options'][i:i+4]] 
                             for i in range(0, len(question['options']), 4)]
                color_markup = ReplyKeyboardMarkup(color_keys, one_time_keyboard=True, resize_keyboard=True)
                
                await update.message.reply_text(
                    question['text'],
                    reply_markup=color_markup
                )
            else:
                await update.message.reply_text(
                    question['text'],
                    reply_markup=ReplyKeyboardRemove()
                )
            
            return IN_TEST
    
    await update.message.reply_text(
        "Пожалуйста, выберите тест из меню!",
        reply_markup=reply_markup
    )
    return CHOOSING_TEST

async def handle_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ответов в тесте"""
    user_id = update.message.from_user.id
    user_answer = update.message.text
    
    if user_id not in user_tests:
        await update.message.reply_text(
            "Тест не найден. Начните заново с /start",
            reply_markup=reply_markup
        )
        return CHOOSING_TEST
    
    test = user_tests[user_id]
    
    # Обрабатываем ответ
    current_question = test.get_current_question()
    
    # Добавляем ответ (проверяем тип вопроса)
    if current_question['type'] == 'color_choice':
        # Обработка цветового выбора (для Люшера)
        color_code = None
        for color in current_question['options']:
            if color['emoji'] == user_answer:
                color_code = color['code']
                break
        if color_code:
            test.add_answer(color_code)
        else:
            await update.message.reply_text("Пожалуйста, выберите вариант из предложенных!")
            return IN_TEST
    else:
        # Для текстовых ответов (Роршах и другие)
        test.add_answer(user_answer)
    
    # Проверяем завершение теста
    if test.is_completed():
        # Вычисляем результаты
        results = test.calculate_result()
        report = test.generate_report(results)
        
        # Сохраняем результаты
        user_db.add_test_result(user_id, test.test_name, results)
        
        # Отправляем отчет
        await update.message.reply_text(
            report,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        # Очищаем тест
        del user_tests[user_id]
        
        return CHOOSING_TEST
    else:
        # Следующий вопрос
        next_question = test.get_current_question()
        
        # ОСОБЕННОСТЬ: Для теста Роршаха отправляем изображения
        if hasattr(test, 'send_question') and callable(getattr(test, 'send_question')):
            # Если тест имеет метод send_question, используем его
            await test.send_question(update, context, next_question)
        else:
            # Стандартная обработка для других тестов
            if next_question['type'] == 'color_choice':
                color_keys = [[color['emoji'] for color in next_question['options'][i:i+4]] 
                             for i in range(0, len(next_question['options']), 4)]
                color_markup = ReplyKeyboardMarkup(color_keys, one_time_keyboard=True, resize_keyboard=True)
                
                await update.message.reply_text(
                    next_question['text'],
                    reply_markup=color_markup
                )
            else:
                await update.message.reply_text(
                    next_question['text'],
                    reply_markup=ReplyKeyboardRemove()
                )
        
        return IN_TEST

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик отмены"""
    user_id = update.message.from_user.id
    
    if user_id in user_tests:
        del user_tests[user_id]
    
    await update.message.reply_text(
        'Тест отменен. До свидания! 👋',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            'Произошла ошибка 😢 Попробуйте еще раз позже!',
            reply_markup=reply_markup
        )

def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Настраиваем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_TEST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_test)
            ],
            IN_TEST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_test_answer)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('cancel', cancel))
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🧠 Психологический бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()