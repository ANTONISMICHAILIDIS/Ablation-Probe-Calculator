import streamlit as st
import pandas as pd

# ===========================================
# 1. Data: Probe Characteristics for Tumor Ablation
# ===========================================
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
    },
    "Breast": {
        "Radiofrequency Ablation": [
            {"name": "Cool-tip™", "size": "17-gauge", "active_tip": "1.5-2 cm"}
        ],
        "Microwave Ablation": [
            {"name": "Emprint™", "size": "Water-cooled", "power": "30-40W", "active_tip": "Variable"}
        ],
        "Cryoablation": [
            {"name": "Visual-ICE™", "iceball": (2.5, 4), "shape": "Elliptical"}
        ]
    },
    "Soft Tissue": {
        "Radiofrequency Ablation": [
            {"name": "Cool-tip™", "size": "18-gauge", "active_tip": "1-1.5 cm"}
        ],
        "Cryoablation": [
            {"name": "CryoCare®", "iceball": (2.5, 3.5), "shape": "Elliptical"}
        ]
    },
    "GYN": {
        "Radiofrequency Ablation": [
            {"name": "STARmed RFA", "size": "18-gauge", "active_tip": "Variable"}
        ],
        "Cryoablation": [
            {"name": "Visual-ICE™", "iceball": (2.5, 4), "shape": "Elliptical"}
        ]
    }
}

