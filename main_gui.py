import tkinter as tk
from tkinter import filedialog, messagebox

from clean_vces import clean_vces
from clean_discovery import clean_discovery


def upload_and_clean(cleaning_function):
    """Handles file upload, cleaning, and saving."""
    filepath = filedialog.askopenfilename(
        title="Select a CSV file to clean",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        return

    try:
        cleaned_df = cleaning_function(filepath)

        save_path = filedialog.asksaveasfilename(
            title="Save Cleaned File As",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not save_path:
            return

        cleaned_df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"File cleaned successfully!\nSaved to: {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during cleaning:\n{e}")


root = tk.Tk()
root.title("KIOSC Data Cleaner")
root.geometry("650x500")

# Load image (must be in same directory or provide full path)
bg_image = tk.PhotoImage(file="bg.png")

# Create label for background
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Main frame with transparent background
main_frame = tk.Frame(root, bg="white", padx=20, pady=20)  # You can set bg to '' if you want transparency
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(main_frame, text="Select Survey Type to Clean:", font=("Arial", 16), bg="white")
title_label.pack(pady=10)

btn_vces = tk.Button(
    main_frame,
    text="Clean VCES Survey",
    command=lambda: upload_and_clean(clean_vces),
    font=("Arial", 12),
    width=25,
    height=2,
)
btn_vces.pack(pady=5)

btn_discovery = tk.Button(
    main_frame,
    text="Clean Discovery Survey",
    command=lambda: upload_and_clean(clean_discovery),
    font=("Arial", 12),
    width=25,
    height=2,
)
btn_discovery.pack(pady=5)

btn_survey_a = tk.Button(
    main_frame,
    text="Clean VCE Survey (Not Implemented)",
    font=("Arial", 12),
    width=35,
    height=2,
    state="disabled",
)
btn_survey_a.pack(pady=5)

instructions = (
    "Instructions:\n"
    "1. Choose the correct survey type.\n"
    "2. Select the raw CSV file of the correct survey type you want to clean.\n"
    "3. The program will automatically process the file. This will be instant.\n"
    "4. You will be prompted to save the cleaned file.\n"
    "5. A confirmation message will appear after saving.\n"
)

instruction_label = tk.Label(main_frame, text=instructions, font=("Arial", 11), bg="white", justify="left", anchor="w")
instruction_label.pack(pady=(10, 5), fill="both")

root.mainloop()
