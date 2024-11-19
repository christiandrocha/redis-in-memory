from quiz_manager import QuizManager

# Inicializa o gerenciador de quizzes
quiz_manager = QuizManager()

# Dados do quiz e das perguntas
quiz_data = {
    "quiz_id": "1",
    "title": "Quiz de Conhecimentos Gerais",
    "description": "Teste seus conhecimentos em várias áreas",
    "questions": [
        {
            "question_id": "1",
            "text": "Qual é a capital da França?",
            "options": {
                "A": "Berlim",
                "B": "Madrid",
                "C": "Paris",
                "D": "Lisboa"
            },
            "correct_answer": "option_C"
        },
        {
            "question_id": "2",
            "text": "Quem pintou a Mona Lisa?",
            "options": {
                "A": "Vincent Van Gogh",
                "B": "Pablo Picasso",
                "C": "Leonardo da Vinci",
                "D": "Michelangelo"
            },
            "correct_answer": "option_C"
        },
        {
            "question_id": "3",
            "text": "Qual é o maior planeta do Sistema Solar?",
            "options": {
                "A": "Terra",
                "B": "Marte",
                "C": "Júpiter",
                "D": "Saturno"
            },
            "correct_answer": "option_C"
        }
    ]
}

# Define o TTL em segundos (30 dias)
# Tempo de 30 dias;
TTL_TIME = 30 * 24 * 60 * 60 
# TTL_TIME = 10
# Cria o quiz com título e descrição
def create_quiz():
    quiz_manager.create_quiz(
        quiz_id=quiz_data["quiz_id"],
        title=quiz_data["title"],
        description=quiz_data["description"]
    )
    # Define o TTL para o quiz
    quiz_manager.set_ttl(f"quiz:{quiz_data['quiz_id']}", TTL_TIME)
    print(f"Quiz '{quiz_data['quiz_id']}' criado com sucesso.")

# Adiciona perguntas ao quiz
def add_questions():
    for question in quiz_data["questions"]:
        quiz_manager.add_question(
            quiz_id=quiz_data["quiz_id"],
            question_id=question["question_id"],
            text=question["text"],
            options=question["options"],
            correct_answer=question["correct_answer"]
        )
        # Define o TTL para cada pergunta
        quiz_manager.set_ttl(f"quiz:{quiz_data['quiz_id']}:question:{question['question_id']}", TTL_TIME)
        print(f"Pergunta '{question['question_id']}' adicionada com sucesso.")

# Função principal para executar a criação do quiz e adição de perguntas
def main():
    create_quiz()
    add_questions()
    print("Quiz e perguntas adicionadas ao Redis para simulação.")

if __name__ == "__main__":
    main()