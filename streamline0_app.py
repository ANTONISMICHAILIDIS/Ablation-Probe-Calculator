import streamlit as st
import pandas as pd

# ==============================
# 1. DATA: Probe Characteristics
# ==============================
ablation_data = {
    "Liver": {
        "Microwave Ablation": [
            {"name": "Emprint™", "size": "Water-cooled", "power": "40W", "active_tip": "Variable"},
            {"name": "NeuWave™", "size": "Standard", "power": "30-60W", "active_tip": "Variable"},
            {"name": "Acculis MTA", "size": "Flexible", "power": "40-60W", "active_tip": "Variable"}
        ],
        "Radiofrequency Ablation": [
            {"name": "Cool-tip™", "size": "17-gauge", "active_tip": "2-3 cm"},
            {"name": "RITA Starburst®", "size": "Deployable array", "active_tip": "Variable"}
        ],
        "Cryoablation": [
            {"name": "Visual-ICE™", "iceball": (3.5, 5), "shape": "Elliptical"},
            {"name": "CryoCare®", "iceball": (3.5, 5), "shape": "Elliptical"}
        ],
        "IRE": [
            {"name": "NanoKnife", "electrodes": 2, "voltage": "1500-3000 V", "spacing": "1.5-2 cm", "protocol": "90 pulses"}
        ]
    },
    "Lung": {
        "Microwave Ablation": [
            {"name": "Lung Emprint™", "size": "Adapted for lung", "power": "30-60W", "active_tip": "Variable"}
        ],
        "Radiofrequency Ablation": [
            {"name": "LeVeen®", "size": "17-gauge", "active_tip": "2-3 cm"}
        ],
        "Cryoablation": [
            {"name": "CryoCare Touch™", "iceball": (3.0, 4.5), "shape": "Elliptical"}
        ],
        "IRE": [
            {"name": "NanoKnife", "electrodes": 2, "voltage": "1500-3000 V", "spacing": "1.5-2 cm", "protocol": "90 pulses"}
        ]
    },
    "Renal": {
        "Radiofrequency Ablation": [
            {"name": "Cool-tip™ RF", "size": "17-gauge", "active_tip": "2-3 cm"},
            {"name": "StarBurst®", "size": "Deployable array", "active_tip": "Variable"}
        ],
        "Microwave Ablation": [
            {"name": "Acculis MTA", "size": "Flexible", "power": "40-60W", "active_tip": "Variable"}
        ],
        "Cryoablation": [
            {"name": "Visual-ICE®", "iceball": (3.5, 5), "shape": "Elliptical"},
            {"name": "CryoCare Touch®", "iceball": (3.5, 5), "shape": "Elliptical"}
        ],
        "IRE": [
            {"name": "NanoKnife", "electrodes": 2, "voltage": "1500-3000 V", "spacing": "1.5-2 cm", "protocol": "90 pulses"}
        ]
    },
    "Bone": {
        "Radiofrequency Ablation": [
            {"name": "LeVeen®", "size": "Variable", "active_tip": "2-3 cm"},
            {"name": "STAR®", "size": "Deployable array", "active_tip": "Variable"},
            {"name": "Articulated Bipolar Probe", "size": "Specialized", "active_tip": "Controlled"}
        ],
        "Cryoablation": [
            {"name": "Visual-ICE®", "iceball": (3.0, 4), "shape": "Elliptical"}
        ]
        # Note: For Bone lesions, multimodal (e.g., combined with vertebroplasty) details are provided in protocols.
    },
    "Thyroid": {
        "Radiofrequency Ablation": [
            {"name": "STARmed Thyroid RFA", "size": "18-gauge", "active_tip": "0.5-1 cm"}
        ],
        "Laser Ablation": [
            {"name": "EchoLaser", "size": "Thin fiber", "power": "3W", "duration": "5-10 min"}
        ]
    },
    "Prostate": {
        "High-Intensity Focused Ultrasound": [
            {"name": "Ablatherm", "approach": "Transrectal", "margin": "3-5 mm"},
            {"name": "Sonablate®", "approach": "Transrectal", "margin": "3-5 mm"}
        ],
        "Cryoablation": [
            {"name": "Endocare Cryosystem", "cycle": "2 freeze-thaw cycles", "target_temp": "Below -40°C", "margin": "3-5 mm"}
        ],
        "Radiofrequency Ablation": [
            {"name": "TUNA", "approach": "Transurethral", "active_tip": "Variable"}
        ]
    }
}

