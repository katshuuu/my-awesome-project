from .base_test import BaseTest

class TemperamentTest(BaseTest):
    def __init__(self):
        super().__init__("temperament")
        self.temperaments = {
            "sanguine": "Сангвиник 🎭",
            "choleric": "Холерик 🔥", 
            "phlegmatic": "Флегматик 🧊",
            "melancholic": "Меланхолиik 🌙"
        }
        self.setup_questions()
    
    def setup_questions(self):
        self.questions = [
            {
                "text": "🔥 Как вы реагируете на неожиданные изменения?",
                "type": "choice",
                "options": [
                    "🎭 Быстро адаптируюсь, нахожу возможности",
                    "🔥 Активно действую, беру контроль",
                    "🧊 Сохраняю спокойствие, анализирую",
                    "🌙 Переживаю,担心юсь о последствиях"
                ]
            },
            {
                "text": "🔥 Ваше отношение к новым знакомствам?",
                "type": "choice",
                "options": [
                    "🎭 Легко иду на контакт, общителен",
                    "🔥 Беру инициативу, веду беседу",
                    "🧊 Наблюдаю со стороны, осторожен",
                    "🌙 Стесняюсь, предпочитаю знакомых"
                ]
            },
            {
                "text": "🔥 Как вы принимаете решения?",
                "type": "choice", 
                "options": [
                    "🎭 Быстро,基于 на intuition",
                    "🔥 Решительно, уверенно",
                    "🧊 Взвешенно, аналитически",
                    "🌙 Осторожно, с сомнениями"
                ]
            },
            {
                "text": "🔥 Ваша рабочая стиль?",
                "type": "choice",
                "options": [
                    "🎭 Многозадачность, быстро переключаюсь",
                    "🔥 Энергично, целеустремленно",
                    "🧊 Методично, систематически",
                    "🌙 Вдумчиво,注重 детали"
                ]
            },
            {
                "text": "🔥 Как вы выражаете эмоции?",
                "type": "choice",
                "options": [
                    "🎭 Ярко, открыто, заразительно",
                    "🔥 Интенсивно, страстно",
                    "🧊 Сдержанно, контролированно",
                    "🌙 Глубоко, но скрытно"
                ]
            }
        ]
    
    def calculate_result(self):
        temperament_scores = {key: 0 for key in self.temperaments.keys()}
        temperament_map = {
            0: "sanguine", 1: "choleric", 2: "phlegmatic", 3: "melancholic"
        }
        
        for answer_index in self.answers:
            temperament_key = temperament_map[answer_index]
            temperament_scores[temperament_key] += 1
        
        return temperament_scores
    
    def generate_report(self, results):
        primary_temp = max(results.items(), key=lambda x: x[1])
        secondary_temp = sorted(results.items(), key=lambda x: x[1], reverse=True)[1]
        
        temp_descriptions = {
            "sanguine": "Жизнерадостный, общительный, оптимистичный. Быстро загорается и остывает. Любит новизну и перемены.",
            "choleric": "Энергичный, целеустремленный, лидер. Решителен и прямолинеен. Склонен к доминированию.",
            "phlegmatic": "Спокойный, уравновешенный, reliable. Методичен и последователен. Избегает конфликтов.",
            "melancholic": "Чувствительный, вдумчивый, перфекционист. Глубоко переживает эмоции.注重 детали."
        }
        
        report = f"""
🔥 **Результаты теста на темперамент**

**Ваш основной темперамент:**
{self.temperaments[primary_temp[0]]} - {primary_temp[1]}/5 баллов

**Второстепенный темперамент:**
{self.temperaments[secondary_temp[0]]} - {secondary_temp[1]}/5 баллов

📊 **Распределение баллов:**
{self.format_scores(results)}

💡 **Описание вашего темперамента:**
{temp_descriptions[primary_temp[0]]}

🌟 **Сильные стороны:**
{self.get_strengths(primary_temp[0])}

⚠️ **Зоны роста:**
{self.get_weaknesses(primary_temp[0])}

💼 **Профессиональные рекомендации:**
{self.get_career_advice(primary_temp[0])}
"""
        return report
    
    def format_scores(self, scores):
        lines = []
        for temp, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"• {self.temperaments[temp]}: {score}/5")
        return "\n".join(lines)
    
    def get_strengths(self, temperament):
        strengths = {
            "sanguine": "Коммуникабельность, адаптивность, оптимизм, энергичность",
            "choleric": "Лидерство, решительность, целеустремленность, efficiency",
            "phlegmatic": "Спокойствие, reliability, терпение, дипломатичность", 
            "melancholic": "Аналитичность, внимательность, креативность, глубина"
        }
        return strengths[temperament]
    
    def get_weaknesses(self, temperament):
        weaknesses = {
            "sanguine": "Поверхностность, непостоянство, impulsiveness",
            "choleric": "Агрессивность, нетерпимость, доминантность",
            "phlegmatic": "Пассивность, медлительность, инертность",
            "melancholic": "Пессимизм, тревожность, перфекционизм"
        }
        return weaknesses[temperament]
    
    def get_career_advice(self, temperament):
        advice = {
            "sanguine": "Продажи, PR, event-менеджмент, teaching, творческие профессии",
            "choleric": "Руководство, предпринимательство, спорт, юриспруденция",
            "phlegmatic": "Администрирование, бухгалтерия, IT, research, медицина",
            "melancholic": "Искусство, дизайн, психология, writing, аналитика"
        }
        return advice[temperament]