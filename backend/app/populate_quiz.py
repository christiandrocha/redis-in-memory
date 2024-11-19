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
        },
        {
            "question_id": "4",
            "text": "Qual é o elemento químico simbolizado por 'O'?",
            "options": {
                "A": "Ouro",
                "B": "Óxido",
                "C": "Oxigênio",
                "D": "Osmium"
            },
            "correct_answer": "option_C"
        },
        {
            "question_id": "5",
            "text": "Em que ano aconteceu a Primeira Guerra Mundial?",
            "options": {
                "A": "1914",
                "B": "1939",
                "C": "1945",
                "D": "1901"
            },
            "correct_answer": "option_A"
        },
        {
            "question_id": "6",
            "text": "Quem descobriu a teoria da relatividade?",
            "options": {
                "A": "Isaac Newton",
                "B": "Galileo Galilei",
                "C": "Nikola Tesla",
                "D": "Albert Einstein"
            },
            "correct_answer": "option_D"
        },
        {
            "question_id": "7",
            "text": "Qual é a moeda do Japão?",
            "options": {
                "A": "Yuan",
                "B": "Won",
                "C": "Yen",
                "D": "Rupia"
            },
            "correct_answer": "option_C"
        },
        {
            "question_id": "8",
            "text": "Qual é o maior oceano do mundo?",
            "options": {
                "A": "Índico",
                "B": "Pacífico",
                "C": "Atlântico",
                "D": "Ártico"
            },
            "correct_answer": "option_B"
        },
        {
            "question_id": "9",
            "text": "Qual é a língua mais falada no mundo?",
            "options": {
                "A": "Espanhol",
                "B": "Mandarim",
                "C": "Inglês",
                "D": "Árabe"
            },
            "correct_answer": "option_B"
        },
        {
            "question_id": "10",
            "text": "Quem escreveu 'Dom Quixote'?",
            "options": {
                "A": "William Shakespeare",
                "B": "Gabriel García Márquez",
                "C": "Miguel de Cervantes",
                "D": "José Saramago"
            },
            "correct_answer": "option_C"
        },
        {
            "question_id": "11",
            "text": "Em que país estão as pirâmides de Gizé?",
            "options": {
                "A": "Peru",
                "B": "Egito",
                "C": "México",
                "D": "China"
            },
            "correct_answer": "option_B"
        },
        {
            "question_id": "12",
            "text": "Qual é o órgão mais pesado do corpo humano?",
            "options": {
                "A": "Cérebro",
                "B": "Fígado",
                "C": "Pulmão",
                "D": "Coração"
            },
            "correct_answer": "option_B"
        },
        {
            "question_id": "13",
            "text": "Qual é o país com a maior população do mundo?",
            "options": {
                "A": "Estados Unidos",
                "B": "Índia",
                "C": "China",
                "D": "Rússia"
            },
            "correct_answer": "option_C"
        },
        {
            "question_id": "14",
            "text": "Qual é a principal língua falada no Brasil?",
            "options": {
                "A": "Inglês",
                "B": "Espanhol",
                "C": "Francês",
                "D": "Português"
            },
            "correct_answer": "option_D"
        },
        {
            "question_id": "15",
            "text": "Em que ano o homem pisou na Lua pela primeira vez?",
            "options": {
                "A": "1959",
                "B": "1965",
                "C": "1969",
                "D": "1972"
            },
            "correct_answer": "option_C"
        },
        {
            "question_id": "16",
            "text": "Qual foi a cidade sede das Olimpíadas de 2008?",
            "options": {
                "A": "Londres",
                "B": "Pequim",
                "C": "Tóquio",
                "D": "Atenas"
            },
            "correct_answer": "option_B"
        },
        {
            "question_id": "17",
            "text": "O Monte Everest está localizado em qual continente?",
            "options": {
                "A": "África",
                "B": "Ásia",
                "C": "América do Sul",
                "D": "Europa"
            },
            "correct_answer": "option_B"
        },
        {
            "question_id": "18",
            "text": "Quantos estados têm os Estados Unidos?",
            "options": {
                "A": "48",
                "B": "50",
                "C": "52",
                "D": "54"
            },
            "correct_answer": "option_B"
        },
        {
            "question_id": "19",
            "text": "Qual é a maior ilha do mundo?",
            "options": {
                "A": "Groenlândia",
                "B": "Madagascar",
                "C": "Nova Guiné",
                "D": "Islândia"
            },
            "correct_answer": "option_A"
        },
        {
            "question_id": "20",
            "text": "Qual é o nome da série de livros que inspirou o seriado 'Game of Thrones'?",
            "options": {
                "A": "Crônicas de Nárnia",
                "B": "Crônicas de Gelo e Fogo",
                "C": "O Senhor dos Anéis",
                "D": "Duna"
            },
            "correct_answer": "option_B"
        }
    ]
}

# Cria o quiz com título e descrição
def create_quiz():
    quiz_manager.create_quiz(
        quiz_id=quiz_data["quiz_id"],
        title=quiz_data["title"],
        description=quiz_data["description"]
    )
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
        print(f"Pergunta '{question['question_id']}' adicionada com sucesso.")

# Função principal para executar a criação do quiz e adição de perguntas
def main():
    create_quiz()
    add_questions()
    print("Quiz e perguntas adicionadas ao Redis para simulação.")

if __name__ == "__main__":
    main()
