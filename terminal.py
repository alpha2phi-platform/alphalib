from prompt_toolkit import ANSI, HTML
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt

if __name__ == "__main__":
    print(HTML('<aaa fg="ansiwhite" bg="ansigreen">White on green</aaa>'))
    print(ANSI("\x1b[31mhello \x1b[32mworld"))