# ==============================
# 2. DATA: Detailed Protocols
# ==============================
# For demonstration purposes, only a sample summary is included.
protocol_details = {
    "Liver": {
        "Microwave Ablation": {
            "Malignant": (
                "MWA Protocol for Hepatic Malignancies:\n\n"
                "• For tumors up to 2 cm, a 40W for 5-minute protocol is applied to produce an ablation zone of approximately 3.6 cm x 2.9 cm x ~2.0 cm, ensuring a ≥1 cm safety margin.\n"
                "• For larger lesions, overlapping ablations or multiple probes may be used.\n"
                "• Guidance: CT/ultrasound; post-procedure contrast-enhanced imaging confirms complete coverage."
            ),
            "Benign": (
                "For benign hepatic lesions (e.g., hemangiomas), a more conservative approach is used with a minimal margin (0.5-1 cm) to preserve liver parenchyma."
            )
        },
        "Radiofrequency Ablation": {
            "Malignant": (
                "RFA Protocol for Hepatic Malignancies:\n\n"
                "• Use cluster needles (e.g., RITA Starburst®) for tumors >3 cm to achieve a 1-1.5 cm ablation zone beyond the tumor edge.\n"
                "• For tumors ≤3 cm, a single needle (e.g., Cool-tip™) may suffice.\n"
                "• Guidance: Real-time CT/ultrasound with impedance monitoring."
            ),
            "Benign": (
                "For benign liver lesions, a single probe with a narrow ablation zone (0.5-1 cm margin) is typically sufficient."
            )
        },
        "Cryoablation": {
            "Malignant": (
                "Cryoablation Protocol for Hepatic Malignancies:\n\n"
                "• Two freeze-thaw cycles (first freeze 10 minutes at <-40°C with an 8-minute active thaw, followed by a second 10-minute freeze and a 3-minute thaw) are applied.\n"
                "• The ice ball should extend at least 10 mm beyond the tumor margin.\n"
                "• Guidance: CT or MRI to monitor ice ball formation."
            ),
            "Benign": (
                "For benign lesions, cryoablation may be performed with a reduced number of cycles and a minimal margin (0.5-1 cm) to limit damage to normal tissue."
            )
        },
        "IRE": {
            "Malignant": (
                "IRE Protocol for Liver Tumors:\n\n"
                "• Employ 90 pulses with electrode spacing of 1.5-2 cm at voltages between 1500-3000 V.\n"
                "• Particularly beneficial for lesions near large vessels where thermal injury is a concern."
            )
        }
    },
    "Lung": {
        "Microwave Ablation": {
            "Malignant": (
                "MWA for Lung Tumors:\n\n"
                "• Power: 30-60W for 3-5 minutes to achieve an ablation zone with a ~1 cm margin.\n"
                "• Guidance: CT with respiratory gating."
            )
        },
        "Radiofrequency Ablation": {
            "Malignant": (
                "RFA for Lung Tumors:\n\n"
                "• Energy delivered for 10-20 minutes at 50-100W.\n"
                "• Aiming for a 1 cm margin; CT guidance is essential."
            )
        },
        "Cryoablation": {
            "Malignant": (
                "Cryoablation for Lung Lesions:\n\n"
                "• Two freeze cycles of 10 minutes each with ~8 minutes thaw, monitoring the ice ball to ensure ≥1 cm coverage.\n"
                "• Guidance: CT; caution for pneumothorax."
            )
        },
        "IRE": {
            "Malignant": (
                "IRE for Lung Tumors follows similar parameters as for liver tumors, with careful electrode placement."
            )
        }
    },
    "Renal": {
        "Cryoablation": {
            "Malignant": (
                "Renal Cryoablation Protocol:\n\n"
                "• Devices: Visual-ICE® System (Boston Scientific) or CryoCare Touch® System (Varian Medical Systems).\n"
                "• Needles: IceRod® 1.2 mm Plus and IceSphere® 1.2 mm (17 gauge) or 16 gauge (1.7 mm) for CryoCare Touch®.\n"
                "• Process: Two cycles – first freeze for 10 minutes at <-40°C with an 8-minute active thaw; second freeze for 10 minutes with a 3-minute active thaw.\n"
                "• The ice ball must extend at least 10 mm beyond the tumor margin.\n"
                "• Temperature is continuously monitored and CT is used for verification. Hydrodissection is performed when necessary."
            ),
            "Benign": (
                "For benign renal lesions (e.g., angiomyolipoma), a similar protocol is used but with adjustments to energy and a target margin of 0.5-1 cm."
            )
        },
        "Radiofrequency Ablation": {
            "Malignant": (
                "RFA for Renal Tumors:\n\n"
                "• Typical settings: 50-100W for 12-20 minutes, aiming for a 1 cm margin.\n"
                "• Guidance: CT/ultrasound with temperature monitoring."
            )
        }
    },
    "Bone": {
        "Radiofrequency Ablation": {
            "Malignant": (
                "Combined Treatment for Spinal Bone Lesions:\n\n"
                "• Step 1: Bipolar RFA using an articulated probe (lumbar via vertebral neck approach, thoracic via lateral paravertebral).\n"
                "• Step 2: Vertebroplasty immediately after RFA to stabilize the vertebrae.\n"
                "• Step 3: Targeted radiotherapy post-procedure for additional local control.\n"
                "• Guidance: CT or fluoroscopy with local anesthesia."
            ),
            "Benign": (
                "For benign bone lesions (e.g., osteoid osteoma), RFA is performed with precise targeting of the nidus using minimal margins (2–3 mm)."
            )
        },
        "Cryoablation": {
            "Malignant": (
                "Bone Cryoablation:\n\n"
                "• Two freeze-thaw cycles are used to create an ice ball extending at least 1 cm beyond the lesion.\n"
                "• Guidance: CT to protect adjacent neurovascular structures."
            )
        }
    },
    "Thyroid": {
        "Radiofrequency Ablation": {
            "Malignant": (
                "Thyroid RFA for Malignancies:\n\n"
                "• Utilizes specialized electrodes (e.g., STARmed) with a 0.5–1 cm active tip.\n"
                "• Energy is titrated under ultrasound guidance to achieve complete ablation with a narrow margin to protect the recurrent laryngeal nerve."
            ),
            "Benign": (
                "For benign thyroid nodules, ablation is confined to the nodule with a minimal margin (<0.5 cm) to avoid injury."
            )
        },
        "Laser Ablation": {
            "Malignant": (
                "Thyroid Laser Ablation:\n\n"
                "• Thin laser fibers (e.g., EchoLaser) are inserted under ultrasound guidance; multiple fibers may be used concurrently.\n"
                "• Energy is delivered until the target zone becomes hypoechoic, indicating necrosis, with a 0.5–1 cm margin."
            ),
            "Benign": (
                "For benign nodules, laser ablation is performed with conservative energy delivery and very narrow margins (<0.5 cm)."
            )
        }
    },
    "Prostate": {
        "High-Intensity Focused Ultrasound": {
            "Malignant": (
                "HIFU for Prostate Cancer:\n\n"
                "• Systems such as Ablatherm or Sonablate® deliver overlapping energy zones transrectally to ablate the tumor with 3–5 mm margins.\n"
                "• Guidance: Real-time ultrasound imaging; post-treatment MRI to assess ablation."
            ),
            "Benign": (
                "For benign prostatic hyperplasia, HIFU is applied to reduce volume with controlled energy delivery."
            )
        },
        "Cryoablation": {
            "Malignant": (
                "Prostate Cryoablation:\n\n"
                "• Devices such as the Endocare Cryosystem are used with two freeze-thaw cycles at temperatures below −40°C.\n"
                "• A 3–5 mm margin is maintained to maximize tumor destruction while preserving function."
            ),
            "Benign": (
                "For benign conditions, cryoablation protocols are adjusted for volume reduction with minimal collateral damage."
            )
        },
        "Radiofrequency Ablation": {
            "Malignant": (
                "Transurethral RFA (TUNA):\n\n"
                "• Energy is delivered via needle electrodes placed under transrectal ultrasound guidance.\n"
                "• The procedure is tailored to ensure tumor ablation while preserving adjacent neurovascular structures."
            ),
            "Benign": (
                "For benign prostatic hyperplasia, TUNA is applied to reduce gland volume with minimal damage."
            )
        }
    }
}

