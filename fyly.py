import click
import os
import gpt
from collections import Counter
import hashlib
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import csv

@click.group()
def commands():
    pass

@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
def ext_sort(path):

    if path == None:
        path = os.getcwd()
    click.echo("Extension sorting files in " + path + "\n")
    
    for filename in os.listdir(path):
        if filename != "main.py":
            file_extension = os.path.splitext(filename)[1]
            if file_extension == "":
                continue
            if not os.path.exists(path + "/" + file_extension):
                os.makedirs(path + "/" + file_extension)
            os.rename(path + "/" + filename, path + "/" + file_extension + "/" + filename)

@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
def smart_sort(path):
    if path == None:
        path = os.getcwd()
    click.echo("Smart sorting files in " + path + "\n")

    filenames = []

    ## retrieve all filenames for ai processing
    for filename in os.listdir(path):
        if filename != "main.py":
            filenames.append(filename)
    
    # read in prompt
    prompt = open("prompt.txt", "r").read()

    prompt = """Organize the following list of files into appropriate folders: """ + ", ".join(filenames) + """

The folders should be: school, finances, images, audio, videos.

Format your output like this:

[/foldername1]
[filename1]
[filename2]

[/foldername2]
[filename3]
[filename4]

Be sure every file and folder is present, and each folder is separated by two newline characters.
"""
    file_groups = gpt.get_response(prompt)

    file_groups = file_groups.replace("Folder: ", "")

    file_groups = file_groups.replace("[", "")

    file_groups = file_groups.replace("]", "")
    
    file_groups = file_groups.replace("- ", "")

    ## put files in folders
    for file_group in file_groups.split("\n\n"):
        file_group = file_group.split("\n")
        folder_name = file_group[0]
        if not os.path.exists(path + "/" + folder_name):
            os.makedirs(path + "/" + folder_name)
        for file in file_group[1:]:
            try:
                os.rename(path + "/" + file, path + "/" + folder_name + "/" + file)
            except (FileNotFoundError):
                continue

    # remove empty directories
    for dirpath, dirnames, filenames in os.walk(path):
        if len(dirnames) == 0 and len(filenames) == 0:
            os.rmdir(dirpath)

@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
def rm_dupes(path):
    list_of_files = os.walk(path)
  
    unique_files = dict()
    
    for root, folders, files in list_of_files:
    
        for file in files:
    
            file_path = Path(os.path.join(root, file))
    
            Hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    
            if Hash_file not in unique_files:
                unique_files[Hash_file] = file_path
            else:
                os.remove(file_path)
                print(f"{file_path} has been deleted")

@click.command()
@click.argument('path', type=click.Path(exists=True), required=False)
# comma seperated option
@click.option('--comma', '-c', is_flag=True, help="Comma seperated list of files")
def list_files(path, comma):
    if path == None:
        path = os.getcwd()
    click.echo("Listing files in " + path + "\n")

    for filename in os.listdir(path):
        if comma:
            print(filename, end=", " if filename != os.listdir(path)[-1] else "")
        else:
            print(filename)

@click.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
def view_ext_stats(folder_path):
    if folder_path == None:
        folder_path = os.getcwd()
    
    click.echo("\nListing files in " + folder_path + "\n")

    for filename in os.listdir(folder_path):
        print(filename)

    click.echo("\n\nGetting file statistics for " + folder_path + "\n")

    extension_counter = Counter()

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_extension = os.path.splitext(filename)[1]
            extension_counter[file_extension] += 1

    # Calculate the total number of files
    total_files = sum(extension_counter.values())

    # Calculate the file type percentages
    file_type_percentages = {ext: (count / total_files * 100) for ext, count in extension_counter.items()}

    click.echo("File Type Statistics:")
    for ext, percentage in file_type_percentages.items():
        print(f"{'Folder' if ext=='' else ext}: {percentage:.2f}%")
    print("\nTotal Files:", total_files)