# ===========================================
# 2. Data: Detailed Protocols for Tumor Ablation
# ===========================================
protocol_details = {
    "Liver": {
        "Microwave Ablation": {
            "Primary Malignancy": (
                "MWA Protocol for Hepatic Malignancies:\n\n"
                "• For tumors up to 2 cm, use 40W for 5 minutes to achieve an ablation zone of ~3.6×2.9×2.0 cm, ensuring a ≥1 cm margin.\n"
                "• For larger lesions, overlapping ablations or multiple probes may be required.\n"
                "• Guidance: CT/ultrasound; post-ablation imaging confirms complete coverage."
            ),
            "Metastasis": (
                "For liver metastases, similar MWA protocols are applied with emphasis on achieving uniform ablation zones, often with a 1 cm margin."
            ),
            "Benign Lesion": (
                "For benign hepatic lesions, a more conservative MWA protocol is used with a minimal margin (0.5-1 cm) to preserve liver tissue."
            )
        },
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "RFA Protocol for Hepatic Malignancies:\n\n"
                "• Use cluster needles (e.g., RITA Starburst®) for tumors >3 cm to achieve a 1-1.5 cm safety margin.\n"
                "• For tumors ≤3 cm, a single probe (e.g., Cool-tip™) may suffice.\n"
                "• Guidance: Real-time CT/ultrasound with impedance monitoring."
            ),
            "Metastasis": (
                "For liver metastases, RFA is tailored to ensure complete coverage, often using overlapping ablations with a 1 cm margin."
            ),
            "Benign Lesion": (
                "For benign lesions, a narrow ablation zone (0.5-1 cm margin) is typically sufficient."
            )
        },
        "Cryoablation": {
            "Primary Malignancy": (
                "Cryoablation Protocol for Hepatic Malignancies:\n\n"
                "• Two freeze-thaw cycles: First freeze for 10 minutes at <-40°C with an 8-minute active thaw, followed by a second 10-minute freeze and a 3-minute thaw.\n"
                "• The ice ball must extend at least 10 mm beyond the tumor margin.\n"
                "• Guidance: CT/MRI monitoring of ice ball formation."
            ),
            "Metastasis": (
                "For metastatic liver lesions, cryoablation follows similar cycles with careful monitoring to ensure complete coverage."
            ),
            "Benign Lesion": (
                "For benign hepatic lesions, cryoablation may be performed with reduced cycles and a target margin of 0.5-1 cm."
            )
        },
        "IRE": {
            "Primary Malignancy": (
                "IRE Protocol for Liver Tumors:\n\n"
                "• Deliver 90 pulses with electrode spacing of 1.5-2 cm at 1500-3000 V.\n"
                "• Especially useful for lesions near large vessels to avoid thermal injury."
            )
        }
    },
    "Lung": {
        "Microwave Ablation": {
            "Primary Malignancy": (
                "MWA for Lung Tumors:\n\n"
                "• 30-60W for 3-5 minutes to create an ablation zone with a ~1 cm margin.\n"
                "• Guidance: CT with respiratory gating."
            )
        },
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "RFA for Lung Tumors:\n\n"
                "• 50-100W delivered over 10-20 minutes to achieve a 1 cm safety margin.\n"
                "• Guidance: CT with real-time monitoring."
            )
        },
        "Cryoablation": {
            "Primary Malignancy": (
                "Cryoablation for Lung Lesions:\n\n"
                "• Two 10-minute freeze cycles with ~8-minute thaw periods, ensuring the ice ball covers the lesion by ≥1 cm.\n"
                "• Guidance: CT; monitor for pneumothorax."
            )
        },
        "IRE": {
            "Primary Malignancy": (
                "IRE for Lung Tumors uses similar parameters as in the liver, with careful electrode placement."
            )
        }
    },
    "Renal": {
        "Cryoablation": {
            "Primary Malignancy": (
                "Renal Cryoablation Protocol:\n\n"
                "• Devices: Visual-ICE® or CryoCare Touch®.\n"
                "• Needles: e.g., IceRod® 1.2 mm Plus, IceSphere® 1.2 mm (17 gauge) or 16 gauge for CryoCare Touch®.\n"
                "• Two freeze-thaw cycles: First freeze for 10 minutes at <-40°C with an 8-minute thaw, then a second 10-minute freeze with a 3-minute thaw.\n"
                "• The ice ball must extend at least 10 mm beyond the tumor margin; CT monitoring and hydrodissection are used as needed."
            ),
            "Metastasis": (
                "For renal metastases, similar cryoablation protocols are applied with strict monitoring to protect renal parenchyma."
            ),
            "Benign Lesion": (
                "For benign renal lesions (e.g., angiomyolipoma), protocols are adjusted with a target margin of 0.5-1 cm."
            )
        },
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "RFA for Renal Tumors:\n\n"
                "• 50-100W for 12-20 minutes, aiming for a 1 cm margin while preserving normal tissue.\n"
                "• Guidance: CT/ultrasound with temperature monitoring."
            )
        }
    },
    "Bone": {
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "Combined Treatment for Spinal Bone Lesions:\n\n"
                "• Step 1: Bipolar RFA using an articulated probe (lumbar: vertebral neck approach; thoracic: lateral paravertebral).\n"
                "• Step 2: Vertebroplasty to stabilize the vertebrae.\n"
                "• Step 3: Follow-up targeted radiotherapy.\n"
                "• Guidance: CT/fluoroscopy with local anesthesia."
            ),
            "Benign Lesion": (
                "For benign bone lesions (e.g., osteoid osteoma), RFA is performed with precise targeting and minimal margins (2–3 mm)."
            )
        },
        "Cryoablation": {
            "Primary Malignancy": (
                "Bone Cryoablation:\n\n"
                "• Two freeze-thaw cycles to create an ice ball extending at least 1 cm beyond the lesion.\n"
                "• Guidance: CT to avoid injury to adjacent neurovascular structures."
            )
        }
    },
    "Thyroid": {
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "Thyroid RFA for Malignancies:\n\n"
                "• Specialized electrodes (e.g., STARmed) with a 0.5–1 cm active tip are used.\n"
                "• Energy titrated under ultrasound guidance to achieve complete ablation while protecting adjacent structures."
            ),
            "Benign Lesion": (
                "For benign thyroid nodules, ablation is confined to the nodule with a minimal margin (<0.5 cm)."
            )
        },
        "Laser Ablation": {
            "Primary Malignancy": (
                "Thyroid Laser Ablation:\n\n"
                "• Multiple thin laser fibers (e.g., EchoLaser) may be used; energy is delivered until the ablation zone becomes hypoechoic, ensuring a 0.5–1 cm margin."
            ),
            "Benign Lesion": (
                "For benign thyroid nodules, a conservative laser ablation protocol is used with very narrow margins (<0.5 cm)."
            )
        }
    },
    "Prostate": {
        "High-Intensity Focused Ultrasound": {
            "Primary Malignancy": (
                "HIFU for Prostate Cancer:\n\n"
                "• Overlapping energy zones are delivered transrectally with target margins of 3–5 mm.\n"
                "• Guidance: Real-time ultrasound; post-treatment MRI confirms ablation."
            ),
            "Benign Lesion": (
                "For BPH, HIFU is applied to reduce gland volume with controlled energy delivery."
            )
        },
        "Cryoablation": {
            "Primary Malignancy": (
                "Prostate Cryoablation:\n\n"
                "• Two freeze-thaw cycles at temperatures below −40°C with 3–5 mm margins to maximize tumor destruction while preserving function."
            ),
            "Benign Lesion": (
                "For benign conditions, protocols are adjusted for volume reduction with minimal collateral damage."
            )
        },
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "Transurethral RFA (TUNA):\n\n"
                "• Energy is delivered via needle electrodes under transrectal ultrasound guidance to ablate the tumor while sparing adjacent tissues."
            ),
            "Benign Lesion": (
                "For benign prostatic hyperplasia, TUNA is used to reduce gland volume with minimal injury."
            )
        }
    },
    "Breast": {
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "Breast RFA Protocol:\n\n"
                "• Typically applied for small invasive carcinomas; 1.5-2 cm active tip probes are used to create an ablation zone with a 1 cm margin.\n"
                "• Guidance: Ultrasound/MRI."
            )
        },
        "Microwave Ablation": {
            "Primary Malignancy": (
                "Breast MWA Protocol:\n\n"
                "• Settings are tailored to lesion size to achieve a sufficient margin, often with a multi-probe approach for larger tumors.\n"
                "• Guidance: Ultrasound."
            )
        },
        "Cryoablation": {
            "Primary Malignancy": (
                "Breast Cryoablation Protocol:\n\n"
                "• Multiple cryoprobes are used based on tumor size and shape to cover the lesion with at least a 1 cm margin.\n"
                "• Guidance: Ultrasound with real-time ice ball monitoring."
            )
        }
    },
    "Soft Tissue": {
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "RFA for Desmoid Tumors:\n\n"
                "• Energy is delivered via a single or clustered probe (e.g., Cool-tip™) to create a controlled ablation zone with a 1 cm margin.\n"
                "• Guidance: Ultrasound/MRI."
            ),
            "Benign Lesion": (
                "For benign soft tissue tumors, RFA is used with a minimal margin to preserve surrounding function."
            )
        },
        "Cryoablation": {
            "Primary Malignancy": (
                "Cryoablation for Desmoid Tumors:\n\n"
                "• Multiple probes (often 2-4) are arranged according to tumor shape to achieve complete coverage with a 1 cm margin.\n"
                "• Guidance: Ultrasound/CT."
            )
        }
    },
    "GYN": {
        "Radiofrequency Ablation": {
            "Primary Malignancy": (
                "GYN RFA Protocol:\n\n"
                "• Applied for select cervical, endometrial, or ovarian cancers, using energy delivery to create a 1 cm margin.\n"
                "• Guidance: Ultrasound/CT."
            ),
            "Benign Lesion": (
                "For benign conditions (e.g., endometrioma, fibroids), RFA is tailored to minimize damage to normal tissue (0.5-1 cm margin)."
            )
        },
        "Cryoablation": {
            "Benign Lesion": (
                "Cryoablation for Endometrioma:\n\n"
                "• Multiple cryoprobes are used to cover the lesion with a minimal margin (<1 cm) to relieve symptoms while preserving function.\n"
                "• Guidance: Ultrasound."
            )
        }
    }
}

