import pyxel

class ChatApp:
    def __init__(self):
        pyxel.init(256, 160, title="Pyxel Chat Experience")
        self.messages = []  # Stores chat messages as (text, is_user)
        self.input_text = ""
        self.typing_mode = True
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.typing_mode:
            self.handle_input()

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.process_user_input()

    def handle_input(self):
        # allow a-z
        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            # add the key
            if pyxel.btnp(key):
                self.input_text += chr(key).lower()

        # check for backspace
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.input_text) > 0:
            # remove previous letter
            self.input_text = self.input_text[:-1]

        # check for space
        if pyxel.btnp(pyxel.KEY_SPACE):
            # add a space
            self.input_text += " "

    def process_user_input(self):
        if self.input_text.strip():
            self.add_message(self.input_text, is_user=True)
            self.input_text = ""
            self.typing_mode = False
            pyxel.play(3, 0)
            self.add_llm_response()

    def add_message(self, text, is_user):
        # Adds a message to the chat
        self.messages.append((text, is_user))

    def add_llm_response(self):
        # Adds a placeholder LLM response
        response = "Hello! How can I assist you today?"
        self.add_message(response, is_user=False)
        self.typing_mode = True




    def draw_avatar(self, x, y, is_user):
        # Draws a simple pixel avatar
        if is_user:
            pyxel.rect(x, y, 7, 7, 7)  # Head
            pyxel.rect(x - 1, y + 7, 9, 2, 6)  # Body
        else:
            pyxel.rect(x, y, 7, 7, 11)  # Head
            pyxel.rect(x - 1, y + 7, 9, 2, 8)  # Body
            pyxel.rect(x + 1, y + 1, 3, 3, 0)  # Eyes
            pyxel.rect(x + 3, y + 3, 1, 1, 7)  # Mouth

    def draw_message(self, text, y_offset, is_user):
        color = 7 if is_user else 11
        x_pos = 20 if is_user else 50  # Adjusted for better spacing
        avatar_x = x_pos - 15 if is_user else x_pos - 25

        # Draw the avatar
        self.draw_avatar(avatar_x, y_offset, is_user)

        # Split text into lines to fit within a certain width
        max_line_length = 50  # Increased max line length for more characters per line
        lines = [text[i:i + max_line_length] for i in range(0, len(text), max_line_length)]

        # Calculate bubble size based on the longest line and number of lines
        bubble_width = max(len(line) for line in lines) * 4 + 6
        bubble_height = len(lines) * 10 + 6
        pyxel.rect(x_pos - 3, y_offset - 3, bubble_width, bubble_height, 5)  # Chat bubble

        # Draw each line of text inside the bubble
        for i, line in enumerate(lines):
            pyxel.text(x_pos, y_offset + i * 10, line, color)  # Adjusted spacing to avoid overlap

    def draw(self):
        pyxel.cls(0)
        
        # Initial offset set higher to leave room for input box and spacing
        y_offset = 120  # Adjust to fit your needs
        
        # Ensure chat bubbles do not overlap with the input box
        min_y_offset = 25  # Minimum distance from the bottom of the screen
        
        for text, is_user in reversed(self.messages[-5:]):
            if y_offset >= min_y_offset:
                self.draw_message(text, y_offset, is_user)
                y_offset -= 35  # Adjust as needed for the size of each bubble

        # Draw input box at the bottom
        pyxel.rect(0, 150, 256, 10, 1)
        pyxel.text(5, 152, "> " + self.input_text, 7)

# check if startup
if __name__ == "__main__":
    # call the app
    ChatApp()
