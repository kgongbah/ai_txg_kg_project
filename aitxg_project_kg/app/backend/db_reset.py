import os 

#Delete test SQLite Database stored on local computer
def delete_test_db():
    test_db_path = r"C:\Users\642672\aitxg_project_kg\app\test.db"
    try:
        if not os.path.exists(test_db_path):
            print("test_db path not found.")
        else:
            os.remove(test_db_path)
            print("test.db deleted successfully.")
    except Exception as e:
        print(f"Unable to delete test_db: {e}")
    return 


#Delete all images uploaded by users
def delete_all_static_uploads():
    static_uploads_folder_path = r"C:\Users\642672\aitxg_project_kg\app\static\uploads"

    for filename in os.listdir(static_uploads_folder_path):
        file_path = os.path.join(static_uploads_folder_path, filename)
        try:
            if not os.path.exists(file_path):
                print(f"Image path not found: {file_path}")
            else:
                os.remove(file_path)
                print(f"Image deleted successfully. Path: {file_path}")
        except Exception as e:
            print(f"Unable to delete image: {e}")
    return

if __name__ == "__main__":
    delete_test_db()
    delete_all_static_uploads()