# ===========================================
# 3. Data: Pain Ablation Protocols
# ===========================================
pain_ablation_protocols = {
    "Stellate Ganglion Cryoneurolysis": (
        "Protocol for Stellate Ganglion Cryoneurolysis:\n\n"
        "• Patient Position: Supine with neck extended.\n"
        "• Guidance: Ultrasound-guided.\n"
        "• Technique: Under local anesthesia, position the cryoprobe adjacent to the stellate ganglion.\n"
        "• Procedure: Two freeze-thaw cycles; each freeze lasts 90 seconds at approximately -50°C, with a 30-second thaw between cycles.\n"
        "• Probes: Typically one probe per side; bilateral treatment may require two probes."
    ),
    "Splanchnic Nerve Cryoablation": (
        "Protocol for Splanchnic Nerve Cryoablation:\n\n"
        "• Patient Position: Prone or lateral decubitus.\n"
        "• Guidance: CT or fluoroscopy-guided.\n"
        "• Technique: Under local anesthesia, position the cryoprobe near the splanchnic nerves.\n"
        "• Procedure: Two freeze-thaw cycles; freeze cycle of 2 minutes at <-40°C with a 1-minute thaw period.\n"
        "• Probes: Typically one probe per side; bilateral treatment may use two probes."
    ),
    "Lumbar Medial Branch RFA": (
        "Protocol for Lumbar Medial Branch Radiofrequency Ablation:\n\n"
        "• Patient Position: Prone.\n"
        "• Guidance: Fluoroscopy or CT-guided.\n"
        "• Technique: Under local anesthesia, place RF electrodes at the medial branches of the dorsal rami.\n"
        "• Procedure: Create lesions at 80°C for 90 seconds per nerve.\n"
        "• Probes: Typically 1 per targeted nerve; 2-4 levels may be treated."
    )
}

