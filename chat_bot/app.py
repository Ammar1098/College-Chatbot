from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from difflib import get_close_matches

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Load college information
def load_college_info(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)  # Load JSON data properly
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return {}

college_data = load_college_info('college_info.txt')

@app.route('/')
def home():
    return render_template('index.html')

def find_best_match(user_input):
    for category, data in college_data.items():
        if isinstance(data, dict):
            possible_keys = list(data.keys())
            match = get_close_matches(user_input, possible_keys, n=1, cutoff=0.6)
            if match:
                return data[match[0]]
    return None

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        user_input = request.json.get("question", "").strip().lower()
        if not user_input:
            return jsonify({"error": "Question not provided."}), 400

         # Check for faculty-related queries for cse, cscf, aiml
        faculty_keywords = ["computer science and engineering faculties", "ai&ml faculties", "cscf faculties", "cse faculties"]
        for keyword in faculty_keywords:
            if keyword in user_input:
                faculty_details = college_data.get("CSE Faculties", {}).get("Computer Science & Engineering Faculties", [])
                if faculty_details:
                    return jsonify({"answer": faculty_details})

        # Check for faculty-related queries for mechanical 
        faculty_keywords = {
            "mechanical engineering faculties": "Mechanical Engineering Faculties",
            "mechanical faculties": "Mechanical Engineering Faculties"
        }

        for keyword, faculty_key in faculty_keywords.items():
            if keyword in user_input:
                faculty_details = college_data.get("Mechanical Faculties", {}).get(faculty_key, [])
                if faculty_details:
                    return jsonify({"answer": faculty_details})

        # Check for faculty-related queries for civil 
        faculty_keywords = {
            "civil engineering faculties": "Civil Engineering Faculties",
            "civil faculties": "CivilEngineering Faculties"
        }

        for keyword, faculty_key in faculty_keywords.items():
            if keyword in user_input:
                faculty_details = college_data.get("Civil Faculties", {}).get(faculty_key, [])
                if faculty_details:
                    return jsonify({"answer": faculty_details})

        # Check for faculty-related queries for Electronics & Communication
        faculty_keywords = {
            "electronics & communication engineering faculties": "Electronics & Communication Engineering Faculties",
            "electronics & communication faculties": "Electronics & Communication Engineering Faculties"
        }

        for keyword, faculty_key in faculty_keywords.items():
            if keyword in user_input:
                faculty_details = college_data.get("Electronics & Communication Faculties", {}).get(faculty_key, [])
                if faculty_details:
                    return jsonify({"answer": faculty_details})

         # Check for faculty-related queries for Physics 
        faculty_keywords = {
            "physics faculties": "Physics Faculties"
        }

        for keyword, faculty_key in faculty_keywords.items():
            if keyword in user_input:
                faculty_details = college_data.get("Physics Faculties", {}).get(faculty_key, [])
                if faculty_details:
                    return jsonify({"answer": faculty_details})

         # Check for faculty-related queries for Mathematics 
        faculty_keywords = {
            "mathematics faculties": "Mathematics Faculties"
        }

        for keyword, faculty_key in faculty_keywords.items():
            if keyword in user_input:
                faculty_details = college_data.get("Mathematics Faculties", {}).get(faculty_key, [])
                if faculty_details:
                    return jsonify({"answer": faculty_details})

         # Check for faculty-related queries for Humanities
        faculty_keywords = {
            "humanities faculties": "Humanities Faculties"
        }

        for keyword, faculty_key in faculty_keywords.items():
            if keyword in user_input:
                faculty_details = college_data.get("Humanities Faculties", {}).get(faculty_key, [])
                if faculty_details:
                    return jsonify({"answer": faculty_details})



        # Search for direct matches
        response = find_best_match(user_input)
        if response:
            return jsonify({"answer": response})  

        # If asking about a specific course
        for course, details in college_data.get("Computer Science Engineering course_details", "Artificial Intelligence and Machine Learning course_details", "Electronics and Communication Engineering course_details", "Mechanical Engineering course_details", "Civil Engineering course_details", "Cyber Security and Cyber Forensics course_details", "All Departments", "small_talk", "politeness", "greetings", "bot_identity",{}).items():
            if course.lower() in user_input:
                return jsonify({"answer": details})

        return jsonify({"answer": "I couldn't find an answer to that."})

        # If asking about a specific college detail
        user_input_lower = user_input.lower()

        for key in ["Contact Info", "Dean", "About SUIET", "our Mission", "Vision", "admissions"]:
            if key.lower() in user_input_lower:  # Convert key to lowercase for comparison
                details = college_data.get(key, "Information not available")  # Remove "college" key if not needed
                return jsonify({"answer": details})

        return jsonify({"answer": "Visit our website for more details."})

        # Check for "courses offered" in input
        if any(word in user_input_lower for word in ["courses", "courses offered", "offered"]):
            courses = college_data.get("courses_offered", [])

            if courses:  # If courses list is found
                return jsonify({"answer": "The courses offered are: " + ", ".join(courses)})
            else:
                return jsonify({"answer": "No course information available."})


    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
