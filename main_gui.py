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
root.geometry("450x300")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

title_label = tk.Label(main_frame, text="Select Survey Type to Clean:", font=("Arial", 16))
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
    text="Clean Survey A (Not Implemented)",
    font=("Arial", 12),
    width=25,
    height=2,
    state="disabled",
)
btn_survey_a.pack(pady=5)

btn_survey_b = tk.Button(
    main_frame,
    text="Clean Survey B (Not Implemented)",
    font=("Arial", 12),
    width=25,
    height=2,
    state="disabled",
)
btn_survey_b.pack(pady=5)

root.mainloop()