# ===========================================
# 4. Utility Function: Recommendation Logic for Tumor Ablation
# (Now with an optional tumor shape parameter for cryoablation.)
# ===========================================
def suggest_probes_and_protocol(body_system, ablation_type, tumor_length, tumor_width, tumor_height, tumor_category, hist_grade, margin_required, tumor_shape=None):
    """
    Suggests optimal ablation probes and returns detailed protocol information based on
    tumor dimensions, category (Primary Malignancy, Metastasis, Benign Lesion), histological grade (if applicable),
    and, if applicable, tumor shape for cryoablation.
    """
    probes = ablation_data.get(body_system, {}).get(ablation_type, [])
    d_ablation = max(tumor_length, tumor_width, tumor_height) + 2 * margin_required
    recommendation = None

    # For IRE, use electrode-based recommendation.
    if ablation_type == "IRE":
        if d_ablation <= 2:
            recommendation = f"NanoKnife (2 electrodes)"
        elif d_ablation <= 4:
            recommendation = f"NanoKnife (4 electrodes)"
        else:
            recommendation = f"NanoKnife (6 electrodes)"
    # For Liver RFA/MWA, check for large lesions.
    elif body_system == "Liver" and ablation_type in ["Radiofrequency Ablation", "Microwave Ablation"]:
        if d_ablation > 3:
            for probe in probes:
                if "Cluster" in probe["name"]:
                    recommendation = f"{probe['name']} (Multiple Probes)"
                    break
            if not recommendation and probes:
                recommendation = f"{probes[0]['name']} (Multiple Probes)"
        else:
            for probe in probes:
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
        # For cryoablation, override with tumor shape mapping if provided.
        if ablation_type == "Cryoablation" and tumor_shape:
            shape_to_probe_count = {
                "Triangular": 3,
                "Rectangle": 4,
                "Diamond": 3,
                "Linear": 2,
                "Mixed": 4
            }
            probe_count = shape_to_probe_count.get(tumor_shape, 2)
            if probes:
                recommendation = f"{probes[0]['name']} ({probe_count} probes)"
        else:
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
        if not recommendation and ablation_type == "Cryoablation" and probes:
            recommendation = f"{probes[0]['name']} (2 probes)"
    
    # Retrieve protocol details text.
    # For tumor ablation, use the tumor category key.
    proto_dict = protocol_details.get(body_system, {}).get(ablation_type, {})
    proto_key = tumor_category  # ("Primary Malignancy", "Metastasis", or "Benign Lesion")
    protocol_text = proto_dict.get(proto_key, "No protocol information available.")
    
    return recommendation if recommendation else "No suitable probe found", protocol_text

