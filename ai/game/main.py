import arcade
import os
import random
rootdir = os.path.dirname(os.path.abspath(__file__))


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(900, 600, "AIrcade")

        Player.texture = arcade.load_texture(os.path.join(rootdir, "player.png"), flipped_diagonally=True, flipped_horizontally=True)

        self.player = Player(self.width / 2, self.height / 2)
        self.food = Food()
        self.food.set_random_position(self.width, self.height)

        self.pressed_keys = set()
        self.score = 0

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.food.draw()

    def on_key_press(self, symbol, modifiers):
        print("pressed:", symbol)
        self.pressed_keys.add(symbol)

    def on_key_release(self, symbol, modifiers):
        print("released:", symbol)
        self.pressed_keys.remove(symbol)

    def on_update(self, delta_time):
        self.player.update(self.pressed_keys)
        self.player.wrap_screen(self.width, self.height)
        if (self.player.collides_with_sprite(self.food)):
            self.food.set_random_position(self.width, self.height)
            self.score += 1
            print("Score:", self.score)


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(texture=Player.texture)
        self.center_x = x
        self.center_y = y

    def update(self, pressed_keys):
        super().update()
        self.change_x = 0    # Reset player speed
        self.change_y = 0
        self.change_angle = 0

        if arcade.key.UP in pressed_keys or arcade.key.W in pressed_keys:
            self.forward(8)

        if arcade.key.DOWN in pressed_keys or arcade.key.S in pressed_keys:
            self.reverse(4)

        if arcade.key.LEFT in pressed_keys or arcade.key.A in pressed_keys:
            self.turn_left(4)

        if arcade.key.RIGHT in pressed_keys or arcade.key.D in pressed_keys:
            self.turn_right(4)

    def wrap_screen(self, s_width, s_height):
        if self.left > s_width:
            self.right = 0
        elif self.right < 0:
            self.left = s_width

        if self.bottom > s_height:
            self.top = 0
        elif self.top < 0:
            self.bottom = s_height



class Food(arcade.Sprite):
    def __init__(self):
        super().__init__(os.path.join(rootdir, "food.png"))

    def set_random_position(self, window_width, window_height):
        margin = self.width // 2
        self.center_x = random.randint(margin, window_width-margin)
        self.center_y = random.randint(margin, window_height-margin)


def run_game():
    GameWindow()
    arcade.run()


if __name__ == "__main__":
    run_game()
