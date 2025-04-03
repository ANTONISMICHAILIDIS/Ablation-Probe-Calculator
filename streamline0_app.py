from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template for the input form
form_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Renal Cryoablation Predictor</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    label { display: block; margin-top: 10px; }
    input, select { width: 300px; padding: 5px; }
    .section { margin-bottom: 20px; }
  </style>
</head>
<body>
  <h1>Renal Cryoablation Predictor</h1>
  
  <h2>Step 1: Calculate RENAL Nephrometry Score</h2>
  <form method="POST" action="/result">
    <div class="section">
      <label for="radius">Radius (maximum diameter in cm):</label>
      <select name="radius" id="radius" required>
        <option value="1">≤4 cm (1 point)</option>
        <option value="2">4-7 cm (2 points)</option>
        <option value="3">≥7 cm (3 points)</option>
      </select>
    </div>
    
    <div class="section">
      <label for="exophytic">Exophytic Tumor Location:</label>
      <select name="exophytic" id="exophytic" required>
        <option value="1">≥50% exophytic (1 point)</option>
        <option value="2"><50% exophytic (2 points)</option>
        <option value="3">100% endophytic (3 points)</option>
      </select>
    </div>
    
    <div class="section">
      <label for="nearness">Nearness to Collecting System (in mm):</label>
      <select name="nearness" id="nearness" required>
        <option value="1">≥7 mm (1 point)</option>
        <option value="2">4-7 mm (2 points)</option>
        <option value="3">≤4 mm (3 points)</option>
      </select>
    </div>
    
    <div class="section">
      <label for="location_pole">Location Relative to Renal Poles:</label>
      <select name="location_pole" id="location_pole" required>
        <option value="1">Entirely below or above the pole (1 point)</option>
        <option value="2">Mass crosses the polar line (2 points)</option>
        <option value="3">>50% crosses the polar line, is entirely between, or crosses the midline (3 points)</option>
      </select>
    </div>
    
    <div class="section">
      <label for="artery">Does the mass touch the main renal artery or vein? (suffix "h")</label>
      <select name="artery" id="artery" required>
        <option value="0">No (0 points)</option>
        <option value="1">Yes (add "h")</option>
      </select>
    </div>
    
    <h2>Step 2: Enter Mass and Additional Data</h2>
    <div class="section">
      <label for="mass_x">Mass Size X (cm):</label>
      <input type="text" name="mass_x" id="mass_x" required>
    </div>
    <div class="section">
      <label for="mass_y">Mass Size Y (cm):</label>
      <input type="text" name="mass_y" id="mass_y" required>
    </div>
    <div class="section">
      <label for="mass_z">Mass Size Z (cm):</label>
      <input type="text" name="mass_z" id="mass_z" required>
    </div>
    <div class="section">
      <label for="pole">Renal Pole Location:</label>
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
      <label for="probe_config">Preferred Cryoablation Probe Configuration:</label>
      <select name="probe_config" id="probe_config" required>
        <option value="rod">Rod-Type</option>
        <option value="sphere">Sphere-Type</option>
        <option value="force">Force (hybrid)</option>
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

# HTML template for the result page
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
    <p><strong>Calculated RENAL Score:</strong> {{ renal_score }} {% if has_h %} (with "h") {% endif %}</p>
    <p><strong>Complexity:</strong> {{ complexity }}</p>
    <p><strong>Mass Size (cm):</strong> {{ mass_x }} x {{ mass_y }} x {{ mass_z }}</p>
    <p><strong>Renal Pole Location:</strong> {{ pole }}</p>
    <p><strong>Cancer Type:</strong> {{ cancer_type }}</p>
    <hr>
    <p><strong>Recommended Probe Configuration:</strong> {{ probe_configuration }}</p>
    <p><strong>Expected Ice-ball Size (cm):</strong> {{ iceball_x }} x {{ iceball_y }} x {{ iceball_z }}</p>
    <p><strong>Hydrodissection:</strong> {{ hydrodissection }}</p>
    <p><strong>Expected Complications:</strong> {{ complications }}</p>
  </div>
  <p><a href="/">Back to Input Form</a></p>
