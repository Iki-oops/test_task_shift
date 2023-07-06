from environs import Env

env = Env()
env.read_env('.env')

DB_HOST = env.str('DB_HOST')
DB_PORT = env.str('DB_PORT')
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')

SECRET_AUTH = env.str('SECRET_AUTH')
