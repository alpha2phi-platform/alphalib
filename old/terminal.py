from prompt_toolkit import ANSI, HTML, Application, PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt

if __name__ == "__main__":
    app = Application(full_screen=True)
    app.run()  # Create prompt object.
