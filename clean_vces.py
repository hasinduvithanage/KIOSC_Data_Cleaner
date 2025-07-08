# In file: clean_vces.py

import pandas as pd

def clean_vces(df):
    # Create a copy
    df_cleaned = df.copy()

    # --- Safe string conversion helper ---
    def safe_str(val):
        if pd.isna(val):
            return ""
        return str(val).strip()

    # Flatten multiindex columns
    df_cleaned.columns = [
        f"{safe_str(col[0])}-{safe_str(col[1])}"
        if safe_str(col[1]).lower() not in ["", "nan"]
        else safe_str(col[0])
        for col in df_cleaned.columns
    ]

    # Strip spaces from all column names
    df_cleaned.columns = df_cleaned.columns.str.strip()

    # DEBUG: print column names
    print("DEBUG COLUMN NAMES:", df_cleaned.columns.tolist())

    # Find the actual First Name column
    first_name_col = None
    for col in df_cleaned.columns:
        if "First Name" in col:
            first_name_col = col
            break

    if first_name_col is None:
        raise ValueError("Could not find 'First Name' column.")

    # Drop rows with empty First Name
    df_cleaned = df_cleaned.dropna(subset=[first_name_col])

    # --- Helper functions using 'endswith' logic ---

    def get_gender(row):
        for col in row.index:
            if col.endswith("-Female") and row[col] == '1':
                return "Female"
            if col.endswith("-Male") and row[col] == '1':
                return "Male"
            if col.endswith("-Other") and row[col] == '1':
                return "Non-binary"
            if col.endswith("-Rather not say") and row[col] == '1':
                return "Rather not say"
        return "Unknown"

    def get_school_name(row):
        other_comment_value = None
        for col in row.index:
            if col.endswith("Other Comments"):
                val = row.get(col)
                if isinstance(val, str) and val.strip():
                    other_comment_value = val.strip()
                else:
                    other_comment_value = None

        for col in row.index:
            if col.endswith("-Other") and row[col] == '1' and other_comment_value:
                return other_comment_value
            if col.startswith("What School are you from?-") and row[col] == '1':
                return col.split("What School are you from?-")[1]
            if "-" + col.split("-")[-1] in col and row[col] == '1':
                return col.split("-")[-1]
        return "Unknown"

    def get_grade(row):
        for col in row.index:
            if col.endswith("-Prep") and row[col] == '1':
                return "Prep"
            if col.endswith("-Year 5") and row[col] == '1':
                return "Year 5"
            if col.endswith("-Year 6") and row[col] == '1':
                return "Year 6"
            if col.endswith("-Year 7") and row[col] == '1':
                return "Year 7"
            if col.endswith("-Year 8") and row[col] == '1':
                return "Year 8"
            if col.endswith("-Year 9") and row[col] == '1':
                return "Year 9"
            if col.endswith("-Year 10") and row[col] == '1':
                return "Year 10"
            if col.endswith("-Year 11") and row[col] == '1':
                return "Year 11"
            if col.endswith("-Year 12") and row[col] == '1':
                return "Year 12"
        return "Unknown"

    def get_recommendation(row):
        for col in row.index:
            if col.endswith("-Strongly agree") and row[col] == '1':
                return "Strongly agree"
            if col.endswith("-Agree") and row[col] == '1':
                return "Agree"
            if col.endswith("-Neither agree nor disagree") and row[col] == '1':
                return "Neither agree nor disagree"
            if col.endswith("-Disagree") and row[col] == '1':
                return "Disagree"
            if col.endswith("-Strongly disagree.") and row[col] == '1':
                return "Strongly disagree"
        return "Unknown"

    def get_new_topics(row):
        for col in row.index:
            if col.startswith("The activity introduced me to new topics and ideas.-") and row[col] == '1':
                return col.split("-")[-1]
        return "Unknown"

    def get_think_hard(row):
        for col in row.index:
            if col.startswith("The activity made me think hard / carefully.-") and row[col] == '1':
                return col.split("-")[-1]
        return "Unknown"

    def get_different_activity(row):
        for col in row.index:
            if col.startswith("The activity was different to regular class at school.-") and row[col] == '1':
                return col.split("-")[-1]
        return "Unknown"

    # Apply functions
    df_cleaned['Gender'] = df_cleaned.apply(get_gender, axis=1)
    df_cleaned['School'] = df_cleaned.apply(get_school_name, axis=1)
    df_cleaned['Year Level'] = df_cleaned.apply(get_grade, axis=1)
    df_cleaned['I would recommend this activity to another student'] = df_cleaned.apply(get_recommendation, axis=1)
    df_cleaned['The activity introduced me to new topics and ideas'] = df_cleaned.apply(get_new_topics, axis=1)
    df_cleaned['The activity made me think hard / carefully'] = df_cleaned.apply(get_think_hard, axis=1)
    df_cleaned['The activity was different to regular class at school.'] = df_cleaned.apply(get_different_activity, axis=1)

    # Add final columns
    df_cleaned['Record Number'] = df_cleaned[first_name_col].str.extract(r'#(\d+)')
    df_cleaned['Timestamp'] = df_cleaned.get('Survey Start')
    df_cleaned['Term'] = ''  # Placeholder
    df_cleaned['ATSI'] = ''  # Placeholder

    # Select and order the final columns
    final_columns = [
        "Record Number", "Timestamp", "Term", "Gender", "ATSI", "School", "Year Level",
        "I would recommend this activity to another student",
        "The activity introduced me to new topics and ideas",
        "The activity made me think hard / carefully",
        "The activity was different to regular class at school."
    ]
    df_final = df_cleaned[final_columns]

    return df_final
