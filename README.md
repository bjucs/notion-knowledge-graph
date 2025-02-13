Setting up development environment for `notion-knowledge-graph`:
- Run `python3 -m venv venv` to create the virtual Python environment for development & testing (if not already created)
- Run `source venv/bin/activate` to activate the virtual environment via the CLI
- Run `pip install -r requirements.txt` to install Python dependencies (if not already installed)
- (Optional): Run `deactivate` to disable venv after finishing development 

Installing new dependencies: 
- Use `pip install <dependency-name>` once within the venv to install any new dependencies, followed by `pip freeze > requirements.txt` to pipe all new dependencies to the `requirements.txt` dependencies list 
- This acts as similar to a `package-lock.json`, allowing collaborators to install exact dependencies with the correct versions.