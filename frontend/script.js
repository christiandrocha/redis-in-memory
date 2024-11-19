const BASE_URL = 'http://127.0.0.1:8000';

let currentQuestionIndex = 0;
let studentName = '';
let questions = [];
let timer;
let timeLeft = 20;
const quizId = '1'; // Código do quiz

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM completamente carregado e analisado");

    // Adicionar event listener no botão de início do quiz
    document.getElementById("start-quiz-button").addEventListener("click", startQuiz);
    console.log("Event listener para o botão de iniciar quiz adicionado");

    // Adicionar event listener no botão de enviar resposta
    document.getElementById("submit-answer-button").addEventListener("click", submitAnswer);
    console.log("Event listener para o botão de enviar resposta adicionado");

    // Adicionar event listener no botão de próxima pergunta
    document.getElementById("next-question-button").addEventListener("click", nextQuestion);
    console.log("Event listener para o botão de próxima pergunta adicionado");

    // Adicionar event listener no botão de ver ranking
    document.getElementById("show-rankings-button").addEventListener("click", fetchRankings);
    console.log("Event listener para o botão de ver ranking adicionado");
});

// Função para verificar se o nome do estudante é único
async function isStudentNameUnique(studentName, quizId) {
    try {
        const response = await fetch(`${BASE_URL}/quizzes/${quizId}/students/${studentName}`);
        
        if (response.ok) {
            const data = await response.json();
            return !data.exists; // Supondo que o servidor retorna um objeto com a propriedade 'exists'
        } else {
            console.error(`Erro ao verificar nome do estudante: ${response.status} ${response.statusText}`);
            return false;
        }
    } catch (error) {
        console.error('Erro ao verificar nome do estudante:', error);
        return false;
    }
}

// Função para iniciar o quiz
async function startQuiz() {
    studentName = document.getElementById('student-name').value.trim();
    if (!studentName) {
        alert('Por favor, insira seu nome.');
        return;
    }
    // Verificar se o nome do estudante é único
    const isUnique = await isStudentNameUnique(studentName, quizId);
    if (!isUnique) {
        alert('Nome já está em uso. Por favor, escolha outro nome.');
        return;
    }
    try {
        const response = await fetch(`${BASE_URL}/quizzes/${quizId}/questions/`);
        if (!response.ok) throw new Error('Erro ao buscar perguntas');

        questions = await response.json();
        if (!questions || questions.length === 0) throw new Error('Nenhuma pergunta encontrada');

        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('quiz-screen').style.display = 'block';
        showQuestion();
    } catch (error) {
        console.error('Erro ao buscar perguntas:', error);
        document.getElementById('feedback').innerText = 'Erro ao carregar perguntas. Tente novamente mais tarde.';
        document.getElementById('feedback').style.display = 'block';
    }
}

// Função para exibir a pergunta atual
function showQuestion() {
    if (currentQuestionIndex >= questions.length) {
        endQuiz();
        return;
    }
    const question = questions[currentQuestionIndex];
    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = `
        <div class="question">
            <h2>${question.text}</h2>
            <ul class="options">
                ${Object.entries(question.options).map(([key, value]) => `
                    <li>
                        <label>
                            <input type="radio" name="option" value="${key}">
                            ${key}: ${value}
                        </label>
                    </li>
                `).join('')}
            </ul>
        </div>
    `;
    resetTimer();
}

// Função para resetar o temporizador
function resetTimer() {
    clearInterval(timer);
    timeLeft = 20;
    document.getElementById('time-left').innerText = timeLeft;
    timer = setInterval(() => {
        timeLeft--;
        document.getElementById('time-left').innerText = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(timer);
            recordAbstention();  // Registra abstenção ao expirar o tempo
            nextQuestion();
        }
    }, 1000);
}

