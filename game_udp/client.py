"""
Multiplayer Game Client Example
By Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import typing
import logging
import pygame
import socket
import threading
import queue
import time
import struct
import sys
import enum
from tkinter import simpledialog
from tkinter import messagebox

# Change below depending on the IP address of the server
SERVER_IP = ("172.19.50.243", 8080)

# note: this must be the same as the server
colors = ["red", "green", "blue", "cyan", "orange", "white", "aqua", "blueviolet", "darkred", "fuchsia"]


class ServerGameComm(enum.Enum):
    new_enemy = enum.auto()
    update_pos = enum.auto()
    del_enemy = enum.auto()


class ClientHandler:
    """
    A client UDP class for handling connecting to the server, send it
    the player position, and receiving updated data from the server
    """
    server_addr = SERVER_IP

    def __init__(self):
        self.log = logging.getLogger('client')
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.conn.settimeout(1)
        self.t = threading.Thread(target=self.run_read)
        self.exit = False

        self.id = None

        self.q = queue.Queue()

    def connect(self) -> typing.Union[None, int]:
        """
        Connect to the server

        Returns:
            None if unable to connect to the server, or an ID that the server gave back

        """
        self.conn.sendto(b"\xFF\xA0", self.server_addr)
        while 1:
            try:
                r = self.conn.recv(1024)
            except socket.timeout:
                return None
            else:
                break
        self.log.debug(f"Received {r} for connect")
        if not r.startswith(b'\xFF\xA1'):
            return None
        self.id, color = struct.unpack("hh", r[2:])
        self.t.start()
        return color

    def run_read(self):
        """
        A thread loop that is used to listen to the server and process all messages from it

        TODO: have `running` be given as an argument
        """
        global running
        while not self.exit:
            try:
                r = self.conn.recv(1024)
            except socket.timeout:
                continue
            self.log.debug(f"Received {r} for data")
            if r.startswith(b'\xFF\x10'):
                p_n = int(r[2])
                data = r[3:]
                for i in range(p_n):
                    id, posx, posy = struct.unpack("hhh", data[:6])
                    self.q.put((ServerGameComm.update_pos, id, posx, posy))
                    data = data[6:]
            elif r.startswith(b'\xFF\x20'):
                data = r[2:]
                other_id, other_color = struct.unpack("hh", data)
                self.q.put([ServerGameComm.new_enemy, other_id, other_color])
            elif r.startswith(b'\xFF\x21'):
                data = r[2:]
                other_id = struct.unpack("h", data)[0]
                self.q.put([ServerGameComm.del_enemy, other_id])
            elif r == b'\xFF\xE0':
                running.set()

    def send_pos(self, p):
        """Sends the current player position to the server"""
        to_send = b"\xFF\x01"+struct.pack("hh", int(p.x), int(p.y))
        self.conn.sendto(to_send, self.server_addr)

    def __del__(self):
        """Calls on the __del__ function to ensure the socket will always close"""
        self.conn.close()

    def close(self):
        """Closes the socket, and indicates end-of-connection to the server"""
        self.log.info("Closing socket")
        self.conn.sendto(b"\xFF\xF0", self.server_addr)
        self.exit = True
        self.t.join()
        self.conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    srv = ClientHandler()
    # todo: implement sending name to server
    # name = simpledialog.askstring("Name", "What is your name to be displayed?")
    p_color = srv.connect()
    if p_color is None:
        messagebox.showwarning("Server Unable", "Unable to connect to server")
        sys.exit(-1)

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((480, 480))
    pygame.display.set_caption("Client UDP Example")
    clock = pygame.time.Clock()
    running = threading.Event()
    dt = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    enemy_pos = {}

    srv.send_pos(player_pos)

    while not running.is_set():
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running.set()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
            srv.send_pos(player_pos)
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
            srv.send_pos(player_pos)
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
            srv.send_pos(player_pos)
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt
            srv.send_pos(player_pos)

        # A 'communication' between the game loop and the server thread
        while not srv.q.empty():
            r = srv.q.get()
            if r[0] == ServerGameComm.new_enemy:
                enemy_pos[r[1]] = {'pos': pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), 'color': colors[r[2]]}
            elif r[0] == ServerGameComm.update_pos:
                if r[1] != srv.id:
                    enemy_pos[r[1]]['pos'].x = r[2]
                    enemy_pos[r[1]]['pos'].y = r[3]
            elif r[0] == ServerGameComm.del_enemy:
                enemy_pos.pop(r[1])
            srv.q.task_done()

        # Draw the enemies
        for e in enemy_pos:
            pygame.draw.circle(screen, enemy_pos[e]['color'], enemy_pos[e]['pos'], 30)
        # Draw the player
        pygame.draw.circle(screen, colors[p_color], player_pos, 30)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
    srv.close()
