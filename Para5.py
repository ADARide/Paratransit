import streamlit as st
import random

# Define life expectancy for demographic evaluation
LIFE_EXPECTANCY = {
    "Male": 73,
    "Female": 79,
    "Other": 76
}

# Collect applicant demographics
st.title("Paratransit Eligibility Questionnaire")

st.header("Applicant Demographics")
name = st.text_input("Full Name:")
age = st.number_input("Age:", min_value=0, max_value=120, step=1)
gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
mobility_device = st.selectbox("Do you use a mobility device?", ["Yes", "No"])

if not name:
    st.warning("Please enter your name to proceed.")
    st.stop()

applicant_info = {
    "Name": name,
    "Age": age,
    "Gender": gender,
    "Mobility Device": mobility_device
}

### DSM & Medical Conditions Logging
st.header("Medical & DSM Diagnoses")

# Sample list of DSM and medical conditions
medical_conditions = [
    "Generalized Anxiety Disorder",
    "Major Depressive Disorder",
    "Schizophrenia",
    "Bipolar Disorder",
    "Autism Spectrum Disorder",
    "Cerebral Palsy",
    "Multiple Sclerosis",
    "Epilepsy",
    "Chronic Pain Syndrome",
    "Post-Traumatic Stress Disorder (PTSD)"
]

# Allow multiple condition selection
selected_conditions = st.multiselect("Select Diagnoses", medical_conditions)

# Dictionary to store provider details
if "medical_providers" not in st.session_state:
    st.session_state.medical_providers = {}

for condition in selected_conditions:
    st.subheader(f"Provider Information for {condition}")
    provider_name = st.text_input(f"Provider Name for {condition}", key=f"{condition}_provider")
    provider_phone = st.text_input(f"Provider Phone for {condition}", key=f"{condition}_phone")

    # Store in session state
    st.session_state.medical_providers[condition] = {
        "Provider Name": provider_name,
        "Provider Phone": provider_phone
    }

