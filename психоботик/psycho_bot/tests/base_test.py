from abc import ABC, abstractmethod

class BaseTest(ABC):
    def __init__(self, test_name):
        self.test_name = test_name
        self.questions = []
        self.current_question = 0
        self.answers = []
    
    @abstractmethod
    def setup_questions(self):
        pass
    
    @abstractmethod
    def calculate_result(self):
        pass
    
    @abstractmethod
    def generate_report(self, results):
        pass
    
    def get_current_question(self):
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None
    
    def add_answer(self, answer):
        self.answers.append(answer)
        self.current_question += 1
    
    def is_completed(self):
        return self.current_question >= len(self.questions)
    
    def get_progress(self):
        return f"{self.current_question}/{len(self.questions)}"