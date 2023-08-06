from test_framework.node_database import update_env_state
from test_framework.test_environment import Environment


@update_env_state
def get_env_identify_info():
    env = Environment()
    env_information = env.get_environments()
    return env_information
