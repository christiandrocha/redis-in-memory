import redis
import time
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.DEBUG)

class QuizManager:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.default_ttl = 30 * 24 * 60 * 60 #30 dias
        # self.default_ttl = 10 #10 seg

    def create_quiz(self, quiz_id, title, description):
        quiz_key = f"quiz:{quiz_id}"
        self.redis_client.hset(quiz_key, mapping={
            "title": title,
            "description": description,
            "created_at": self._current_timestamp()
        })
        # Define o TTL para o quiz
        self.set_ttl(quiz_key, self.default_ttl)  

    def is_student_name_unique(self, quiz_id, student_name):
        # Verificar se o nome do estudante já está registrado para o quiz especificado no Redis
        student_exists = self.redis_client.sismember(f"quiz:{quiz_id}:students", student_name)
        return not student_exists

    def add_question(self, quiz_id, question_id, text, options, correct_answer):
        question_key = f"quiz:{quiz_id}:question:{question_id}"
        self.redis_client.hset(question_key, mapping={
            "text": text,
            "option_A": options.get('A', ''),
            "option_B": options.get('B', ''),
            "option_C": options.get('C', ''),
            "option_D": options.get('D', ''),
            "correct_answer": correct_answer
        })
        self.redis_client.sadd(f"quiz:{quiz_id}:questions", question_id)
        # Define o TTL para a pergunta
        self.set_ttl(question_key, self.default_ttl)
        # Define o TTL para o conjunto de perguntas
        self.set_ttl(f"quiz:{quiz_id}:questions", self.default_ttl)

    def set_ttl(self, key, ttl_seconds):
        try:
            self.redis_client.expire(key, ttl_seconds)
            logging.debug(f"TTL definido para {key}: {ttl_seconds} segundos")
        except Exception as e:
            logging.error(f"Erro ao definir TTL para {key}: {e}")

    def record_response(self, quiz_id, student_id, question_id, selected_option, response_time):
        try:
            response_key = f"quiz:{quiz_id}:student:{student_id}:responses"
            
            # Registra abstenção se selected_option ou response_time forem None
            self.redis_client.hset(response_key, question_id, selected_option if selected_option else "abstention")
            if response_time is not None:
                self.redis_client.hset(f"quiz:{quiz_id}:student:{student_id}:times", question_id, int(response_time))
            
            # Atualiza a contagem de votos por opção e registra o aluno
            if selected_option:
                self.redis_client.hincrby(f"quiz:{quiz_id}:question:{question_id}:votes", selected_option, 1)
            self.redis_client.sadd(f"quiz:{quiz_id}:students", student_id)
        except Exception as e:
            print(f"Error recording response: {e}")

    def get_questions(self, quiz_id):
        # Obter todos os IDs das questões do quiz
        question_ids = self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        
        # Ordenar os IDs das questões
        sorted_question_ids = sorted(question_ids, key=int)
        
        questions = []
        for question_id in sorted_question_ids:
            # Obter os dados da questão
            question_data = self.redis_client.hgetall(f"quiz:{quiz_id}:question:{question_id}")
            
            # Filtrar as opções que começam com 'option_'
            options = {k: v for k, v in question_data.items() if k.startswith('option_')}
            
            # Adicionar a questão à lista
            questions.append({
                "id": question_id,
                "text": question_data.get("text", ""),
                "options": options,
                "correct_answer": question_data.get("correct_answer", "")
            })
        
        return questions

    def get_most_voted_options(self, quiz_id):
        questions = self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        most_voted_options = {}
        for question_id in questions:
            votes = self.redis_client.hgetall(f"quiz:{quiz_id}:question:{question_id}:votes")
            if votes:
                most_voted_option = max(votes, key=votes.get)
                most_voted_options[question_id] = {
                    "most_voted_option": most_voted_option,
                    "vote_count": votes[most_voted_option]
                }
        return most_voted_options
    
    def get_most_correct_questions(self, quiz_id):
        questions = self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        most_correct_options = {}

        for question_id in questions:
            correct_answer = self.redis_client.hget(f"quiz:{quiz_id}:question:{question_id}", "correct_answer")
            logging.debug(f"Correct answer for question {question_id}: {correct_answer}")

            correct_count = 0
            students = self.redis_client.smembers(f"quiz:{quiz_id}:students")

            for student_id in students:
                response = self.redis_client.hget(f"quiz:{quiz_id}:student:{student_id}:responses", question_id)
                logging.debug(f"Response from student {student_id} for question {question_id}: {response}")

                if response == correct_answer:
                    correct_count += 1

            logging.debug(f"Response correct: {correct_answer} Response student: {response}")
            if correct_count > 0:
                most_correct_options[question_id] = {
                    "most_correct_option": correct_answer,
                    "correct_count": correct_count
                }

        # Ordenar as questões por número de acertos em ordem decrescente
        sorted_most_correct_options = dict(sorted(most_correct_options.items(), key=lambda item: item[1]['correct_count'], reverse=True))

        return sorted_most_correct_options

    def get_questions_most_abstentions(self, quiz_id):
        # Obter todas as questões do quiz
        questions = self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        abstention_counts = {}

        for question_id in questions:
            abstention_count = 0

            # Iterar sobre cada estudante para verificar suas respostas
            for student_id in self.redis_client.smembers(f"quiz:{quiz_id}:students"):
                response = self.redis_client.hget(f"quiz:{quiz_id}:student:{student_id}:responses", question_id)
                logging.debug(f"Correct answer for question {question_id}: {response}")

                if response is None or response == "abstention":
                    abstention_count += 1

            # Armazenar o número de abstenções para cada questão
            abstention_counts[question_id] = abstention_count
            logging.debug(f"Question: {question_id} Abstenções: {abstention_counts}")


        # Determinar o maior número de abstenções
        if abstention_counts:
            max_abstentions = max(abstention_counts.values())
            questions_with_most_abstentions = {
                question_id: {
                    "question_id": question_id,
                    "abstention_count": count
                }
                for question_id, count in abstention_counts.items() if count == max_abstentions
            }
            return questions_with_most_abstentions
        else:
            return {}

    def get_average_times(self, quiz_id):
        # Obter todas as questões e estudantes do quiz
        questions = self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        students = self.redis_client.smembers(f"quiz:{quiz_id}:students")
        average_times = {}

        for question_id in questions:
            total_time = 0
            count = 0

            for student_id in students:
                # Buscar o tempo de resposta para a questão específica
                response_time = self.redis_client.hget(f"quiz:{quiz_id}:student:{student_id}:times", question_id)
                
                if response_time:
                    total_time += int(response_time)
                    count += 1

            # Armazenar a média de tempo de resposta apenas se houver respostas válidas
            if count > 0:
                average_time = total_time / count
                average_times[question_id] = {
                    "question_response": question_id,
                    "average_time": round(average_time, 1)
                }

        return average_times
    
    def get_average_response_times(self, quiz_id):
        questions = self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        students = self.redis_client.smembers(f"quiz:{quiz_id}:students")
        average_times = {}

        for question_id in questions:
            total_time = 0
            count = 0

            for student_id in students:
                response_time = self.redis_client.hget(f"quiz:{quiz_id}:student:{student_id}:times", question_id)
                if response_time:
                    try:
                        total_time += int(response_time)
                        count += 1
                    except ValueError as e:
                        print(f"Erro ao converter tempo de resposta para inteiro: {e}")

            average_time = total_time / count if count > 0 else 0
            average_times[question_id] = average_time

            return average_times
            
    def get_top_students(self, quiz_id):
        # Obter todos os estudantes do quiz
        students = self.redis_client.smembers(f"quiz:{quiz_id}:students")
        
        # Obter todas as respostas corretas para as questões do quiz
        correct_answers = {
            q: self.redis_client.hget(f"quiz:{quiz_id}:question:{q}", "correct_answer")
            for q in self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        }
        
        # Dicionário para armazenar o número de acertos e tempo total de cada estudante
        student_scores = {}
        
        for student_id in students:
            responses = self.redis_client.hgetall(f"quiz:{quiz_id}:student:{student_id}:responses")
            correct_count = sum(1 for q, a in responses.items() if correct_answers.get(q) == a)
            response_times = self.redis_client.hvals(f"quiz:{quiz_id}:student:{student_id}:times")
            total_time = sum(map(int, response_times))
            
            student_scores[student_id] = (correct_count, total_time)
        
        # Encontrar o maior número de acertos
        max_correct_count = max(score[0] for score in student_scores.values())
        
        # Filtrar estudantes com o maior número de acertos
        top_students = {student_id: score for student_id, score in student_scores.items() if score[0] == max_correct_count}
        
        # Encontrar o menor tempo entre os estudantes com o maior número de acertos
        min_time = min(score[1] for score in top_students.values())
        
        # Filtrar estudantes com o menor tempo
        final_top_students = [student_id for student_id, score in top_students.items() if score[1] == min_time]
        
        return final_top_students, max_correct_count, min_time
    
    def get_best_students(self, quiz_id):
        # Obter todos os estudantes do quiz
        students = self.redis_client.smembers(f"quiz:{quiz_id}:students")
        
        # Obter todas as respostas corretas para as questões do quiz
        correct_answers = {
            q: self.redis_client.hget(f"quiz:{quiz_id}:question:{q}", "correct_answer")
            for q in self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        }
        
        # Dicionário para armazenar o número de acertos e tempo total de cada estudante
        student_scores = {}
        
        for student_id in students:
            responses = self.redis_client.hgetall(f"quiz:{quiz_id}:student:{student_id}:responses")
            correct_count = sum(1 for q, a in responses.items() if correct_answers.get(q) == a)
            response_times = self.redis_client.hvals(f"quiz:{quiz_id}:student:{student_id}:times")
            total_time = sum(map(int, response_times))
            
            student_scores[student_id] = (correct_count, total_time)
        
        # Encontrar o maior número de acertos
        max_correct_count = max(score[0] for score in student_scores.values())
        
        # Filtrar estudantes com o maior número de acertos
        best_students = {student_id: score for student_id, score in student_scores.items() if score[0] == max_correct_count}
        
        # Encontrar o menor tempo entre os estudantes com o maior número de acertos
        min_time = min(score[1] for score in best_students.values())
        
        # Filtrar estudantes com o menor tempo
        final_best_students = [student_id for student_id, score in best_students.items() if score[1] == min_time]
        
        # Retornar um dicionário com as informações
        return {
            "students": final_best_students,
            "max_correct_count": max_correct_count,
            "min_time": min_time
        }

    def get_students_with_most_correct_answers(self, quiz_id):
        # Obter todos os estudantes do quiz
        students = self.redis_client.smembers(f"quiz:{quiz_id}:students")
        
        # Obter todas as respostas corretas para as questões do quiz
        correct_answers = {
            q: self.redis_client.hget(f"quiz:{quiz_id}:question:{q}", "correct_answer")
            for q in self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        }
        
        student_correct_counts = {}
        
        # Calcular o número de acertos para cada estudante
        for student_id in students:
            responses = self.redis_client.hgetall(f"quiz:{quiz_id}:student:{student_id}:responses")
            correct_count = sum(1 for q, a in responses.items() if correct_answers.get(q) == a)
            student_correct_counts[student_id] = correct_count
        
        # Encontrar o número máximo de acertos
        max_correct_count = max(student_correct_counts.values(), default=0)
        
        # Encontrar todos os estudantes com o número máximo de acertos
        top_students = [student_id for student_id, count in student_correct_counts.items() if count == max_correct_count]
        
        return top_students, max_correct_count

    def get_students_most_correct_answers(self, quiz_id):
        # Obter todos os estudantes do quiz
        students = self.redis_client.smembers(f"quiz:{quiz_id}:students")
        
        # Obter todas as respostas corretas para as questões do quiz
        correct_answers = {
            q: self.redis_client.hget(f"quiz:{quiz_id}:question:{q}", "correct_answer")
            for q in self.redis_client.smembers(f"quiz:{quiz_id}:questions")
        }
        
        # Dicionário para armazenar o número de acertos de cada estudante
        student_correct_counts = {}
        
        # Calcular o número de acertos para cada estudante
        for student_id in students:
            responses = self.redis_client.hgetall(f"quiz:{quiz_id}:student:{student_id}:responses")
            correct_count = sum(1 for q, a in responses.items() if correct_answers.get(q) == a)
            student_correct_counts[student_id] = correct_count
        
        # Encontrar o número máximo de acertos
        max_correct_count = max(student_correct_counts.values(), default=0)
        
        # Encontrar todos os estudantes com o número máximo de acertos
        top_students = [student_id for student_id, count in student_correct_counts.items() if count == max_correct_count]
        
        # Retornar um dicionário semelhante ao método get_fastest_stud
        return {
            "max_correct_count": max_correct_count,
            "students": top_students
        }


    def get_fastest_stud(self, quiz_id):
        students = self.redis_client.smembers(f"quiz:{quiz_id}:students")
        fastest_students_info = {
            "fastest_time": 21,  # Tempo máximo permitido + 1
            "students": set()    # Usar um conjunto para evitar duplicatas
        }

        for student_id in students:
            # Obter tempos de resposta para cada questão
            question_times = self.redis_client.hvals(f"quiz:{quiz_id}:student:{student_id}:times")
            
            # Encontrar o menor tempo para este estudante
            min_time_for_student = min(int(time_str) for time_str in question_times)
            
            # Verificar se este tempo é o menor encontrado
            if min_time_for_student < fastest_students_info["fastest_time"]:
                # Novo tempo mais rápido encontrado
                fastest_students_info["fastest_time"] = min_time_for_student
                fastest_students_info["students"] = {student_id}  # Reiniciar o conjunto com o novo estudante
            elif min_time_for_student == fastest_students_info["fastest_time"]:
                # Tempo igual ao tempo mais rápido atual
                fastest_students_info["students"].add(student_id)

        # Converter o conjunto de estudantes de volta para uma lista antes de retornar
        fastest_students_info["students"] = list(fastest_students_info["students"])
        
        return fastest_students_info

    def _current_timestamp(self):
        return int(time.time())