# ===========================================
# 5. Main App
# ===========================================
def main():
    st.set_page_config(page_title="Ablation Probe and Protocol Calculator", layout="centered")
    
    # Title and Subheading
    st.title("Ablation Probe and Protocol Calculator")
    st.markdown("<p style='font-size:14px;'>Created by Michailidis A. for free use</p>", unsafe_allow_html=True)
    
    # Select Procedure Category: Tumor Ablation or Pain Palliation
    proc_category = st.sidebar.selectbox("Procedure Category", ["Tumor Ablation", "Pain Palliation"])
    
    if proc_category == "Tumor Ablation":
        st.markdown("### Tumor Ablation Planning")
        # Tumor category: Primary Malignancy, Metastasis, or Benign Lesion.
        tumor_category = st.sidebar.selectbox("Tumor Category", ["Primary Malignancy", "Metastasis", "Benign Lesion"])
        hist_grade = None
        if tumor_category == "Primary Malignancy":
            hist_grade = st.sidebar.selectbox("Histological Grade", ["High Grade", "Low Grade"])
        
        # Organ selection (includes Liver, Lung, Renal, Bone, Thyroid, Prostate, Breast, Soft Tissue, GYN)
        organ_options = list(ablation_data.keys())
        body_system = st.sidebar.selectbox("Organ", organ_options)
        
        # Ablation Type selection from available options for the chosen organ.
        ablation_type = st.sidebar.selectbox("Ablation Type", list(ablation_data[body_system].keys()))
        
        st.sidebar.header("Tumor Dimensions (cm)")
        tumor_length = st.sidebar.number_input("Tumor Length", min_value=0.1, step=0.1, format="%.1f")
        tumor_width  = st.sidebar.number_input("Tumor Width", min_value=0.1, step=0.1, format="%.1f")
        tumor_height = st.sidebar.number_input("Tumor Height", min_value=0.1, step=0.1, format="%.1f")
        
        # For cryoablation, let the user choose the tumor shape.
        tumor_shape = None
        if ablation_type == "Cryoablation":
            tumor_shape = st.sidebar.selectbox("Tumor Shape", ["Triangular", "Rectangle", "Diamond", "Linear", "Mixed"])
        
        # Determine required ablation margin based on tumor category and grade.
        if tumor_category == "Primary Malignancy":
            margin_required = 1.2 if hist_grade == "High Grade" else 0.7
        else:
            # For metastasis and benign lesions, use a more conservative margin.
            margin_required = 0.5
        st.sidebar.write(f"**Required Ablation Margin:** {margin_required} cm")
        
        if st.sidebar.button("Calculate Tumor Ablation Protocol"):
            recommendation, protocol_info = suggest_probes_and_protocol(
                body_system, ablation_type, tumor_length, tumor_width, tumor_height,
                tumor_category, hist_grade, margin_required, tumor_shape
            )
            st.success(f"Recommended Probe: {recommendation}")
            st.markdown("#### Detailed Tumor Ablation Protocol")
            st.info(protocol_info)
        
        st.markdown("---")
        st.subheader(f"{body_system} - {ablation_type} Probe Details")
        probe_info_list = ablation_data.get(body_system, {}).get(ablation_type, [])
        if probe_info_list:
            probe_df = pd.DataFrame(probe_info_list)
            st.table(probe_df)
        else:
            st.write("No probe details available for this selection.")
    
    else:  # Pain Palliation
        st.markdown("### Pain Palliation / Nerve Ablation Protocols")
        pain_choice = st.sidebar.selectbox("Pain Ablation Technique", list(pain_ablation_protocols.keys()))
        if st.sidebar.button("Show Pain Ablation Protocol"):
            protocol_text = pain_ablation_protocols.get(pain_choice, "No protocol information available.")
            st.success(f"Selected Pain Ablation: {pain_choice}")
            st.markdown("#### Detailed Pain Palliation Protocol")
            st.info(protocol_text)
    
    st.markdown("---")
    st.markdown("Developed for efficient ablation planning based on current research literature and clinical protocols.")

if __name__ == "__main__":
    main()
