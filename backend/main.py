from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import quiz_router
import redis

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Configura a conexão com o Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Configuração de CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],  # Permite o frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas do quiz
app.include_router(quiz_router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Sistema Gameficado de Quiz com Redis"}