# Only once for the first commit in a new repository

1. git init --> Initialize Git (if not already)
2. git add . --> Add all files in the folder
3. git commit -m "Initial commit" --> Commit your files
4. git branch -M main --> Rename your local branch to 'main'
5. git remote add origin https://github.com/githubUsername/FileName.git --> Add your GitHub remote
6. git push -u origin main --> Push your code to GitHub

# Commit Push Pull

1. git remote -v --> Check linked Repositor
2. git add.
3. git commit -m "comments"
4. git push origin main
5. git pull

# Delete Folder & File

1.  git rm filename --> Delete file from Git
2.  git rm -r foldername --> Delete folder from Git
3.  git rm --cached filename --> Delete from Git, keep locally
4.  git rm -r --cached foldername --> Delete from Git, keep locally
5.  git commit -m "Delete ..." --> Commit deletion

# Clone a GitHub Repository

    1.	git clone https://github.com/githubUsername/RepoName.git –> Download the repo and set up Git locally
    2.	cd RepoName –> Move into the cloned folder
    3.	git pull –> Update your local copy with the latest changes from GitHub

# Run a Python Program

1. python filename.py
2. python3 filename.py
