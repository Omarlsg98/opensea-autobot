from config import DATA_DIR
from os.path import join
data_dir = DATA_DIR
temp_dir = join(data_dir, "temp")
input_dir = join(data_dir, "input")
output_dir = join(data_dir, "output")

users_temp_path = join(temp_dir, "users.csv")
users_path = join(output_dir, "users.csv")
to_post_path = join(input_dir, "to_post.csv")
posted_path = join(output_dir, "posted.csv")
