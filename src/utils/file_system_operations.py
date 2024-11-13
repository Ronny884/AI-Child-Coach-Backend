import os


def create_or_clean_directory_in_media(directory_name):
    media_path = os.path.join(os.getcwd(), 'media')
    directory_path = os.path.join(media_path, directory_name)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Директория '{directory_path}' успешно создана.")
    else:
        delete_files_in_directory(directory_path)
        print(f"Директория '{directory_path}' очищена.")


def delete_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


