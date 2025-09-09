import random
import os
from telegram import InputFile
from .base_test import BaseTest

class RorschachTest(BaseTest):
    def __init__(self):
        super().__init__("rorschach")
        self.images = ["blot1", "blot2", "blot3", "blot4", "blot5", "blot6", "blot7", "blot8", "blot9", "blot10"]
        self.setup_questions()
    
    def setup_questions(self):
        self.questions = []
        for i, blot in enumerate(self.images):
            self.questions.append({
                "text": f"🦋 Что вы видите на этом изображении? Опишите ассоциацию.",
                "type": "text_input",
                "image": f"images/rorschach/{blot}.jpg",
                "image_caption": f"Пятно Роршаха {i+1}/10"
            })
    
    def get_image_path(self, image_name):
        """Получает полный путь к изображению"""
        # Путь относительно корневой директории проекта
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), image_name)
    
    async def send_question(self, update, context, question):
        """Отправляет вопрос с изображением"""
        image_path = self.get_image_path(question["image"])
        
        # Проверяем существует ли файл
        if os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=InputFile(photo),
                        caption=question["text"]
                    )
            except Exception as e:
                # Если не удалось отправить фото, отправляем текст
                await update.message.reply_text(
                    f"{question['text']}\n\n(Изображение временно недоступно)"
                )
        else:
            # Если файл не найден
            await update.message.reply_text(
                f"{question['text']}\n\n⚠️ Изображение не найдено по пути: {image_path}"
            )
    
    def calculate_result(self):
        # Анализ ответов
        analysis = {
            "animal_count": 0,
            "human_count": 0, 
            "object_count": 0,
            "abstract_count": 0,
            "response_length": 0
        }
        
        for answer in self.answers:
            if answer:  # Проверяем что ответ не пустой
                answer_lower = answer.lower()
                analysis["response_length"] += len(answer)
                
                if any(word in answer_lower for word in ["животн", "звер", "птиц", "насеком", "animal", "beast"]):
                    analysis["animal_count"] += 1
                elif any(word in answer_lower for word in ["человек", "лицо", "фигура", "тело", "person", "human", "face"]):
                    analysis["human_count"] += 1
                elif any(word in answer_lower for word in ["предмет", "вещь", "объект", "строение", "object", "thing", "building"]):
                    analysis["object_count"] += 1
                else:
                    analysis["abstract_count"] += 1
        
        return analysis
    
    def generate_report(self, results):
        total_responses = len(self.answers)
        if total_responses == 0:
            return "❌ Не получено ни одного ответа для анализа."
        
        animal_percent = (results["animal_count"] / total_responses) * 100
        human_percent = (results["human_count"] / total_responses) * 100
        object_percent = (results["object_count"] / total_responses) * 100
        abstract_percent = (results["abstract_count"] / total_responses) * 100
        
        avg_length = results["response_length"] / total_responses if total_responses > 0 else 0
        
        report = f"""
🦋 **Результаты теста Роршаха**

📝 Проанализировано ответов: {total_responses}

**Типы ассоциаций:**
🐶 Животные: {animal_percent:.1f}%
👥 Люди: {human_percent:.1f}%  
📦 Объекты: {object_percent:.1f}%
🎭 Абстрактные: {abstract_percent:.1f}%

📊 Средняя длина ответа: {avg_length:.1f} символов

**Интерпретация:**
{self.get_interpretation(animal_percent, human_percent, object_percent, abstract_percent, avg_length)}
"""
        return report
    
    def get_interpretation(self, animal, human, object_p, abstract, avg_len):
        interpretations = []
        
        if animal > 40:
            interpretations.append("• Вы обладаете сильными инстинктами и природной энергией.")
        elif animal < 20:
            interpretations.append("• Вы больше ориентированы на абстрактные концепции, чем на природные.")
        
        if human > 30:
            interpretations.append("• Вы социально ориентированы и внимательны к людям.")
        elif human < 15:
            interpretations.append("• Вы более интровертны и сосредоточены на внутреннем мире.")
        
        if object_p > 25:
            interpretations.append("• Вы практичны и ориентированы на материальный мир.")
        elif object_p < 10:
            interpretations.append("• Вы менее материалистичны и больше цените идеи.")
        
        if abstract > 35:
            interpretations.append("• Вы обладаете развитым абстрактным мышлением.")
        elif abstract < 20:
            interpretations.append("• Вы более конкретны и практичны в мышлении.")
        
        if avg_len > 50:
            interpretations.append("• Вы подробны и внимательны к деталям.")
        elif avg_len < 20:
            interpretations.append("• Вы лаконичны и прямолинейны в мышлении.")
        else:
            interpretations.append("• Вы balanced в выражениях мыслей.")
        
        return "\n".join(interpretations)