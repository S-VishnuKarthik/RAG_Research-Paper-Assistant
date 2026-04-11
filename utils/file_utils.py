import os

def save_uploaded_file(uploaded_file, folder="data/"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, uploaded_file.name)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return filepath

def list_files(folder):
    return os.listdir(folder) if os.path.exists(folder) else []

def file_exists(path):
    return os.path.exists(path)