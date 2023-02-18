# continous-code-quality
Analyse whether we are actually doing continuous code quality?

This project is using poetry for dependency management so you will have to install poetry on your local.

1. Install potery if not already present in your local system:
    
    curl -sSL https://install.python-poetry.org | python3 -
2. Use poetry install to install the packages required.
    
    poetry install  

Developement process:
1. Create a branch from main.
2. Do the developement work.
3. Merge to main.


If any new dependencies are added use this command to generate a requirement file.
    
    poetry export -f requirements.txt --without-hashes --output requirements.txt
