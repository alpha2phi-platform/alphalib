from prompt_toolkit import prompt

if __name__ == "__main__":
    answer = prompt("Query>")
    print("You ask: %s" % answer)