</body>
</html>
"""

# Function to calculate the RENAL score from input values
def calculate_renal_score(radius, exophytic, nearness, pole_location, artery):
    # radius: 1, 2, or 3 points
    # exophytic: 1, 2, or 3 points
    # nearness: 1, 2, or 3 points
    # pole location: 1, 2, or 3 points
    # artery: 0 or 1 (if touches, we add an "h" flag, but not counted in score)
    score = int(radius) + int(exophytic) + int(nearness) + int(pole_location)
    return score

# Function to classify complexity based on RENAL score
def classify_complexity(renal_score):
    if renal_score <= 6:
        return "Low Complexity (RENAL 4-6)"
    elif 7 <= renal_score <= 9:
        return "Moderate Complexity (RENAL 7-9)"
    else:
        return "High Complexity (RENAL 10-12)"

# Function to predict cryoablation parameters for renal masses
def predict_parameters(mass_x, mass_y, mass_z, renal_score, pole, cancer_type, probe_config):
    # For simplicity, we use a basic rule-based approach to choose probe configuration and estimate ice-ball size.
    # Note: In a real application, these rules would be based on extensive data and validated models.
    
    # Example rules:
    # For sphere-type: assume each sphere produces a 4.0 cm ice-ball diameter.
    # For rod-type: assume each rod produces an elliptical ice-ball with baseline 1.4 x 2.6 x 2.8 cm (for single probe).
    # For mixed (2 ROD + 1 SPHERE), we assume a combination result.
    # Also, if the pole is "upper", we note that hydrodissection is less feasible and complication risk (e.g., pneumothorax) is higher.
    
    # For demonstration, we define:
    if probe_config == "sphere":
        # Single sphere values scaled by number of probes (assuming linear arrangement for 1-2, triangular for 3, etc.)
        # We'll use a simple mapping: for 1 probe, use the baseline; for 2 probes, add 1.0 cm to each dimension; for 3 probes, add 2.0 cm, etc.
        # Here, we assume the number of probes required is determined by renal score: lower score gets fewer probes.
        if renal_score <= 6:
            n = 1
        elif 7 <= renal_score <= 9:
            n = 2
        else:
            n = 3
        
        base_diam = 4.0  # cm (spherical diameter)
        spacing = 1.0  # cm
        margin = 0.75  # cm per side
        
        # For a linear arrangement: Overall Diameter = (n-1)*spacing + n*base_diam + 2*margin.
        overall_diam = (n - 1) * spacing + n * base_diam + 2 * margin
        
        probe_configuration = f"{n} SPHERE"
        iceball_x = iceball_y = iceball_z = round(overall_diam, 1)
    
    elif probe_config == "rod":
        # For rod-type, assume baseline dimensions (for 1 probe): 1.4 x 2.6 x 2.8 cm.
        # We'll decide n based on renal score as above.
        if renal_score <= 6:
            n = 1
        elif 7 <= renal_score <= 9:
            n = 2
        else:
            n = 3
        
        # For linear arrangement along the largest dimension:
        base_x, base_y, base_z = 1.4, 2.6, 2.8  # cm for 1 probe
        spacing = 1.0
        margin = 0.75
        
        # For each axis, predicted dimension = (n-1)*spacing + n*(base dimension) + 2*margin.
        iceball_x = round((n - 1) * spacing + n * base_x + 2 * margin, 1)
        iceball_y = round((n - 1) * spacing + n * base_y + 2 * margin, 1)
        iceball_z = round((n - 1) * spacing + n * base_z + 2 * margin, 1)
        probe_configuration = f"{n} ROD"
    
    elif probe_config == "force":
        # Force probes assumed to have larger ablation effect; use baseline 5.0 x 4.0 x 4.8 cm for 1 probe.
        if renal_score <= 6:
            n = 1
        elif 7 <= renal_score <= 9:
            n = 2
        else:
            n = 3
        
        base_x, base_y, base_z = 5.0, 4.0, 4.8
        spacing = 1.0
        margin = 0.75
        iceball_x = round((n - 1) * spacing + n * base_x + 2 * margin, 1)
        iceball_y = round((n - 1) * spacing + n * base_y + 2 * margin, 1)
        iceball_z = round((n - 1) * spacing + n * base_z + 2 * margin, 1)
        probe_configuration = f"{n} FORCE"
    
    elif probe_config == "mixed":
        # For a mixed configuration such as "2 ROD + 1 SPHERE" (total 3 probes),
        # we can average the dimensions from the rod and sphere predictions.
        n = 3
        # Assume 2 rod probes and 1 sphere probe.
        # Use previous baseline for rod and sphere:
        rod_dims = [1.4, 2.6, 2.8]  # for rod (per probe)
        sphere_diam = 4.0
        # Calculate average per axis as weighted average:
        # For simplicity, we average the sphere value with the rod value for the two rod probes.
        avg_x = (2 * rod_dims[0] + sphere_diam) / 3
        avg_y = (2 * rod_dims[1] + sphere_diam) / 3
        avg_z = (2 * rod_dims[2] + sphere_diam) / 3
        spacing = 1.0
        margin = 0.75
        iceball_x = round((n - 1) * spacing + n * avg_x + 2 * margin, 1)
        iceball_y = round((n - 1) * spacing + n * avg_y + 2 * margin, 1)
        iceball_z = round((n - 1) * spacing + n * avg_z + 2 * margin, 1)
        probe_configuration = "2 ROD + 1 SPHERE"
    
    # Based on pole location: if "upper", assume no hydrodissection possible and higher risk of pneumothorax.
    if pole.lower() == "upper":
        hydrodissection = "Not possible"
        complications = "Pneumothorax risk"
    else:
        hydrodissection = "Recommended"
        complications = "Standard risk"
    
    # For demonstration, let’s adjust the prediction if the cancer type is "clear cell"
    if cancer_type.lower() == "clear cell":
        # For example, assume clear cell histology slightly increases the ablation zone need by 10%
        iceball_x = round(iceball_x * 1.1, 1)
        iceball_y = round(iceball_y * 1.1, 1)
        iceball_z = round(iceball_z * 1.1, 1)
    
    return probe_configuration, iceball_x, iceball_y, iceball_z, hydrodissection, complications

@app.route("/", methods=["GET"])
def index():
    return render_template_string(form_template)

@app.route("/result", methods=["POST"])
def result():
    # Get RENAL inputs and calculate score
    radius = request.form.get("radius")
    exophytic = request.form.get("exophytic")
    nearness = request.form.get("nearness")
    location_pole = request.form.get("location_pole")
    artery = request.form.get("artery")
    renal_score = calculate_renal_score(radius, exophytic, nearness, location_pole, artery)
    complexity = classify_complexity(renal_score)
    
    # Get mass size and other details
    mass_x = float(request.form.get("mass_x"))
    mass_y = float(request.form.get("mass_y"))
    mass_z = float(request.form.get("mass_z"))
    pole = request.form.get("pole")
    cancer_type = request.form.get("cancer_type")
    probe_config = request.form.get("probe_config")
    
    # Get predicted parameters
    probe_configuration, iceball_x, iceball_y, iceball_z, hydrodissection, complications = predict_parameters(
        mass_x, mass_y, mass_z, renal_score, pole, cancer_type, probe_config
    )
    
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
                                  complications=complications)

if __name__ == "__main__":
    app.run(debug=True)
