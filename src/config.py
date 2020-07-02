"""
Public config
"""


# --- Server ---

server_host = '0.0.0.0'
server_port = '8001'
server_n_threads = 6


# --- Index Page Plot ---

plot_n_points = 100
plot_n_lines = 3
plot_std = 0.1
plot_y_scale = 3.
plot_rand_seconds = 2


# --- Logging in UTC timezone ---

logging_fpath = '../logs/log.log'
logging_format = '%(asctime)s.%(msecs)03d UTC %(levelname)s: %(message)s'
logging_datefmt = '%Y-%m-%dT%H:%M:%S'
# logging_datefmt = '%Y-%m-%dT%H:%M:%S.%f+%Z'
logging_level = 'DEBUG'
logging_maxbytes = 10 * 1024 * 1024
logging_backups = 1
