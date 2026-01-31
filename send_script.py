import socket
import sys
import os


def send_script_file(file_path, host="127.0.0.1", port=30002):
    # 1. Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: Could not find file '{file_path}'.")
        return

    try:
        # 2. Read the .script file
        with open(file_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # 3. Send to URSim inside Docker
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((host, port))

            # Handle the last newline
            if not script_content.endswith("\n"):
                script_content += "\n"

            s.sendall(script_content.encode('utf-8'))
            print(f"Success: Sent '{file_path}' (port {port})")

    except ConnectionRefusedError:
        print("Error: Could not connect to URSim. Check if Docker is running and port 30002 is open.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # If the terminal input argument is missing (no filename)
    if len(sys.argv) < 2:
        print("Usage: python3 send_script.py <filename.script>")
    else:
        # Receive the first command-line argument as the filename
        target_file = sys.argv[1]
        send_script_file(target_file)
