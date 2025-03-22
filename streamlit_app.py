import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# File path for local storage
excel_file = ""

# Helper function to calculate time in months
def calculate_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

# Load existing data or create a new DataFrame
def load_data():
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    else:
        return pd.DataFrame(columns=[
            "MRN", "Date_of_Birth", "Age", "Date_of_Last_Radiotherapy", "Follow_up_date", "Follow_up_time",
            "Histology", "Grade", "Necrosis", "LVI", "Mytotic_Count", "Location", "Clinical_Stage_Extremity",
            "Clinical_Stage_Retroperitoneum", "Biopsy_date", "Recurrent_Tumor", "Recurrence_date", "Surgery_type",
            "Surgery_date", "Systemic_Treatment", "Systemic_Treatment_first_date", "Systemic_Treatment_last_date",
            "Dose", "Fractionation", "Fatigue", "Dysuria", "Cystitis", "Bladder_Perforation", "Hematuria",
            "Urinary_Fistula", "Urinary_Obstruction", "Ureteral_Stenosis", "Diarrhea", "Nausea", "Bowel_Perforation",
            "Bowel_Obstruction", "Overal_tolerance", "Local_Recurrence", "Regional_Recurrence", "Distant_Recurrence",
            "Death", "Time_to_Local_Recurrence", "Time_to_Regional_Recurrence", "Time_to_Distant_Recurrence",
            "Time_to_Death"
        ])

# Function to safely retrieve data, handling NaN values
def safe_get(data, key, default=""):
    value = data.get(key, default)
    return value if pd.notna(value) else default

# Function to safely retrieve a list from stored string values
def safe_get_list(data, key):
    value = data.get(key, "")
    if pd.isna(value) or not isinstance(value, str):
        return []
    return [item.strip() for item in value.replace("[", "").replace("]", "").replace("'", "").split(",") if item]


# Function to fetch existing patient data by MRN
def get_patient_data(mrn):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    mrn = str(mrn).strip()
    if mrn in df["MRN"].values:
        return df[df["MRN"] == mrn].iloc[0].to_dict()
    return None

# Function to save patient data (Appending Instead of Overwriting)
def save_data(data):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    data["MRN"] = str(data["MRN"]).strip()

    # Append new data as a separate row instead of replacing the existing one
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Save the updated DataFrame
    df.to_excel(excel_file, index=False)


# Streamlit app layout
st.title("Patient Information Database - Preoperative RT for Sarcomas Prospective Registry")

# Input for MRN
mrn = st.text_input("Enter MRN (Medical Record Number) and press Enter", key="mrn")

# Fetch existing patient data
patient_data = get_patient_data(mrn) if mrn else None

