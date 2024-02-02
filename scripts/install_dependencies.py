import subprocess

def install_dependencies():
    try:
        # Read the requirements.txt file
        with open('requirements.txt', 'r') as requirements_file:
            requirements = requirements_file.readlines()
        
        # Install dependencies using pip
        for requirement in requirements:
            requirement = requirement.strip()
            if requirement:
                subprocess.run(['pip', 'install', requirement])

        print("Dependencies installed successfully.")

    except Exception as e:
        print(f"Error installing dependencies: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    main_script_path = os.path.join(script_dir, "..", "main.py")
    
    subprocess.run(["python", main_script_path])