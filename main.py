from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from random import randint

Window.size = (400, 600)

class SnakeGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.snake = [(100, 100)]
        self.food = (200, 200)

        self.dx = 20
        self.dy = 0

        Window.bind(on_key_down=self.key_action)

        Clock.schedule_interval(self.update, 0.2)

    def draw(self):
        self.canvas.clear()

        with self.canvas:
            Color(0, 1, 0)

            for part in self.snake:
                Rectangle(pos=part, size=(20, 20))

            Color(1, 0, 0)
            Rectangle(pos=self.food, size=(20, 20))

    def update(self, dt):

        head_x, head_y = self.snake[0]

        new_head = (head_x + self.dx, head_y + self.dy)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = (
                randint(0, 19) * 20,
                randint(0, 29) * 20
            )
        else:
            self.snake.pop()

        self.draw()

    def key_action(self, window, key, *args):

        if key == 273:
            self.dx = 0
            self.dy = 20

        elif key == 274:
            self.dx = 0
            self.dy = -20

        elif key == 275:
            self.dx = 20
            self.dy = 0

        elif key == 276:
            self.dx = -20
            self.dy = 0

class SnakeApp(App):
    def build(self):
        return SnakeGame()

SnakeApp().run()