# Start the form
with st.form("patient_form", clear_on_submit=False):
    st.subheader("Patient Details")

    date_of_birth = st.date_input("Date of Birth",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Birth", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today(), min_value=datetime(1900, 1, 1).date(), max_value=datetime.today().date()
    )

    mrn = st.text_input("MRN (Medical Record Number)", value=mrn)

    last_radiotherapy_date = st.date_input("Date of Last Radiotherapy",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Last_Radiotherapy", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    follow_up_date = st.date_input("Date of Follow-up",
        value=datetime.strptime(safe_get(patient_data, "Follow_up_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    Histology = st.multiselect("Histology", ["Atypical lipomatous tumour",
    "Liposarcoma",
    "Myxoid liposarcoma",
    "Pleomorphic liposarcoma",
    "Dermatofibrosarcoma protuberans NOS",
    "Dermatofibrosarcoma protuberans, fibrosarcomatous",
    "Solitary fibrous tumour NOS",
    "Inflammatory myofibroblastic tumour",
    "Epithelioid inflammatory myofibroblastic sarcoma",
    "Myxoinflammatory fibroblastic sarcoma",
    "Infantile fibrosarcoma",
    "Fibrosarcoma NOS",
    "Myxofibrosarcoma",
    "Epithelioid myxofibrosarcoma",
    "Low grade fibromyxoid sarcoma",
    "Sclerosing epithelioid fibrosarcoma",
    "Plexiform fibrohistiocytic tumour",
    "Giant cell tumour of soft parts",
    "Haemangioendothelioma",
    "Kaposi sarcoma",
    "Epithelioid haemangioendothelioma NOS",
    "Epithelioid haemangioendothelioma with WWTR1-CAMTA1 fusion",
    "Epithelioid haemangioendothelioma with YAP1-TFE3 fusion",
    "Angiosarcoma",
    "Glomus tumour, malignant",
    "Leiomyosarcoma NOS",
    "Embryonal rhabdomyosarcoma NOS",
    "Embryonal rhabdomyosarcoma, pleomorphic",
    "Alveolar rhabdomyosarcoma",
    "Pleomorphic rhabdomyosarcoma NOS",
    "Spindle cell rhabdomyosarcoma",
    "Osteosarcoma, extraskeletal",
    "Malignant peripheral nerve sheath tumour NOS",
    "Malignant peripheral nerve sheath tumour, epithelioid",
    "Malignant melanotic nerve sheath tumour",
    "Atypical fibroxanthoma",
    "Angiomatoid fibrous histiocytoma",
    "Ossifying fibromyxoid tumour NOS",
    "Synovial sarcoma, specify type",
    "Epithelioid sarcoma",
    "Proximal or large cell epithelioid sarcoma",
    "Classic epithelioid sarcoma",
    "Alveolar soft part sarcoma",
    "Clear cell sarcoma of soft tissue",
    "Extraskeletal myxoid chondrosarcoma",
    "Desmoplastic small round cell tumour",
    "Rhabdoid tumour of soft tissue",
    "Perivascular epithelioid tumour, malignant",
    "Myoepithelial carcinoma",
    "Mixed tumour, malignant, NOS",
    "Undifferentiated sarcoma",
    "Spindle cell sarcoma, undifferentiated",
    "Pleomorphic sarcoma, undifferentiated",
    "Round cell sarcoma, undifferentiated",
    "Ewing sarcoma",
    "Other"],
       default=safe_get_list(patient_data, "Histology") if patient_data else []
    )

    Grade = st.radio("Grade", ["I", "II", "III", "Not Reported"],
        index=["I", "II", "III", "Not Reported"].index(safe_get(patient_data, "Grade", "Not Reported")) if patient_data else 0
    )

    Necrosis = st.radio("Necrosis", ["Present", "Absent", "Not Reported"],
        index=["Present", "Absent", "Not Reported"].index(safe_get(patient_data, "Tumor_Focality", "Unifocal")) if patient_data else 0
    )

    LVI = st.radio("LVI", ["Present", "Absent", "Not Reported"],
        index=["Present", "Absent", "Not Reported"].index(safe_get(patient_data, "Tumor_Focality", "Unifocal")) if patient_data else 0
    )

    Mytotic_Count = st.number_input("Mytotic_Count", min_value=0, max_value=100, step=1, value=int(safe_get(patient_data, "IPSS", 0)) if patient_data else 0
    )

    Location = st.radio("Location", ["Extremity", "Trunk", "Head and Neck", "Retroperitoneum", "Prostate", "Non-Extremity Bone", "Other"],
        index=["Extremity", "Trunk", "Head and Neck", "Retroperitoneum", "Prostate", "Non-Extremity Bone", "Other"].index(safe_get(patient_data, "Location", "Extremity")) if patient_data
        else 0
    )

    Clinical_Stage_Extremity = st.multiselect("Clinical Stage Extremity", ["cT0", "cTx", "cT1", "cT2", "cT3", "cT4", "cN0", "cN1", "M0", "M1", "Non Extremity"]),
    with st.expander("Clinical Stage Extremity Classification"):
        st.write("cT0: No evidence of primary tumor")
        st.write("cTx: Primary tumor cannot be assessed")
        st.write("cT1: Tumor ≤5 cm in greatest dimension")
        st.write("cT2: Tumor >5 cm but ≤10 cm in greatest dimension")
        st.write("cT3: Tumor >10 cm in greatest dimension")
        st.write("cT4: Tumor of any size with direct extension into the ipsilateral adrenal gland")
    default=safe_get_list(patient_data, "Clinical_Stage_Extremity") if patient_data else []

    Clinical_Stage_Retroperitoneum = st.multiselect("Clinical Stage Retroperitoneum", ["cT0", "cTx", "cT1", "cT2a", "cT2b", "cT3", "cT4a", "cT4b", "cT4c", "cN0", "cN1", "M0", "M1", "Non Retroperitoneal"]),
    with st.expander("Clinical Stage Retroperitoneum Classification"):
        st.write("cT0: No evidence of primary tumor")
        st.write("cTx: Primary tumor cannot be assessed")
        st.write("cT1: Organ confined tumor")
        st.write("cT2a: Tumor invades serosa or visceral peritoneum")
        st.write("cT2b: TTumor extends beyond serosa (mesentery)")
        st.write("cT3: Tumor invades another organ")
        st.write("cT4a: Multifocal tumor involvement (2 sites)")
        st.write("cT4b: Multifocal tumor involvement (3-5 sites)")
        st.write("cT4c: Multifocal tumor involvement (> 5 sites)")
    default=safe_get_list(patient_data, "Clinical_Stage_Retroperitoneum") if patient_data else []

    Biopsy_date = st.date_input("Date of Biopsy",
        value=datetime.strptime(safe_get(patient_data, "Surgery_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    Recurrent_Tumor = st.radio("Recurrent Tumor", ["No", "Yes"]),
    index=["No", "Yes"].index(safe_get(patient_data, "Recurrent_Tumor", "No")) if patient_data else 0
    
    if Recurrent_Tumor == "Yes":
        Recurrence_date = st.date_input("Date of Recurrence",
            value=datetime.strptime(safe_get(patient_data, "Recurrence_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
        Surgery_date = st.date_input("Date of Surgery",
            value=datetime.strptime(safe_get(patient_data, "Surgery_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    
    # Systemic Treatment
    st.subheader("Systemic Treatment")
    Systemic_Treatment = st.multiselect("Systemic_Treatment", ["None", "Conventional Chemotherapy", "Target Therapy", "Immunotherapy", "Radioligant", "ADC", "Others"]),
    if Systemic_Treatment : ("None", "Conventional Chemotherapy", "Target Therapy", "Immunotherapy", "Radioligant", "ADC", "Others").index(safe_get(patient_data, "Systemic_Treatment", "None")) if patient_data else 0
    Systemic_Treatment_first_date = st.date_input("First Date of Systemic_Treatment",   
            value=datetime.strptime(safe_get(patient_data, "Systemic_Treatment_first_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    Systemic_Treatment_last_date = st.date_input("Last Date of Systemic_Treatment",
            value=datetime.strptime(safe_get(patient_data, "Systemic_Treatment_last_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    default=safe_get_list(patient_data, "Systemic_Treatment") if patient_data else []

    # Treatment Details
    st.subheader("Treatment Details")
    Dose_per_fraction = st.number_input("Dose_per_fraction (Gy)", min_value=0, max_value=100, step=1, value=int(safe_get(patient_data, "Dose_per_fraction", 0)) if patient_data else 0
    )

    Fractionation = st.number_input("Fractionation", min_value=0, max_value=100, step=1, value=int(safe_get(patient_data, "Fractionation", 0)) if patient_data else 0
    )
    
    st.markdown("<hr style='border: 2px solid #666; margin: 20px 0;'>", unsafe_allow_html=True)

    # Side effects
    st.subheader("Urinary Side Effects")

    Dysuria = st.radio("Dysuria (CTCAE v5)", ["Present", "Absent"])
    
    Cystitis = st.radio("Cystitis (CTCAE v5)", ["None", "I", "II", "III", "IV", "V"])
    with st.expander("Cystitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Microscopic hematuria; minimal increase in frequency, urgency, dysuria, or nocturia; new onset of incontinence ")
        st.write("Grade II: Moderate hematuria; moderate increase in frequency, urgency, dysuria, nocturia or incontinence; urinary catheter placement or bladder irrigation indicated; limiting instrumental ADL ")     
        st.write("Grade III: Gross hematuria; transfusion, IV medications, or hospitalization indicated; elective invasive intervention indicated ")
        st.write("Grade IV: Life-threatening consequences; urgent invasive intervention indicated ")
        st.write("Grade V: Death")

    Bladder_Perforation = st.radio("Bladder Perforation (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Bladder Perforation Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Hematuria = st.radio("Hematuria (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Hematuria Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; urinary catheter or bladder irrigation indicated; limiting instrumental ADL")
        st.write("Grade III: Gross hematuria; transfusion, IV medications, or hospitalization indicated; elective invasive intervention indicated; limiting self care ADL")
        st.write("Grade IV: Life-threatening consequences; urgent invasive intervention indicated")
        st.write("Grade V: Death")

    Urinary_Fistula = st.radio("Urinary Fistula (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Urinary Fistula Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Urinary_Obstruction = st.radio("Urinary Obstruction (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Urinary Obstruction Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic but no hydronephrosis, sepsis, or renal dysfunction; urethral dilation, urinary or suprapubic catheter indicated")
        st.write("Grade III: Altered organ function (e.g., hydronephrosis or renal dysfunction); invasive intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Ureteral_Stenosis = st.radio("Ureteral Stenosis", ["Absent", "Present"])
    if Ureteral_Stenosis == "Present":
        Ureteral_Stenosis_date = st.date_input("Date of Ureteral Stenosis")

    Urinary_Retention = st.radio("Urinary Retention (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Urinary Retention Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Urinary, suprapubic or intermittent catheter placement not indicated; able to void with some residual")
        st.write("Grade II: Placement of urinary, suprapubic or intermittent catheter placement indicated; medication indicated")
        st.write("Grade III: Elective invasive intervention indicated; substantial loss of affected kidney function or mass")
        st.write("Grade IV: Life-threatening consequences; organ failure; urgent operative intervention indicated")
        st.write("Grade V: Death")

    # Side Effects - Gastrointestinal
    st.subheader("Gastrointestinal Side Effects")

    Diarrhea = st.radio("Diarrhea (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Diarrhea Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Increase of <4 stools/day over baseline; mild increase in ostomy output compared to baseline")
        st.write("Grade II: Increase of 4-6 stools/day over baseline; moderate increase in ostomy output compared to baseline; limiting instrumental ADL")
        st.write("Grade III: Increase of ≥7 stools/day over baseline; incontinence; limiting self care ADL")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Nausea = st.radio("Nausea (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Nausea Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Loss of appetite without alteration in eating habits")
        st.write("Grade II: Oral intake decreased without significant weight loss, dehydration, or malnutrition; IV fluids indicated <24 hrs")
        st.write("Grade III: Inadequate oral caloric or fluid intake; tube feeding or TPN indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Bowel_Perforation = st.radio("Bowel Perforation (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Bowel Perforation Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Bowel_Obstruction = st.radio("Bowel Obstruction (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Bowel Obstruction Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; noninvasive intervention indicated")
        st.write("Grade III: Symptomatic; invasive intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Proctitis = st.radio("Proctitis (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Proctitis Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic (e.g., rectal discomfort, passing blood or mucus); medical intervention indicated; limiting instrumental ADL ")
        st.write("Grade III: Severe symptoms; fecal urgency or stool incontinence; limiting self care ADL ")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Rectal_Fistula = st.radio("Rectal Fistula (CTCAE v5)", ["Absent", "I" "II", "III", "IV", "V"])
    with st.expander("Rectal Fistula Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic, Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Rectal_Hemorrhage = st.radio("Rectal Hemorrhage (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Rectal Hemorrhage Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Minimal bleeding identified on imaging; intervention not indicated")
        st.write("Grade II: Moderate bleeding; medical intervention indicated")
        st.write("Grade III: Transfusion, radiologic, endoscopic or elective operative intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Rectal_Pain = st.radio("Rectal Pain (CTCAE v5)", ["Absent", "I", "II", "III"])
    with st.expander("Rectal Pain Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Mild discomfort; analgesics not indicated")
        st.write("Grade II: Moderate pain; analgesics indicated; limiting instrumental ADL")
        st.write("Grade III: Severe pain; limiting self care ADL")

    Rectal_perforation = st.radio("Rectal Perforation (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Rectal Perforation Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Rectal_Stenosis = st.radio("Rectal Stenosis (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Rectal Stenosis Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; medical intervention indicated")
        st.write("Grade III: Severe symptoms; limiting self care ADL ")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Organ_Failure = st.radio("Organ Failure (CTCAE v5)", ["Absent", "III", "IV", "V"])
    with st.expander("Organ Failure Classification"):
        st.write("Absent: No change")
        st.write("Grade III: Shock with azotemia and acidbase disturbances; significant coagulation abnormalities ")
        st.write("Grade IV: Life-threatening consequences (e.g., vasopressor dependent and oliguric or anuric or ischemic colitis or lactic acidosis) ")
        st.write("Grade V: Death")

    #Other Side Effects
    st.subheader("Fatigue")

    Fatigue = st.radio("Fatigue", ["None", "I", "II", "III"])
    with st.expander("Fatigue Classification"):
        st.write("Grade 0: No fatigue")
        st.write("Grade I: Mild fatigue; no change in activity")
        st.write("Grade II: Moderate fatigue; limiting instrumental ADL")
        st.write("Grade III: Severe fatigue; limiting self care ADL")

    st.subheader("Side Effects - Others")
    Pneumonitis = st.radio("Pneumonitis", ["None", "I", "II", "III", "IV", "V"])
    with st.expander("Pneumonitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; medical intervention indicated but not limiting instrumental ADL")
        st.write("Grade III: Severe symptoms; limiting self care ADL, O2 indicated")
        st.write("Grade IV: Life-threatening respiratory compromise; urgent intervention indicated")
        st.write("Grade V: Death")

    Esophagitis = st.radio("Esophagitis", ["None", "I", "II", "III", "IV", "V"])
    with st.expander("Esophagitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; altered eating/swallowing; oral supplements indicated ")
        st.write("Grade III: Severely altered eating/swallowing; tube feeding, TPN, or hospitalization indicated")
        st.write("Grade IV: Life-threatening consequences; urgent operative intervention indicated")
        st.write("Grade V: Death")

    Overal_tolerance = st.radio("Overall Tolerance", ["Excellent", "Good", "Fair", "Poor"])

    # Recurrence details
    st.subheader("Recurrence Details")
    local_recurrence = st.radio("Local Recurrence", ["No", "Yes"])
    regional_recurrence = st.radio("Regional Recurrence", ["No", "Yes"])
    distant_recurrence = st.radio("Distant Recurrence", ["No", "Yes"])
    death = st.radio("Death", ["No", "Yes"])

    
    time_to_local_recurrence = None
    if local_recurrence == "Yes":
        time_to_local_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Local Recurrence"))

    time_to_regional_recurrence = None
    if regional_recurrence == "Yes":
        time_to_regional_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Regional Recurrence"))

    time_to_distant_recurrence = None
    if distant_recurrence == "Yes":
        time_to_distant_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Distant Recurrence"))

    death_date = None
    if death == "Yes":
        Cancer_related_death = st.radio("Cancer Related Death", ["No", "Yes"])
        time_to_death = calculate_months(last_radiotherapy_date, st.date_input("Date of Death"))

    # Submit button to trigger calculation
    submitted = st.form_submit_button("Calculate")

    if submitted:
        st.session_state.age = datetime.today().year - date_of_birth.year - (
            (datetime.today().month, datetime.today().day) < (date_of_birth.month, date_of_birth.day)
        )
        st.session_state.time_since_treatment = calculate_months(last_radiotherapy_date, follow_up_date)
        st.session_state.time_to_local_recurrence = time_to_local_recurrence if local_recurrence == "Yes" else "N/A"
        st.session_state.time_to_regional_recurrence = time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A"
        st.session_state.time_to_distant_recurrence = time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A"
        st.session_state.time_to_death = time_to_death if death == "Yes" else "N/A"

        st.subheader("Calculated Results:")
        st.write(f"**Calculated Age**: {st.session_state.age} years")
        st.write(f"**Time since last radiotherapy**: {st.session_state.time_since_treatment} months")
        if local_recurrence == "Yes":
            st.write(f"**Time to local recurrence**: {st.session_state.time_to_local_recurrence} months")
        if regional_recurrence == "Yes":
            st.write(f"**Time to regional recurrence**: {st.session_state.time_to_regional_recurrence} months")
        if distant_recurrence == "Yes":
            st.write(f"**Time to distant recurrence**: {st.session_state.time_to_distant_recurrence} months")
        if death == "Yes":
            st.write(f"**Time to death**: {st.session_state.time_to_death} months")

# Save button is placed outside the form so it persists after submission
if st.button("Save Information"):
    if st.session_state.age is None or st.session_state.time_since_treatment is None:
        st.error("Please calculate the age and treatment times before saving.")
    else:
        data = {
            # Patient details
            "MRN": mrn if mrn else "N/A",
            "Date_of_Birth": date_of_birth.strftime("%Y-%m-%d"),
            "Age": st.session_state.age,
            "Date_of_Last_Radiotherapy": last_radiotherapy_date.strftime("%Y-%m-%d"),
            "Follow_up_date": follow_up_date.strftime("%Y-%m-%d"),
            "Follow_up_time": st.session_state.time_since_treatment,
            "Histology": Histology,
            "Grade": Grade,
            "Necrosis": Necrosis,
            "LVI": LVI,
            "Mytotic_Count": Mytotic_Count,
            "Location": Location,
            "Clinical_Stage_Extremity": Clinical_Stage_Extremity,
            "Clinical_Stage_Retroperitoneum": Clinical_Stage_Retroperitoneum,
            "Biopsy_date": Biopsy_date.strftime("%Y-%m-%d"),
            "Recurrent_Tumor": Recurrent_Tumor,
            "Recurrence_date": Recurrence_date.strftime("%Y-%m-%d") if Recurrent_Tumor == "Yes" else "N/A",
            "Surgery_date": Surgery_date.strftime("%Y-%m-%d") if Recurrent_Tumor == "Yes" else "N/A",
            # Systemic Treatment
            "Systemic_Treatment": Systemic_Treatment,
            "Systemic_Treatment_first_date": Systemic_Treatment_first_date.strftime("%Y-%m-%d"),
            "Systemic_Treatment_last_date": Systemic_Treatment_last_date.strftime("%Y-%m-%d"),
            # Treatment Details
            "Dose_per_Fraction": Dose_per_fraction,
            "Fractionation": Fractionation,
            # Side Effects
                "Dysuria": Dysuria,
            "Cystitis": Cystitis,
            "Bladder_Perforation": Bladder_Perforation,
            "Hematuria": Hematuria,
            "Urinary_Fistula": Urinary_Fistula,
            "Urinary_Obstruction": Urinary_Obstruction,
            "Ureteral_Stenosis": Ureteral_Stenosis,
            "Ureteral_Stenosis_Date": Ureteral_Stenosis_date.strftime("%Y-%m-%d") if Ureteral_Stenosis_date else "N/A",
            "Urinary_Retention": Urinary_Retention,
            "Diarrhea": Diarrhea,
            "Nausea": Nausea,
            "Bowel_Perforation": Bowel_Perforation,
            "Bowel_Obstruction": Bowel_Obstruction,
            "Proctitis": Proctitis,
            "Rectal_Fistula": Rectal_Fistula,
            "Rectal_Hemorrhage": Rectal_Hemorrhage,
            "Rectal_Pain": Rectal_Pain,
            "Rectal_Perforation": Rectal_perforation,
            "Rectal_Stenosis": Rectal_Stenosis,
            "Organ_Failure": Organ_Failure,
            "Fatigue": Fatigue,
            "Pneumonitis": Pneumonitis,
            "Esophagitis": Esophagitis,
            "Overall_Tolerance": Overal_tolerance,
            # Recurrence Details
            "Local Recurrence": local_recurrence,
            "Time_to_local_recurrence": st.session_state.time_to_local_recurrence if local_recurrence == "Yes" else "N/A",
            "Regional_recurrence": regional_recurrence,
            "Time_to_regional_recurrence": st.session_state.time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A",
            "Distant_recurrence": distant_recurrence,
            "Time_to_distant_recurrence": st.session_state.time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A",
            "Cancer Related Death": Cancer_related_death if death == "Yes" else "N/A",
            "Death": death,
            "time_to_death": st.session_state.time_to_death if death == "Yes" else "N/A",
        }
        save_data(data)
        st.success("Patient data has been successfully saved!")
