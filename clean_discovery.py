import pandas as pd


def clean_discovery(input_file: str) -> pd.DataFrame:
    """Clean a raw Discovery survey CSV and return the processed DataFrame."""

    # Load dataset (skip metadata rows)
    df = pd.read_csv(input_file, skiprows=4)

    # Replace columns named 'Unnamed' with empty strings
    df.columns = ["" if "Unnamed" in str(col) else col for col in df.columns]

    # Helper to combine header and first data row
    def create_column_name(header, row_value):
        if pd.isna(header) or "Unnamed" in str(header) or str(header).strip() == "":
            return str(row_value)
        elif pd.notna(row_value) and str(row_value).strip() != "":
            return f"{header}-{row_value}"
        else:
            return header

    # Build combined column names using the first row
    df.columns = [create_column_name(df.columns[i], df.iloc[0, i]) for i in range(len(df.columns))]

    # Remove the row used for column renaming
    df = df.iloc[1:].reset_index(drop=True)

    # Drop rows missing a first name
    df = df.dropna(subset=["First Name"])

    # Ensure duplicate column names are unique
    df.columns = [f"{col}_{i}" if df.columns.tolist().count(col) > 1 else col for i, col in enumerate(df.columns)]

    df.columns = df.columns.str.strip()

    def get_gender(row):
        if row['Which of the following most accurately describes your gender?-Female'] == '1':
            return 'Female'
        elif row['Male'] == '1':
            return 'Male'
        elif row['Non-binary'] == '1':
            return 'Non-binary'
        elif row['Rather not say'] == '1':
            return 'Rather not say'
        elif row['Let me explain'] == '1':
            return row.get('Let me explain Comments', 'Other')
        else:
            return 'Unknown'

    df['Gender'] = df.apply(get_gender, axis=1)

    def get_school_name(row):
        school_columns = [
            "What school are you from? (If not listed, choose 'Other', and type your school name)-Bayswater Secondary College", "Boronia K-12 College", "Fairhills High School",
            "Rowville Secondary College", "Scoresby Secondary College", "Wantirna College",
            "Alamanda College", "Albert Park Primary School", "Aquinas College", "Ashwood College",
            "Auburn High School", "Avila College", "Balwyn High School", "Balwyn Primary School",
            "Beaumaris Secondary College", "Bentleigh West Primary School", "Berwick Primary School",
            "Billanook College", "Blackburn High School", "Box Hill High School", "Brentwood College",
            "Brighton Secondary College", "Brunswick Secondary College", "Cambridge Primary School",
            "Canterbury Primary School", "Carranballac College", "Caulfield Grammar", "Charlton College",
            "CIRE Community School", "Coburg Primary School", "Croydon Community School",
            "Dandenong High School", "Diamond Valley College", "Doncaster Secondary College",
            "Donvale Christian College", "East Doncaster Secondary College", "Edinburgh College",
            "Elliminyt Primary School", "Eltham High School", "Elwood College",
            "Emerald Primary School", "Emerald Secondary College", "Emmaus College", "Essendon Keilor College",
            "Fairhills High School", "Forest Hill College", "Glen Waverley Secondary College", "Hazel Glen College",
            "Healesville High School", "Heathmont East Primary School", "Heathmont Secondary College", "Highvale Secondary College",
            "Kananook Primary School", "Kew High School", "Keysborough College", "Killester College",
            "Knox School", "Launching Place Primary School", "Lilydale Heights College", "Lilydale High School",
            "Luther College", "Mansfield Secondary College", "Mary MacKillop Catholic Regional College",
            "Mater Christi College", "Mazenod College", "McClelland College", "McKinnon Secondary College",
            "Melba College", "Mill Park Primary School", "Monbulk College", "Mooroolbark College",
            "Mount Evelyn Christian College", "Mount Lilydale Mercy College", "Mount Waverley Secondary College",
            "Mountain District Christian School", "Mountain District Learning Centre", "Mullauna College",
            "Narre Warren South P12 College", "Nazareth College", "North Ringwood Community House",
            "Northern Bay P-12", "Norwood Secondary College", "Oakwood School", "Our Lady of Sion College",
            "Oxley Christian College", "Oxley College", "Pines Learning Centre", "Ranges TEC",
            "Reservoir West Primary School", "Richmond West primary school", "Ringwood Secondary College",
            "Rosanna Golf Links Primary School", "Sherbrooke Community School", "South Melbourne Park Primary School",
            "St Andrew's Christian College", "St Joseph's College", "St Kilda Park Primary School",
            "Strathmore Secondary College", "Swan Hill College", "Taylors Lakes Secondary College",
            "Tecoma Primary School", "Templestowe College", "Tintern Schools", "Upper Yarra Secondary College",
            "Upwey High School", "Vermont Secondary College", "Victoria Road Primary School",
            "Viewbank College", "Wantirna College", "Wantirna South Primary School", "Warrandyte High School",
            "Waverley Christian College", "Wellington College", "Wheelers Hill Secondary College", "Whitefriars College",
            "Whittlesea Secondary College", "Wodonga Middle School", "Woodleigh School",
            "Yarra Hills Secondary College", "Yarra Junction primary", "Yarra Valley Grammar School"
        ]

        for school in school_columns:
            if school in row and str(row[school]) == '1':
                return school.split('-', 1)[-1]

        if 'Other' in row and str(row['Other']) == '1':
            return row.get('Other Comments', 'Other')

        return 'Unknown'

    df['School'] = df.apply(get_school_name, axis=1)
    if 'Other Comments' in df.columns:
        df.loc[df['School'] == 'Unknown', 'School'] = df['Other Comments']

    def get_year_level(row):
        if row['What year level are you?-Year 5'] == '1':
            return 'Year 5'
        elif row['Year 6'] == '1':
            return 'Year 6'
        elif row['Year 7'] == '1':
            return 'Year 7'
        elif row['Year 8'] == '1':
            return 'Year 8'
        elif row['Year 9'] == '1':
            return 'Year 9'
        elif row['Year 10'] == '1':
            return 'Year 10'
        elif row['Year 11'] == '1':
            return 'Year 11'
        elif row['Year 12'] == '1':
            return 'Year 12'
        else:
            return 'Unknown'

    df['Year Level'] = df.apply(get_year_level, axis=1)

    def get_program_name(row):
        if str(row.get('What\xa0program did you attend?-Discovery: 3D Design and Merge', '')) == '1':
            return 'Discovery: 3D Design and Merge'
        elif str(row.get('Discovery: Aspirin Analysis', '')) == '1':
            return 'Discovery: Aspirin Analysis'
        elif str(row.get('Discovery: STEM to the Rescue', '')) == '1':
            return 'Discovery: STEM to the Rescue'
        elif str(row.get('Discovery: Emergency Technology', '')) == '1':
            return 'Discovery: Emergency Technology'
        elif str(row.get('Discovery: Forensic Science: Crack the COVID Case', '')) == '1':
            return 'Discovery: Forensic Science: Crack the COVID Case'
        elif str(row.get('Discovery: Forensic Science: Major Crime', '')) == '1':
            return 'Discovery: Forensic Science: Major Crime'
        elif str(row.get('Discovery: Genetics &amp; Micro arrays', '')) == '1':
            return 'Discovery: Genetics & Micro arrays'
        elif str(row.get('Discovery: Hydrogen GRAND PRIX', '')) == '1':
            return 'Discovery: Hydrogen GRAND PRIX'
        elif str(row.get('Discovery: Logistic FAILs', '')) == '1':
            return 'Discovery: Logistic FAILs'
        elif str(row.get('Discovery: Makey Music Laser Cut Design', '')) == '1':
            return 'Discovery: Makey Music Laser Cut Design'
        elif str(row.get('Discovery: OZGRAV Space', '')) == '1':
            return 'Discovery: OZGRAV Space'
        elif str(row.get('Discovery: TECHSprint', '')) == '1':
            return 'Discovery: TECHSprint'
        else:
            return 'Unknown'

    df['Program Name'] = df.apply(get_program_name, axis=1)

    def get_delivery_mode(row):
        if row['How was your KIOSC program delivered?-Onsite (face to face at KIOSC)'] == '1':
            return 'Onsite'
        elif row['Offsite (face to face at your school by your teachers OR a KIOSC facilitator)'] == '1':
            return 'Offsite'
        elif row['Online (delivered zia Zoom, Webex, Teams etc)'] == '1':
            return 'Online'
        elif row['Immersion (delivered at an industry site)'] == '1':
            return 'Immersion'
        else:
            return 'Unknown'

    df['Delivery Mode'] = df.apply(get_delivery_mode, axis=1)

    df = df.rename(columns={'Survey Start': 'Timestamp'})
    df['Record Number'] = df['First Name'].str.extract(r'#(\d+)')
    df['Term'] = ''
    df['ATSI'] = ''

    selected_columns = [
        'Record Number',
        'Timestamp',
        'Term',
        'Gender',
        'ATSI',
        'School',
        'Year Level',
        'Program Name',
        'Delivery Mode',
        'How much did you enjoy the sessions today?',
        'How much do you think you have learnt today?',
        'I learnt something new today',
        'The program I did motivated me to explore new ideas and concepts',
        'I used technology to help me learn',
        'I had the opportunity to collaborate with other students',
        'I learnt about industries that use science, technology, engineering, or maths (referred to as STEM) in my local area',
        'If given the opportunity, would you like to attend another KIOSC program?'
    ]

    df_selected = df[selected_columns]

    return df_selected
