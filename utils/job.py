import os


# Function to create a repository
def create_repository(repository):
    if not os.path.exists(repository):
        print("Creating repository", repository)
        os.makedirs(repository)
