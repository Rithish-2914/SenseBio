import os
import random
import math
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
CORS(app)

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

@app.route('/api/cortisol')
def get_cortisol():
    cortisol_value = sensor.get_reading()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({
        "cortisol": cortisol_value,
        "unit": "ng/mL",
        "timestamp": timestamp
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