// Função para registrar uma abstenção
async function recordAbstention() {
    const questionId = questions[currentQuestionIndex].id;
    try {
        await fetch(`${BASE_URL}/quizzes/${quizId}/responses/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_id: studentName,
                question_id: questionId,
                selected_option: "",  // Indica que não houve resposta
                response_time: 0      // Tempo não informado para abstenção
            })
        });
    } catch (error) {
        console.error('Erro ao registrar abstenção:', error);
    }
}

// Função para enviar a resposta do aluno
async function submitAnswer() {
    console.log("submitAnswer foi chamada");
    const selectedOption = document.querySelector('input[name="option"]:checked');
    if (!selectedOption) {
        alert('Por favor, selecione uma resposta.');
        return;
    }
    const answer = selectedOption.value;
    const questionId = questions[currentQuestionIndex].id;
    const responseTime = 20 - timeLeft;

    // Log para verificar os dados antes de enviar
    console.log("studentName:", studentName);
    console.log("questionId:", questionId);
    console.log("selectedOption:", answer);
    console.log("responseTime:", responseTime);
    

    try {
        await fetch(`${BASE_URL}/quizzes/${quizId}/responses/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_id: studentName,
                question_id: questionId,
                selected_option: answer,
                response_time: responseTime  // Tempo de resposta registrado
            })
        });
        nextQuestion();
    } catch (error) {
        console.error('Erro ao enviar resposta:', error);
        document.getElementById('feedback').innerText = 'Erro ao enviar resposta. Tente novamente.';
        document.getElementById('feedback').style.display = 'block';
    }
}

// Função para avançar para a próxima pergunta
function nextQuestion() {
    clearInterval(timer);
    currentQuestionIndex++;
    showQuestion();
}

// Função para finalizar o quiz
function endQuiz() {
    document.getElementById('quiz-screen').style.display = 'none';
    document.getElementById('thank-you-screen').style.display = 'block';
}

// Função para buscar e exibir rankings
async function fetchRankings() {
    try {
        const mostVotedOptions = await fetch(`${BASE_URL}/quizzes/${quizId}/most_voted_options/`).then(res => res.json());
        const mostCorrectQuestions = await fetch(`${BASE_URL}/quizzes/${quizId}/most_correct_questions/`).then(res => res.json());
        const questionsMostAbstentions = await fetch(`${BASE_URL}/quizzes/${quizId}/questions_most_abstentions/`).then(res => res.json());
        const averageTimes = await fetch(`${BASE_URL}/quizzes/${quizId}/average_times/`).then(res => res.json());
        const bestStudents = await fetch(`${BASE_URL}/quizzes/${quizId}/best_students/`).then(res => res.json());
        const studentsWithMostCorrectAnswers = await fetch(`${BASE_URL}/quizzes/${quizId}/students_with_most_correct_answers/`).then(res => res.json());
        const studentsMostCorrectAnswers = await fetch(`${BASE_URL}/quizzes/${quizId}/students_most_correct_answers/`).then(res => res.json());
        const fastestStud = await fetch(`${BASE_URL}/quizzes/${quizId}/fastest_stud/`).then(res => res.json());

        displayRankings({
            mostVotedOptions,
            mostCorrectQuestions,
            questionsMostAbstentions,
            averageTimes,
            bestStudents,
            studentsWithMostCorrectAnswers,
            studentsMostCorrectAnswers,
            fastestStud
        });
    } catch (error) {
        console.error('Erro ao buscar rankings:', error);
        document.getElementById('feedback').innerText = 'Erro ao carregar rankings. Tente novamente mais tarde.';
        document.getElementById('feedback').style.display = 'block';
    }
}

