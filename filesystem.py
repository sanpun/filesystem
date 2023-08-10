import os
import platform
import shutil
import zipfile
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

class FileSystemGUI(tk.Tk):

    LOG_FILE = "filelog.txt"

    def __init__(self):
        super().__init__()
        self.title("File System")
        self.geometry("600x600")
        self.current_directory = os.getcwd()
        self.is_windows = platform.system() == 'Linux'
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Create File", command=self.create_file)
        file_menu.add_command(label="Delete File", command=self.delete_file)
        file_menu.add_command(label="Read File", command=self.read_file)
        file_menu.add_command(label="Write File", command=self.write_file)
        file_menu.add_command(label="Append File", command=self.append_file)
        file_menu.add_command(label="Rename File", command=self.rename_file)
        file_menu.add_command(label="Copy File", command=self.copy_file)
        file_menu.add_command(label="Get Permissions", command=self.get_permissions)
        file_menu.add_command(label="Set Permissions", command=self.set_permissions)


        dir_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Directory", menu=dir_menu)

        dir_menu.add_command(label="Create Directory", command=self.create_directory)
        dir_menu.add_command(label="Delete Directory", command=self.delete_directory)
        dir_menu.add_command(label="Rename Directory", command=self.rename_directory)
        dir_menu.add_command(label="Change Directory", command=self.change_directory)
        dir_menu.add_command(label="Copy Directory", command=self.copy_directory)
        dir_menu.add_command(label="List Directory Content", command=self.list_directory_contents)
        dir_menu.add_command(label="Get Directory Permissions", command=self.get_directory_permissions)
        dir_menu.add_command(label="Set Directory Permissions", command=self.set_directory_permissions)

        com_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="compress&decompress", menu=com_menu)
        com_menu.add_command(label="Compress File/Directory", command=self.compress_file_or_directory)
        com_menu.add_command(label="Decompress File/Directory", command=self.decompress_file_or_directory)

        self.log_area = tk.Text(self, wrap=tk.WORD)
        self.log_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.log_area.config(state=tk.DISABLED)

    def log_action(self, action, filename=None):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{current_time} - {action}"
        if filename:
            log_entry += f" - File/Directory: {filename}"
        log_entry += "\n"

        with open(self.LOG_FILE, "a") as log_file:
            log_file.write(log_entry)

        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, log_entry)
        self.log_area.config(state=tk.DISABLED)

    def create_file(self):
        filename = filedialog.asksaveasfilename(title="Create File", defaultextension=".txt")
        if not filename:
            return

        filepath = os.path.join(self.current_directory, filename)
        if os.path.exists(filepath):
            messagebox.showerror("Error", f"File '{filename}' already exists.")
            return

        with open(filepath, 'w') as file:
            messagebox.showinfo("Success", f"File '{filename}' created successfully.")

        self.log_action("Created file", filename)


    def create_directory(self):
        dirname = simpledialog.askstring("Create Directory", "Enter the directory name:")
        if not dirname:
            return

        dirpath = os.path.join(self.current_directory, dirname)
        if os.path.exists(dirpath):
            messagebox.showerror("Error", f"Directory '{dirname}' already exists.")
            return

        os.makedirs(dirpath)
        messagebox.showinfo("Success", f"Directory '{dirname}' created successfully.")

        self.log_action("Created directory", dirname)



    def delete_file(self):
        filename = filedialog.askopenfilename(title="Delete File")
        if not filename:
            return

        if os.path.exists(filename):
            os.remove(filename)
            messagebox.showinfo("Success", f"File '{filename}' deleted successfully.")
        else:
            messagebox.showerror("Error", f"File '{filename}' does not exist.")
        self.log_action("Deleted file", filename)


    def delete_directory(self):
        dirname = filedialog.askdirectory(title="Delete Directory")
        if not dirname:
            return

        if os.path.exists(dirname):
            shutil.rmtree(dirname)
            messagebox.showinfo("Success", f"Directory '{dirname}' deleted successfully.")
        else:
            messagebox.showerror("Error", f"Directory '{dirname}' does not exist.")
        self.log_action("Deleted directory", dirname)



    def read_file(self):
        filename = filedialog.askopenfilename(title="Read File")
        if not filename:
            return

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                file_content = file.read()
            messagebox.showinfo("File Content", file_content)
        else:
            messagebox.showerror("Error", f"File '{filename}' does not exist.")
        self.log_action("Read file", filename)


    def list_directory_contents(self):
        dirname = filedialog.askdirectory(title="List Directory Contents")
        if not dirname:
            return

        if os.path.exists(dirname):
            contents = os.listdir(dirname)
            content_str = "\n".join(contents)
            messagebox.showinfo("Directory Contents", content_str)
            self.log_action("Listed directory contents", dirname)
        else:
            messagebox.showerror("Error", f"Directory '{dirname}' does not exist.")



    def write_file(self):
        filename = filedialog.askopenfilename(title="Write File")
        if not filename:
            return

        if os.path.exists(filename):
            content = simpledialog.askstring("Write File", "Enter the content to write:")
            if content is not None:
                with open(filename, 'w') as file:
                    file.write(content)
                messagebox.showinfo("Success", f"Content written to file '{filename}' successfully.")
        else:
            messagebox.showerror("Error", f"File '{filename}' does not exist.")
        self.log_action("Wrote to file", filename)


    def append_file(self):
        filename = filedialog.askopenfilename(title="Append File")
        if not filename:
            return

        if os.path.exists(filename):
            content = simpledialog.askstring("Append File", "Enter the content to append:")
            if content is not None:
                with open(filename, 'a') as file:
                    file.write(content)
                messagebox.showinfo("Success", f"Content appended to file '{filename}' successfully.")
        else:
            messagebox.showerror("Error", f"File '{filename}' does not exist.")
        self.log_action("Appended to file", filename)


    def rename_file(self):
        old_filename = filedialog.askopenfilename(title="Rename File")
        if not old_filename:
            return
        new_filename = simpledialog.askstring("Rename File", "Enter the new filename:")
        if not new_filename:
            return
        old_filepath = os.path.join(self.current_directory, old_filename)
        new_filepath = os.path.join(self.current_directory, new_filename)

        if os.path.exists(old_filepath):
            os.rename(old_filepath, new_filepath)
            messagebox.showinfo("Success", f"File '{old_filename}' renamed to '{new_filename}' successfully.")
        else:
            messagebox.showerror("Error", f"File '{old_filename}' does not exist.")
        self.log_action(f"Renamed file '{old_filename}' to '{new_filename}'", old_filename)



    def rename_directory(self):
        old_dirname = filedialog.askdirectory(title="Rename Directory")
        if not old_dirname:
            return
        new_dirname = simpledialog.askstring("Rename Directory", "Enter the new directory name:")
        if not new_dirname:
            return

        old_dirpath = os.path.join(self.current_directory, old_dirname)
        new_dirpath = os.path.join(self.current_directory, new_dirname)

        if os.path.exists(old_dirpath):
            os.rename(old_dirpath, new_dirpath)
            messagebox.showinfo("Success", f"Directory '{old_dirname}' renamed to '{new_dirname}' successfully.")
        else:
            messagebox.showerror("Error", f"Directory '{old_dirname}' does not exist.")
        self.log_action(f"Renamed directory '{old_dirname}' to '{new_dirname}'", old_dirname)


    def get_permissions(self):
        filename = filedialog.askopenfilename(title="Get Permissions")
        if not filename:
            return

        filepath = os.path.join(self.current_directory, filename)
        if os.path.exists(filepath):
            permissions = oct(os.stat(filepath).st_mode & 0o777)
            messagebox.showinfo("Permissions", f"Permissions for '{filename}': {permissions}")
        else:
            messagebox.showerror("Error", f"File '{filename}' does not exist.")
        self.log_action("Get permissions", filename)


    def set_permissions(self):
        filename = filedialog.askopenfilename(title="Set Permissions")
        if not filename:
            return

        filepath = os.path.join(self.current_directory, filename)
        if os.path.exists(filepath):
            permissions = simpledialog.askstring("Set Permissions", "Enter the new permissions (in octal):")
            try:
                permissions = int(permissions, 8)
                os.chmod(filepath, permissions)
                messagebox.showinfo("Success", f"Permissions for '{filename}' set to {oct(permissions)}")
            except ValueError:
                messagebox.showerror("Error", "Invalid permissions format. Please use octal format (e.g., 755).")
        else:
            messagebox.showerror("Error", f"File '{filename}' does not exist.")
        self.log_action("Set permissions", filename)

    def get_directory_permissions(self):
        dirname = filedialog.askdirectory(title="Get Directory Permissions")
        if not dirname:
            return

        dirpath = os.path.join(self.current_directory, dirname)
        if os.path.exists(dirpath):
            permissions = oct(os.stat(dirpath).st_mode & 0o777)
            messagebox.showinfo("Permissions", f"Permissions for directory '{dirname}': {permissions}")
        else:
            messagebox.showerror("Error", f"Directory '{dirname}' does not exist.")
        self.log_action("Get directory permissions", dirname)

    def set_directory_permissions(self):
        dirname = filedialog.askdirectory(title="Set Directory Permissions")
        if not dirname:
            return

        dirpath = os.path.join(self.current_directory, dirname)
        if os.path.exists(dirpath):
            permissions = simpledialog.askstring("Set Directory Permissions", "Enter the new permissions (in octal):")
            try:
                permissions = int(permissions, 8)
                os.chmod(dirpath, permissions)
                messagebox.showinfo("Success", f"Permissions for directory '{dirname}' set to {oct(permissions)}")
            except ValueError:
                messagebox.showerror("Error", "Invalid permissions format. Please use octal format (e.g., 755).")
        else:
            messagebox.showerror("Error", f"Directory '{dirname}' does not exist.")
        self.log_action("Set directory permissions", dirname)


    def copy_file(self):
        src_filename = filedialog.askopenfilename(title="Copy File")
        if not src_filename:
            return

        dest_filename = simpledialog.askstring("Copy File", "Enter the destination filename:")
        if not dest_filename:
            return

        src_filepath = os.path.join(self.current_directory, src_filename)
        dest_filepath = os.path.join(self.current_directory, dest_filename)

        if os.path.exists(src_filepath):
            try:
                shutil.copy2(src_filepath, dest_filepath)
                messagebox.showinfo("Success", f"File '{src_filename}' copied to '{dest_filename}' successfully.")
            except shutil.SameFileError:
                messagebox.showerror("Error", "Source and destination are the same.")
            except PermissionError:
                messagebox.showerror("Error", "Permission denied. You may not have the required permissions.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", f"File '{src_filename}' does not exist.")
        self.log_action(f"Copied file '{src_filename}' to '{dest_filename}'", src_filename)


    def copy_directory(self):
        src_dirname = filedialog.askdirectory(title="Copy Directory")
        if not src_dirname:
            return

        dest_dirname = simpledialog.askstring("Copy Directory", "Enter the destination directory name:")
        if not dest_dirname:
            return

        src_dirpath = os.path.join(self.current_directory, src_dirname)
        dest_dirpath = os.path.join(self.current_directory, dest_dirname)

        if os.path.exists(src_dirpath):
            try:
                shutil.copytree(src_dirpath, dest_dirpath)
                messagebox.showinfo("Success", f"Directory '{src_dirname}' copied to '{dest_dirname}' successfully.")
            except shutil.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            except FileExistsError:
                messagebox.showerror("Error", f"Directory '{dest_dirname}' already exists.")
            except PermissionError:
                messagebox.showerror("Error", "Permission denied. You may not have the required permissions.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", f"Directory '{src_dirname}' does not exist.")
        self.log_action(f"Copied directory '{src_dirname}' to '{dest_dirname}'", src_dirname)


    def change_directory(self):
        dirname = filedialog.askdirectory(title="Change Directory")
        if not dirname:
            return

        if os.path.exists(dirname):
            self.current_directory = dirname
            os.chdir(dirname)
            messagebox.showinfo("Success", f"Changed working directory to '{dirname}'")
            self.log_action("Changed directory", dirname)
        else:
            messagebox.showerror("Error", f"Directory '{dirname}' does not exist.")


    def compress_file_or_directory(self):
        src_path = filedialog.askdirectory(title="Compress File/Directory")
        if not src_path:
            return

        dest_filename = simpledialog.askstring("Compress File/Directory", "Enter the destination ZIP filename:")
        if not dest_filename:
            return

        dest_filepath = os.path.join(self.current_directory, dest_filename)

        try:
            with zipfile.ZipFile(dest_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isdir(src_path):
                    for foldername, subfolders, filenames in os.walk(src_path):
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            arcname = os.path.relpath(file_path, src_path)
                            zipf.write(file_path, arcname)
                else:
                    zipf.write(src_path, os.path.basename(src_path))

            messagebox.showinfo("Success", f"File/Directory '{src_path}' compressed to '{dest_filename}' successfully.")
            self.log_action(f"Compressed file/directory '{src_path}' to '{dest_filename}'", src_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while compressing: {e}")


    def decompress_file_or_directory(self):
        src_path = filedialog.askopenfilename(title="Decompress File/Directory", filetypes=[("ZIP files", "*.zip")])
        if not src_path:
            return

        dest_folder = filedialog.askdirectory(title="Select destination folder for extraction")
        if not dest_folder:
            return

        try:
            with zipfile.ZipFile(src_path, 'r') as zipf:
                zipf.extractall(dest_folder)

            messagebox.showinfo("Success", f"File/Directory '{src_path}' decompressed to '{dest_folder}' successfully.")
            self.log_action(f"Decompressed file/directory '{src_path}' to '{dest_folder}'", src_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while decompressing: {e}")
            

if __name__ == "__main__":
    app = FileSystemGUI()
    app.mainloop()


