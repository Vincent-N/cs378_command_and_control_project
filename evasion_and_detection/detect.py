import shutil
import subprocess
import os

def get_ls_path():
    """
    Find the path of 'ls'.

    :return: Full path to 'ls' if found, else None
    """
    print("Testing ls Path:")
    print()
    ls_path = shutil.which('ls')
    if ls_path != "/bin/ls":
        print("ALERT: path isn't as expected: " + ls_path)
    else:
        print("Path is as expected")

def is_ls_alias_or_function():
    """
    Check if 'ls' has aliases

    :return: True if 'ls' is not aliased, False otherwise
    """
    print("Testing ls Aliases:")
    print()
    cwd = os.getcwd()
    result = subprocess.run(['bash', '-ic', 'alias', 'ls'], stdout=subprocess.PIPE)

    # Update with files you want to check.
    files_to_check = [cwd + "/.bashrc", "/etc/profile", cwd+"/.bash_profile"]

    alerted = False
    for file in files_to_check:
        print("File: " + file)
        result = subprocess.run(
            ['grep', 'alias ls', file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True 
        )   
        if result.returncode == 0:
                # Pattern found
                matched_lines = result.stdout.strip().split('\n')
                for line in matched_lines:
                      
                    splitted = line.split("=")
                    potential_path = splitted[1].replace("'", "")
                      
                    # Check if it is replacing something or if the alias is a file path
                    if "grep" in line or os.path.isfile(splitted[1].replace("'", "")):
                        print("SUSPICIOUS Alias found: " + line)
                        print()
                        alerted = True
                    else: 
                         print("Alias found: " + line)
                         print()
        elif result.returncode == 1:
                # Pattern not found
                print("No aliases found in " + file)
                print()
        else:
                # Error occurred
                print(f"Error executing grep: {result.stderr}")
                print()
    if not alerted:
         print("No aliases found for ls.")
         print()
        

if __name__ == "__main__":
    print("---------------------------------------")
    get_ls_path()
    print("---------------------------------------")
    is_ls_alias_or_function()