# ========================================
# 3. UTILITY FUNCTION: Recommendation Logic
# ========================================
def suggest_probes_and_protocol(body_system, ablation_type, tumor_length, tumor_width, tumor_height, condition_type, tumor_grade, margin_required):
    """
    Suggests optimal ablation probes and returns detailed protocol information based on
    tumor dimensions, condition (malignant/benign), and, if malignant, tumor grade.
    """
    probes = ablation_data.get(body_system, {}).get(ablation_type, [])
    d_ablation = max(tumor_length, tumor_width, tumor_height) + 2 * margin_required

    recommendation = None

    # Special handling for IRE:
    if ablation_type == "IRE":
        if d_ablation <= 2:
            recommendation = f"NanoKnife (2 electrodes)"
        elif d_ablation <= 4:
            recommendation = f"NanoKnife (4 electrodes)"
        else:
            recommendation = f"NanoKnife (6 electrodes)"
    # For Liver RFA/MWA: use multiple probe suggestion if lesion is large
    elif body_system == "Liver" and ablation_type in ["Radiofrequency Ablation", "Microwave Ablation"]:
        if d_ablation > 3:
            # Prefer cluster or multiple probes approach
            for probe in probes:
                if "Cluster" in probe["name"]:
                    recommendation = f"{probe['name']} (Multiple Probes)"
                    break
            if not recommendation and probes:
                recommendation = f"{probes[0]['name']} (Multiple Probes)"
        else:
            # Use single probe if lesion is small
            for probe in probes:
                # For modalities with active tip (RFA) or iceball (Cryoablation)
                if ablation_type in ["Radiofrequency Ablation", "Microwave Ablation"]:
                    if "active_tip" in probe:
                        try:
                            active_tip_length = float(probe["active_tip"].split()[0].split("-")[0])
                            if active_tip_length >= d_ablation:
                                recommendation = f"{probe['name']} (1 probe)"
                                break
                        except Exception:
                            continue
                elif ablation_type == "Cryoablation" and "iceball" in probe:
                    if probe["iceball"][1] >= d_ablation:
                        recommendation = f"{probe['name']} (1 probe)"
                        break
    else:
        # General approach for other systems/modalities
        for probe in probes:
            if ablation_type == "Cryoablation" and "iceball" in probe:
                if probe["iceball"][1] >= d_ablation:
                    recommendation = f"{probe['name']} (1 probe)"
                    break
            elif ablation_type in ["Radiofrequency Ablation", "Microwave Ablation", "Laser Ablation"]:
                if "active_tip" in probe:
                    try:
                        active_tip_length = float(probe["active_tip"].split()[0].split("-")[0])
                        if active_tip_length >= d_ablation:
                            recommendation = f"{probe['name']} (1 probe)"
                            break
                    except Exception:
                        continue
        # Fallback: if no probe meets criteria, suggest multiple probes (for cryoablation)
        if not recommendation and ablation_type == "Cryoablation" and probes:
            recommendation = f"{probes[0]['name']} (2 probes)"
    
    # Retrieve the protocol details text (if available)
    # For modalities without separate malignant/benign (like IRE), we use the key as "Malignant"
    cond_key = condition_type if condition_type == "Benign" else "Malignant"
    protocol_text = protocol_details.get(body_system, {}).get(ablation_type, {}).get(cond_key, "No protocol information available.")
    
    return recommendation if recommendation else "No suitable probe found", protocol_text