@click.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
def get_ext_stats(folder_path):
    if folder_path == None:
        folder_path = os.getcwd()
    
    click.echo("\nListing files in " + folder_path + "\n")

    for filename in os.listdir(folder_path):
        print(filename)

    click.echo("\n\nGetting file statistics for " + folder_path + "\n")

    extension_counter = Counter()

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_extension = os.path.splitext(filename)[1]
            extension_counter[file_extension] += 1

    # Calculate the total number of files
    total_files = sum(extension_counter.values())

    # Calculate the file type percentages
    file_type_percentages = {ext: (count / total_files * 100) for ext, count in extension_counter.items()}

    click.echo("File Type Statistics:")
    with open('ext_stats.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for ext, percentage in file_type_percentages.items():
            print(f"{ext}: {percentage:.2f}%")
            csv_writer.writerow([ext, round(percentage, 1)])
        print("\nTotal Files:", total_files)

def memory_stats(folder_path):
    total_memory_usage = 0
    
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            
            file_size = os.path.getsize(file_path)
            
            total_memory_usage += file_size
    
    return total_memory_usage

@click.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
def view_memory_usage(folder_path):
    if folder_path == None:
        folder_path = os.getcwd()

    total_folder_memory = memory_stats(folder_path)
    
    file_memory_statistics = {}
    
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            
            file_size = os.path.getsize(file_path)
            
            memory_percentage = (file_size / total_folder_memory) * 100
            
            file_memory_statistics[file_path] = memory_percentage

    click.echo("File Memory Usage Statistics:")
    for file_path, memory_percentage in file_memory_statistics.items():
        click.echo(f"{os.path.basename(file_path)}: {memory_percentage:.2f}%")

@click.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
def get_memory_usage(folder_path):
    if folder_path == None:
        folder_path = os.getcwd()

    total_folder_memory = memory_stats(folder_path)
    
    file_memory_statistics = {}
    
    with open('memory_stats.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:  

                file_path = os.path.join(dirpath, filename)
                
                file_size = os.path.getsize(file_path)
                
                memory_percentage = (file_size / total_folder_memory) * 100
                memory_percentage = round(memory_percentage)
                
                file_memory_statistics[file_path] = memory_percentage

                csv_writer.writerow([filename, memory_percentage, file_size])

    click.echo("File Memory Usage Statistics:")
    for file_path, memory_percentage in file_memory_statistics.items():
        click.echo(f"{os.path.basename(file_path)}: {memory_percentage:.2f}%")
    

def create_folder(drive, folder_name):
    folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()
    return folder

@click.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
@click.argument('destination_folder_name', type=str, required=True)
def upload_to_drive(folder_path, destination_folder_name):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    destination_folder = create_folder(drive, destination_folder_name)

    for x in os.listdir(folder_path):
        file_path = os.path.join(folder_path, x)
    
        if os.path.isfile(file_path):
            f = drive.CreateFile({'title': x, 'parents': [{'id': destination_folder['id']}]})
            f.SetContentFile(file_path)
            f.Upload()
        
            f = None

            print(f"Uploaded: {x} to {destination_folder_name}")

@click.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
def takeout_files(folder_path):
    if folder_path == None:
        folder_path = os.getcwd()
    click.echo("Taking files out of folders in " + folder_path + "\n")

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            os.rename(file_path, os.path.join(folder_path, filename))

@click.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
def rm_empty_dirs(folder_path):
    if folder_path == None:
        folder_path = os.getcwd()
    click.echo("Removing empty directories in " + folder_path + "\n")

    count = 0

    for dirpath, dirnames, filenames in os.walk(folder_path):
        if len(dirnames) == 0 and len(filenames) == 0:
            click.echo("Removing " + dirpath)
            count += 1
            os.rmdir(dirpath)
    
    click.echo("Removed " + str(count) + " empty directories")

commands.add_command(ext_sort)
commands.add_command(smart_sort)
commands.add_command(rm_dupes)
commands.add_command(list_files)
commands.add_command(view_ext_stats)
commands.add_command(get_ext_stats)
commands.add_command(view_memory_usage)
commands.add_command(get_memory_usage)
commands.add_command(upload_to_drive)
commands.add_command(takeout_files)
commands.add_command(rm_empty_dirs)

if __name__ == '__main__':
    commands()