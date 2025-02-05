import streamlit as st
import pandas as pd

# Expanded ablation data with probe characteristics for different body systems
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
        ],
        "IRE": [
            {"name": "NanoKnife", "electrodes": 2, "voltage": "1500-3000 V", "spacing": "1.5-2 cm", "protocol": "90 pulses"}
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
        ],
        "IRE": [
            {"name": "NanoKnife", "electrodes": 2, "voltage": "1500-3000 V", "spacing": "1.5-2 cm", "protocol": "90 pulses"}
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
        ],
        "IRE": [
            {"name": "NanoKnife", "electrodes": 2, "voltage": "1500-3000 V", "spacing": "1.5-2 cm", "protocol": "90 pulses"}
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

# Research-based protocol recommendations (from recent literature)
ablation_protocols = {
    "Renal": {
        "Cryoablation": (
            "Studies suggest that renal cryoablation should achieve an iceball diameter that exceeds the tumor diameter "
            "by at least 1 cm. A typical protocol involves 2 cycles of a 10-min freeze followed by a 10-min thaw."
        ),
        "Radiofrequency Ablation": (
            "For renal RFA, the active tip should cover the tumor’s longest dimension plus at least a 1 cm margin. "
            "Probe selection is based on the tumor size and location."
        ),
        "Microwave Ablation": (
            "Renal microwave ablation is typically performed with power settings between 60-100W. A 1 cm margin "
            "beyond the tumor boundary is recommended."
        ),
        "IRE": (
            "IRE protocols in renal tumors recommend electrode spacing of 1.5-2 cm with 90 pulses at 1500-3000 V. "
            "This nonthermal technique is especially useful near critical structures."
        )
    },
    "Liver": {
        "Cryoablation": (
            "In liver cryoablation, a minimum ablation margin of 1 cm is advised. A typical protocol may include a "
            "10-min freeze cycle, ensuring complete coverage of the tumor with a safety margin."
        ),
        "Radiofrequency Ablation": (
            "Liver RFA protocols often favor cluster needles for tumors larger than 3 cm, aiming for an ablation zone that "
            "extends 1-1.5 cm beyond the tumor margins. For lesions ≤3 cm, a single needle may be sufficient, but for masses >3 cm, "
            "a multi-probe or cluster configuration is recommended to ensure complete ablation."
        ),
        "Microwave Ablation": (
            "For liver tumors, microwave ablation is performed with power between 60-100W, with a targeted ablation "
            "margin of 1-1.5 cm. For tumors ≤3 cm, a single probe may suffice; however, for lesions larger than 3 cm, consider using multiple "
            "microwave probes to achieve full coverage."
        ),
        "IRE": (
            "IRE for liver tumors (using systems like NanoKnife) typically involves 90 pulses with electrode spacing "
            "of 1.5-2 cm and voltages ranging from 1500-3000 V. This is particularly beneficial for tumors near large vessels."
        )
    },
    "Lung": {
        "Cryoablation": (
            "Lung cryoablation employs slower freeze cycles to protect surrounding lung parenchyma, with a recommended "
            "margin of 0.5-1 cm."
        ),
        "Radiofrequency Ablation": (
            "Due to the aerated nature of lung tissue, RFA for lung tumors typically uses shorter active tip lengths "
            "with margins of 0.5-1 cm."
        ),
        "Microwave Ablation": (
            "Lung microwave ablation uses power settings between 60-100W, with an ablation margin goal of 0.5-1 cm."
        ),
        "IRE": (
            "IRE is an emerging modality for lung tumors. Recommended protocols advise careful electrode placement "
            "with 1.5-2 cm spacing and 90 pulses, optimizing ablation while preserving surrounding lung tissue."
        )
    },
    "Bone": {
        "Radiofrequency Ablation": (
            "For bone lesions, RFA requires electrodes designed to accommodate cortical bone. An ablation margin of ~1 cm "
            "is typically targeted."
        ),
        "Cryoablation": (
            "Bone cryoablation uses cryoprobes that generate an elliptical iceball, ensuring at least a 1 cm safety margin."
        ),
        "Laser Ablation": (
            "Laser ablation in bone is less common but is performed with lower power settings to maintain control over the ablation zone."
        )
    },
    "Thyroid": {
        "Radiofrequency Ablation": (
            "Thyroid RFA protocols recommend electrodes with active tips between 0.5-1 cm. The goal is to minimize damage "
            "to adjacent structures while ensuring complete ablation of the nodule."
        ),
        "Laser Ablation": (
            "For thyroid nodules, laser ablation is typically performed at around 3W for 5-10 minutes, tailored to the nodule's size."
        )
    }
}

def suggest_probes(body_system, ablation_type, tumor_length, tumor_width, tumor_height, margin_required):
    """
    Suggest optimal ablation probes based on tumor size and required margin.
    For IRE (irreversible electroporation), the recommendation is based on electrode spacing.
    For liver RFA and MW, if the effective ablation diameter (tumor plus margin) is >3 cm, a multiple-probe approach is suggested.
    """
    probes = ablation_data.get(body_system, {}).get(ablation_type, [])
    # Calculate the required ablation diameter (tumor plus safety margins on both sides)
    d_ablation = max(tumor_length, tumor_width, tumor_height) + 2 * margin_required

    # Special handling for IRE
    if ablation_type == "IRE":
        if d_ablation <= 2:
            return [f"NanoKnife (2 electrodes)"]
        elif d_ablation <= 4:
            return [f"NanoKnife (4 electrodes)"]
        else:
            return [f"NanoKnife (6 electrodes)"]

    # For Liver RFA and MW, check if the tumor is large (>3 cm effective diameter)
    if body_system == "Liver" and ablation_type in ["Radiofrequency Ablation", "Microwave Ablation"]:
        if d_ablation > 3:
            # For RFA, try to return the cluster needle if available
            for probe in probes:
                if "Cluster" in probe["name"]:
                    return [f"{probe['name']} (Multiple Probes)"]
            # For MW or if no cluster needle is available, assume a multiple probe approach.
            return [f"{probes[0]['name']} (Multiple Probes)"]

    # For other cases or if d_ablation is small, use available probe parameters
    for probe in probes:
        if ablation_type == "Cryoablation" and "iceball" in probe:
            iceball_max = probe["iceball"][1]
            if iceball_max >= d_ablation:
                return [f"{probe['name']} (1 probe)"]
        elif ablation_type in ["Radiofrequency Ablation", "Microwave Ablation", "Laser Ablation"]:
            if "active_tip" in probe:
                try:
                    # Extract the first number from the active tip string (handles cases like "2-3 cm")
                    active_tip_length = float(probe["active_tip"].split()[0].split("-")[0])
                    if active_tip_length >= d_ablation:
                        return [f"{probe['name']} (1 probe)"]
                except Exception:
                    continue

    # If no single probe is sufficient, for Cryoablation suggest using multiple probes.
    for probe in probes:
        if ablation_type == "Cryoablation" and "iceball" in probe:
            iceball_max = probe["iceball"][1]
            return [f"{probe['name']} (2 probes)"] if d_ablation > iceball_max else [f"{probe['name']} (1 probe)"]

    return ["No suitable probe found"]

def main():
    st.set_page_config(page_title="Ablation Probe Calculator", layout="centered")
    
    st.title("Ablation Probe Calculator")
    st.markdown("Select the clinical parameters to receive an optimal ablation probe recommendation and review research-based protocols.")
    
    # Sidebar for user input
    st.sidebar.header("Input Parameters")
    
    condition_type = st.sidebar.selectbox("Condition Type", ["Benign", "Malignant"])
    body_system = st.sidebar.selectbox("Body System", list(ablation_data.keys()))
    ablation_type = st.sidebar.selectbox("Ablation Type", list(ablation_data[body_system].keys()))
    
    st.sidebar.header("Tumor Dimensions (cm)")
    tumor_length = st.sidebar.number_input("Tumor Length", min_value=0.1, step=0.1, format="%.1f")
    tumor_width  = st.sidebar.number_input("Tumor Width", min_value=0.1, step=0.1, format="%.1f")
    tumor_height = st.sidebar.number_input("Tumor Height", min_value=0.1, step=0.1, format="%.1f")
    
    # Define margin based on tumor size
    margin_required = 1.0 if max(tumor_length, tumor_width, tumor_height) > 4 else 0.5
    st.sidebar.write(f"**Required Ablation Margin:** {margin_required} cm")
    
    if st.sidebar.button("Calculate Probes"):
        suggested_probes = suggest_probes(body_system, ablation_type, tumor_length, tumor_width, tumor_height, margin_required)
        if suggested_probes:
            st.success(f"Recommended Probe(s): {', '.join(suggested_probes)}")
        else:
            st.warning("No suitable probe found for the given parameters.")
    
    st.markdown("---")
    st.subheader(f"{body_system} - {ablation_type} Probe Information")
    probe_info = ablation_data[body_system].get(ablation_type, [])
    if probe_info:
        probe_df = pd.DataFrame(probe_info)
        st.table(probe_df)
    else:
        st.write("No probe details available for this selection.")
    
    st.markdown("---")
    st.subheader("Research-Based Ablation Protocol Recommendations")
    protocol_text = ablation_protocols.get(body_system, {}).get(ablation_type, "No protocol information available.")
    st.info(protocol_text)
    
    st.markdown("---")
    st.markdown("Developed for efficient ablation planning based on current research.")
    
if __name__ == "__main__":
    main()