# ========================================
# 4. MAIN APP
# ========================================
def main():
    st.set_page_config(page_title="Ablation Probe and Protocol Calculator", layout="centered")
    
    # Title and subheading
    st.title("Ablation Probe and Protocol Calculator")
    st.markdown("<p style='font-size:14px;'>Created by Michailidis A. for free use</p>", unsafe_allow_html=True)
    
    st.markdown("### Select the clinical parameters to get a tailored ablation probe recommendation and detailed protocol information.")
    
    # Sidebar: Input Parameters
    st.sidebar.header("Input Parameters")
    
    condition_type = st.sidebar.selectbox("Condition Type", ["Malignant", "Benign"])
    
    # If malignant, let the user choose tumor grade
    tumor_grade = None
    if condition_type == "Malignant":
        tumor_grade = st.sidebar.selectbox("Tumor Grade", ["High Grade", "Low Grade"])
    
    body_system = st.sidebar.selectbox("Body System", list(ablation_data.keys()))
    ablation_type = st.sidebar.selectbox("Ablation Type", list(ablation_data[body_system].keys()))
    
    st.sidebar.header("Tumor Dimensions (cm)")
    tumor_length = st.sidebar.number_input("Tumor Length", min_value=0.1, step=0.1, format="%.1f")
    tumor_width  = st.sidebar.number_input("Tumor Width", min_value=0.1, step=0.1, format="%.1f")
    tumor_height = st.sidebar.number_input("Tumor Height", min_value=0.1, step=0.1, format="%.1f")
    
    # Determine required ablation margin based on condition type and grade
    if condition_type == "Malignant":
        # For malignant lesions: if high grade, margin >1 cm (e.g., 1.2 cm); if low grade, margin between 0.5 and 1 cm (e.g., 0.7 cm)
        margin_required = 1.2 if tumor_grade == "High Grade" else 0.7
    else:
        # For benign lesions, minimal margin is used (e.g., 0.5 cm)
        margin_required = 0.5
    st.sidebar.write(f"**Required Ablation Margin:** {margin_required} cm")
    
    if st.sidebar.button("Calculate Probes and Protocol"):
        probe_recommendation, protocol_info = suggest_probes_and_protocol(
            body_system, ablation_type, tumor_length, tumor_width, tumor_height, condition_type, tumor_grade, margin_required
        )
        st.success(f"Recommended Probe: {probe_recommendation}")
        st.markdown("#### Detailed Protocol Information")
        st.info(protocol_info)
    
    st.markdown("---")
    st.subheader(f"{body_system} - {ablation_type} Probe Details")
    probe_info_list = ablation_data.get(body_system, {}).get(ablation_type, [])
    if probe_info_list:
        probe_df = pd.DataFrame(probe_info_list)
        st.table(probe_df)
    else:
        st.write("No probe details available for this selection.")
    
    st.markdown("---")
    st.markdown("Developed for efficient ablation planning based on current research literature and clinical protocols.")
    
if __name__ == "__main__":
    main()
