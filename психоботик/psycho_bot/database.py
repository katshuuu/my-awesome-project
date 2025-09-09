import json
import os
from datetime import datetime

class UserDatabase:
    def __init__(self, file_path='users_data.json'):
        self.file_path = file_path
        self.users = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def add_user(self, user_id, username, first_name):
        if str(user_id) not in self.users:
            self.users[str(user_id)] = {
                'username': username,
                'first_name': first_name,
                'registration_date': datetime.now().isoformat(),
                'tests_completed': 0,
                'test_history': []
            }
            self.save_data()
    
    def add_test_result(self, user_id, test_name, result):
        if str(user_id) in self.users:
            test_entry = {
                'test_name': test_name,
                'date': datetime.now().isoformat(),
                'result': result
            }
            self.users[str(user_id)]['test_history'].append(test_entry)
            self.users[str(user_id)]['tests_completed'] += 1
            self.save_data()
    
    def get_user_stats(self, user_id):
        if str(user_id) in self.users:
            return self.users[str(user_id)]
        return None

# Глобальный экземпляр базы данных
user_db = UserDatabase()