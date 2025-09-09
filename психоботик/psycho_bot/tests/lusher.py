import random
from .base_test import BaseTest

class LusherTest(BaseTest):
    def __init__(self):
        super().__init__("lusher")
        self.colors = [
            {"code": "blue", "emoji": "🔵", "name": "Синий"},
            {"code": "green", "emoji": "🟢", "name": "Зеленый"},
            {"code": "red", "emoji": "🔴", "name": "Красный"},
            {"code": "yellow", "emoji": "🟡", "name": "Желтый"},
            {"code": "purple", "emoji": "🟣", "name": "Фиолетовый"},
            {"code": "brown", "emoji": "🟤", "name": "Коричневый"},
            {"code": "black", "emoji": "⚫", "name": "Черный"},
            {"code": "gray", "emoji": "⚪", "name": "Серый"}
        ]
        self.setup_questions()
    
    def setup_questions(self):
        self.questions = [
            {
                "text": "🎨 Выберите цвет, который вам нравится больше всего в данный момент:",
                "type": "color_choice",
                "options": self.colors
            },
            {
                "text": "🎨 Теперь выберите второй по предпочтению цвет:",
                "type": "color_choice", 
                "options": self.colors
            },
            {
                "text": "🎨 Выберите третий цвет:",
                "type": "color_choice",
                "options": self.colors
            },
            {
                "text": "🎨 И четвертый цвет:",
                "type": "color_choice",
                "options": self.colors
            }
        ]
    
    def calculate_result(self):
        # Анализ выбора цветов
        color_meaning = {
            "blue": {"energy": 5, "calmness": 8, "creativity": 6},
            "green": {"energy": 6, "calmness": 7, "creativity": 5},
            "red": {"energy": 9, "calmness": 3, "creativity": 7},
            "yellow": {"energy": 7, "calmness": 4, "creativity": 8},
            "purple": {"energy": 4, "calmness": 6, "creativity": 9},
            "brown": {"energy": 3, "calmness": 7, "creativity": 4},
            "black": {"energy": 2, "calmness": 5, "creativity": 3},
            "gray": {"energy": 4, "calmness": 6, "creativity": 5}
        }
        
        scores = {"energy": 0, "calmness": 0, "creativity": 0}
        
        for i, color_code in enumerate(self.answers):
            weight = 4 - i  # Больший вес для первых выборов
            color_data = color_meaning.get(color_code, {})
            for key in scores:
                scores[key] += color_data.get(key, 0) * weight
        
        return scores
    
    def generate_report(self, results):
        energy = results["energy"]
        calmness = results["calmness"] 
        creativity = results["creativity"]
        
        # Генерация уникального отчета
        if energy > calmness and energy > creativity:
            personality = "Энергичный и активный"
        elif calmness > energy and calmness > creativity:
            personality = "Спокойный и уравновешенный"
        else:
            personality = "Творческий и креативный"
        
        report = f"""
📊 **Результаты теста Люшера**

🎨 Ваш выбор цветов: {', '.join([self.get_color_name(color) for color in self.answers])}

**Основные характеристики:**
⚡ Энергичность: {energy}/40
😌 Спокойствие: {calmness}/40  
🎨 Креативность: {creativity}/40

**Ваш психологический портрет:**
{personality}

💡 **Рекомендации:**
{self.get_recommendations(energy, calmness, creativity)}
"""
        return report
    
    def get_color_name(self, color_code):
        for color in self.colors:
            if color["code"] == color_code:
                return color["emoji"]
        return ""
    
    def get_recommendations(self, energy, calmness, creativity):
        if energy > 25:
            return "Вам полезны активные виды деятельности, спорт и динамичная работа."
        elif calmness > 25:
            return "Рекомендуются медитация, йога и спокойные хобби."
        else:
            return "Развивайте творческие навыки через искусство, музыку или писательство."