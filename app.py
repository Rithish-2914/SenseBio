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
        recommendations["status"] = "Low Cortisol"
        recommendations["diet_advice"] = [
            "Increase salt intake moderately",
            "Eat regular meals to maintain blood sugar",
            "Focus on whole grains and complex carbohydrates"
        ]
        recommendations["foods_to_eat"] = [
            "Olives and pickles",
            "Sweet potatoes",
            "Brown rice",
            "Bananas",
            "Coconut",
            "Lean proteins (chicken, fish)"
        ]
        recommendations["foods_to_avoid"] = [
            "Excessive caffeine",
            "Processed sugars",
            "Alcohol"
        ]
        recommendations["lifestyle_tips"] = [
            "Get 7-9 hours of sleep",
            "Practice stress-reduction techniques",
            "Avoid intense exercise temporarily"
        ]
    elif 5 <= cortisol_level <= 18:
        recommendations["status"] = "Normal Cortisol"
        recommendations["diet_advice"] = [
            "Maintain balanced nutrition",
            "Continue healthy eating patterns",
            "Stay hydrated throughout the day"
        ]
        recommendations["foods_to_eat"] = [
            "Leafy greens (spinach, kale)",
            "Fatty fish (salmon, mackerel)",
            "Nuts and seeds",
            "Berries",
            "Whole grains",
            "Lean proteins"
        ]
        recommendations["foods_to_avoid"] = [
            "Excessive processed foods",
            "Too much caffeine (limit to 1-2 cups)",
            "High-sugar snacks"
        ]
        recommendations["lifestyle_tips"] = [
            "Maintain regular sleep schedule",
            "Exercise regularly (30 mins/day)",
            "Practice mindfulness or meditation"
        ]
    else:
        recommendations["status"] = "High Cortisol"
        recommendations["diet_advice"] = [
            "Reduce caffeine and stimulants",
            "Focus on anti-inflammatory foods",
            "Eat foods rich in omega-3 fatty acids"
        ]
        recommendations["foods_to_eat"] = [
            "Dark chocolate (70%+ cocoa)",
            "Green tea",
            "Fatty fish (salmon, sardines)",
            "Blueberries and other berries",
            "Avocados",
            "Chamomile tea"
        ]
        recommendations["foods_to_avoid"] = [
            "Caffeine (coffee, energy drinks)",
            "Refined sugars and carbs",
            "Alcohol",
            "Processed foods",
            "Trans fats"
        ]
        recommendations["lifestyle_tips"] = [
            "Practice deep breathing exercises",
            "Prioritize 8+ hours of sleep",
            "Try yoga or gentle stretching",
            "Reduce work/study stress if possible"
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
