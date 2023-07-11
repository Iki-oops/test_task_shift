from environs import Env

env = Env()
env.read_env('.env')

DB_HOST = env.str('DB_HOST')
DB_PORT = env.str('DB_PORT')
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASS = env.str('DB_PASS')

DB_HOST_TEST = env.str('DB_HOST_TEST')
DB_PORT_TEST = env.str('DB_PORT_TEST')
DB_NAME_TEST = env.str('DB_NAME_TEST')
DB_USER_TEST = env.str('DB_USER_TEST')
DB_PASS_TEST = env.str('DB_PASS_TEST')

SECRET_AUTH = env.str('SECRET_AUTH')
