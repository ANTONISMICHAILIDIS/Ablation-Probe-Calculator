import streamlit as st
import pandas as pd

# Define ablation data with probe characteristics for different body systems
ablation_data = {
    "Renal": {
        "Cryoablation": [
            {"name": "Icerod", "iceball": (2.5, 4), "shape": "Elliptical"},
            {"name": "Icesphere", "iceball": (2, 3), "shape": "Spherical"},
            {"name": "Iceforce", "iceball": (3.5, 5), "shape": "Hybrid"}
        ],
        "Radiofrequency Ablation": [
            {"name": "Single Needle", "size": "17-gauge", "active_tip": "2-3 cm"},
            {"name": "Cluster Needle", "size": "17-gauge", "active_tip": "2.5 cm"}
        ],
        "Microwave Ablation": [
            {"name": "Standard Microwave Probe", "size": "14-17 gauge", "power": "60-100W"}
        ]
    },
    "Liver": {
        "Radiofrequency Ablation": [
            {"name": "Single Needle", "size": "17-gauge", "active_tip": "2-3 cm"},
            {"name": "Cluster Needle", "size": "17-gauge", "active_tip": "2.5 cm"}
        ],
        "Microwave Ablation": [
            {"name": "Standard Microwave Probe", "size": "14-17 gauge", "power": "60-100W"}
        ],
        "Cryoablation": [
            {"name": "Cryoprobe", "iceball": (3.5, 5), "shape": "Elliptical"}
        ]
    },
    "Lung": {
        "Radiofrequency Ablation": [
            {"name": "Single Needle", "size": "17-gauge", "active_tip": "2-3 cm"}
        ],
        "Microwave Ablation": [
            {"name": "Standard Microwave Probe", "size": "14-17 gauge", "power": "60-100W"}
        ],
        "Cryoablation": [
            {"name": "Cryoprobe", "iceball": (3.5, 5), "shape": "Elliptical"}
        ]
    },
    "Bone": {
        "Radiofrequency Ablation": [
            {"name": "Single-Tined Electrode", "size": "14-17 gauge", "active_tip": "2-3 cm"},
            {"name": "Multi-Tined Electrode", "size": "14-17 gauge", "active_tip": "3-5 cm"}
        ],
        "Cryoablation": [
            {"name": "Cryoprobe", "iceball": (3.5, 5), "shape": "Elliptical"}
        ],
        "Laser Ablation": [
            {"name": "Laser Fiber", "size": "18-gauge", "power": "2W for 6-10 min"}
        ]
    },
    "Thyroid": {
        "Radiofrequency Ablation": [
            {"name": "Thyroid RFA Electrode", "size": "18-gauge", "active_tip": "0.5-1 cm"}
        ],
        "Laser Ablation": [
            {"name": "Laser Fiber", "size": "21-gauge", "power": "3W for 5-10 min"}
        ]
    }
}

def suggest_probes(body_system, ablation_type, tumor_length, tumor_width, tumor_height, margin_required):
    """
    Suggests optimal ablation probes based on tumor size and required margin.
    """
    probes = ablation_data.get(body_system, {}).get(ablation_type, [])
    d_ablation = max(tumor_length, tumor_width, tumor_height) + 2 * margin_required

    # If lesion is small, suggest the smallest available probe
    for probe in probes:
        if ablation_type == "Cryoablation" and "iceball" in probe:
            iceball_max = probe["iceball"][1]
            if iceball_max >= d_ablation:
                return [f"{probe['name']} (1 probe)"]
        elif ablation_type in ["Radiofrequency Ablation", "Microwave Ablation", "Laser Ablation"] and "active_tip" in probe:
            active_tip_length = float(probe["active_tip"].split()[0])
            if active_tip_length >= d_ablation:
                return [f"{probe['name']} (1 probe)"]

    # If no single probe is sufficient, suggest multiple
    for probe in probes:
        if ablation_type == "Cryoablation" and "iceball" in probe:
            iceball_max = probe["iceball"][1]
            return [f"{probe['name']} (2 probes)"] if d_ablation > iceball_max else [f"{probe['name']} (1 probe)"]

    return ["No suitable probe found"]

def main():
    st.set_page_config(page_title="Ablation Probe Calculator", layout="centered")
    
    st.title("Ablation Probe Calculator")
    st.markdown("Select the medical parameters to get the optimal ablation probe recommendation.")

    # Sidebar for user input
    st.sidebar.header("Input Parameters")
    
    condition_type = st.sidebar.selectbox("Condition Type", ["Benign", "Malignant"])
    body_system = st.sidebar.selectbox("Body System", list(ablation_data.keys()))
    ablation_type = st.sidebar.selectbox("Ablation Type", list(ablation_data[body_system].keys()))
    
    st.sidebar.header("Tumor Dimensions (cm)")
    tumor_length = st.sidebar.number_input("Tumor Length", min_value=0.1, step=0.1)
    tumor_width = st.sidebar.number_input("Tumor Width", min_value=0.1, step=0.1)
    tumor_height = st.sidebar.number_input("Tumor Height", min_value=0.1, step=0.1)
    
    # Define margin based on tumor size
    margin_required = 1.0 if max(tumor_length, tumor_width, tumor_height) > 4 else 0.5
    st.sidebar.write(f"**Required Ablation Margin:** {margin_required} cm")
    
    if st.sidebar.button("Calculate Probes"):
        suggested_probes = suggest_probes(body_system, ablation_type, tumor_length, tumor_width, tumor_height, margin_required)
        if suggested_probes:
            st.success(f"Recommended Probes: {', '.join(suggested_probes)}")
        else:
            st.warning("No suitable probes found for the given parameters.")
    
    # Display ablation probe details
    st.subheader(f"{body_system} - {ablation_type} Probe Information")
    probe_df = pd.DataFrame(ablation_data[body_system][ablation_type])
    st.table(probe_df)
    
    # Footer
    st.markdown("---")
    st.markdown("Developed for efficient ablation planning.")

if __name__ == "__main__":
    main()
