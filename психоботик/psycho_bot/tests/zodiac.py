from .base_test import BaseTest

class ZodiacTest(BaseTest):
    def __init__(self):
        super().__init__("zodiac")
        self.zodiac_signs = {
            "aries": "Овен ♈", "taurus": "Телец ♉", "gemini": "Близнецы ♊",
            "cancer": "Рак ♋", "leo": "Лев ♌", "virgo": "Дева ♍",
            "libra": "Весы ♎", "scorpio": "Скорпион ♏", "sagittarius": "Стрелец ♐",
            "capricorn": "Козерог ♑", "aquarius": "Водолей ♒", "pisces": "Рыбы ♓"
        }
        self.setup_questions()
    
    def setup_questions(self):
        self.questions = [
            {
                "text": "♈ Как вы подходите к достижению целей?",
                "type": "choice",
                "options": [
                    "♈ Решительно и напролом",
                    "♉ Упорно и методично", 
                    "♊ Используя интеллект и общение",
                    "♋ Чувствуя интуитивно правильный путь",
                    "♌ Ярко и заметно для всех",
                    "♍ Совершенствуя каждый шаг",
                    "♎ Взвешивая все варианты",
                    "♏ Стратегически и глубоко",
                    "♐ С оптимизмом и adventure",
                    "♑ Ответственно и дисциплинированно",
                    "♒ Инновационно и нестандартно",
                    "♓ Творчески и мечтательно"
                ]
            },
            {
                "text": "♈ Что для вас最重要的 в отношениях?",
                "type": "choice",
                "options": [
                    "♈ Страсть и excitement",
                    "♉ Надежность и стабильность",
                    "♊ Интеллектуальная связь",
                    "♋ Эмоциональная безопасность",
                    "♌ Восхищение и признание",
                    "♍ Практическая поддержка",
                    "♎ Гармония и баланс",
                    "♏ Глубина и интенсивность",
                    "♐ Свобода и adventure",
                    "♑ Уважение и традиции",
                    "♒ Дружба и innovation",
                    "♓ Духовная связь и romance"
                ]
            },
            {
                "text": "♈ Как вы отдыхаете?",
                "type": "choice", 
                "options": [
                    "♈ Активный спорт и competition",
                    "♉ Комфорт и хорошая еда",
                    "♊ Общение и новые знакомства",
                    "♋ Домашний уют и семья",
                    "♌ Творчество и самовыражение",
                    "♍ Порядок и организация",
                    "♎ Искусство и beauty",
                    "♏ Тайны и исследования",
                    "♐ Путешествия и философия",
                    "♑ Карьера и достижения",
                    "♒ Технологии и будущее",
                    "♓ Мечты и фантазии"
                ]
            },
            {
                "text": "♈ Ваш подход к проблемам?",
                "type": "choice",
                "options": [
                    "♈ Атаковать напрямую",
                    "♉ Упорно работать над решением",
                    "♊ Найти clever обходной путь",
                    "♋ Полагаться на интуицию",
                    "♌ Вдохновлять других на решение",
                    "♍ Анализировать и совершенствовать",
                    "♎ Искать компромисс",
                    "♏ Преобразовать проблему в opportunity",
                    "♐ Видеть bigger picture",
                    "♑ Системный и disciplined подход",
                    "♒ Инновационное решение",
                    "♓ Творческий и гибкий подход"
                ]
            },
            {
                "text": "♈ Что вас мотивирует?",
                "type": "choice",
                "options": [
                    "♈ Вызов и competition",
                    "♉ Материальная стабильность",
                    "♊ Интеллектуальный интерес",
                    "♋ Эмоциональная connection",
                    "♌ Признание и слава",
                    "♍ Стремление к perfection",
                    "♎ Красота и гармония",
                    "♏ Власть и transformation",
                    "♐ Свобода и истина",
                    "♑ Статус и achievements",
                    "♒ Прогресс и innovation",
                    "♓ Вдохновение и dreams"
                ]
            }
        ]
    
    def calculate_result(self):
        zodiac_scores = {key: 0 for key in self.zodiac_signs.keys()}
        zodiac_map = {
            0: "aries", 1: "taurus", 2: "gemini", 3: "cancer",
            4: "leo", 5: "virgo", 6: "libra", 7: "scorpio",
            8: "sagittarius", 9: "capricorn", 10: "aquarius", 11: "pisces"
        }
        
        for answer_index in self.answers:
            zodiac_key = zodiac_map[answer_index]
            zodiac_scores[zodiac_key] += 1
        
        return zodiac_scores
    
    def generate_report(self, results):
        primary_zodiac = max(results.items(), key=lambda x: x[1])
        secondary_zodiac = sorted(results.items(), key=lambda x: x[1], reverse=True)[1]
        
        zodiac_descriptions = {
            "aries": "Энергичный, смелый, impulsive. Первопроходец с сильной волей.",
            "taurus": "Надежный, практичный, sensual. Ценит комфорт и стабильность.",
            "gemini": "Коммуникабельный, интеллектуальный, adaptable. Любознательный и versatile.",
            "cancer": "Чувствительный, nurturing, intuitive. Сильная emotional intelligence.",
            "leo": "Творческий, гордый, generous. Прирожденный лидер с charisma.",
            "virgo": "Аналитичный, practical, perfectionist.注重 детали и service.",
            "libra": "Дипломатичный, harmonious, artistic. Стремится к balance и beauty.",
            "scorpio": "Интенсивный, passionate, transformative. Глубокий и mysterious.",
            "sagittarius": "Оптимистичный, adventurous, philosophical. Свободолюбивый и truth-seeking.",
            "capricorn": "Дисциплинированный, ambitious, responsible. Сильный work ethic.",
            "aquarius": "Инновационный, independent, humanitarian. Прогрессивный и original.",
            "pisces": "Сострадательный, creative, intuitive. Мечтательный и spiritual."
        }
        
        report = f"""
♈ **Результаты теста на знак зодиака по характеру**

**Ваш характер соответствует знаку:**
{self.zodiac_signs[primary_zodiac[0]]} - {primary_zodiac[1]}/5 баллов

**Второстепенный знак:**
{self.zodiac_signs[secondary_zodiac[0]]} - {secondary_zodiac[1]}/5 баллов

📊 **Распределение баллов:**
{self.format_scores(results)}

💫 **Описание вашего знака:**
{zodiac_descriptions[primary_zodiac[0]]}

🌟 **Сильные качества:**
{self.get_strengths(primary_zodiac[0])}

🌙 **Особенности характера:**
{self.get_traits(primary_zodiac[0])}

❤️ **Совместимость в отношениях:**
{self.get_compatibility(primary_zodiac[0])}

💼 **Профессиональные склонности:**
{self.get_career(primary_zodiac[0])}
"""
        return report
    
    def format_scores(self, scores):
        lines = []
        for zodiac, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"• {self.zodiac_signs[zodiac]}: {score}/5")
        return "\n".join(lines)
    
    def get_strengths(self, zodiac):
        strengths = {
            "aries": "Смелость, initiative, энергичность, прямота",
            "taurus": "Надежность, терпение, практичность, sensualность",
            "gemini": "Адаптивность, коммуникабельность, интеллект, curiosity",
            "cancer": "Эмпатия, забота, интуиция, loyalty",
            "leo": "Творчество, щедрость, лидерство, confidence",
            "virgo": "Аналитичность, внимание к деталям, service, практичность",
            "libra": "Дипломатичность, sense of beauty, гармония, fairness",
            "scorpio": "Страсть, глубина, resilience, transformational",
            "sagittarius": "Оптимизм, adventure, философия, honesty",
            "capricorn": "Дисциплина, ответственность, ambition, patience",
            "aquarius": "Инновационность, independence, гуманизм, originality",
            "pisces": "Сострадание, creativity, духовность, adaptability"
        }
        return strengths[zodiac]
    
    def get_traits(self, zodiac):
        traits = {
            "aries": "Импульсивный, competitive, прямой, enthusiastic",
            "taurus": "Упрямый, материалистичный, comfort-loving, steadfast",
            "gemini": "Непоследовательный, superficial, restless, versatile",
            "cancer": "Чувствительный, moody, protective, nostalgic",
            "leo": "Гордый, dramatic, fixed, generous",
            "virgo": "Критичный, worry-prone, modest, analytical",
            "libra": "Нерешительный, people-pleasing, indecisive, charming",
            "scorpio": "Ревнивый, secretive, intense, powerful",
            "sagittarius": "Безответственный, tactless, optimistic, freedom-loving",
            "capricorn": "Холодный, pessimistic, controlling, disciplined",
            "aquarius": "Отстраненный, unpredictable, unconventional, idealistic",
            "pisces": "Беспорядочный, escapist, oversensitive, compassionate"
        }
        return traits[zodiac]
    
    def get_compatibility(self, zodiac):
        compatibility = {
            "aries": "Лев, Стрелец, Близнецы - страсть и adventure",
            "taurus": "Дева, Козерог, Рак - стабильность и comfort",
            "gemini": "Весы, Водолей, Овен - интеллект и общение",
            "cancer": "Скорпион, Рыбы, Телец - эмоциональная глубина",
            "leo": "Овен, Стрелец, Близнецы - творчество и яркость",
            "virgo": "Телец, Козерог, Рак - практичность и забота",
            "libra": "Близнецы, Водолей, Лев - гармония и красота",
            "scorpio": "Рак, Рыбы, Дева - интенсивность и трансформация",
            "sagittarius": "Овен, Лев, Водолей - свобода и оптимизм",
            "capricorn": "Телец, Дева, Рыбы - ответственность и традиции",
            "aquarius": "Близнецы, Весы, Стрелец - инновации и дружба",
            "pisces": "Рак, Скорпион, Козерог - духовность и мечты"
        }
        return compatibility[zodiac]
    
    def get_career(self, zodiac):
        careers = {
            "aries": "Спорт, военное дело, предпринимательство, руководство",
            "taurus": "Финансы, кулинария, искусство, недвижимость",
            "gemini": "Журналистика, преподавание, продажи, коммуникации",
            "cancer": "Психология, уход, дизайн интерьеров, кулинария",
            "leo": "Артист, руководитель, дизайнер, event-менеджмент",
            "virgo": "Аналитика, здравоохранение, research, editing",
            "libra": "Дизайн, юриспруденция, дипломатия, искусство",
            "scorpio": "Психология, криминалистика, research, финансы",
            "sagittarius": "Путешествия, философия, преподавание, спорт",
            "capricorn": "Бизнес, управление, инженерия, политика",
            "aquarius": "Технологии, наука, социальная работа, innovation",
            "pisces": "Искусство, музыка, терапия, духовные практики"
        }
        return careers[zodiac]