import os


# Function to create a repository
def create_repository(repository):
    if not os.path.exists(repository):
        print("Creating repository", repository)
        print("Press Ctrl + C to exit")
        os.makedirs(repository)
