import redis

class QuizManager:
    def __init__(self):
        # Inicialize o cliente Redis aqui
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    def create_quiz(self, quiz_id, title, description):
        # Crie o hash para o quiz
        self.redis_client.hmset(f"quiz:{quiz_id}", {"title": title, "description": description})

    def add_question(self, quiz_id, question_id, text, options, correct_answer):
        # Crie o hash para a pergunta
        self.redis_client.hmset(f"quiz:{quiz_id}:question:{question_id}", {
            "text": text,
            "options": options,
            "correct_answer": correct_answer
        })

    def set_ttl(self, key, ttl):
        # Define o TTL usando o comando EXPIRE
        self.redis_client.expire(key, ttl)