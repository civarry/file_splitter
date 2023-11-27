import tkinter as tk
from tkinter import filedialog, messagebox
import os
import configparser


class FileSplitterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Splitter")
        self.chunk_size_var = tk.StringVar()
        self.chunk_size_var.set("25 MB")  # Default chunk size
        self.create_widgets()
        self.load_config()

    def load_config(self):
        # Create a default config.ini if it doesn't exist
        if not os.path.exists('config.ini'):
            self.create_default_config()

        # Load configuration from config.ini
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        if 'Settings' in self.config:
            file_path = self.config['Settings'].get('file_path', '')
            combine_var = self.config['Settings'].get('combine_var', '')
            chunk_size_var = self.config['Settings'].get('chunk_size_var', '')

            if file_path:
                self.file_path = file_path
                self.file_extension = os.path.splitext(file_path)[1][1:]
                self.combine_var.set(combine_var)
                self.chunk_size_var.set(chunk_size_var)

                self.textarea.config(state="normal")
                self.textarea.delete("1.0", tk.END)
                self.textarea.insert("1.0", f"Selected file: {
                                     os.path.basename(file_path)}")
                self.textarea.config(state="disabled")

    def create_default_config(self):
        # Create a default config.ini file
        self.config = configparser.ConfigParser()
        self.config['Settings'] = {'file_path': '',
                                   'combine_var': '', 'chunk_size_var': ''}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def save_config(self):
        # Save configuration to config.ini
        if not self.config.has_section('Settings'):
            self.config.add_section('Settings')
        self.config['Settings']['file_path'] = self.file_path
        self.config['Settings']['combine_var'] = self.combine_var.get()
        self.config['Settings']['chunk_size_var'] = self.chunk_size_var.get()
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def create_widgets(self):
        # Define primary and secondary colors for modern design
        primary_color = "#3498db"  # Blue
        secondary_color = "#2ecc71"  # Green
        text_color = "#2c3e50"  # Dark Gray

        # Create textarea and buttons
        text_width = 40
        text_height = 1
        button_size = 20  # Set the desired size for buttons

        self.textarea = tk.Text(
            self.master, height=text_height, width=text_width, state="disabled", bg="#ecf0f1", fg=text_color)
        self.textarea.grid(row=0, column=0, columnspan=3,
                           pady=0)  # Set pady to 0
        self.textarea.insert("1.0", "Select a file:")

        # Create label for chunk size dropdown
        label_chunk_size = tk.Label(
            self.master, text="Chunk size:", bg="#ecf0f1", fg=text_color)
        label_chunk_size.grid(
            row=1, column=0, columnspan=1, pady=0, sticky="w")  # Set pady to 0

        # Create a dropdown for choosing the chunk size with a larger width
        chunk_sizes = ["1 MB", "2 MB", "5 MB", "10 MB", "20 MB", "50 MB",
                       "100 MB", "200 MB", "500 MB", "1 GB", "2 GB", "5 GB", "10 GB"]
        self.chunk_size_dropdown = tk.OptionMenu(
            self.master, self.chunk_size_var, *chunk_sizes)
        self.chunk_size_dropdown.grid(
            row=2, column=0, columnspan=3, pady=0, sticky="ew")  # Set pady to 0
        self.chunk_size_dropdown.config(width=20)  # Set the width as desired

        # Style 'Select File' and 'Split File' buttons with primary color
        self.select_button = tk.Button(
            self.master, text="Select File", command=self.select_file, width=button_size, height=text_height,
            bg=primary_color, fg="white", activebackground="#2980b9")
        self.select_button.grid(
            row=3, column=0, columnspan=1, pady=0)  # Set pady to 0

        self.split_button = tk.Button(
            self.master, text="Split File", command=self.split_file, width=button_size, height=text_height,
            bg=primary_color, fg="white", activebackground="#2980b9")
        self.split_button.grid(
            row=3, column=1, columnspan=2, pady=0)  # Set pady to 0

        # Style 'Browse Folder' and 'Combine Files' buttons with secondary color
        self.combine_var = tk.StringVar()
        self.combine_var.set("")  # Empty initially

        self.browse_button = tk.Button(
            self.master, text="Browse Folder", command=self.browse_combine_folder, width=button_size, height=text_height,
            bg=secondary_color, fg="white", activebackground="#27ae60")
        self.browse_button.grid(
            row=4, column=0, columnspan=1, pady=0)  # Set pady to 0

        self.combine_button = tk.Button(
            self.master, text="Combine Files", command=self.combine_files, width=button_size, height=text_height,
            bg=secondary_color, fg="white", activebackground="#27ae60")
        self.combine_button.grid(
            row=4, column=1, columnspan=2, pady=0)  # Set pady to 0

        # Apply additional modernizing touches to the GUI
        # Set window background color to light gray
        self.master.config(bg="#ecf0f1")
        # Remove textarea border
        self.textarea.config(borderwidth=0, relief="flat")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.file_extension = os.path.splitext(file_path)[1][1:]
            self.combine_var.set(os.path.dirname(file_path))
            self.textarea.config(state="normal")
            self.textarea.delete("1.0", tk.END)
            self.textarea.insert("1.0", f"Selected file: {
                                 os.path.basename(file_path)}")
            self.textarea.config(state="disabled")
            self.save_config()

    def split_file(self):
        if hasattr(self, 'file_path'):
            if not self.textarea.get("1.0", tk.END).startswith("Selected file:"):
                messagebox.showwarning(
                    "Warning", "Please select a file to split.")
                return

            # Convert selected chunk size to bytes
            chunk_size_str = self.chunk_size_var.get().replace(" MB", "").replace(" GB", "")
            chunk_size = int(chunk_size_str) * 1000 * 1000 * \
                1000 if "GB" in self.chunk_size_var.get() else int(chunk_size_str) * 1000 * 1000

            # Check if chunk size is larger than the file size
            file_size = os.path.getsize(self.file_path)
            if chunk_size > file_size:
                messagebox.showwarning(
                    "Warning", "Selected chunk size is larger than the file size. Please choose another chunk size.")
                return

            output_folder = os.path.join(os.path.dirname(self.file_path), f"{
                                         os.path.splitext(os.path.basename(self.file_path))[0]}_split")
            os.makedirs(output_folder, exist_ok=True)

            original_filename = os.path.splitext(
                os.path.basename(self.file_path))[0]

            with open(self.file_path, 'rb') as infile:
                index = 1
                while True:
                    chunk = infile.read(chunk_size)
                    if not chunk:
                        break

                    output_file_path = os.path.join(
                        output_folder, f"{original_filename}_chunk_{index}.bin")
                    with open(output_file_path, 'wb') as outfile:
                        outfile.write(chunk)

                    index += 1

            messagebox.showinfo("Success", "File has been successfully split!")
        else:
            messagebox.showwarning("Warning", "Please select a file first.")

    def browse_combine_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.combine_var.set(folder_path)
            self.textarea.config(state="normal")
            self.textarea.delete("1.0", tk.END)
            self.textarea.insert("1.0", f"Combine folder: {folder_path}")
            self.textarea.config(state="disabled")

    def combine_files(self):
        combine_folder_path = self.combine_var.get().strip()

        if not combine_folder_path:
            messagebox.showwarning(
                "Warning", "Please select a folder to combine files.")
            return

        # No need to check for the selected folder message, just proceed
        try:
            if os.path.isdir(combine_folder_path):
                output_folder = os.path.dirname(combine_folder_path)
                original_filename = os.path.splitext(
                    os.path.basename(self.file_path))[0]

                output_file_path = os.path.join(
                    output_folder, f"{original_filename}_combined.{self.file_extension}")

                with open(output_file_path, 'wb') as outfile:
                    index = 1
                    while True:
                        chunk_file_path = os.path.join(combine_folder_path, f"{
                                                       original_filename}_chunk_{index}.bin")
                        if not os.path.exists(chunk_file_path):
                            break

                        with open(chunk_file_path, 'rb') as infile:
                            chunk = infile.read()
                            outfile.write(chunk)

                        index += 1

                messagebox.showinfo(
                    "Success", "Files have been successfully combined!")
            else:
                messagebox.showwarning(
                    "Warning", "Please select a valid folder containing split files.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    root = tk.Tk()
    app = FileSplitterApp(root)
    root.resizable(width=False, height=False)
    root.mainloop()


if __name__ == "__main__":
    main()
