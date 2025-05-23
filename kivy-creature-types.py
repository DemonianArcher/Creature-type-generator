"""First try doing Kivy"""

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import ColorProperty
from random import choice
import os

# Path to the Playfair Display font file
FONT_PATH = "C:\python_projects\Creature-type-generator\PlayfairDisplayfont\PlayfairDisplay-VariableFont_wght.ttf"

# Custom button with rounded corners and color change on touch
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Make the old button background transparent
        self.font_name = FONT_PATH  # Set the font to Playfair Display
        with self.canvas.before:
            self.color_instruction = Color(0.0, 0.0, 0.5, 1)  # Dark blue color
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
            self.bind(pos=self.update_rect, size=self.update_rect)

    # Update the size and position of the rounded rectangle
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # Change color on touch down
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.color_instruction.rgba = (0.0, 0.0, 0.7, 1)  # Lighter blue color on touch down
        return super(RoundedButton, self).on_touch_down(touch)

    # Reset color on touch up
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.color_instruction.rgba = (0.0, 0.0, 0.5, 1)  # Reset to dark blue color on touch up
        return super(RoundedButton, self).on_touch_up(touch)

# Main application class for the Creature Type Generator
class CreatureGeneratorApp(App):
    background_color = ColorProperty((0.1, 0.1, 0.1, 1))  # Very dark grey color

    # Build the main layout of the application
    def build(self):
        self.creature_types = self.load_creature_types("creature_types.txt")
        if not self.creature_types:
            self.creature_types = ["Default Creature"]
            print("Warning: creature_types.txt is empty or not found. Using default creature.")

        self.generated_creatures = []
        self.load_generated_creatures()  # Load from file on startup

        Window.size = (1080, 1920)  # Adjust as needed for your target devices
        Window.clearcolor = self.background_color

        main_layout = FloatLayout()

        main_layout.add_widget(self.create_title())
        main_layout.add_widget(self.create_generate_button())
        main_layout.add_widget(self.create_intermediate_label())
        main_layout.add_widget(self.create_prev_gen_creatures())
        main_layout.add_widget(self.create_result_input())
        main_layout.add_widget(self.create_generated_list())
        main_layout.add_widget(self.create_new_game_button())

        return main_layout

    # Create the title label
    def create_title(self):
        return Label(text="Creature Type Generator", font_size=90, halign='center', size_hint=(0.8, 0.1), pos_hint={'x': 0.1, 'top': 1}, font_name=FONT_PATH)

    # Create the generate creature button
    def create_generate_button(self):
        generate_button = RoundedButton(text="Generate Creature Type?", size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.69}, font_size=65)
        generate_button.bind(on_press=self.generate_creature)
        return generate_button

    # Create the intermediate label
    def create_intermediate_label(self):
        return Label(text="This creature is of course a...", font_size=40, halign='center', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.614}, font_name=FONT_PATH)

    # Create the previously generated creatures label
    def create_prev_gen_creatures(self):
        return Label(text="Previously generated creatures:", font_size=40, halign='center', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.48}, font_name=FONT_PATH)

    # Create the result input field
    def create_result_input(self):
        self.result_input = TextInput(readonly=True, multiline=False, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.55}, font_size=60, halign='center', padding_y=(10, 10), background_color=(0, 0, 0, 0), foreground_color=(1, 1, 1, 1), font_name=FONT_PATH)
        self.result_input.bind(text=self.update_text_alignment)
        return self.result_input

    # Update the text alignment in the result input field
    def update_text_alignment(self, *args):
        self.result_input.text = self.result_input.text.strip()
        self.result_input.cursor = (len(self.result_input.text), 0)

    # Create the scrollable list of generated creatures
    def create_generated_list(self):
        self.generated_list = ScrollView(size_hint=(0.3, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        with self.generated_list.canvas.before:
            Color(0.15, 0.15, 0.15, 1)  # Dark grey color
            self.rect = Rectangle(size=self.generated_list.size, pos=self.generated_list.pos)
        self.generated_list.bind(size=self.update_generated_list_rect, pos=self.update_generated_list_rect)
        self.generated_creatures_layout = GridLayout(cols=1, size_hint_y=None, padding=[0, 40, 0, 20], spacing=40)
        self.generated_list.add_widget(self.generated_creatures_layout)
        self.update_generated_list()
        return self.generated_list

    # Update the size and position of the rectangle in the generated list
    def update_generated_list_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    # Create the new game button
    def create_new_game_button(self):
        new_game_button = RoundedButton(text="New Game", size_hint=(0.2, 0.1), pos_hint={'right': 0.97, 'y': 0.03})
        new_game_button.bind(on_press=self.new_game)
        return new_game_button

    # Load creature types from a file
    def load_creature_types(self, filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(filepath, 'r', encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    # Load previously generated creatures from a file
    def load_generated_creatures(self):
        filepath = os.path.join(os.path.dirname(__file__), "generated_creatures.txt")
        try:
            with open(filepath, 'r', encoding="utf-8") as f:
                self.generated_creatures = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            pass  # Ignore if file doesn't exist yet

    # Generate a new creature type
    def generate_creature(self, instance):
        if not self.creature_types:
            self.result_input.text = "No creature types loaded!"
            return

        creature = choice(self.creature_types)
        self.result_input.text = creature
        self.generated_creatures.append(creature)
        self.save_generated_creatures()
        self.update_generated_list()

    # Update the list of generated creatures
    def update_generated_list(self):
        self.generated_creatures_layout.clear_widgets()
        for creature in self.generated_creatures:
            label = Label(text=creature, size_hint_y=None, height=30, font_name=FONT_PATH)
            self.generated_creatures_layout.add_widget(label)
        self.generated_creatures_layout.height = len(self.generated_creatures) * 70  # Adjust height to account for spacing

    # Save the list of generated creatures to a file
    def save_generated_creatures(self):
        filepath = os.path.join(os.path.dirname(__file__), "generated_creatures.txt")
        with open(filepath, 'w', encoding="utf-8") as f:
            for creature in self.generated_creatures:
                f.write(creature + '\n')

    # Start a new game by clearing the list of generated creatures
    def new_game(self, instance):
        self.generated_creatures = []
        self.result_input.text = ""
        self.update_generated_list()
        self.save_generated_creatures()  # Save empty list to clear file


if __name__ == '__main__':
    CreatureGeneratorApp().run()
