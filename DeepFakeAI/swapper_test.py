import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
from queue import Queue

class DeepFakeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepFake Command GUI")
        
        # Add padding to the GUI elements
        self.root.geometry("400x400")
        self.root.configure(padx=10, pady=10)

        self.password_var = tk.StringVar()
        self.password_entry = self.create_text_input("Sudo Password:", password=True)
        
        self.target_file = self.create_file_input("Target File:")
        self.source_file = self.create_file_input("Source File:")
        self.output_file = self.create_file_input("Output File:", save=True)
        
        self.execution_provider = self.create_text_input("Execution Provider:", default="cpu")
        self.frame_processor = self.create_text_input("Frame Processor:", default="face_swapper face_enhancer")
        
        self.run_button = tk.Button(root, text="Run Command", command=self.run_command)
        self.run_button.pack()

        self.load_last_values()
        
        self.output_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.output_queue = Queue()  # To store command output
        
        self.run_button = tk.Button(root, text="Run Command", command=self.run_command)
        self.run_button.pack()
        
        self.output_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    def load_last_values(self):
        try:
            with open("last_selected_values.txt", "r") as file:
                lines = file.readlines()
                print("Checking File...", lines)
                if len(lines) >= 3:
                    print("fetching...")
                    self.target_file.insert(0, lines[0].strip())
                    self.source_file.insert(0, lines[1].strip())
                    self.output_file.insert(0, lines[2].strip())
        except FileNotFoundError:
            pass

    def save_last_values(self):
        open("last_selected_values.txt", "a").close()

        with open("last_selected_values.txt", "w") as file:
            file.write(self.target_file.get() + "\n")
            file.write(self.source_file.get() + "\n")
            file.write(self.output_file.get() + "\n")
        
    def create_file_input(self, label_text, save=False):
        frame = tk.Frame(root)
        frame.pack(fill=tk.X)
        
        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)
        
        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        button_text = "Browse" if not save else "Save As"
        button = tk.Button(frame, text=button_text, command=lambda: self.browse_file(entry, save))
        button.pack(side=tk.LEFT)
        
        return entry
    
    def create_text_input(self, label_text, default="", password=False):
        frame = tk.Frame(root)
        frame.pack(fill=tk.X)
        
        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)
        
        var = tk.StringVar(value=default)
        # entry = tk.Entry(frame, textvariable=var)
        entry = tk.Entry(frame, show="*") if password else tk.Entry(frame)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        if default:
            entry.insert(0, default)
        
        return entry
    
    def browse_file(self, entry, save=False):
        if save:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        else:
            file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def run_command(self):
        sudo_password = self.password_entry.get()

        # Make sure the password is not empty
        if not sudo_password:
            self.update_output("Please enter the sudo password.")
            return
        
        print("Entered...", sudo_password)
        command = (
            f"echo '{sudo_password}' | sudo -S python3 run.py --target {self.target_file.get()} "
            f"--source {self.source_file.get()} -o {self.output_file.get()} "
            f"--execution-provider {self.execution_provider.get()} "
            f"--frame-processor {self.frame_processor.get()}"
        )

        # command = (
        #     f"sudo python3 roop/run.py --target {self.target_file.get()} "
        #     f"--source {self.source_file.get()} -o {self.output_file.get()} "
        #     f"--execution-provider {self.execution_provider.get()} "
        #     f"--frame-processor {self.frame_processor.get()}"
        # )

        print("Running command... ", command)
        
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        self.output_text.insert(tk.END, "Running command:\n" + command + "\n\n")
        self.output_text.config(state=tk.DISABLED)
        
        # Run the command in a separate thread
        thread = threading.Thread(target=self.execute_command, args=(command,))
        thread.start()
    
    def execute_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            output_str = output.decode("utf-8")
            self.update_output("Command output:\n" + output_str)
        except subprocess.CalledProcessError as e:
            error_message = e.output.decode("utf-8")
            self.update_output("Command error:\n" + error_message)
    
    def update_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.config(state=tk.DISABLED)

    def on_closing(self):
        self.save_last_values()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DeepFakeGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()