from flask import Flask, render_template, jsonify, request
import subprocess
import os

app = Flask(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))

# Initial detected object
detected_object = "None"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Exercise.html')
def exercise():
    return render_template('Exercise.html')

@app.route('/guide.html')
def guide():
    return render_template('guide.html')

@app.route('/update', methods=['POST'])
def update():
    global detected_object
    detected_object = request.json.get('object_name', 'None')
    return jsonify(success=True)

@app.route('/get_object')
def get_object():
    return jsonify(object_name=detected_object)

@app.route('/run-exercise/<exercise_type>')
def run_exercise(exercise_type):
    try:
        script_path = None
        if exercise_type == "push-up":
            script_path = os.path.join(base_path, "exercise", "Pushup.py")
        elif exercise_type == "squats":
            script_path = os.path.join(base_path, "exercise", "squat.py")
        elif exercise_type == "lateral-rise":
            script_path = os.path.join(base_path, "exercise", "lateral2.py")
        elif exercise_type == "alt-dumbbell-curls":
            script_path = os.path.join(base_path, "exercise", "alternative2.py")
        elif exercise_type == "barbell-row":
            script_path = os.path.join(base_path, "exercise", "barbell2.py")
        elif exercise_type == "shoulder-press":
            script_path = os.path.join(base_path, "exercise", "Shoulder_press.py")
        elif exercise_type == "tricep-dips":
            script_path = os.path.join(base_path, "exercise", "Tricep_Dips.py")
        else:
            return jsonify(error=f"Unknown exercise type: {exercise_type}")
        
        if script_path:
            # Start the Python script as a separate process
            subprocess.Popen(["python", script_path], shell=True)
            return jsonify(output=f"Started {exercise_type} tracking")
        else:
            return jsonify(error="Script path not found")
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)