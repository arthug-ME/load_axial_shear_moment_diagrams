from subprocess import call
import os

def introduction():
    print("1 - Simply Supported Beam")
    print("2 - Cantilever Beam")
    print("3 - Overhanging Beam")
    print()
    while True:
        try:
            inputted_number = float(input("Hello, please pick the beam required for "
                                          "your situation by typing the necessary number: "))
            if inputted_number < 0 or inputted_number > 3:
                print("Invalid input. Please choose from these three options")
            else:
                return inputted_number
        except ValueError:
            print("Invalid input. Please input only a number.")

def open_py_file(inputted_number):
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