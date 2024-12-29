import subprocess
import tkinter as tk
from tkinter import messagebox

class GameInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Microcraft Installer")
        self.root.geometry("530x270")
        self.page = 1
        
        # Page 1: User Agreement
        self.agreement_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
        self.agreement_text.insert(tk.END, "User Agreement:\n\nPlease accept this agreement to install the game. "
                                           "By proceeding, you agree to the terms and conditions:\nThis game is not in the property of mojang, microsoft or 4J Studios.\nThis is a fan made project and is not trying to copy minecraft or reforj.\nPlease do not report this as a scam.")
        self.agreement_text.configure(state=tk.DISABLED)
        self.agreement_text.pack(pady=10)

        self.checkbox_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(root, text="I Agree to the Terms and Conditions", variable=self.checkbox_var)
        self.checkbox.pack()

        self.next_button = tk.Button(root, text="Next", command=self.next_page)
        self.next_button.pack(pady=10)

    def next_page(self):
        if self.page == 1:
            if not self.checkbox_var.get():
                messagebox.showerror("Error", "You must agree to the terms and conditions to proceed.")
                return
            self.page += 1
            self.show_install_page()

    def show_install_page(self):
        # Clear page 1 elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Page 2: Installation Details
        label = tk.Label(self.root, text="The following packages will be installed:", font=("Arial", 12))
        label.pack(pady=10)

        packages_label = tk.Label(self.root, text="ursina, perlin-noise", font=("Arial", 10))
        packages_label.pack(pady=5)

        install_button = tk.Button(self.root, text="Install", command=self.install_packages)
        install_button.pack(pady=10)

    def install_packages(self):
        try:
            # Run the pip install command
            subprocess.run(["pip", "install", "--user", "ursina", "perlin-noise"], check=True, text=True)
            messagebox.showinfo("Success", "All packages have been installed successfully!")
            self.show_finish_page()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Installation failed.\nError: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred.\nError: {e}")

    def show_finish_page(self):
        # Clear current page elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Page 3: Finish Page
        label = tk.Label(self.root, text="Installation Complete!", font=("Arial", 16))
        label.pack(pady=20)

        finish_button = tk.Button(self.root, text="Finish", command=self.root.quit)
        finish_button.pack(pady=10)


# Run the Installer
if __name__ == "__main__":
    root = tk.Tk()
    installer = GameInstaller(root)
    root.mainloop()
