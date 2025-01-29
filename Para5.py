import streamlit as st
import random

# Define life expectancy for demographic evaluation
LIFE_EXPECTANCY = {
    "Male": 73,
    "Female": 79,
    "Other": 76  # Default life expectancy for non-binary/unspecified gender
}

# Define all 50 questions (but only displaying Q1 & Q50)
questions = {
    "Q1": {
        "text": "How often do you use public transit?",
        "options": ["Daily", "Weekly", "Occasionally", "Rarely", "Never"]
    },
    "Q50": {
        "text": "How often do background noises interfere with your ability to hear transit announcements?",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
    },
    # Other 48 questions exist for scoring but are not displayed in UI
}

# Store randomized questions persistently across reruns
if "randomized_questions" not in st.session_state:
    st.session_state.randomized_questions = list(questions.items())
    random.shuffle(st.session_state.randomized_questions)

# Store user responses persistently
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Applicant information input
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

# Questionnaire section (Only displaying Q1 & Q50)
st.header("Questionnaire")

for key, question in st.session_state.randomized_questions:
    if key in ["Q1", "Q50"]:  # Only display Q1 and Q50
        selected_option = st.radio(question["text"], question["options"], index=None, key=key)
        st.session_state.responses[key] = question["options"].index(selected_option) if selected_option else None

# Scoring functions based on all 50 questions
def calculate_score(responses):
    score = sum(responses.values())
    middle_count = sum(1 for v in responses.values() if v == 2)
    return score, middle_count

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

def determine_pca(responses):
    return any(responses.get(q, 0) > 2 for q in ["Q5", "Q18"])

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
    justification += f"- Neutral Responses: {middle_count} out of 50 questions\n"
    justification += f"- Challenges Identified in: {', '.join(classifications) if classifications else 'None'}\n"
    justification += (
        f"- Age vs. Life Expectancy: {applicant_info['Age']} years old, expected lifespan for {applicant_info['Gender']} is {LIFE_EXPECTANCY.get(applicant_info['Gender'], 76)} years.\n"
    )

    return justification

# Submit button
if st.button("Submit Responses"):
    if None in st.session_state.responses.values():
        st.warning("Please answer all questions before submitting.")
    else:
        score, middle_count = calculate_score(st.session_state.responses)
        classifications, category_scores = classify_impairments_and_scores(st.session_state.responses)
        eligibility = determine_eligibility(score, middle_count, 50, applicant_info)
        pca_needed = determine_pca(st.session_state.responses)

        st.header("Results")
        st.write(f"**Overall Score:** {score}")
        st.write(f"**Eligibility:** {eligibility}")
        st.write(f"**Personal Care Attendant (PCA) Required:** {'Yes' if pca_needed else 'No'}")
        st.write("### Detailed Justification:")
        st.text(generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info))
