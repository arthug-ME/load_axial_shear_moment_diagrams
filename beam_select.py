from subprocess import call
import os

# Pre: Accepts nothing.
# Post: This clears the console when called.
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Pre: Accepts nothing.
# Post: This prints the introduction to allow the user to select the beam they need.
#       Will only accept whole numbers between [1, 3]
def introduction():
    print("1 - Simply Supported Beam")
    print("2 - Cantilever Beam")
    print("3 - Overhanging Beam")
    print()
    while True:
        try:
            inputted_number = float(input("Hello, please pick the beam required for "
                                          "your situation by typing the necessary number: "))
            if inputted_number.is_integer() and 0 <= inputted_number <= 3:
                return int(inputted_number)
            else:
                print("Invalid input. Please choose from these three options"
                      " and input a whole number.")
        except ValueError:
            print("Invalid input. Please input only a number.")


# Pre: Accepts inputted_number
# Post: This accepts the number that the user inputs and opens the corresponding file
def open_py_file(inputted_number):
    clear_console()
    script_directory = os.path.dirname(os.path.abspath(__file__))
    beam_type = ""
    if inputted_number == 1:
        beam_type = "simply_supported_beam.py"
    elif inputted_number == 2:
        beam_type = "cantilever_beam.py"
    else:
        beam_type = "overhanging_beam.py"
    script_path = os.path.join(script_directory, 'beam_types', beam_type)
    call(["python", script_path])


def main():
    inputted_number = introduction()
    open_py_file(inputted_number)


if __name__ == "__main__":
    main()
