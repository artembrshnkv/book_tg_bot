from environs import Env

env = Env()
env.read_env()

TOKEN = env('API_TOKEN')
ADMIN_ID_LIST = env('ADMIN_ID_LIST')


