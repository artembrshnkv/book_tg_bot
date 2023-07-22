from environs import Env

env = Env()
env.read_env()

TOKEN = env('API_TOKEN')
ADMINS_ID_LIST = env('ADMINS_ID_LIST')

DATABASE_NAME = env('DATABASE_NAME')
DB_PORT = env('DB_PORT')
DB_HOST = env('DB_HOST')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')



