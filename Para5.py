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

# Define all 50 questions but only display Q1 and Q50
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

# Ensure state persistence
if "responses" not in st.session_state:
    st.session_state.responses = {key: None for key in questions}

# Display questionnaire (Only Q1 and Q50)
st.header("Questionnaire")
for key, question in questions.items():
    selected_option = st.radio(question["text"], question["options"], index=None, key=key)
    st.session_state.responses[key] = question["options"].index(selected_option) if selected_option else None

# Function to calculate the score
def calculate_score(responses):
    score = sum(value for value in responses.values() if value is not None)
    middle_count = sum(1 for value in responses.values() if value == 2)  # Track neutral answers
    return score, middle_count

# Function to classify impairments and scores
def classify_impairments_and_scores(responses):
    classifications = []
    category_scores = {
        "Vision Impairment": sum(responses.get(q, 0) for q in ["Q3", "Q15", "Q24"]),
        "Cognitive Impairment": sum(responses.get(q, 0) for q in ["Q4", "Q12", "Q26"]),
        "Physical Impairment": sum(responses.get(q, 0) for q in ["Q2", "Q7", "Q29"]),
        "Hearing Impairment": sum(responses.get(q, 0) for q in ["Q16", "Q50"]),
    }

    for category, score in category_scores.items():
        if score > 2:
            classifications.append(category)

    return classifications, category_scores

# Function to determine eligibility
def determine_eligibility(score, middle_count, total_questions, applicant_info):
    age = applicant_info["Age"]
    gender = applicant_info["Gender"]
    mobility_device = applicant_info["Mobility Device"]

    if age > LIFE_EXPECTANCY.get(gender, 76):
        return "Unconditional Eligibility"

    if score >= 120:
        return "Unconditional Eligibility"

    if mobility_device == "Yes":
        return "Conditional Eligibility"

    if middle_count >= total_questions * 0.75:
        return "Ineligible"
    elif 80 <= score < 120:
        return "Conditional Eligibility"
    else:
        return "Ineligible"

# Function to determine if a PCA is needed
def determine_pca(responses):
    pca_questions = ["Q5", "Q18"]
    return any(responses.get(q, 0) > 2 for q in pca_questions)

# Function to generate justification
def generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info):
    justification = (
        f"Applicant {applicant_info['Name']} (age {applicant_info['Age']}, gender {applicant_info['Gender']}) "
        f"achieved an overall score of {score}, resulting in a determination of {eligibility}. "
    )

    if classifications:
        justification += f"This determination was influenced by challenges related to: {', '.join(classifications)}. "

    if middle_count > 0:
        justification += (
            f"The applicant selected {middle_count} neutral responses, indicating moderate challenges that influenced "
            f"the eligibility outcome. "
        )

    total_category_score = sum(category_scores.values())
    if total_category_score > 0:
        justification += "\n\nCategory Impact on Transit Eligibility (Percentage Breakdown):\n"
        for category, score in category_scores.items():
            percentage = (score / total_category_score) * 100
            justification += f"- {category}: {percentage:.1f}%\n"

    total_impairments = len(classifications)
    if total_impairments > 0:
        proportion = total_impairments / 4
        justification += (
            f"A total of {total_impairments} out of 4 potential impairments were identified, "
            f"indicating {proportion * 100:.1f}% of possible impairments may affect transit eligibility. "
        )
    else:
        justification += "No specific impairments were identified that affect transit eligibility. "

    if eligibility == "Unconditional Eligibility":
        justification += "The applicant demonstrates severe and consistent barriers to using fixed-route transit services. "
    elif eligibility == "Conditional Eligibility":
        justification += (
            "The applicant shows specific barriers that limit fixed-route transit use under certain conditions, "
            "such as weather, fatigue, or accessibility challenges. "
        )
    else:
        justification += (
            "The applicant does not demonstrate sufficient barriers to qualify for paratransit services. "
        )

    justification += "\n\nDetailed Statistical Breakdown:\n"
    justification += f"- Total Score: {score}\n"
    justification += f"- Neutral Responses: {middle_count} out of {len(questions)} questions\n"
    justification += f"- Challenges Identified in: {', '.join(classifications) if classifications else 'None'}\n"
    justification += (
        f"- Age vs. Life Expectancy: {applicant_info['Age']} years old, expected lifespan for {applicant_info['Gender']} is {LIFE_EXPECTANCY.get(applicant_info['Gender'], 76)} years.\n"
    )

    return justification

# Process results when Submit is clicked
if st.button("Submit Responses"):
    if None in st.session_state.responses.values():
        st.warning("Please answer all questions before submitting.")
    else:
        score, middle_count = calculate_score(st.session_state.responses)
        classifications, category_scores = classify_impairments_and_scores(st.session_state.responses)
        eligibility = determine_eligibility(score, middle_count, len(questions), applicant_info)
        pca_needed = determine_pca(st.session_state.responses)

        # Display results
        st.header("Results")
        st.write(f"**Overall Score:** {score}")
        st.write(f"**Eligibility:** {eligibility}")
        st.write(f"**PCA Required:** {'Yes' if pca_needed else 'No'}")
        st.write("### Detailed Justification:")
        st.text(generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info))
