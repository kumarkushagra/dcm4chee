import os

def delete_temp_files():
    directory_path = "./Temp_Downloads"

    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
            except OSError as e:
                print(f"Failed to delete {dir_path}. Reason: {e}")
    print("Temporary files deleted.")


if __name__=="__main__":
    delete_temp_files()