// Função para exibir os rankings no HTML
function displayRankings(rankings) {
    // console.log("Rankings recebidos:", rankings); // Log para verificar os dados recebidos

    const rankingsContainer = document.getElementById('rankings-container');
    rankingsContainer.style.display = 'block';

    // Converter o objeto de alternativas mais votadas em um array de strings
    const mostVotedOptionsArray = Object.entries(rankings.mostVotedOptions || {}).map(([questionId, data]) => {
        const mostVotedOption = data.most_voted_option.replace("option_", "");
        return `Questão ${questionId}: ${mostVotedOption} com ${data.vote_count} voto(s).`;
    });

    // Converter o objeto de questões mais corretas em um array de strings
    const mostCorrectQuestionsArray = Object.entries(rankings.mostCorrectQuestions || {}).map(([questionId, data]) => { 
        const mostCorrectOption = data.most_correct_option.replace("option_", "");
        return `Questão ${questionId}: ${mostCorrectOption} com ${data.correct_count} acerto(s).`;
    });
    
    // Converter o objeto de questões mais corretas em um array de strings
    const questionsMostAbstentionsArray = Object.entries(rankings.questionsMostAbstentions || {}).map(([questionId, data]) => { 
        return `Questão ${questionId}: com ${data.abstention_count} abstenção(ôes).`;
    });

    // Converter o objeto de questões com média em um array de strings
    const averageTimesArray = Object.entries(rankings.averageTimes || {}).map(([questionId, data]) => { 
        return `Questão ${questionId}: ${data.average_time} segundo(s)`;
    }); 

    // Acessar o objeto de estudantes mais rápidos e converter em um array de strings
    const bestStudentsArray = Array.isArray((rankings.bestStudents || {}).students) ? 
    (rankings.bestStudents || {}).students.map(studentId => {
        return `Estudante: "${studentId}" com ${rankings.bestStudents.max_correct_count} acerto(s) e total de ${rankings.bestStudents.min_time} segundo(s).`;
    }) : [];

    // Acessar o objeto de estudantes mais rápidos e converter em um array de strings
    const studentsMostCorrectAnswersArray = (rankings.studentsMostCorrectAnswers || {}).students.map(studentId => {
        return `Estudante: "${studentId}" com ${rankings.studentsMostCorrectAnswers.max_correct_count} acerto(s).`;
    });

    // Acessar o objeto de estudantes mais rápidos e converter em um array de strings
    const fastestStudArray = (rankings.fastestStud || {}).students.map(studentId => {
        return `Estudante: "${studentId}" com tempo de ${rankings.fastestStud.fastest_time} segundo(s).`;
    });

    // Função auxiliar para criar listas
    const createList = (items, defaultMessage) => {
        if (!Array.isArray(items) || items.length === 0) {
            console.error("Esperado um array, mas recebeu:", items);
            return `<li>${defaultMessage || "Dados indisponíveis"}</li>`;
        }
        return items.map(item => `<li>${item}</li>`).join('');
    };

    rankingsContainer.innerHTML = `
        <h2>Rankings</h2>
        <div>
            <h3>Alternativas Mais Votadas</h3>
            <ul>${createList(mostVotedOptionsArray, "Nenhuma opção votada disponível")}</ul>
        </div>
        <div>
            <h3>Questões Mais Acertadas</h3>
            <ul>${createList(mostCorrectQuestionsArray, "Nenhuma questão acertada disponível")}</ul>
        </div>
        <div>
            <h3>Questões com Mais Abstenções</h3>
            <ul>${createList(questionsMostAbstentionsArray, "Nenhuma abstenção registrada")}</ul>
        </div>
        <div>
            <h3>Tempo Médio de Resposta por Questão</h3>
            <ul>${createList(averageTimesArray, "Nenhum tempo de resposta disponível")}</ul>
        </div>
        <div>
            <h3>Alunos com Maior Acerto e Mais Rápidos</h3>
            <ul>${createList(bestStudentsArray, "Nenhum aluno encontrado")}</ul>
        </div>
        <div>
            <h3>Alunos com Maior Número de Acertos</h3>
            <ul>${createList(studentsMostCorrectAnswersArray, "Nenhum aluno encontrado")}</ul>
        </div>
        <div>
            <h3>Alunos Mais Rápidos</h3>
            <ul>${createList(fastestStudArray, "Nenhum aluno encontrado")}</ul>
        </div>
    `;
}