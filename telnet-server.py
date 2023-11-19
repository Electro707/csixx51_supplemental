"""
Telnet and TCP Server Example
By Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import socket
import time

addr = ("127.0.0.1", 8081)  # loopback (localhost), port 8080

def send_slow(conn, text):
    """ Function to slowly send out a text over a socket"""
    for t in text:
        conn.send(bytes([t]))
        time.sleep(0.1)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Set this so that we can re-use the same address without waiting for TIME_WAIT
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # We bind to the address we want
    s.bind(addr)
    # We start listening for connections
    s.listen()
    # We accept one connection with a client
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        conn.send(f"Welcome to Jamal's GREAT application!\n".encode())
        conn.send(f"You're name is {addr}, and you can drown yourself in the digital lake!\n".encode())
        f = conn.makefile()     # Convinent so we can use `readline` without doing it ourselves
        while True:
            conn.sendall(b"> ")        # disable for python!
            l = f.readline()
            if l == '':
                break
            l = l.strip()
            if l == 'help':
                conn.sendall("Welcome to [[APPLICATION GOOD!]], would you like to [[CONSUME NUTRIENTS!]]\n".encode())
            elif l == 'quit':
                conn.sendall("Closing!\n".encode())
                break
            elif l == 'ping':
                conn.sendall(b'\033[1mpong!\033[0m\n')
            elif l == 'dance':
                send_slow(conn, b"DANCING!!!")
                for i in range(40, 48):
                    conn.sendall(f'\033[{i:d}m\033[2J'.encode())
                    time.sleep(0.25)
                conn.sendall(b'\033[0m\033[2J\033[1;1H')
            elif l == 'python':
                conn.sendall(b'\xab\xcd\xef'*1000)
                conn.sendall(b'\n')
            elif l == 'clear':
                conn.sendall(b'\033[0m\033[2J\033[1;1H')
            elif l == 'colorme':
                conn.sendall(b'\033[91m\033[1mCOLORED BABY!!!\033[2m\033[36m\n')
            else:
                conn.sendall(b"Wrong command!\n")
            # data = conn.recv(1024)
            # if not data:
            #     break
            # conn.sendall(f"-> {data}".encode())
        conn.sendall(b'\033[0m')
        conn.shutdown(socket.SHUT_RD)
