from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.quiz_manager import QuizManager

quiz_router = APIRouter()
quiz_manager = QuizManager()

# Definição do modelo Pydantic diretamente no routes.py
class Response(BaseModel):
    student_id: str
    question_id: str
    selected_option: str
    response_time: int

    class Config:
        from_attributes = True

# Endpoint para criar um novo quiz
@quiz_router.post("/quizzes/")
async def create_quiz(quiz_id: str, title: str, description: str):
    try:
        quiz_manager.create_quiz(quiz_id, title, description)
        return {"message": "Quiz criado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para adicionar uma pergunta a um quiz existente
@quiz_router.post("/quizzes/{quiz_id}/questions/")
async def add_question(quiz_id: str, question_id: str, text: str, options: dict, correct_answer: str):
    try:
        quiz_manager.add_question(quiz_id, question_id, text, options, correct_answer)
        return {"message": "Pergunta adicionada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
# Endpoint para verificar se o nome do estudante é único
@quiz_router.get("/quizzes/{quiz_id}/students/{student_name}")
async def check_student_name(quiz_id: str, student_name: str):
    try:
        is_unique = quiz_manager.is_student_name_unique(quiz_id, student_name)
        return {"exists": not is_unique}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para registrar a resposta de um aluno
@quiz_router.post("/quizzes/{quiz_id}/responses/")
async def record_response(quiz_id: str, response: Response):
    try:
        # Os dados da resposta são extraídos diretamente do modelo Pydantic
        student_id = response.student_id
        question_id = response.question_id
        selected_option = response.selected_option
        response_time = response.response_time

        # Registra a resposta no Redis
        quiz_manager.record_response(quiz_id, student_id, question_id, selected_option, response_time)
        
        # Retorna uma resposta de sucesso
        return {"message": "Resposta registrada com sucesso"}
    except Exception as e:
        # Em caso de erro, retorna uma exceção HTTP com status 500
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter todas as perguntas de um quiz
@quiz_router.get("/quizzes/{quiz_id}/questions/")
async def get_questions(quiz_id: str):
    try:
        questions = quiz_manager.get_questions(quiz_id)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter as opções mais votadas para todas as perguntas de um quiz
@quiz_router.get("/quizzes/{quiz_id}/most_voted_options/")
async def get_most_voted_options(quiz_id: str):
    try:
        most_voted_options = quiz_manager.get_most_voted_options(quiz_id)
        return most_voted_options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter as questões mais acertadas
@quiz_router.get("/quizzes/{quiz_id}/most_correct_questions/")
async def get_most_correct_questions(quiz_id: str):
    try:
        most_correct_questions = quiz_manager.get_most_correct_questions(quiz_id)
        return most_correct_questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para obter questões com mais abstenções
@quiz_router.get("/quizzes/{quiz_id}/questions_most_abstentions/")
async def get_questions_most_abstentions(quiz_id: str):
    try:
        questions_most_abstentions = quiz_manager.get_questions_most_abstentions(quiz_id)
        return questions_most_abstentions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

# Endpoint para obter o tempo médio de resposta por questão
@quiz_router.get("/quizzes/{quiz_id}/average_times/")
async def get_average_times(quiz_id: str):
    try:
        average_times = quiz_manager.get_average_times(quiz_id)
        return average_times
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter o tempo médio de resposta por questão
@quiz_router.get("/quizzes/{quiz_id}/average_response_times/")
async def get_average_response_times(quiz_id: str):
    try:
        average_response_times = quiz_manager.get_average_response_times(quiz_id)
        return average_response_times
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter os alunos com maior número de acertos e mais rápidos
@quiz_router.get("/quizzes/{quiz_id}/top_students/")
async def get_top_students(quiz_id: str):
    try:
        top_students = quiz_manager.get_top_students(quiz_id)
        return top_students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para obter os alunos com maior número de acertos e mais rápidos
@quiz_router.get("/quizzes/{quiz_id}/best_students/")
async def get_best_students(quiz_id: str):
    try:
        best_students = quiz_manager.get_best_students(quiz_id)
        return best_students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter os alunos com maior número de acertos
@quiz_router.get("/quizzes/{quiz_id}/students_with_most_correct_answers/")
async def get_students_with_most_correct_answers(quiz_id: str):
    try:
        students_with_most_correct_answers = quiz_manager.get_students_with_most_correct_answers(quiz_id)
        return students_with_most_correct_answers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter os alunos com maior número de acertos
@quiz_router.get("/quizzes/{quiz_id}/students_most_correct_answers/")
async def get_students_most_correct_answers(quiz_id: str):
    try:
        students_most_correct_answers = quiz_manager.get_students_most_correct_answers(quiz_id)
        return students_most_correct_answers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para obter os alunos mais rápidos
@quiz_router.get("/quizzes/{quiz_id}/fastest_stud/")
async def get_fastest_stud(quiz_id: str):
    try:
        fastest_stud = quiz_manager.get_fastest_stud(quiz_id)
        return fastest_stud
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))