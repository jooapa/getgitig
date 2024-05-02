import inquirer, requests
from gitignore_files import gitignore_files

args = ""

def main():
    questions = [
        inquirer.List('action',
                    message="Do you want to search or select a gitignore file?",
                    choices=['Select', 'Search (by name or extension)'], 
                ),
    ]
    answers = inquirer.prompt(questions)
    action = answers['action']
    if action == 'Select':
        selection()
    elif action == 'Search (by name or extension)':
        search()

def search(search=None):
    try:
        if not search:
            questions = [
                inquirer.Text('search',
                            message="Search by name or extension",
                        ),
            ]
        
            answers = inquirer.prompt(questions)
            search = answers['search']
        
        language = find_in_gitignore_files_by_name(search)
        if not language:
            language = find_in_gitignore_files_by_ext(search)
        if not language:
            print("No language found")
            return
        
        print("Selected: " + language[0])
    except Exception as e:
        exit()
    
    download(language)
        
def find_in_gitignore_files_by_name(name):
    for language in gitignore_files:
        if name.lower() == language[0].lower():
            return language
        
    for language in gitignore_files:
        if name.lower() in language[0].lower():
            return language

def find_in_gitignore_files_by_ext(ext):
    for language in gitignore_files:
        if ext.lower() == language[1].lower():
            return language
        
    for language in gitignore_files:
        if ext.lower() in language[1].lower():
            return language
    return None
        
def selection():
    try:
        questions = [
            inquirer.List('language',
                        message="Select a language",
                        choices=[language[0] + ", " + language[1] for language in gitignore_files],
                    ),
        ]
        
        answers = inquirer.prompt(questions)
        
        language = answers['language']
        language = language.split(", ")
        language = (language[0], language[1])
        print("Selected: " + language[0])
        
    except Exception as e:
        exit()
    
    download(language)
    
def download(language):
    try:
        # if gitignore file already exists, ask if user wants to overwrite
        try:
            with open(".gitignore", "x") as f:
                f.write("")
                
        except FileExistsError:
            questions = [
                inquirer.List('action',
                            message=".gitignore already exists, do you want to overwrite it?",
                            choices=['Yes', 'No'],
                        ),
            ]
            
            answers = inquirer.prompt(questions)
            action = answers['action']
            if action == 'No':
                print("Aborted")
                return
    except Exception as e:
        exit()
        
    print("Downloading...")
    r = requests.get(gitignore_files[language])
    print("Downloaded")
    
    with open(".gitignore", "w") as f:
        f.write(r.text)

if __name__ == "__main__":
    # get arguments
    import sys
    args = sys.argv[1:]
    
    if len(args) == 0:
        main()
        exit()
        
    for arg in args:
        if arg == "-v" or arg == "--version":
            from __init__ import __version__
            print(__version__)
        elif arg == "-h" or arg == "--help":
            print(f"""
getgitig    
    -h, --help                          Show this help message
    -v, --version                       Show the version of the program
    -s, --select                        Select the right .gitignore file
    -sr, --search <name or extension>   Search for a .gitignore file by name or extension
    -l, --list                          List all available .gitignore files
                  """)
            
        elif arg == "-l" or arg == "--list":
            for language in gitignore_files:
                print(language[0] + ", " + language[1])
        elif arg == "-s" or arg == "--select":
            selection()
        elif arg == "-sr" or arg == "--search":
            search(args[1])
        else:
            print("Use -h or --help for help.")
            exit()
            
        