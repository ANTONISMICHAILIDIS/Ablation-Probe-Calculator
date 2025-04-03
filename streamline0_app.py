from flask import Flask, render_template_string, request
import math

app = Flask(__name__)

# --- HTML Templates ---

form_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Renal Cryoablation Probe Calculator</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    label { display: block; margin-top: 10px; }
    input, select { width: 300px; padding: 5px; }
    .section { margin-bottom: 20px; }
  </style>
</head>
<body>
  <h1>Renal Cryoablation Probe Calculator</h1>
  <p>This tool calculates the recommended cryoablation probe configuration and predicts the resulting ice‐ball dimensions based on tumor size, RENAL score, and kidney pole location.</p>
  <form method="POST" action="/result">
    <h2>1. Tumor Characteristics</h2>
    <div class="section">
      <label for="mass_x">Mass Size X (cm):</label>
      <input type="number" step="0.1" name="mass_x" id="mass_x" required>
    </div>
    <div class="section">
      <label for="mass_y">Mass Size Y (cm):</label>
      <input type="number" step="0.1" name="mass_y" id="mass_y" required>
    </div>
    <div class="section">
      <label for="mass_z">Mass Size Z (cm):</label>
      <input type="number" step="0.1" name="mass_z" id="mass_z" required>
    </div>
    <h2>2. RENAL Nephrometry Score Parameters</h2>
    <div class="section">
      <label for="radius">Radius (max diameter):</label>
      <select name="radius" id="radius" required>
        <option value="1">≤4 cm (1 point)</option>
        <option value="2">4-7 cm (2 points)</option>
        <option value="3">≥7 cm (3 points)</option>
      </select>
    </div>
    <div class="section">
      <label for="exophytic">Exophytic Component:</label>
      <select name="exophytic" id="exophytic" required>
        <option value="1">≥50% exophytic (1 point)</option>
        <option value="2"><50% exophytic (2 points)</option>
        <option value="3">100% endophytic (3 points)</option>
      </select>
    </div>
    <div class="section">
      <label for="nearness">Nearness to Collecting System (mm):</label>
      <select name="nearness" id="nearness" required>
        <option value="1">≥7 mm (1 point)</option>
        <option value="2">4-7 mm (2 points)</option>
        <option value="3">≤4 mm (3 points)</option>
      </select>
    </div>
    <div class="section">
      <label for="pole_rel">Location Relative to Renal Poles:</label>
      <select name="pole_rel" id="pole_rel" required>
        <option value="1">Entirely above/below pole (1 point)</option>
        <option value="2">Mass crosses the polar line (2 points)</option>
        <option value="3">>50% crosses polar line/crosses midline (3 points)</option>
      </select>
    </div>
    <div class="section">
      <label for="artery">Touches Main Renal Vessels?</label>
      <select name="artery" id="artery" required>
        <option value="0">No</option>
        <option value="1">Yes (adds "h" suffix)</option>
      </select>
    </div>
    <h2>3. Additional Details</h2>
    <div class="section">
      <label for="pole">Renal Pole (for hydrodissection considerations):</label>
      <select name="pole" id="pole" required>
        <option value="upper">Upper Pole</option>
        <option value="mid">Mid Pole</option>
        <option value="lower">Lower Pole</option>
      </select>
    </div>
    <div class="section">
      <label for="cancer_type">Cancer Type (e.g., Clear Cell, Papillary):</label>
      <input type="text" name="cancer_type" id="cancer_type" required>
    </div>
    <div class="section">
      <label for="probe_type">Preferred Probe Type:</label>
      <select name="probe_type" id="probe_type" required>
        <option value="rod">Rod-Type</option>
        <option value="sphere">Sphere-Type</option>
        <option value="force">Force-Type</option>
        <option value="mixed">Mixed (e.g., 2 ROD + 1 SPHERE)</option>
      </select>
    </div>
    <div class="section">
      <button type="submit">Calculate Prediction</button>
    </div>
  </form>
</body>
</html>
"""

result_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Renal Cryoablation Prediction Result</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .result { margin-top: 20px; padding: 10px; border: 1px solid #ccc; }
  </style>
</head>
<body>
  <h1>Prediction Result</h1>
  <div class="result">
    <p><strong>Calculated RENAL Score:</strong> {{ renal_score }} {% if has_h %}(with "h"){% endif %}</p>
    <p><strong>Complexity:</strong> {{ complexity }}</p>
    <p><strong>Mass Size (cm):</strong> {{ mass_x }} × {{ mass_y }} × {{ mass_z }}</p>
    <p><strong>Renal Pole:</strong> {{ pole }}</p>
    <p><strong>Cancer Type:</strong> {{ cancer_type }}</p>
    <hr>
    <p><strong>Recommended Probe Configuration:</strong> {{ probe_configuration }}</p>
    <p><strong>Expected Ice-ball Dimensions (cm):</strong> {{ iceball_x }} × {{ iceball_y }} × {{ iceball_z }}</p>
    <p><strong>Hydrodissection:</strong> {{ hydrodissection }}</p>
    <p><strong>Expected Complications:</strong> {{ complications }}</p>
    <hr>
    <p><strong>Protocol:</strong> {{ protocol.description }}<br>
       <em>{{ protocol.technicalParameters }}</em><br>
       <strong>Total Duration:</strong> {{ protocol.duration }}</p>
  </div>
  <p><a href="/">Back to Input Form</a></p>
</body>
</html>
"""

# --- Calculation Functions ---

def calculate_renal_score(radius, exophytic, nearness, pole_rel, artery):
    # Sum up the points from the RENAL parameters
    score = int(radius) + int(exophytic) + int(nearness) + int(pole_rel)
    return score

