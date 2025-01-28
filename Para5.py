import streamlit as st
import random

# Define life expectancy for demographic evaluation
LIFE_EXPECTANCY = {
    "Male": 73,
    "Female": 79,
    "Other": 76  # Default life expectancy for non-binary/unspecified gender
}

# Collect applicant demographics
if "applicant_info" not in st.session_state:
    st.session_state["applicant_info"] = {"submitted": False}

if not st.session_state["applicant_info"]["submitted"]:
    st.title("Demographics")
    st.write("Please provide your information below:")

    # Streamlit widgets for data collection
    name = st.text_input("Full Name:", key="name_input")
    age = st.number_input("Age:", min_value=0, max_value=120, step=1, key="age_input")
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"], key="gender_input")
    mobility_device = st.radio("Do you use a mobility device?", ["Yes", "No"], key="mobility_device_input")

    if st.button("Submit Demographics"):
        if name.strip() and age and gender and mobility_device:
            # Save demographic info to session state
            st.session_state["applicant_info"] = {
                "Name": name.strip(),
                "Age": int(age),
                "Gender": gender,
                "Mobility Device": mobility_device,
                "submitted": True,
            }
            # Initialize other session variables
            st.session_state["current_question_index"] = 0
            st.session_state["responses"] = {}
            st.experimental_rerun()  # Reload app to move to the first question
        else:
            st.error("Please fill out all fields correctly.")
else:
    # If demographics have been submitted, proceed with the questionnaire
    st.title("Questionnaire")

    # Ensure other session variables are initialized
    if "current_question_index" not in st.session_state:
        st.session_state["current_question_index"] = 0
    if "responses" not in st.session_state:
        st.session_state["responses"] = {}

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
# Shuffle the questions for randomness
if "randomized_questions" not in st.session_state:
    randomized_questions = list(questions.items())
    random.shuffle(randomized_questions)
    st.session_state["randomized_questions"] = randomized_questions
else:
    randomized_questions = st.session_state["randomized_questions"]

if "responses" not in st.session_state:
    st.session_state["responses"] = {}

if "current_question_index" not in st.session_state:
    st.session_state["current_question_index"] = 0


def calculate_score(responses):
    score = 0
    middle_count = 0
    for _, answer in responses.items():
        score += answer
        if answer == 2:
            middle_count += 1
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
        category_scores["Vision Impairment"] += responses.get(q, 0)
    for q in cognitive_questions:
        category_scores["Cognitive Impairment"] += responses.get(q, 0)
    for q in physical_questions:
        category_scores["Physical Impairment"] += responses.get(q, 0)
    for q in auditory_questions:
        category_scores["Hearing Impairment"] += responses.get(q, 0)

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

    if age > LIFE_EXPECTANCY.get(gender, 76):
        return "Unconditional Eligibility"

    if score >= 120:  # Threshold for high scores
        return "Unconditional Eligibility"

    if mobility_device == "Yes":
        return "Conditional Eligibility"

    if middle_count >= total_questions * 0.75:
        return "Ineligible"
    elif 80 <= score < 120:  # Adjusted threshold for Conditional Eligibility
        return "Conditional Eligibility"
    else:
        return "Ineligible"


def determine_pca(responses):
    pca_questions = ["Q5", "Q18"]
    return any(responses.get(q, 0) > 2 for q in pca_questions)


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
    justification += f"- Neutral Responses: {middle_count} out of {len(randomized_questions)} questions\n"
    justification += f"- Challenges Identified in: {', '.join(classifications) if classifications else 'None'}\n"
    justification += (
        f"- Age vs. Life Expectancy: {applicant_info['Age']} years old, expected lifespan for {applicant_info['Gender']} is {LIFE_EXPECTANCY.get(applicant_info['Gender'], 76)} years.\n"
    )

    return justification


def display_question(index):
    question_data = randomized_questions[index][1]
    st.write(f"Question {index + 1}: {question_data['text']}")  # Display question number and text

    # Radio buttons for answer choices
    selected_option = st.radio(
        "Choose an option:",
        options=list(question_data["options"].keys()),
        format_func=lambda x: question_data["options"][x],
        key=f"radio_question_{index}",
    )

    # Button to submit the answer
    if st.button("Submit Answer", key=f"submit_answer_{index}"):
        if selected_option is not None:
            st.session_state["responses"][randomized_questions[index][0]] = selected_option
            st.session_state["current_question_index"] += 1
            st.experimental_rerun()
        else:
            st.error("Please select an option before proceeding.")


# Main application logic
if st.session_state["current_question_index"] < len(randomized_questions):
    display_question(st.session_state["current_question_index"])
else:
    st.title("Thank You!")
    st.write("You have completed the questionnaire.")
    st.json(st.session_state["responses"])