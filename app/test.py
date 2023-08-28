import os
import subprocess
ffmpeg_path = '..\FFmpeg\bin'

# # os.environ["FFmpeg"] = ffmpeg_path



current_path = os.environ.get("PATH","")
# print(ffmpeg_path)
new_path = f"{ffmpeg_path}{os.pathsep}{current_path}"
os.environ["PATH"] = new_path
# flag = os.environ.get("ffmpeg")
# print(flag)
# if flag:
#     version = "-version"
    # command = [flag,version]
    # print(command)
# subprocess.run(f"ffmpeg")
# else:
#     print("flag not set")

env_variables = os.environ

# # Print each environment variable
for key, value in env_variables.items():
    print(f"{key}: {value}")