import os
import shutil

def clear_pub_dir(pub_path):

    if os.path.exists(pub_path):
        pub_list = os.listdir(pub_path)
    if len(pub_list) != 0:
        for file in pub_list:
            filename = os.path.join(pub_path, file)
            if os.path.isdir(filename):
                shutil.rmtree(filename)
            else:
                os.remove(filename)
            print(f"REMOVING: {filename}")

    return True

def copy_static_to_public(static_path, pub_path):

    if not os.path.exists(pub_path):
        os.mkdir(pub_path)
        print(f"CREATING DIR: {pub_path}")

    if os.path.exists(static_path):
        static_list = os.listdir(static_path)
    else:
        print(f"STATIC DIRECTORY DOES NOT EXIST: {static_path}")
        return False

    print(static_list)
    recurse_copy(static_list, static_path, pub_path)
    return True

def recurse_copy(static_list, static_path, pub_path):
    list_len = len(static_list)
    for static in static_list:
        if os.path.isfile(os.path.join(static_path, static)):
            file = os.path.join(static_path, static)
            new_file = os.path.join(pub_path, static)
            print(f"COPY: {file} TO: {new_file}") 
            shutil.copy(file, new_file)
        
        elif os.path.isdir(os.path.join(static_path, static)):
            cur_dir = os.path.join(static_path, static)
            new_dir = os.path.join(pub_path, static)
            print(f"COPY DIR: {cur_dir} TO: {new_dir}")
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            recurse_copy(os.listdir(cur_dir), cur_dir, new_dir)

    if list_len == 0:
        return True

def main():
    pub_path = "./public"
    static_path = "./static"
    
    status_rc = clear_pub_dir(pub_path)
    if status_rc:
        print("SUCCESS: Cleared old public directory")

    copy_static_to_public(static_path, pub_path)


if __name__ == "__main__":
    main()
