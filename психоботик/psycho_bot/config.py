import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

# Доступные тесты
AVAILABLE_TESTS = {
    'lusher': '🎨 Тест Люшера',
    'rorschach': '🦋 Тест Роршаха',
    'love_language': '💝 Языки любви',
    'temperament': '🔥 Темперамент', 
    'zodiac': '♈ Знак зодиака по характеру',
    'personality': '📊 Личностный опросник'
}
# Состояния бота
CHOOSING_TEST, IN_TEST, TEST_COMPLETED = range(3)