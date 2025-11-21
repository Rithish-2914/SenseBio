import os
import random
import math
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
CORS(app)

manual_cortisol_value = None

class CortisolSensor:
    def __init__(self):
        self.calibration_factor = 1.0
        self.amplification_gain = 1000
        self.calibration_offset = 0.0
        self.last_variation = 0
        
    def get_circadian_cortisol(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        time_decimal = hour + (minute / 60.0)
        
        circadian_phase = (time_decimal - 7.0) / 24.0 * 2 * math.pi
        
        base_level = 10.0
        amplitude = 8.0
        circadian_value = base_level + amplitude * math.cos(circadian_phase)
        
        small_variation = random.uniform(-0.2, 0.2)
        self.last_variation = self.last_variation * 0.85 + small_variation * 0.15
        
        return max(2.0, circadian_value + self.last_variation)
    
    def simulate_isf_to_current(self, cortisol_ng_ml):
        conversion_factor = 0.0275
        raw_current_ua = cortisol_ng_ml * conversion_factor
        return raw_current_ua
    
    def amplify_signal(self, raw_current_ua):
        amplified_signal = raw_current_ua * self.amplification_gain
        return amplified_signal
    
    def add_sensor_noise(self, signal):
        noise_percent = random.uniform(-0.015, 0.015)
        noisy_signal = signal * (1 + noise_percent)
        return noisy_signal
    
    def calibrate_to_cortisol(self, noisy_signal):
        raw_cortisol = (noisy_signal / self.amplification_gain) / (0.0275)
        calibrated_cortisol = (raw_cortisol * self.calibration_factor) + self.calibration_offset
        return calibrated_cortisol
    
    def get_reading(self):
        target_cortisol = self.get_circadian_cortisol()
        
        raw_current = self.simulate_isf_to_current(target_cortisol)
        amplified = self.amplify_signal(raw_current)
        noisy = self.add_sensor_noise(amplified)
        final_cortisol = self.calibrate_to_cortisol(noisy)
        
        return round(final_cortisol, 2)

sensor = CortisolSensor()

@app.route('/')
def index():
    return render_template('index.html')

def get_diet_recommendations(cortisol_level):
    recommendations = {
        "status": "",
        "diet_advice": [],
        "foods_to_eat": [],
        "foods_to_avoid": [],
        "lifestyle_tips": []
    }
    
    if cortisol_level < 5:
        recommendations["status"] = "Low Cortisol - Adrenal Fatigue Risk"
        recommendations["diet_advice"] = [
            "Increase sodium intake moderately to support adrenal function",
            "Eat small, frequent meals every 3-4 hours to stabilize blood sugar",
            "Focus on nutrient-dense whole foods with adequate calories",
            "Include vitamin C-rich foods (supports adrenal health)"
        ]
        recommendations["foods_to_eat"] = [
            "Sea salt, olives, and naturally salty foods",
            "Sweet potatoes, quinoa, and complex carbs",
            "Citrus fruits (oranges, grapefruits) for vitamin C",
            "Grass-fed beef, organic eggs for B vitamins",
            "Avocados and coconut oil for healthy fats",
            "Licorice root tea (consult healthcare provider)"
        ]
        recommendations["foods_to_avoid"] = [
            "Excessive caffeine (worsens adrenal fatigue)",
            "Refined sugars causing blood sugar crashes",
            "Alcohol (depletes cortisol further)",
            "Processed foods lacking nutrients"
        ]
        recommendations["lifestyle_tips"] = [
            "Prioritize 8-10 hours of sleep for adrenal recovery",
            "Avoid high-intensity exercise; opt for gentle yoga or walking",
            "Practice stress management (meditation, deep breathing)",
            "Consider adaptogenic herbs: Ashwagandha, Rhodiola (consult doctor)",
            "Monitor for signs of Addison's disease if persistent"
        ]
    elif 5 <= cortisol_level <= 18:
        recommendations["status"] = "Optimal Cortisol Range"
        recommendations["diet_advice"] = [
            "Maintain balanced macronutrients (40% carbs, 30% protein, 30% fat)",
            "Continue anti-inflammatory Mediterranean-style diet",
            "Stay hydrated: 8-10 glasses of water daily",
            "Support hormonal balance with nutrient-rich foods"
        ]
        recommendations["foods_to_eat"] = [
            "Leafy greens (spinach, kale) for magnesium",
            "Wild-caught fatty fish (salmon, mackerel) for omega-3s",
            "Nuts, seeds (walnuts, flaxseeds) for healthy fats",
            "Berries and citrus fruits for antioxidants",
            "Whole grains (oats, quinoa) for sustained energy",
            "Probiotic-rich foods (yogurt, kefir) for gut health"
        ]
        recommendations["foods_to_avoid"] = [
            "Excessive processed foods and preservatives",
            "High-sugar snacks causing insulin spikes",
            "Trans fats and hydrogenated oils",
            "Limit caffeine to 1-2 cups coffee per day"
        ]
        recommendations["lifestyle_tips"] = [
            "Maintain consistent sleep schedule (7-9 hours)",
            "Regular moderate exercise (30-45 mins, 5x/week)",
            "Practice mindfulness or meditation daily",
            "Stay socially connected for emotional well-being",
            "Continue monitoring hormone levels for early detection"
        ]
    else:
        recommendations["status"] = "Elevated Cortisol - Chronic Stress Indicator"
        recommendations["diet_advice"] = [
            "Eliminate caffeine completely (worsens cortisol elevation)",
            "Focus on anti-inflammatory, cortisol-lowering foods",
            "Increase omega-3 fatty acids to reduce inflammation",
            "Consider magnesium-rich foods for stress reduction",
            "Avoid intermittent fasting (may elevate cortisol further)"
        ]
        recommendations["foods_to_eat"] = [
            "Dark chocolate 85%+ cocoa (lowers cortisol naturally)",
            "Green tea (L-theanine promotes calm without stimulation)",
            "Wild salmon, sardines, walnuts (omega-3s)",
            "Blueberries, blackberries (antioxidants)",
            "Chamomile, holy basil tea (adaptogenic herbs)",
            "Phosphatidylserine-rich foods (soybeans, white beans)"
        ]
        recommendations["foods_to_avoid"] = [
            "All caffeinated beverages (coffee, energy drinks, black tea)",
            "Refined sugars and high-glycemic carbs",
            "Alcohol (disrupts HPA axis regulation)",
            "Processed foods with additives",
            "Trans fats and fried foods"
        ]
        recommendations["lifestyle_tips"] = [
            "Prioritize 8+ hours quality sleep in dark, cool room",
            "Practice deep breathing: 4-7-8 technique or box breathing",
            "Engage in restorative yoga, tai chi, or gentle stretching",
            "Limit screen time 2 hours before bed",
            "Consider cortisol-lowering supplements: Ashwagandha, Rhodiola (medical supervision)",
            "Screen for Cushing's syndrome if cortisol remains elevated",
            "Monitor for metabolic syndrome and PCOS indicators"
        ]
    
    return recommendations

@app.route('/api/cortisol')
def get_cortisol():
    global manual_cortisol_value
    
    if manual_cortisol_value is not None:
        cortisol_value = manual_cortisol_value
    else:
        cortisol_value = sensor.get_reading()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({
        "cortisol": cortisol_value,
        "unit": "ng/mL",
        "timestamp": timestamp
    })

@app.route('/api/input-cortisol', methods=['POST'])
def input_cortisol():
    global manual_cortisol_value
    
    try:
        data = request.get_json()
        if not data or 'cortisol' not in data:
            return jsonify({"error": "Missing cortisol value in request"}), 400
        
        cortisol_value = float(data.get('cortisol', 0))
        
        if cortisol_value < 0 or cortisol_value > 50:
            return jsonify({"error": "Invalid cortisol value. Please enter a value between 0 and 50 ng/mL"}), 400
        
        manual_cortisol_value = round(cortisol_value, 2)
        recommendations = get_diet_recommendations(manual_cortisol_value)
        
        return jsonify({
            "success": True,
            "cortisol": manual_cortisol_value,
            "unit": "ng/mL",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": recommendations
        })
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data format. Please provide a valid number."}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

@app.route('/api/reset-mode', methods=['POST'])
def reset_mode():
    global manual_cortisol_value
    manual_cortisol_value = None
    
    return jsonify({"success": True, "message": "Switched to automatic simulation mode"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
