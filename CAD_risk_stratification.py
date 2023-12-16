import pandas as pd
import numpy as np
from datetime import datetime
import re
import matplotlib.pyplot as plt
import seaborn as sns


# Define file paths for the datasets
medical_notes_path = "D:/EMR_Dataset_HTN_Medical-Notes-2023.csv"
lab_results_path = "D:/EMR_Dataset_HTN_LabResults-2023.csv"

# Load datasets into Pandas DataFrames
medical_notes_df = pd.read_csv(medical_notes_path)
lab_results_df = pd.read_csv(lab_results_path)

# Step A: Cleaning medication dataset
# Step 1: Calculate Age
current_date = datetime.strptime("2023-12-03", "%Y-%m-%d")
medical_notes_df['Patient_DOB'] = pd.to_datetime(medical_notes_df['Patient_DOB'])
medical_notes_df['Age_in_Days'] = (current_date - medical_notes_df['Patient_DOB']).dt.days
medical_notes_df['Age_Years'] = round(medical_notes_df['Age_in_Days'] / 365.25)

# Step 2: Categorize Age
medical_notes_df['Age_Category'] = pd.cut(
    medical_notes_df['Age_Years'],
    bins=[0, 45, 65, float('inf')],
    labels=['Below 45 years', '45-65 years', 'Above 65 years']
)

# Step 3: Categorize Systolic Blood Pressure
medical_notes_df['Systolic_BP_Category'] = pd.cut(
    medical_notes_df['Systolic_BP'],
    bins=[-float('inf'), 125, 140, float('inf')],
    labels=['Good', 'Stable', 'High']
)

# Step 4: Generate Smoking Status
smoking_keywords = ['smokes', 'has smoked', 'of smoking']
medical_notes_df['Smoking_Status'] = medical_notes_df['Notes'].apply(
    lambda note: 'Yes' if isinstance(note, str) and any(keyword in note for keyword in smoking_keywords) else 'No'
)

# Step 4: Create Hypertension_in_Notes column
hypertension_pattern = r'\b(?:HTN|H(?:yperten(?:ision|tion|sion|ssion))|hypertension)\b'
medical_notes_df['Hypertension_in_Notes'] = medical_notes_df['Notes'].apply(lambda x: str(x)).str.contains(hypertension_pattern, case=False, regex=True)

# Step 5: Create Diagnosis_Notes_With_Hypertension column
medical_notes_df['Diagnosis_Notes_With_Hypertension'] = medical_notes_df.apply(
    lambda row: 'Yes' if (row['Hypertension_in_Notes'] or 'Hypertension' in row['Diagnosis']) and str(row['Notes']) not in ('', 'nan', 'NaN', 'None', 'nan nan', 'NaN NaN') else 'No',
    axis=1
)

# Step 7: Create Diabetes_in_Notes column
diabetes_pattern = r'\b(?:Diabetes)\b'
medical_notes_df['Diabetes_in_Notes'] = medical_notes_df['Notes'].apply(lambda x: str(x)).str.contains(diabetes_pattern, case=False, regex=True)

# Step 8: Create Diagnosis_Notes_With_Diabetes column
medical_notes_df['Diagnosis_Notes_With_Diabetes'] = medical_notes_df.apply(
    lambda row: 'Yes' if (row['Diabetes_in_Notes'] or 'Diabetes' in row['Diagnosis']) and str(row['Notes']) not in ('', 'nan', 'NaN', 'None', 'nan nan', 'NaN NaN') else 'No',
    axis=1
)

# Step 9: Select attributes for joining
selected_attributes = ['Encounter_ID', 'Age_Category', 'Systolic_BP_Category',
                        'Diagnosis_Notes_With_Hypertension', 'Diagnosis_Notes_With_Diabetes',
                        'Patient_Gender', 'Diagnosis', 'Smoking_Status']

medication_notes_selected_df = medical_notes_df[selected_attributes]


# Step B: Cleaning lab dataset
# Step 1: Select attributes (Encounter_ID, Test_Name, Numeric_Result, Units)
lab_results_subset_df = lab_results_df[['Encounter_ID', 'Test_Name', 'Numeric_Result', 'Units']]

# Step 2: Filter by example where Test_Name contains "HDL"
lab_results_hdl_df = lab_results_subset_df[lab_results_subset_df['Test_Name'].str.contains('HDL')]

# # Step 3: Generate HDL_Category attribute
# def categorize_hdl(row):
#     if row['Test_Name'] == "HDL-C":
#         if row['Numeric_Result'] > 1.6:
#             return "Good"
#         elif 0.9 <= row['Numeric_Result'] <= 1.6:
#             return "Normal"
#         elif row['Numeric_Result'] < 0.9:
#             return "Poor"
#     return ""

# # Create a new column using .loc to avoid SettingWithCopyWarning
# lab_results_hdl_df['HDL_Category'] = lab_results_hdl_df.apply(categorize_hdl, axis=1)


# # Step 4: Select attributes (Encounter_ID, HDL_Category)
# lab_results_selected_df = lab_results_hdl_df[['Encounter_ID', 'HDL_Category']]

# Step 3: Generate HDL_Category attribute
def categorize_hdl(row):
    if row['Test_Name'] == "HDL-C":
        if row['Numeric_Result'] > 1.6:
            return "Good"
        elif 0.9 <= row['Numeric_Result'] <= 1.6:
            return "Normal"
        elif row['Numeric_Result'] < 0.9:
            return "Poor"
    return ""

