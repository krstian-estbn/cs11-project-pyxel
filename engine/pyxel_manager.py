import pyxel
from engine.game_manager import GameManager

class App:
    def __init__(self, map_file):
        self.game = GameManager()
        
        self.map_file = map_file
        self.tile_map = {
            "T": (0,0,0),   # tree
            "+": (0,16,0),  # mushroom
            "L": (0,16,16),   # player
            "R": (0,0,32),   # rock
            "~": (0,48,0),   # water
            "-": (0,0,16),   # ground
            "D": (0,32,16),   # drowned
            ".": (0,32,32),   # empty
            "x": (0,32,0),   # axe
            "*": (0,48,16),  # flame
        }
        self.text_tile = {
            "+": (0,16,32),
            "x": (0, 24, 32),
            "*": (0, 16, 40)
        }
        self.tile_size = 16
        
        # dynamic window format
        self.game.initialize_game(self.map_file)
        self.map_width = len(self.game.map_level[0]) * self.tile_size
        self.map_height = len(self.game.map_level) * self.tile_size
        self.width = max(self.map_width + 80, 180)
        self.height = max(self.map_height + 120, 160)


        self.status = False
        self.message = ""
        self.message_color = 0

        pyxel.init(self.width, self.height, title="SHROOOOOOOOOOMSSSSS")
        pyxel.load("default_tile_map.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        # inputs
        if pyxel.btnp(pyxel.KEY_R):
            self.restart()
            return
        elif pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            return
        

        if self.game.player.points == self.game.mushroom_count:
            if not self.status:
                self.status = True
                self.game.player.status = False
                self.message = "PALDOOOO"
                self.message_color = 9
            return
        
        if not self.game.player.status:
            self.message = "tanga amputa"
            self.message_color = 8
            if pyxel.btnp(pyxel.KEY_R):
                self.restart()
            elif pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            return



        move = ""
        if pyxel.btnp(pyxel.KEY_W): move = "W"
        elif pyxel.btnp(pyxel.KEY_S): move = "S"
        elif pyxel.btnp(pyxel.KEY_A): move = "A"
        elif pyxel.btnp(pyxel.KEY_D): move = "D"
        elif pyxel.btnp(pyxel.KEY_P): move = "P"

        if move:
            if move == "P":
                self.game.player.pickup_item()
            else:
                self.game.player.movement(
                    self.game.map_level,
                    move,
                    self.game.input_handler.moves,
                    self.game.row_len,
                    self.game.col_len
                )

    def restart(self):
        self.game.reset_game()
        self.game.initialize_game(self.map_file)
        self.status = False

    def draw(self):
        pyxel.cls(0)

        # center div ahh moment
        map_offset_x = (self.width - self.map_width) // 2
        map_offset_y = (self.height - self.map_height) // 2 - 30


        # draws the map
        for r, row in enumerate(self.game.map_level):
            for c, cell in enumerate(row):
                img, u, v = self.tile_map[cell]
                x = map_offset_x + c * self.tile_size
                y = map_offset_y + r * self.tile_size
                pyxel.blt(
                x,
                y,
                img, u, v, self.tile_size, self.tile_size)

        # css ahh shit
        hud_x = 40
        hud_y = self.height - 80

        # brute force formatting
        pyxel.text(hud_x, hud_y + 2, "Collected:", 9)
        img, u, v = self.text_tile["+"]
        pyxel.blt(hud_x + 40, hud_y, img, u, v, 8, 8)
        pyxel.text(hud_x + 50, hud_y + 2, f"{self.game.player.points}/{self.game.mushroom_count}", 9)

        pyxel.text(hud_x, hud_y + 10, "Item Below:", 7)
        if self.game.player.under_l in ("x", "*"):
            img, u, v = self.text_tile[self.game.player.under_l]
            pyxel.blt(hud_x + 44, hud_y + 8, img, u, v, 8, 8)

        pyxel.text(hud_x, hud_y + 18, "Current Item:", 7)
        if self.game.player.item:
            img, u, v = self.text_tile[self.game.player.item.symbol]
            pyxel.blt(hud_x + 52, hud_y + 16, img, u, v, 8, 8)

        pyxel.text(hud_x, hud_y + 26, "[WASD] Move", 6)
        pyxel.text(hud_x, hud_y + 34, "[P] Pickup", 6)
        pyxel.text(hud_x, hud_y + 42, "[R] Reset", 6)
        pyxel.text(hud_x, hud_y + 50, "[Q] Quit", 6)
        
        # center div round 2
        if not self.game.player.status:
            message_width = len(self.message) * 4
            pyxel.text((self.width - (message_width)) // 2, (self.height - 65) // 2, self.message, self.message_color)
            pyxel.text((self.width - 80)// 2 , (self.height - 50) // 2, "PRESS [R] TO RESTART", 7)
