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

Window.size = (400, 600)

BLOCK = 20


class Dashboard(Screen):

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
            size=(250, 250),
            spacing=10
        )

        title = Label(text='SNAKE GAME', font_size=28)

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

        Window.bind(on_key_down=self.key_input)

        layout = BoxLayout(orientation='vertical')

        self.label = Label(text='MODE: NONE', size_hint=(1, 0.1))
        self.canvas_area = FloatLayout()

        back = Button(text='Back', size_hint=(1, 0.1))
        back.bind(on_press=self.back)

        layout.add_widget(self.label)
        layout.add_widget(self.canvas_area)
        layout.add_widget(back)

        self.add_widget(layout)

    def set_mode(self, mode):

        self.label.text = f'MODE: {mode}'

        if mode == 'Easy':
            self.speed = 0.25
        elif mode == 'Medium':
            self.speed = 0.15
        elif mode == 'Hard':
            self.speed = 0.08

        if self.event:
            self.event.cancel()

        self.event = Clock.schedule_interval(self.update, self.speed)

    def draw(self):

        self.canvas_area.canvas.clear()

        with self.canvas_area.canvas:

            Color(0, 1, 0)
            for x, y in self.snake:
                Rectangle(pos=(x, y), size=(BLOCK, BLOCK))

            Color(1, 0, 0)
            Rectangle(pos=self.food, size=(BLOCK, BLOCK))

    def update(self, dt):

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = (
                randint(0, 18) * BLOCK,
                randint(0, 28) * BLOCK
            )
        else:
            self.snake.pop()

        self.draw()

    def key_input(self, window, key, *args):

        if key == 273:
            self.direction = (0, BLOCK)
        elif key == 274:
            self.direction = (0, -BLOCK)
        elif key == 275:
            self.direction = (BLOCK, 0)
        elif key == 276:
            self.direction = (-BLOCK, 0)

    def back(self, instance):
        self.manager.current = 'modes'


class AboutScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        label = Label(text='About Us\nBSIT Project', font_size=24)
        back = Button(text='Back')

        back.bind(on_press=self.go_back)

        layout.add_widget(label)
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


SnakeApp().run()