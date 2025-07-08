# In file: main_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Import your cleaning functions
from clean_vces import clean_vces
# You can add imports for A, B, and C here once they are ready
# from clean_survey_a import clean_survey_a 

def upload_and_clean(cleaning_function):
    """Handles file upload, cleaning, and saving."""
    filepath = filedialog.askopenfilename(
        title="Select a CSV file to clean",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not filepath:
        return # User cancelled

    try:
        # For VCES, we need to skip the first 3 rows. We can detect the function.
        if cleaning_function.__name__ == 'clean_vces':
            df = pd.read_csv(filepath, skiprows=4, header=[0, 1])
        else:
            df = pd.read_csv(filepath)
        
        # Run the selected cleaning function
        cleaned_df = cleaning_function(df)

        save_path = filedialog.asksaveasfilename(
            title="Save Cleaned File As",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not save_path:
            return # User cancelled

        cleaned_df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"File cleaned successfully!\nSaved to: {save_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during cleaning:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("KIOSC Data Cleaner")
root.geometry("450x300")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

title_label = tk.Label(main_frame, text="Select Survey Type to Clean:", font=("Arial", 16))
title_label.pack(pady=10)

# --- Buttons for each survey type ---
btn_vces = tk.Button(
    main_frame, text="Clean VCES Survey",
    command=lambda: upload_and_clean(clean_vces),
    font=("Arial", 12), width=25, height=2
)
btn_vces.pack(pady=5)

# Add placeholder buttons for other surveys. They are disabled for now.
btn_survey_a = tk.Button(
    main_frame, text="Clean Survey A (Not Implemented)",
    font=("Arial", 12), width=25, height=2, state="disabled"
)
btn_survey_a.pack(pady=5)

btn_survey_b = tk.Button(
    main_frame, text="Clean Survey B (Not Implemented)",
    font=("Arial", 12), width=25, height=2, state="disabled"
)
btn_survey_b.pack(pady=5)

# Start the application
root.mainloop()