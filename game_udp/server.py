"""
Multiplayer Game Server Example
By Jamal Bouajjaj, 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import socket
import threading
import queue
import typing
import time
import struct
import sys
import logging
import dataclasses
import pygame
import random


@dataclasses.dataclass
class ClientObject:
    ip: tuple
    id: int
    color_idx: int
    pos: tuple = (-50, -50)


# note: this must be the same as the server
colors = ["red", "green", "blue", "cyan", "orange", "white", "aqua", "blueviolet", "darkred", "fuchsia"]


class ServerHandler:
    addr = ("0.0.0.0", 8080)
    max_players = len(colors)

    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.conn.settimeout(2)
        self.t = threading.Thread(target=self.run_thread)
        self.exit = False
        self.clock = pygame.time.Clock()
        self.log = logging.getLogger('server')

        self.clients = {}       # type: typing.Dict[tuple, ClientObject]
        self.client_lock = threading.Lock()

    def run(self):
        self.conn.bind(self.addr)
        self.t.start()
        while not self.exit:
            with self.client_lock:
                self.update_clients()
            try:
                self.clock.tick(60)
            except KeyboardInterrupt:
                break

    def run_thread(self):
        while not self.exit:
            try:
                r, r_from = self.conn.recvfrom(1024)
                self.log.debug(f"Recv {r} from {r_from}")
            except socket.timeout:
                continue
            if r[0] != 0xFF:
                continue
            command = r[1]
            data = r[2:]
            with self.client_lock:
                if command == 0xA0:
                    self.add_player(r_from)
                elif command == 0x01:
                    pos = struct.unpack("hh", data)
                    self.clients[r_from].pos = pos
                elif command == 0xF0:
                    self.remove_player(r_from)

    def add_player(self, ip: tuple):
        if len(self.clients) >= self.max_players:
            self.conn.sendto(b'\xFF\xA2', ip)
            return
        p_id = self.generate_new_id()
        new_color = random.randint(0, len(colors)-1)
        # todo: check if player is already in IP list
        self.conn.sendto(b'\xFF\xA1' + struct.pack("hh", p_id, new_color), ip)
        # Update all the other clients about the new player
        for f in self.clients.values():
            # Update the other connected client about the new player
            self.conn.sendto(b'\xFF\x20' + struct.pack("hh", p_id, new_color), f.ip)
            # Update the just-connected client about the other players
            self.conn.sendto(b'\xFF\x20' + struct.pack("hh", f.id, f.color_idx), ip)

        self.clients[ip] = ClientObject(ip=ip, id=p_id, color_idx=new_color)
        self.log.info(f"Player from ip {ip} joined!")

    def remove_player(self, ip: tuple):
        p_id = self.clients[ip].id
        self.log.info(f"Removing player {self.clients[ip]}")
        for f in self.clients.values():
            if f.ip != ip:
                self.conn.sendto(b'\xFF\x21' + struct.pack("h", p_id), f.ip)
        self.conn.sendto(b'\xFF\xF1', ip)
        self.clients.pop(ip)

    def generate_new_id(self):
        """Generates a new unique ID for the player"""
        while 1:
            p_id = random.randint(0, 1000)
            for f in self.clients.values():
                if p_id == f.id:
                    continue
            break
        return p_id

    def generate_new_color(self):
        """Generates a new unique color for the player"""
        while 1:
            new_color = random.randint(0, len(colors)-1)
            for f in self.clients.values():
                if new_color == f.color_idx:
                    continue
            break
        return new_color

    def update_clients(self):
        data = bytearray([0xFF, 0x10, len(self.clients)])
        for c in self.clients.values():
            data += struct.pack("hhh", c.id, c.pos[0], c.pos[1])

        for c in self.clients.values():
            self.conn.sendto(data, c.ip)

    def __exit__(self):
        self.close()

    def close(self):
        print("Closing socket")
        for c in self.clients.values():
            self.conn.sendto(b"\xFF\xE0", c.ip)
        self.exit = True
        self.t.join()
        self.conn.close()


logging.basicConfig(level=logging.DEBUG)
srv = ServerHandler()
srv.run()

srv.close()
