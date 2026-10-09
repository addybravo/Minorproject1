import pandas as pd
import glob

# Automatically find any Excel file in the folder so you never have to type the name!
excel_files = glob.glob("*.xlsx")

if len(excel_files) == 0:
    print("Error: No Excel file found in the folder! Please put your file here.")
    exit()

# Use the first excel file it finds
file_name = excel_files[0]

# load the excel file and convert it to a csv dataset
try:
    data = pd.read_excel(file_name, sheet_name="Daily Log", skiprows=4)
    data.to_csv("activity_dataset.csv", index=False)
except Exception as e:
    print(f"Could not read {file_name}.")
    print("Error:", e)
    exit()

# drop any empty rows at the bottom
data = data.dropna(subset=['Date'])

# convert dates to string just in case to make searching easier
data['Date'] = data['Date'].astype(str)

# ensure numeric columns are actually treated as numbers
numeric_columns = [
    'Sleep (min)', 'Fitness (min)', 'Study (min)', 'Coding (min)', 
    'Class (min)', 'Other Activities (min)', 'Total Tracked (min)', 'Free/Unaccounted (min)'
]
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')

print(f"\n[+] Automatically loaded data from: {file_name}")

# This is the ONLY thing you have to enter now
user_choice = input("Enter a date (e.g. 2026-08-15) OR enter '45' for the full summary: ").strip().lower()

# Check if user wants full report (handles '45', 'all', or '45 days')
if user_choice == '45' or user_choice == 'all' or user_choice == '45 days':
    valid_days = len(data)
    total_days_expected = 45 
    missing_days = max(0, total_days_expected - valid_days)

    print("\n=========================================")
    print("       1. FULL ACTIVITY SUMMARY          ")
    print("=========================================")
    print("Expected number of days :", total_days_expected)
    print("Valid days recorded :", valid_days)
    print("Missing days :", missing_days)
    print("Invalid / excluded records : 0")

    avg_sleep = data['Sleep (min)'].mean()
    avg_fitness = data['Fitness (min)'].mean()
    avg_study = data['Study (min)'].mean()
    avg_coding = data['Coding (min)'].mean()
    avg_class = data['Class (min)'].mean()
    avg_other = data['Other Activities (min)'].mean()
    avg_free = data['Free/Unaccounted (min)'].mean()

    print(f"Average Sleep/day : {round(avg_sleep, 2)} mins")
    print(f"Average Fitness/day : {round(avg_fitness, 2)} mins")
    print(f"Average Study/day : {round(avg_study, 2)} mins")
    print(f"Average Coding/day : {round(avg_coding, 2)} mins")
    print(f"Average Class/day : {round(avg_class, 2)} mins")
    print(f"Average Other Activities/day : {round(avg_other, 2)} mins")
    print(f"Average Free / Unaccounted Time : {round(avg_free, 2)} mins\n")

    print("=========================================")
    print("            2. INDEX VALUES              ")
    print("=========================================")
    tpi = avg_coding
    aai = avg_study + avg_class
    phai = avg_fitness
    sri = avg_sleep
    abi = avg_free
    tui = data['Total Tracked (min)'].mean()

    feelings_score = {'Excellent': 5, 'Good': 4, 'Neutral': 3, 'Low': 2, 'Stressed': 1}
    satisfaction_score = {'Very Satisfied': 5, 'Satisfied': 4, 'Neutral': 3, 'Unsatisfied': 2, 'Very Unsatisfied': 1}
    energy_score = {'High': 3, 'Medium': 2, 'Low': 1}

    data['f_score'] = data["Day's Feeling"].map(feelings_score)
    data['s_score'] = data["Satisfaction Level"].map(satisfaction_score)
    data['e_score'] = data["Energy Level"].map(energy_score)

    data['daily_ei'] = (data['f_score'] + data['s_score'] + data['e_score']) / 3
    ei = data['daily_ei'].mean()
    dci = (valid_days / total_days_expected) * 100

    pai = (0.15 * tpi) + (0.20 * aai) + (0.15 * phai) + (0.20 * sri) + (0.15 * tui) + (0.10 * ei) + (0.05 * dci)

    print(f"TPI: {round(tpi, 2)} min/day") # Tech Productivity Index
    print(f"AAI: {round(aai, 2)} min/day") # Academic Activity Index
    print(f"PhAI: {round(phai, 2)} min/day") # Physical Activity Index
    print(f"SRI: {round(sri, 2)} min/day")  # Sleep Recovery Index
    print(f"ABI: {round(abi, 2)} min/day")  # Available Balance Index
    print(f"TUI: {round(tui, 2)} min/day")  # Total Utilization Index
    print(f"EI: {round(ei, 2)} / 5")   # Experience Index
    print(f"DCI: {round(dci, 2)} %")   # Daily Continuity Index
    print(f"Final PAI: {round(pai, 2)}\n")  # Personal Activity Index

else:
    # User entered a specific date
    matching_data = data[data['Date'].str.contains(user_choice, na=False)]

    if len(matching_data) == 0:
        print(f"\nNo records found for the date: '{user_choice}'")
        print("Please make sure you entered it exactly as it appears in Excel (e.g. 2026-08-15).")
    else:
        day_data = matching_data.iloc[0]
        print("\n=========================================")
        print(f"       DATA FOR DATE: {user_choice}      ")
        print("=========================================")
        print(f"Sleep (min):        {day_data['Sleep (min)']}")
        print(f"Fitness (min):      {day_data['Fitness (min)']}")
        print(f"Study (min):        {day_data['Study (min)']}")
        print(f"Coding (min):       {day_data['Coding (min)']}")
        print(f"Class (min):        {day_data['Class (min)']}")
        print(f"Other Activities:   {day_data['Other Activities (min)']}")
        print(f"Free/Unaccounted:   {day_data['Free/Unaccounted (min)']}")
        print(f"Day's Feeling:      {day_data['Day\'s Feeling']}")
        print(f"Satisfaction Level: {day_data['Satisfaction Level']}")
        print(f"Energy Level:       {day_data['Energy Level']}")
        print(f"Notes:              {day_data['Notes']}")
        print("=========================================\n")