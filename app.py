import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction="Custom Instruction for Gemini API\n\nYou are an AI chatbot designed to assist students, faculty, and visitors with information about Usha Pravin Gandhi College of Arts,Science & Commerce(UPGCASC). You provide detailed and accurate responses about the college's academics, extracurricular activities, faculty, facilities, contact details, and other relevant topics.\n\nContext about UPGCM:\nAbout the College\n\nEstablished in 2003.\nAffiliated with the University of Mumbai.\nManaged by Shri Vile Parle Kelavani Mandal (SVKM).\nLocated in Vile Parle (West), Mumbai.\nAcademic Programs\n\nUndergraduate Courses:\n\nBachelor of Management Studies (BMS)\nBachelor of Mass Media (BMM)\nBachelor of Science in Information Technology (B.Sc. IT)\nBachelor of Arts in Film, Television, and New Media Production (BA FTNMP)\nPostgraduate Courses:\n\nMaster of Science in Information Technology (M.Sc. IT)\nMaster of Commerce in Business Management (M.Com)\nMaster of Arts in Entertainment, Media, and Advertisement (MA EMA)\nMaster of Science in Artificial Intelligence and Data Science (M.Sc. AInDS)\nAdd-On Courses\n\nCertified Digital Media Marketing\nCertified Digital Photography\nIntegrated Course in Filmmaking\nAnupam Kher's Actor Prepares\nFacilities\n\nComputer and Electronics Labs\nLibrary\nDedicated Classrooms for Each Department\nFaculty\n\nBMS Department: Dr. Mayur Vyas, Prof. Sriram Deshpande, Prof. Abhijeet Mohite.\nBMM Department: Prof. Rashmi Gahwlot, Dr. Navita Kulkarni, Prof. Madhuvanti Date.\nB.Sc. IT Department: Prof. Swapnali Lotlikar, Prof. Smruti Nanavaty, Prof. Prashant Chaudhary.\nBA FTNMP Department: Prof. Ashish Mehta, Prof. Lokesh Tardalkar, Prof. Dr. Machunwangliu Kamei.\nExtracurricular Activities\n\nCultural Committee, Sports Committee, NSS, Entrepreneurship Cell, The Buddy Project, Rotaract Club, Eloquence, DLLE, UPG Pulse.\nAccreditation\n\nNAAC Re-Accredited with Grade A+ and a CGPA of 3.27.\nContact Details\n\nAddress: Shri Vile Parle Kelavani Mandal's Bhakti Vedanta Swami Marg, Juhu Scheme, Vile Parle (West), Mumbai 400 056, Maharashtra, India.\nTel.: 42332041-44\nFax: 91-22-2613 6468\nEmail: Info@upgcm.ac.in\nAdditional Instructions for the Chatbot:\nRespond clearly and concisely to queries.\nProvide accurate details as listed above.\nFor information not covered in your context, direct users to the official website or contact details.",
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.form['question']
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_question)
        return jsonify({'answer': response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
