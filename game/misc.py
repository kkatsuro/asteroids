import os

def coords_to_points(x1, x2, y1, y2):
    return (x1, y1), (x1, y2), (x2, y1), (x2, y2)

# get environment variable
# https://www.howtogeek.com/668503/how-to-set-environment-variables-in-bash-on-linux/
# with default value set to 'default_value' if env variable not available
def env_default(env_variable_name, default_value):
    value = os.environ.get(env_variable_name)
    if value == None:
        return default_value
    if value.isnumeric():
        value = float(value)
    return value