# Create a new column using .loc to avoid SettingWithCopyWarning
lab_results_hdl_df['HDL_Category'] = lab_results_hdl_df.apply(categorize_hdl, axis=1)

# Use .loc to create a new DataFrame
lab_results_selected_df = lab_results_hdl_df.loc[:, ['Encounter_ID', 'HDL_Category']].copy()


# # Display the updated Laboratory dataset with HDL_Category
# print(lab_results_selected_df)


# Step C: Left join the datasets on 'Encounter_ID'
merged_dataset = pd.merge(medication_notes_selected_df, lab_results_selected_df, on='Encounter_ID', how='left')

# # Display the merged dataset
# print(merged_dataset)

# Step D: Creating risk scores

# Step 1: Creation of individual factor scores
# i. Age_Category_Score
merged_dataset['Age_Category_Score'] = 0  # Initialize the column with 0

# Use .loc for assignments
merged_dataset.loc[(merged_dataset['Age_Category'] == 'Below 45 years') & (merged_dataset['Patient_Gender'] == 'M'), 'Age_Category_Score'] = 5
merged_dataset.loc[(merged_dataset['Age_Category'] == 'Below 45 years') & (merged_dataset['Patient_Gender'] == 'F'), 'Age_Category_Score'] = 4
merged_dataset.loc[(merged_dataset['Age_Category'] == '45-65 years') & (merged_dataset['Patient_Gender'] == 'M'), 'Age_Category_Score'] = 10
merged_dataset.loc[(merged_dataset['Age_Category'] == '45-65 years') & (merged_dataset['Patient_Gender'] == 'F'), 'Age_Category_Score'] = 8
merged_dataset.loc[(merged_dataset['Age_Category'] == 'Above 65 years') & (merged_dataset['Patient_Gender'] == 'M'), 'Age_Category_Score'] = 15
merged_dataset.loc[(merged_dataset['Age_Category'] == 'Above 65 years') & (merged_dataset['Patient_Gender'] == 'F'), 'Age_Category_Score'] = 12


# ii. Systolic_BP_Category_Score
merged_dataset['Systolic_BP_Category_Score'] = (
    np.where((merged_dataset['Systolic_BP_Category'] == 'Good'), 0,
    np.where((merged_dataset['Systolic_BP_Category'] == 'Stable') & (merged_dataset['Patient_Gender'] == 'M'), 2,
    np.where((merged_dataset['Systolic_BP_Category'] == 'Stable') & (merged_dataset['Patient_Gender'] == 'F'), 3,
    np.where((merged_dataset['Systolic_BP_Category'] == 'High') & (merged_dataset['Patient_Gender'] == 'M'), 4,
    np.where((merged_dataset['Systolic_BP_Category'] == 'High') & (merged_dataset['Patient_Gender'] == 'F'), 5, 0))))))

# iii. Smoking_Category_Score
merged_dataset['Smoking_Category_Score'] = (
    np.where((merged_dataset['Smoking_Status'] == 'Yes') & (merged_dataset['Patient_Gender'] == 'M'), 4,
    np.where((merged_dataset['Smoking_Status'] == 'Yes') & (merged_dataset['Patient_Gender'] == 'F'), 3,
    np.where((merged_dataset['Smoking_Status'] == 'No'), 0, 0))))

# iv. Diabetes_Category_Score
merged_dataset['Diabetes_Category_Score'] = (
    np.where((merged_dataset['Diagnosis_Notes_With_Diabetes'] == 'Yes'), 2,
    np.where((merged_dataset['Diagnosis_Notes_With_Diabetes'] == 'No'), 0, 0)))

# v. HDL_Category_Score
merged_dataset['HDL_Category_Score'] = (
    np.where((merged_dataset['HDL_Category'] == 'Good'), -1,
    np.where((merged_dataset['HDL_Category'] == 'Normal'), 0,
    np.where((merged_dataset['HDL_Category'] == 'Poor'), 1, 0))))

# Step 2: Risk Score Calculation
merged_dataset['Risk_Score'] = (
    merged_dataset['Age_Category_Score'] +
    merged_dataset['Systolic_BP_Category_Score'] +
    merged_dataset['Smoking_Category_Score'] +
    merged_dataset['Diabetes_Category_Score'] +
    merged_dataset['HDL_Category_Score']
)

# Step 3: Risk Score Categorization
merged_dataset['Risk_Score_Category'] = (
    np.where((merged_dataset['Risk_Score'] < 10), 'Low risk',
    np.where((merged_dataset['Risk_Score'] <= 20), 'Moderate risk', 'High risk'))
)

# Display the updated merged dataset with individual factor scores, risk score, and risk score category
# print(merged_dataset[['Encounter_ID', 'Age_Category_Score', 'Systolic_BP_Category_Score', 'Smoking_Category_Score', 'Diabetes_Category_Score', 'HDL_Category_Score', 'Risk_Score', 'Risk_Score_Category']])

# # Assuming 'merged_dataset' is your DataFrame

# # Specify the path where you want to save the CSV file
# output_csv_path = "D:/output_file.csv"

# # Export the DataFrame to a CSV file
# merged_dataset.to_csv(output_csv_path, index=False)

# print(f"File saved successfully at: {output_csv_path}")
