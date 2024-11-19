# from flash import Flask
# from redis import Redis
# from .routes import init_routes

# def create_app():
#     app = Flask(__name__)
#     app.config['REDIS_URL'] = 'redis://localhost:6379/0'
    
#     redis_client = Redis.from_url(app.config['REDIS_URL'])

#     init_routes(app, redis_client)

#     return app