import sys

def check_file_for_backdoor(filename):
    try:
        with open(filename, 'r') as file:
            contents = file.read()
            if "backdoor" in contents:
                print(f'The string "backdoor" was found in {filename}.')
            else:
                print(f'The string "backdoor" was not found in {filename}.')
    except FileNotFoundError:
        print(f'Error: The file {filename} does not exist.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_backdoor.py <filename>")
    else:
        filename = sys.argv[1]
        check_file_for_backdoor(filename)