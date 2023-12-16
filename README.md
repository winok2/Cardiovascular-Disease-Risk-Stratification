# Caronary-Artery-Disease-Risk-Stratification

## Introduction

This project focuses on CAD risk stratification using electronic health records (EHR) data. It involves the cleaning, processing, and analysis of medical notes and laboratory results to categorize patients into different risk groups. 

## Prerequisites
- Python
- Regex
- Power BI

# Framingham Risk Score (FRS)

The simplified version of the Framingham Risk Score (FRS) is used for estimating a 10-year cardiovascular disease risk. The FRS table provides risk points associated with various risk factors for both males and females.

## Risk Factors and Corresponding Risk Points

| Risk Factor       | Risk Points (Male) | Risk Points (Female) |
| ----------------- | ------------------- | -------------------- |
| **Age**            |                    |                      |
| Below 45 years     | 5                   | 4                    |
| 45-65 years        | 10                  | 8                    |
| Above 65 years     | 15                  | 12                   |
| **HDL**            |                    |                      |
| Good (>1.6)        | -1                  | -1                   |
| Normal (0.9-1.6)   | 0                   | 0                    |
| Poor (<0.9)        | 1                   | 1                    |
| **Systolic BP**    |                    |                      |
| Good (<125)        | 0                   | 0                    |
| Stable (125-140)   | 2                   | 3                    |
| High (>140)        | 4                   | 5                    |
| **Smoker**         |                    |                      |
| Yes               | 4                   | 3                    |
| No                | 0                   | 0                    |
| **Diabetes**       |                    |                      |
| Yes               | 2                   | 2                    |
| No                | 0                   | 0                    |

These risk points are utilized in the risk stratification process to calculate an individual's risk score.
The risk stratification was based on three classes: Low risk: <10 points, Moderate risk: 10-20 points and High risk: >20 points


## Data Cleaning and Processing
The primary key for these datasets is Encounter_ID while the attributes of the datasets that are used in this analysis are as follows:
-MedicaNote
--Attributes: Encounter_ID, Diagnosis, Patient_Gender, Notes, Systolic_BP, Diastolic_BP and Patient_DOB 
-LabResults
--Attributes: Encounter_ID, Test_Name, Numeric_Result and Units.

### Medication Dataset Cleaning

- **Step 1:** Calculate Age - Derived the age of patients from their date of birth.
- **Step 2:** Categorize Age - Groups patients into age categories.
- **Step 3:** Categorize Systolic Blood Pressure - Classifies patients based on their systolic blood pressure.
- **Step 4:** Generate Smoking Status - Determines patients' smoking status.
- **Step 5:** Generated Diabetes Status

### Lab Dataset

- **Step 1:** Select attributes - Chooses relevant attributes from the lab results dataset.
- **Step 2:** Created HDL attribute and categorized it

## Dataset Joining

Joined the medication and lab datasets using the 'Encounter_ID' as a key.

## Risk Stratification

Assigns risk scores to patients based on various factors such as age, blood pressure, smoking, diabetes, and HDL cholesterol levels.
Exported the file to local drive for further visualization in PowerBI

## Visualization

Utilized Microsoft PowerBI to visualize the analzed dataset
![image](https://github.com/winok2/Coronary-Artery-Disease-Risk-Stratification/assets/137515971/58910683-2823-4d8e-9e8a-250c29606e1f)


## Key Takeaways

- **Moderate Risk Prevalence:**
  Approximately 75% of the patients in the dataset are identified to be at a moderate risk of developing coronary artery disease. This suggests that a significant portion of the population may require closer monitoring and proactive health management.

- **Age Distribution:**
  Among patients with a moderate risk, a notable majority falls within the age category of 45-60 years. This finding indicates that the risk of coronary artery disease tends to be more pronounced in the middle-aged population, emphasizing the importance of targeted interventions and health strategies for individuals in this age range.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