# Define the questions
questions = {
    "Q1": {
        "text": "How often do you use public transit?",
        "options": {
            0: "Daily",
            1: "Weekly",
            2: "Occasionally",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q2": {
        "text": "What is your primary mode of transportation?",
        "options": {
            0: "Walking",
            1: "Public Transit",
            2: "Driving Yourself",
            3: "Paratransit Services",
            4: "None"
        }
    },
    "Q3": {
        "text": "Do you have difficulty reading signs due to visual impairments?",
        "options": {
            0: "No difficulty",
            1: "Mild difficulty",
            2: "Moderate difficulty",
            3: "Severe difficulty",
            4: "Cannot read signs"
        }
    },
    "Q4": {
        "text": "Do you use any mobility aids?",
        "options": {
            0: "None",
            1: "Cane/Walker",
            2: "Manual Wheelchair",
            3: "Motorized Wheelchair/Scooter",
            4: "Other"
        }
    },
    "Q5": {
        "text": "Do you travel alone or with assistance?",
        "options": {
            0: "Alone",
            1: "Occasionally with assistance",
            2: "Always with assistance",
            3: "Only with assistance",
            4: "Never travel alone"
        }
    },
    "Q6": {
        "text": "How far can you walk without resting?",
        "options": {
            0: "More than 500 meters (5 blocks or more)",
            1: "100–500 meters (1–5 blocks)",
            2: "50–100 meters",
            3: "Less than 50 meters",
            4: "I cannot walk"
        }
    },
    "Q7": {
        "text": "Can you navigate stairs or steep inclines independently?",
        "options": {
            0: "Always",
            1: "With some difficulty",
            2: "With assistance",
            3: "Not at all",
            4: "Rarely"
        }
    },
    "Q8": {
        "text": "Can you stand for at least 10 minutes while waiting for a bus?",
        "options": {
            0: "Yes, without discomfort",
            1: "Yes, but with mild discomfort",
            2: "Only for short periods",
            3: "No",
            4: "Not at all"
        }
    },
    "Q9": {
        "text": "Do you experience fatigue when walking to a transit stop?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Frequently",
            4: "Always"
        }
    },
    "Q10": {
        "text": "How do weather conditions impact your ability to travel to a bus stop?",
        "options": {
            0: "Not at all",
            1: "Occasionally",
            2: "Often",
            3: "Severely",
            4: "Always prevent me"
        }
    },
    "Q11": {
        "text": "How easy is it for you to understand bus or train schedules?",
        "options": {
            0: "Very easy",
            1: "Somewhat easy",
            2: "Somewhat difficult",
            3: "Very difficult",
            4: "I cannot read schedules"
        }
    },
    "Q12": {
        "text": "If given verbal directions, can you follow them?",
        "options": {
            0: "Always",
            1: "Usually",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q13": {
        "text": "Can you independently navigate a transfer between bus or train routes?",
        "options": {
            0: "Always",
            1: "Usually",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q14": {
        "text": "Can you identify landmarks or stops while traveling?",
        "options": {
            0: "Always",
            1: "Most of the time",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q15": {
        "text": "Can you recognize bus numbers or route signs?",
        "options": {
            0: "Always",
            1: "Most of the time",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q16": {
        "text": "Do you have difficulty hearing announcements on public transit?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q17": {
        "text": "Do crowded spaces affect your ability to use public transit?",
        "options": {
            0: "Not at all",
            1: "Occasionally",
            2: "Often",
            3: "Severely",
            4: "Always avoid"
        }
    },
    "Q18": {
        "text": "Do you need assistance to manage your travel anxiety?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q19": {
        "text": "Can you travel independently during nighttime?",
        "options": {
            0: "Always",
            1: "Most of the time",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q20": {
        "text": "If you miss a bus, how do you manage the delay?",
        "options": {
            0: "Adjust independently",
            1: "Ask for assistance",
            2: "Wait for a long time",
            3: "Unable to proceed",
            4: "Never proceed"
        }
    },
    "Q21": {
        "text": "Can you hear traffic while walking to a bus stop?",
        "options": {
            0: "Always",
            1: "Most of the time",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q22": {
        "text": "Do you require additional time to board or disembark a bus?",
        "options": {
            0: "No",
            1: "Occasionally",
            2: "Most of the time",
            3: "Always",
            4: "Never board"
        }
    },
    "Q23": {
        "text": "Do you rely on visual cues to navigate transit systems?",
        "options": {
            0: "Never",
            1: "Occasionally",
            2: "Most of the time",
            3: "Always",
            4: "Cannot rely"
        }
    },
    "Q24": {
        "text": "Do you have difficulty reading signs or maps due to visual impairments?",
        "options": {
            0: "No",
            1: "Rarely",
            2: "Sometimes",
            3: "Frequently",
            4: "Always"
        }
    },
    "Q25": {
        "text": "Can you safely cross streets or intersections without assistance?",
        "options": {
            0: "Always",
            1: "Most of the time",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q26": {
        "text": "Do you require assistance with remembering directions while traveling?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q27": {
        "text": "Can you manage transfers independently between two routes?",
        "options": {
            0: "Always",
            1: "Most of the time",
            2: "Sometimes",
            3: "Rarely",
            4: "Never"
        }
    },
    "Q28": {
        "text": "How often do you rely on someone else to manage your travel details?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q29": {
        "text": "How easily can you understand verbal transit announcements?",
        "options": {
            0: "Very easily",
            1: "Easily",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot understand"
        }
    },
    "Q30": {
        "text": "How quickly can you adjust when a bus or train stop is skipped?",
        "options": {
            0: "Immediately",
            1: "Quickly",
            2: "Neutral",
            3: "Slowly",
            4: "Cannot adjust"
        }
    },
    "Q31": {
        "text": "How well can you predict travel times using schedules?",
        "options": {
            0: "Very well",
            1: "Well",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot predict"
        }
    },
    "Q32": {
        "text": "How frequently do you lose track of time while traveling?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q33": {
        "text": "How long can you walk without needing to rest?",
        "options": {
            0: "More than 500 meters",
            1: "200–500 meters",
            2: "100–200 meters",
            3: "Under 100 meters",
            4: "Cannot walk"
        }
    },
    "Q34": {
        "text": "How easily can you navigate stairs or steep inclines?",
        "options": {
            0: "Very easily",
            1: "Easily",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot navigate"
        }
    },
    "Q35": {
        "text": "How well can you balance while walking on uneven surfaces?",
        "options": {
            0: "Very well",
            1: "Well",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot balance"
        }
    },
    "Q36": {
        "text": "How easily can you carry items (e.g., bags, backpacks) while traveling?",
        "options": {
            0: "Very easily",
            1: "Easily",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot carry"
        }
    },
    "Q37": {
        "text": "How long can you stand while waiting for a bus or train?",
        "options": {
            0: "More than 15 minutes",
            1: "10–15 minutes",
            2: "5–10 minutes",
            3: "Under 5 minutes",
            4: "Cannot stand"
        }
    },
    "Q38": {
        "text": "How easily can you board a bus or train independently?",
        "options": {
            0: "Very easily",
            1: "Easily",
            2: "Neutral",
            3: "With assistance",
            4: "Cannot board"
        }
    },
    "Q39": {
        "text": "How frequently do you need to take breaks while walking?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q40": {
        "text": "How confident are you walking through crowded areas?",
        "options": {
            0: "Very confident",
            1: "Confident",
            2: "Neutral",
            3: "Unsure",
            4: "Not confident at all"
        }
    },
    "Q41": {
        "text": "How well can you use handrails while walking up or down stairs?",
        "options": {
            0: "Very well",
            1: "Well",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot use handrails"
        }
    },
    "Q42": {
        "text": "How often do you use mobility aids while traveling?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q43": {
        "text": "How well can you hear transit announcements in noisy environments?",
        "options": {
            0: "Very well",
            1: "Well",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot hear"
        }
    },
    "Q44": {
        "text": "How frequently do you rely on visual cues rather than auditory ones?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q45": {
        "text": "How often do background noises interfere with your ability to focus?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q46": {
        "text": "How easily can you distinguish different sounds while traveling?",
        "options": {
            0: "Very easily",
            1: "Easily",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot distinguish"
        }
    },
    "Q47": {
        "text": "How well can you hear and react to vehicle horns or warning sounds?",
        "options": {
            0: "Very well",
            1: "Well",
            2: "Neutral",
            3: "With difficulty",
            4: "Cannot hear"
        }
    },
    "Q48": {
        "text": "How often do you miss important announcements on public transit?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    },
    "Q49": {
        "text": "How confident are you navigating loud, busy environments?",
        "options": {
            0: "Very confident",
            1: "Confident",
            2: "Neutral",
            3: "Unsure",
            4: "Not confident"
        }
    },
    "Q50": {
        "text": "How often do background noises interfere with your ability to hear transit announcements?",
        "options": {
            0: "Never",
            1: "Rarely",
            2: "Sometimes",
            3: "Often",
            4: "Always"
        }
    }
}  

# Store full question list for scoring (though only Q1 and Q50 are shown)
all_questions = [f"Q{i}" for i in range(1, 51)]

# Shuffle question order ONCE at startup
if "randomized_questions" not in st.session_state:
    st.session_state.randomized_questions = list(questions.items())
    random.shuffle(st.session_state.randomized_questions)

# Ensure responses are stored in session state
if "responses" not in st.session_state:
    st.session_state.responses = {key: None for key in questions}

# Randomize option order to prevent predictable responses
if "randomized_options" not in st.session_state:
    st.session_state.randomized_options = {}
    for key, q in questions.items():
        options = list(q["options"].items())  # Convert to list of (value, text)
        random.shuffle(options)  # Shuffle the order of the choices
        st.session_state.randomized_options[key] = dict(options)  # Store shuffled

st.header("Questionnaire")
for key, question in st.session_state.randomized_questions:
    selected_option = st.radio(
        question["text"], 
        st.session_state.randomized_options[key].values(), 
        index=None, 
        key=key
    )

    if selected_option is not None:
        st.session_state.responses[key] = [
            value for value, text in st.session_state.randomized_options[key].items() if text == selected_option
        ][0]
    else:
        st.session_state.responses[key] = None  # Prevents errors if left blank

# Submit button
if st.button("Submit Responses"):
    if None in st.session_state.responses.values():
        st.warning("Please answer all questions before submitting.")
    else:
        def calculate_score(responses):
            score = sum(responses.values())
            middle_count = sum(1 for v in responses.values() if v == 2)
            return score, middle_count

        def classify_impairments_and_scores(responses):
            classifications = []
            category_scores = {
                "Vision Impairment": 0,
                "Cognitive Impairment": 0,
                "Physical Impairment": 0,
                "Hearing Impairment": 0,
            }

            vision_questions = ["Q3", "Q15", "Q24"]
            cognitive_questions = ["Q4", "Q12", "Q26"]
            physical_questions = ["Q2", "Q7", "Q29"]
            auditory_questions = ["Q16", "Q50"]

            for q in vision_questions:
                if q in responses:
                    category_scores["Vision Impairment"] += responses[q]
            for q in cognitive_questions:
                if q in responses:
                    category_scores["Cognitive Impairment"] += responses[q]
            for q in physical_questions:
                if q in responses:
                    category_scores["Physical Impairment"] += responses[q]
            for q in auditory_questions:
                if q in responses:
                    category_scores["Hearing Impairment"] += responses[q]

            if category_scores["Vision Impairment"] > 2:
                classifications.append("Vision Impairment")
            if category_scores["Cognitive Impairment"] > 2:
                classifications.append("Cognitive Impairment")
            if category_scores["Physical Impairment"] > 2:
                classifications.append("Physical Impairment")
            if category_scores["Hearing Impairment"] > 2:
                classifications.append("Hearing Impairment")

            return classifications, category_scores

        def determine_eligibility(score, middle_count, total_questions, applicant_info):
            age = applicant_info["Age"]
            gender = applicant_info["Gender"]
            mobility_device = applicant_info["Mobility Device"]

            if middle_count >= total_questions * 0.75:
                return "Ineligible"

            if score >= 120 or (age > LIFE_EXPECTANCY.get(gender, 76)):
                return "Unconditional Eligibility"

            return "Conditional Eligibility"

        score, middle_count = calculate_score(st.session_state.responses)
        classifications, category_scores = classify_impairments_and_scores(st.session_state.responses)
        eligibility = determine_eligibility(score, middle_count, len(all_questions), applicant_info)

        def generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info):
            justification = (
                f"Applicant {applicant_info['Name']} (age {applicant_info['Age']}, gender {applicant_info['Gender']}) "
                f"achieved an overall score of {score}, resulting in a determination of {eligibility}. "
            )

            if classifications:
                justification += f"This determination was influenced by challenges related to: {', '.join(classifications)}. "

            if eligibility == "Unconditional Eligibility":
                justification += "The applicant demonstrates severe and consistent barriers to using fixed-route transit services. "
            elif eligibility == "Conditional Eligibility":
                justification += "The applicant shows specific barriers that limit fixed-route transit use under certain conditions."
            else:
                justification += "The applicant does not demonstrate sufficient barriers to qualify for paratransit services. "

            return justification

        st.header("Results")
        st.write(f"**Overall Score:** {score}")
        st.write(f"**Eligibility:** {eligibility}")
        st.write(generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info))
        st.write("### Medical Provider Details", st.session_state.medical_providers)
