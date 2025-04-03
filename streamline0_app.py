import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# A) Define the Main Table (df_main) with numbering from 1 to 53
# -------------------------
main_data = [
    {"number": 1, "size_mass": "1,9 x 2,1 x 2,8", "RENAL_score": "7P", "BIOPSY": "CLEAR CELL"},
    {"number": 2, "size_mass": "1 x 1,7 x 1,3", "RENAL_score": "6x", "BIOPSY": "CLEAR CELL"},
    {"number": 3, "size_mass": "2,1 x 2,5 x 2,8", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 4, "size_mass": "2 x 2,8 x 2,8", "RENAL_score": "4x", "BIOPSY": "CLEAR CELL"},
    {"number": 5, "size_mass": "1,6 x 1,2 x 1,8", "RENAL_score": "7p", "BIOPSY": "CLEAR CELL"},
    {"number": 6, "size_mass": "2,9 x 2,6 x 2,8", "RENAL_score": "5a", "BIOPSY": "CLEAR CELL"},
    {"number": 7, "size_mass": "2,9 x 2,6 x 3 (1,9 x 2,2 x 3)", "RENAL_score": "6x", "BIOPSY": "CLEAR CELL"},
    {"number": 8, "size_mass": "3,5 x 3,4 x 3,9", "RENAL_score": "4x", "BIOPSY": "CLEAR CELL"},
    {"number": 9, "size_mass": "2,1 x 1,9 x 1,9", "RENAL_score": "5a", "BIOPSY": "CLEAR CELL"},
    {"number": 10, "size_mass": "2,3 x 2 x 2,1", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 11, "size_mass": "2,9 x 3,3 x 3,1", "RENAL_score": "5x", "BIOPSY": "CLEAR CELL"},
    {"number": 12, "size_mass": "3,6 x 3,5 x 3,7", "RENAL_score": "5x", "BIOPSY": "CLEAR CELL"},
    {"number": 13, "size_mass": "3,6 x 3,8 x 2,8", "RENAL_score": "7ph", "BIOPSY": "CLEAR CELL"},
    {"number": 14, "size_mass": "3,2 x 3,4 x 3,1", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 15, "size_mass": "3 x 2,8 x 2,7", "RENAL_score": "4p", "BIOPSY": "CLEAR CELL"},
    {"number": 16, "size_mass": "2,8 x 2,4 x 2", "RENAL_score": "6x", "BIOPSY": "CLEAR CELL"},
    {"number": 17, "size_mass": "1,7 x 1,6 x 1,8", "RENAL_score": "5a", "BIOPSY": "CLEAR CELL"},
    {"number": 18, "size_mass": "2,6 x 2,5 x 2,6", "RENAL_score": "7xh", "BIOPSY": "CLEAR CELL"},
    {"number": 19, "size_mass": "5,8 x 4,3 x 6,2", "RENAL_score": "5x", "BIOPSY": "CLEAR CELL"},
    {"number": 20, "size_mass": "2,9 x 3,2 x 2,6", "RENAL_score": "6x", "BIOPSY": "CLEAR CELL"},
    {"number": 21, "size_mass": "1,4 x 1,4 x 1,5", "RENAL_score": "4p", "BIOPSY": "CLEAR CELL"},
    {"number": 22, "size_mass": "2,6 x 2,3 x 2,1", "RENAL_score": "7ph", "BIOPSY": "CLEAR CELL"},
    {"number": 23, "size_mass": "2 x 1,8 x 1,9", "RENAL_score": "4p", "BIOPSY": "CLEAR CELL"},
    {"number": 24, "size_mass": "3,2 x 2,9 x 3,2", "RENAL_score": "4p", "BIOPSY": "CLEAR CELL"},
    {"number": 25, "size_mass": "3,1 x 2,9 x 2,8", "RENAL_score": "6a", "BIOPSY": "CLEAR CELL"},
    {"number": 26, "size_mass": "1,9 x 1,6 x 1,6", "RENAL_score": "6x", "BIOPSY": "CLEAR CELL"},
    {"number": 27, "size_mass": "2 x 2,5 x 2,3", "RENAL_score": "7p", "BIOPSY": "CLEAR CELL"},
    {"number": 28, "size_mass": "2,4 x 2,6 x 2", "RENAL_score": "6a", "BIOPSY": "CLEAR CELL"},
    {"number": 29, "size_mass": "3,6 x 3,7 x 4,3", "RENAL_score": "10a", "BIOPSY": "CLEAR CELL"},
    {"number": 30, "size_mass": "1,8 x 2 x 2,1", "RENAL_score": "4x", "BIOPSY": "CLEAR CELL"},
    {"number": 31, "size_mass": "2,2 x 2,5 x 2,4", "RENAL_score": "4x", "BIOPSY": "CLEAR CELL"},
    {"number": 32, "size_mass": "2,5 x 2,1 x 2,2", "RENAL_score": "4p", "BIOPSY": "CLEAR CELL"},
    {"number": 33, "size_mass": "19 x 19 x 2,1", "RENAL_score": "4x", "BIOPSY": "CLEAR CELL"},
    {"number": 34, "size_mass": "2,6 x 2,5 x 2,1", "RENAL_score": "4a", "BIOPSY": "CLEAR CELL"},
    {"number": 35, "size_mass": "4,6 x 3,8 x 4,8", "RENAL_score": "8x", "BIOPSY": "CLEAR CELL"},
    {"number": 36, "size_mass": "2,6 x 1,9 x 2,2", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 37, "size_mass": "4,2 x 3,6 x 4,6", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 38, "size_mass": "3,1 x 2,5 x 4,8", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 39, "size_mass": "3,1 x 3,9 x 3,4", "RENAL_score": "4x", "BIOPSY": "CLEAR CELL"},
    {"number": 40, "size_mass": "2,5 x 2,7 x 2,8", "RENAL_score": "5x", "BIOPSY": "CLEAR CELL"},
    {"number": 41, "size_mass": "3,4 x 3,5 x 2,9", "RENAL_score": "6p", "BIOPSY": "CLEAR CELL"},
    {"number": 42, "size_mass": "3,7 x 3,5 x 3,4", "RENAL_score": "4p", "BIOPSY": "CLEAR CELL"},
    {"number": 43, "size_mass": "1,7 x 1,9 x 2", "RENAL_score": "5a", "BIOPSY": "CLEAR CELL"},
    {"number": 44, "size_mass": "3,7 x 3,5 x 4", "RENAL_score": "4a", "BIOPSY": "CLEAR CELL"},
    {"number": 45, "size_mass": "2,4 x 2,0 x 2,6", "RENAL_score": "4p", "BIOPSY": "CLEAR CELL"},
    {"number": 46, "size_mass": "2,6 x 2,3 x 2,1", "RENAL_score": "7ah", "BIOPSY": "CLEAR CELL"},
    {"number": 47, "size_mass": "2,9 x 2,7 x 2,7", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 48, "size_mass": "3,2 x 2,5 x 3,7", "RENAL_score": "4ah", "BIOPSY": "CLEAR CELL"},
    {"number": 49, "size_mass": "2,9 x 2,8 x 2,9", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 50, "size_mass": "3,7 x 3,2 x 3,5", "RENAL_score": "5a", "BIOPSY": "CLEAR CELL"},
    {"number": 51, "size_mass": "2 x 2,2 x 1,9", "RENAL_score": "4a", "BIOPSY": "CLEAR CELL"},
    {"number": 52, "size_mass": "2,8 x 2,7 x 2", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"},
    {"number": 53, "size_mass": "2 x 1 x 2", "RENAL_score": "5p", "BIOPSY": "CLEAR CELL"}
]
df_main = pd.DataFrame(main_data)

# -------------------------
# B) Define the Cryoablation Results Table (df_cryo) with numbering from 1 to 54
# (Note: There is one extra row in the cryo data, so we assume the first 53 rows match the main data)
# -------------------------
cryo_data = [
    {"number": 1, "cryoprobes": "3 rod", "types_of_probes": "ROD", "size_Ice_ball": "2,7x1,9x3,2", "protection": "NO", "complications": "NONE"},
    {"number": 2, "cryoprobes": "1", "types_of_probes": "", "size_Ice_ball": "1,4 x 2,6 x 2,8 or 1,7", "protection": "YES/COLON SPLEEN", "complications": "NONE"},
    {"number": 3, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "2,8 x 2,7 x 3,5", "protection": "NONE", "complications": "NONE"},
    {"number": 4, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "3 x 3,6 x 2", "protection": "NONE", "complications": "PNEUMOTH"},
    {"number": 5, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "2,7 x 2,4 x 2,8", "protection": "NONE", "complications": "NONE"},
    {"number": 6, "cryoprobes": "2", "types_of_probes": "", "size_Ice_ball": "2,9 x 3 x 4,2", "protection": "YES/SPLEEN", "complications": ""},
    {"number": 7, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3 x 3,8 x 3,4", "protection": "NO", "complications": "MILD HEMORRHAGE?"},
    {"number": 8, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,8 x 5,2 x 4,9", "protection": "YES/PSOAS", "complications": "none"},
    {"number": 9, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,2 x 3,4 x 3", "protection": "NO", "complications": "NONE"},
    {"number": 10, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,7 x 2,4 x 3,2", "protection": "NO", "complications": "NONE"},
    {"number": 11, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "4,2 x 3,6 x 4,1", "protection": "NO", "complications": "NONE"},
    {"number": 12, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,8 x 4,2 x 4,9", "protection": "YES/COLON", "complications": "MILD HEMORRHAGE?"},
    {"number": 13, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 3,6 x 3,3", "protection": "YES/ COLON", "complications": "NONE"},
    {"number": 14, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 3,2 x 3,6", "protection": "YES/ COLON", "complications": "MILD HEMORRHAGE?"},
    {"number": 15, "cryoprobes": "3", "types_of_probes": "2ROD+1SPHERE", "size_Ice_ball": "3,6 x 2,9 x 3,4", "protection": "NO", "complications": "NONE?"},
    {"number": 16, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "2,7 x 3,7 x 3,5", "protection": "YES/COLON", "complications": ""},
    {"number": 17, "cryoprobes": "1", "types_of_probes": "SPHERE", "size_Ice_ball": "1,2 x 1,8 x 2", "protection": "YES/PSOAS", "complications": ""},
    {"number": 18, "cryoprobes": "3", "types_of_probes": "4SPHERE", "size_Ice_ball": "3,5 x 3,3 x 3,8", "protection": "COLON/SPLEEN", "complications": "none"},
    {"number": 19, "cryoprobes": "5", "types_of_probes": "4FORCE+1ROD", "size_Ice_ball": "5,5 x 5,7 x 6,5", "protection": "YES/COLON/SPLEEN", "complications": "none"},
    {"number": 20, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 4,8 x 4", "protection": "HYDRO/COLON", "complications": "none"},
    {"number": 21, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,1 x 2,9 x 2,7", "protection": "NO", "complications": "MILD HEMORRHAGE"},
    {"number": 22, "cryoprobes": "3", "types_of_probes": "2ROD+1SPHERE", "size_Ice_ball": "2,6 x 4,4 x 3,5", "protection": "YES/LIVER/COLON", "complications": "NONE"},
    {"number": 23, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,1 x 2,5 x 3", "protection": "NO", "complications": "NONE"},
    {"number": 24, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,5 x 4,7 x 5", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 25, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,2 x 4 x 4", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 26, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3 x 2,5 x 2,8", "protection": "NO", "complications": "NONE"},
    {"number": 27, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,4 x 3,3 x 3", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 28, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "4 x 2,4 x 3,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 29, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "5,2 x 4 x 4,8", "protection": "YES/SPLEEN", "complications": "MILD HEMORRHAGE"},
    {"number": 30, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,7 x 3,3 x 2,8", "protection": "NO", "complications": "NONE"},
    {"number": 31, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "2,9 x 3,3 x 2,9", "protection": "YES/PSOAS,RENAL VEIN", "complications": "NONE"},
    {"number": 32, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,7 x 3,4 x 2,7", "protection": "YES/SPLEEN", "complications": "NONE"},
    {"number": 33, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3 x 3,6 x 3,8", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 34, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,1 x 2,7 x 2,4", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 35, "cryoprobes": "4", "types_of_probes": "FORCE", "size_Ice_ball": "5,2 x 4,1 x 4,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 36, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "2,6 x 2,2 x 2,1", "protection": "YES/PSOAS", "complications": "NONE"},
    {"number": 37, "cryoprobes": "3", "types_of_probes": "FORCE", "size_Ice_ball": "5,2 x 4,2 x 4,8", "protection": "YES/PSOAS", "complications": "HEMORRHAGE- νοσηλεία"},
    {"number": 38, "cryoprobes": "3", "types_of_probes": "FORCE", "size_Ice_ball": "", "protection": "", "complications": ""},
    {"number": 39, "cryoprobes": "4", "types_of_probes": "FORCE", "size_Ice_ball": "5,0 x 3,5 x 5,3", "protection": "YES/COLON, PSOAS", "complications": "NONE"},
    {"number": 40, "cryoprobes": "2", "types_of_probes": "FORCE", "size_Ice_ball": "3,5 x 4,1 x 4,3", "protection": "YES/ COLON", "complications": "MILD HEMORRHAGE"},
    {"number": 41, "cryoprobes": "2", "types_of_probes": "ROD", "size_Ice_ball": "3 x 4,1 x 2,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 42, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "5,5 x 5,5 x 4,6", "protection": "NO", "complications": "MILD HEMORRHAGE"},
    {"number": 43, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "4,2 x 3,9 x 5,4", "protection": "YES/ COLON, PSOAS", "complications": "NONE"},
    {"number": 44, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "3,4 x 2,6 x 3,1", "protection": "YES/COLON", "complications": "HEMORRHAGE ΜΕΓΑΛΗ"},
    {"number": 45, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "3,8 x 5,3 x 6,5", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 46, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "3,2 x 3,7 x 3,6", "protection": "YES/PSOAS", "complications": "MILD HEMORRHAGE"},
    {"number": 47, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,8 x 2,8 x 2,9", "protection": "YES/COLON", "complications": "NONE"},
    {"number": 48, "cryoprobes": "4", "types_of_probes": "SPHERE", "size_Ice_ball": "4,6 x 3,6 x 3,6", "protection": "YES/LIVER,COLON", "complications": "NONE"},
    {"number": 49, "cryoprobes": "3", "types_of_probes": "ROD", "size_Ice_ball": "4,2 x 3,1 x 3,6", "protection": "YES/LIVER,COLON", "complications": "NONE"},
    {"number": 50, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "3,6 x 3 x 3,5", "protection": "YES/SPLEEN,COLON", "complications": "NONE"},
    {"number": 51, "cryoprobes": "4", "types_of_probes": "ROD", "size_Ice_ball": "4,1 x 4 x 5,2", "protection": "YES/COLON", "complications": "SUBCUTANEUS HEMATOMA / MILD HEMORRHAGE"},
    {"number": 52, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "2,7 x 2,9 x 2,6", "protection": "YES/ COLON", "complications": "NONE"},
    {"number": 53, "cryoprobes": "3", "types_of_probes": "SPHERE", "size_Ice_ball": "4,7 x 3,6 x 3,5", "protection": "YES/ COLON", "complications": "NONE"},
    {"number": 54, "cryoprobes": "2", "types_of_probes": "SPHERE", "size_Ice_ball": "2,3 x 33 x 2,5", "protection": "YES/ PSOAS", "complications": "NONE"}
]
df_cryo = pd.DataFrame(cryo_data)

# ------------------------------------
# Merge the two tables by "number"
# We'll merge only the first 53 rows (matching main_data) to ensure a one-to-one match.
# ------------------------------------
df_main = df_main[df_main["number"] <= 53]
df_cryo = df_cryo[df_cryo["number"] <= 53]
df_merged = pd.merge(df_main, df_cryo, on="number")

# ------------------------------------
# Helper function to parse "size_mass" into a numeric array
# ------------------------------------
def parse_size(s):
    try:
        # Replace commas with dots, split on "x", and convert to floats
        parts = s.replace(',', '.').split('x')
        return [float(part.strip()) for part in parts]
    except Exception as e:
        return None

df_merged["size_parsed"] = df_merged["size_mass"].apply(parse_size)

# ------------------------------------
# Streamlit App Interface
# ------------------------------------
st.title("Renal Cryoablation Treatment Planner")
st.markdown("""
This application matches your tumor parameters to our reference data and provides a recommended cryoablation plan.
Enter your tumor parameters in the sidebar.
""")

# ---------------------------
# Sidebar: User Input Section
# ---------------------------
st.sidebar.header("Enter Tumor Parameters")
inp_size_mass = st.sidebar.text_input("Tumor Size (Mass) (e.g., 4,2 x 3,6 x 4,6)", value="4,2 x 3,6 x 4,6")
inp_renal_score = st.sidebar.text_input("RENAL Score (e.g., 5p)", value="5p")
inp_histology = st.sidebar.selectbox("Histology Type", options=["CLEAR CELL", "PAPILLARY", "CHROMOPHOBE"], index=0)

# Display user input for confirmation
st.sidebar.markdown("### Your Input:")
st.sidebar.write(f"**Tumor Size (Mass):** {inp_size_mass} cm")
st.sidebar.write(f"**RENAL Score:** {inp_renal_score}")
st.sidebar.write(f"**Histology Type:** {inp_histology}")

# ------------------------------------
# Matching Algorithm: Find the closest matching row based on Tumor Size, RENAL Score, and Histology
# ------------------------------------
if st.sidebar.button("Generate Cryoablation Plan"):
    def extract_numeric_from_score(s):
        try:
            return float(''.join(ch for ch in s if ch.isdigit() or ch == '.'))
        except:
            return np.nan

    user_dims = parse_size(inp_size_mass)
    if user_dims is None or len(user_dims) != 3:
        st.error("Invalid Tumor Size format. Please use the format: '4,2 x 3,6 x 4,6'.")
    else:
        user_dims = np.array(user_dims)
        user_sorted = np.sort(user_dims)
        user_mean = np.mean(user_dims)
        user_renal_numeric = extract_numeric_from_score(inp_renal_score)

        best_idx = None
        best_diff = float("inf")
    
        # Define weights: mass difference weight = 5, RENAL score difference = 2, histology penalty = 1
        mass_weight = 5
        renal_weight = 2
        histology_weight = 1
    
        for idx, row in df_merged.iterrows():
            parsed = row["size_parsed"]
            if parsed is None or len(parsed) != 3:
                continue
            ref_dims = np.array(parsed)
            ref_sorted = np.sort(ref_dims)
            ref_mean = np.mean(ref_dims)
            ref_renal = extract_numeric_from_score(row["RENAL_score"])
    
            # Calculate the weighted mass difference: (5 * mean difference) + sum of absolute differences in sorted dimensions.
            mass_diff = mass_weight * abs(ref_mean - user_mean) + np.sum(np.abs(ref_sorted - user_sorted))
            # Calculate the weighted RENAL score difference
            renal_diff = renal_weight * abs(ref_renal - user_renal_numeric)
            # Histology penalty: if the reference histology (BIOPSY) does not match the user input (case-insensitive), add a penalty.
            if row["BIOPSY"].strip().lower() == inp_histology.strip().lower():
                histology_penalty = 0
            else:
                histology_penalty = histology_weight * 1
    
            total_diff = mass_diff + renal_diff + histology_penalty
    
            if total_diff < best_diff:
                best_diff = total_diff
                best_idx = idx
    
        if best_idx is None:
            st.error("No matching data found. Please verify your tumor size or RENAL score.")
        else:
            match = df_merged.loc[best_idx]
            st.header("Recommended Cryoablation Plan")
            st.subheader("Matched Reference Parameters")
            st.write(f"**Tumor Size (Mass):** {match['size_mass']} cm")
            st.write(f"**RENAL Score:** {match['RENAL_score']}")
            st.write(f"**Histology Type:** {match['BIOPSY']}")
            st.markdown("---")
            st.subheader("Cryoablation Parameters")
            st.write(f"**Cryoprobes:** {match['cryoprobes']}")
            st.write(f"**Types of Probes:** {match['types_of_probes']}")
            st.write(f"**Estimated Ice Ball Size:** {match['size_Ice_ball']} cm")
            st.write(f"**Protection:** {match['protection']}")
            st.write(f"**Complications:** {match['complications']}")
            st.info(f"Matching difference metric: {best_diff:.2f}")

st.markdown("---")
st.write("Created by Michailidis A. for free use (demo).")
