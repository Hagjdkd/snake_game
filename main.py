from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from random import randint

# Window Setup
Window.size = (400, 600)

BLOCK = 20
WIDTH = 400
HEIGHT = 480


class Dashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        # Main Menu Background
        bg = Image(
            source='assets/images/background.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )

        center = AnchorLayout(anchor_x='center', anchor_y='center')
        box = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(250, 250),
            spacing=10
        )

        title = Label(text='SNAKE GAME', font_size=28, color=(1, 1, 1, 1))
        start = Button(text='Start Game')
        about = Button(text='About')
        exit_btn = Button(text='Exit')

        start.bind(on_press=self.go_modes)
        about.bind(on_press=self.go_about)
        exit_btn.bind(on_press=self.exit_app)

        box.add_widget(title)
        box.add_widget(start)
        box.add_widget(about)
        box.add_widget(exit_btn)

        center.add_widget(box)
        root.add_widget(bg)
        root.add_widget(center)
        self.add_widget(root)

    def go_modes(self, instance):
        self.manager.current = 'modes'

    def go_about(self, instance):
        self.manager.current = 'about'

    def exit_app(self, instance):
        App.get_running_app().stop()


class ModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        bg = Image(
            source='assets/images/background.png',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )

        center = AnchorLayout(anchor_x='center', anchor_y='center')
        box = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(250, 300),
            spacing=10
        )

        title = Label(text='SELECT MODE', font_size=26)
        easy = Button(text='Easy')
        medium = Button(text='Medium')
        hard = Button(text='Hard')
        back = Button(text='Back')

        easy.bind(on_press=lambda x: self.start('Easy'))
        medium.bind(on_press=lambda x: self.start('Medium'))
        hard.bind(on_press=lambda x: self.start('Hard'))
        back.bind(on_press=self.go_back)

        box.add_widget(title)
        box.add_widget(easy)
        box.add_widget(medium)
        box.add_widget(hard)
        box.add_widget(back)

        center.add_widget(box)
        root.add_widget(bg)
        root.add_widget(center)
        self.add_widget(root)

    def start(self, mode):
        game = self.manager.get_screen('game')
        game.set_mode(mode)
        self.manager.current = 'game'

    def go_back(self, instance):
        self.manager.current = 'dashboard'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [(100, 100)]
        self.direction = (BLOCK, 0)
        self.food = (200, 200)
        self.speed = 0.2
        self.event = None
        self.score = 0
        self.game_over = False
        self.paused = False

        Window.bind(on_key_down=self.key_input)

        self.main_layout = BoxLayout(orientation='vertical')

        # UI Bar
        self.top_bar = BoxLayout(size_hint=(1, 0.1))
        self.label = Label(text='MODE: NONE')
        self.score_label = Label(text='SCORE: 0')
        self.top_bar.add_widget(self.label)
        self.top_bar.add_widget(self.score_label)

        # Game Area with your custom Background
        self.canvas_area = FloatLayout()
        self.bg_image = Image(
            source='assets/images/background_grid.png',  # Ensure filename is correct
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        self.canvas_area.add_widget(self.bg_image)

        # Bottom Menu
        back_btn = Button(text='Back to Menu', size_hint=(1, 0.1))
        back_btn.bind(on_press=self.back)

        self.main_layout.add_widget(self.top_bar)
        self.main_layout.add_widget(self.canvas_area)
        self.main_layout.add_widget(back_btn)

        self.add_widget(self.main_layout)

    def set_mode(self, mode):
        self.label.text = f'MODE: {mode}'
        if mode == 'Easy':
            self.speed = 0.25
        elif mode == 'Medium':
            self.speed = 0.15
        elif mode == 'Hard':
            self.speed = 0.08
        self.restart()

    def restart(self):
        # Remove any existing Game Over UI
        for child in self.canvas_area.children[:]:
            if isinstance(child, BoxLayout):
                self.canvas_area.remove_widget(child)

        self.snake = [(100, 100)]
        self.direction = (BLOCK, 0)
        self.food = (randint(0, 18) * BLOCK, randint(0, 22) * BLOCK)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.score_label.text = 'SCORE: 0'

        if self.event:
            self.event.cancel()
        self.event = Clock.schedule_interval(self.update, self.speed)

        self.canvas_area.canvas.after.clear()
        self.draw()

    def draw(self):
        with self.canvas_area.canvas.after:
            # Snake Color (Dark Green to stand out on Yellow)
            Color(0.1, 0.5, 0.1, 1)
            for x, y in self.snake:
                Rectangle(pos=(x, y), size=(BLOCK, BLOCK))

            # Food Color (Red)
            Color(1, 0, 0, 1)
            Rectangle(pos=self.food, size=(BLOCK, BLOCK))

    def update(self, dt):
        if self.paused or self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Collision Check
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT):

            self.game_over = True
            if self.event:
                self.event.cancel()

            # Show Game Over Overlay
            over_layout = BoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint=(None, None),
                size=(300, 200),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            over_layout.add_widget(Label(text='GAME OVER', font_size=40, color=(0, 0, 0, 1)))
            over_layout.add_widget(Label(text=f'FINAL SCORE: {self.score}', font_size=24, color=(0, 0, 0, 1)))
            over_layout.add_widget(Label(text='Press R to Restart', font_size=18, color=(0, 0, 0, 1)))

            self.canvas_area.add_widget(over_layout)
            return

        self.snake.insert(0, new_head)

        # Eating Food
        if new_head == self.food:
            self.score += 1
            self.score_label.text = f'SCORE: {self.score}'
            self.food = (randint(0, 18) * BLOCK, randint(0, 22) * BLOCK)
        else:
            self.snake.pop()

        self.canvas_area.canvas.after.clear()
        self.draw()

    def key_input(self, window, key, *args):
        if key == ord('r'):
            self.restart()
        elif key == 32 or key == ord('p'):
            self.paused = not self.paused
            self.label.text = 'PAUSED' if self.paused else 'GAME RUNNING'

        if self.paused: return

        if (key == 273 or key == ord('w')) and self.direction != (0, -BLOCK):
            self.direction = (0, BLOCK)
        elif (key == 274 or key == ord('s')) and self.direction != (0, BLOCK):
            self.direction = (0, -BLOCK)
        elif (key == 275 or key == ord('d')) and self.direction != (-BLOCK, 0):
            self.direction = (BLOCK, 0)
        elif (key == 276 or key == ord('a')) and self.direction != (BLOCK, 0):
            self.direction = (-BLOCK, 0)

    def back(self, instance):
        if self.event:
            self.event.cancel()
        self.manager.current = 'dashboard'


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)
        layout.add_widget(Label(text='SNAKE GAME\n\nBSIT Project\nCreated with Kivy', font_size=20, halign='center'))
        back = Button(text='Back', size_hint=(1, 0.2))
        back.bind(on_press=self.go_back)
        layout.add_widget(back)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'dashboard'


class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Dashboard(name='dashboard'))
        sm.add_widget(ModeScreen(name='modes'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(AboutScreen(name='about'))
        return sm


if __name__ == '__main__':
    SnakeApp().run()