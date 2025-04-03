import os
import shutil
from markdown_html import markdown_to_html_node

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

def extract_title(markdown):
    header_line = ""
    markdown_list = markdown.splitlines()
    for i in range(len(markdown_list)):
        if markdown_list[i].startswith("# "):
            result = markdown_list[i][2:]
            return (result, '\n'.join(markdown_list).strip())

def generate_page(from_path, template_path, dest_path):
    file = open(from_path, "r")
    source = file.read()
    if source:
        print(f"Loaded file at {from_path}")
    else:
        print(f"Failed to load file at {from_path}")
        return False

    file = open(template_path, "r")
    template = file.read()
    if source:
        print(f"Loaded file at {template_path}")
    else:
        print(f"Failed to load file at {template_path}")
        return False
    
    print(f"Generating page from {from_path} and {template_path} to {dest_path}")

    header_md = extract_title(source)
    header = header_md[0]
    md = header_md[1]
    start = template.find("{{")
    end = template.find("}}")
    content_start = template[end + 2:].find("{{")
    content_end = template[end + 2:].find("}}")
    md = markdown_to_html_node(md)

    html = template[:start] + header + template[end + 2:content_start + (end + 2)] + md.to_html() + template[content_end + (end + 4):]
    print(html) 
    file = open(dest_path, "w")
    print(f"Creating file at {file}")

    file.write(html)
    return True

def copy_content_to_public(source_path, template_path, destination):

    if os.path.exists(source_path):
        source_list = os.listdir(source_path)
        print(f"CONTENT SOURCE LIST: {source_list}")
    else:
        print(f"CONTENT DIRECTORY DOES NOT EXIST: {source_path}")
        return False

    print(source_list)
    generate_page_recurse(source_list, source_path, template_path, destination)
    #return True

def generate_page_recurse(source_list, source_path, template_path, destination):
    list_len = len(source_list)
    for source in source_list:
        if os.path.isfile(os.path.join(source_path, source)):
            source_file = os.path.join(source_path, source)
            destination_path = os.path.join(destination, source[:-2] + 'html')
            print(f"Generate from: {source_file} TO: {destination_path}") 
            generate_page(source_file, template_path, destination_path)

        elif os.path.isdir(os.path.join(source_path, source)):
            new_source_path = os.path.join(source_path, source)
            destination_path = os.path.join(destination, source)
            print(f"MOVE DIR: {new_source_path} TO: {destination_path}")
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
            generate_page_recurse(os.listdir(new_source_path), new_source_path, template_path, destination_path)

    if list_len == 0:
        return True


def main():
    pub_path = "./public"
    static_path = "./static"
    
    status_rc = clear_pub_dir(pub_path)
    if status_rc:
        print("SUCCESS: Cleared old public directory")

    copy_static_to_public(static_path, pub_path)
    
    source_path = "content/"
    template_path = "template.html"
    destination = "public/"
    status = copy_content_to_public(source_path, template_path, destination)
    if status:
        print(f"Page Generation Succes")


if __name__ == "__main__":
    main()