def classify_complexity(renal_score):
    if renal_score <= 6:
        return "Low Complexity (RENAL 4-6)"
    elif 7 <= renal_score <= 9:
        return "Moderate Complexity (RENAL 7-9)"
    else:
        return "High Complexity (RENAL 10-12)"

def recommend_probe_count(max_mass):
    # Simple rule: if maximum tumor dimension <= 3 cm -> 1 probe; >3 and <= 4 -> 2 probes; >4 -> 3 probes
    if max_mass <= 3:
        return 1
    elif max_mass <= 4:
        return 2
    else:
        return 3

def predict_iceball_size(probe_type, probe_count):
    # Baseline dimensions for a single probe
    # For sphere-type probes:
    sphere_baseline = {"x": 1.2, "y": 1.8, "z": 2.0}
    # For rod-type probes:
    rod_baseline = {"x": 1.4, "y": 2.6, "z": 2.8}
    # For force-type probes:
    force_baseline = {"x": 5.0, "y": 4.0, "z": 4.8}
    
    if probe_type == "sphere":
        baseline = sphere_baseline
    elif probe_type == "rod":
        baseline = rod_baseline
    elif probe_type == "force":
        baseline = force_baseline
    elif probe_type == "mixed":
        # Assume mixed is an average of 2 rod and 1 sphere
        baseline = {
            "x": (2*rod_baseline["x"] + sphere_baseline["x"]) / 3,
            "y": (2*rod_baseline["y"] + sphere_baseline["y"]) / 3,
            "z": (2*rod_baseline["z"] + sphere_baseline["z"]) / 3
        }
    else:
        baseline = rod_baseline

    spacing = 1.0   # inter-probe spacing (cm)
    margin = 0.5    # safety margin per side (cm)
    
    # Calculate overall dimension for each axis:
    overall = {}
    for axis in ["x", "y", "z"]:
        overall[axis] = probe_count * baseline[axis] + (probe_count - 1) * spacing + 2 * margin

    # Apply configuration factor based on probe count and assumed arrangement:
    config_factors = {1: 1.0, 2: 1.0, 3: 0.9, 4: 0.85, 5: 0.8, 6: 0.75}
    factor = config_factors.get(probe_count, 1.0)
    overall = {axis: round(val * factor, 1) for axis, val in overall.items()}
    
    max_dimension = max(overall.values())
    return overall["x"], overall["y"], overall["z"], max_dimension

def get_hydrodissection_and_complications(pole):
    if pole.lower() == "upper":
        return "Not possible", "High risk: Pneumothorax"
    else:
        return "Recommended", "Standard risk"

def get_protocol(probe_type, probe_count, max_dimension):
    if probe_type == "rod":
        freeze_time = 10
    elif probe_type == "sphere":
        freeze_time = 8
    elif probe_type == "force":
        freeze_time = 12
    else:
        freeze_time = 10
    return {
        "description": f"Cryoablation using {probe_count} {probe_type.upper()} probe{'s' if probe_count>1 else ''}",
        "technicalParameters": f"Double freeze-thaw cycle: Freeze for {freeze_time} minutes, Thaw for 8 minutes, Freeze for {freeze_time} minutes, Final Thaw for 3 minutes",
        "duration": f"Approximately {2*freeze_time + 11} minutes total"
    }

def recommend_probe_configuration(mass_x, mass_y, mass_z):
    max_mass = max(mass_x, mass_y, mass_z)
    return recommend_probe_count(max_mass)

# --- Flask Routes ---

@app.route("/", methods=["GET"])
def index():
    return render_template_string(form_template)

@app.route("/result", methods=["POST"])
def result():
    # Get tumor dimensions
    mass_x = float(request.form.get("mass_x"))
    mass_y = float(request.form.get("mass_y"))
    mass_z = float(request.form.get("mass_z"))
    
    # RENAL score parameters
    radius = request.form.get("radius")
    exophytic = request.form.get("exophytic")
    nearness = request.form.get("nearness")
    pole_rel = request.form.get("pole_rel")
    artery = request.form.get("artery")
    renal_score = calculate_renal_score(radius, exophytic, nearness, pole_rel, artery)
    complexity = classify_complexity(renal_score)
    
    # Additional details
    pole = request.form.get("pole")
    cancer_type = request.form.get("cancer_type")
    probe_type = request.form.get("probe_type")  # "rod", "sphere", "force", "mixed"
    
    # Recommend probe count based on mass size
    recommended_probe_count = recommend_probe_configuration(mass_x, mass_y, mass_z)
    
    # Predict iceball size using our model
    iceball_x, iceball_y, iceball_z, max_dimension = predict_iceball_size(probe_type, recommended_probe_count)
    
    # Get hydrodissection and complications based on pole location
    hydrodissection, complications = get_hydrodissection_and_complications(pole)
    
    # Get ablation protocol details
    protocol = get_protocol(probe_type, recommended_probe_count, max_dimension)
    
    probe_configuration = f"{recommended_probe_count} {probe_type.upper()}"
    
    return render_template_string(result_template,
                                  renal_score=renal_score,
                                  has_h="Yes" if artery=="1" else "No",
                                  complexity=complexity,
                                  mass_x=mass_x,
                                  mass_y=mass_y,
                                  mass_z=mass_z,
                                  pole=pole,
                                  cancer_type=cancer_type,
                                  probe_configuration=probe_configuration,
                                  iceball_x=iceball_x,
                                  iceball_y=iceball_y,
                                  iceball_z=iceball_z,
                                  hydrodissection=hydrodissection,
                                  complications=complications,
                                  protocol=protocol)

if __name__ == "__main__":
    # Disable the reloader to avoid the "signal only works in main thread" error.
    app.run(debug=True, use_reloader=False)
