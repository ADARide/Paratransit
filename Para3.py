import streamlit as st
import random

# Define life expectancy for demographic evaluation
LIFE_EXPECTANCY = {
    "Male": 73,
    "Female": 79,
    "Other": 76  # Default life expectancy for non-binary/unspecified gender
}

# Collect applicant demographics
applicant_info = {}

def collect_applicant_info():
    def submit_info():
        try:
            applicant_info["Name"] = name_entry.get().strip()
            applicant_info["Age"] = int(age_entry.get().strip())
            applicant_info["Gender"] = gender_var.get()
            applicant_info["Mobility Device"] = mobility_var.get()
            if not applicant_info["Name"] or not applicant_info["Gender"] or not applicant_info["Mobility Device"]:
                raise ValueError
            root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please fill out all fields correctly.")

    root = tk.Tk()
    root.title("Applicant Demographics")

    tk.Label(root, text="Please provide your information:").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Full Name:").grid(row=1, column=0, sticky="e")
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1)

    tk.Label(root, text="Age:").grid(row=2, column=0, sticky="e")
    age_entry = tk.Entry(root)
    age_entry.grid(row=2, column=1)

    tk.Label(root, text="Gender:").grid(row=3, column=0, sticky="e")
    gender_var = tk.StringVar(value="Other")
    gender_menu = tk.OptionMenu(root, gender_var, "Male", "Female", "Other")
    gender_menu.grid(row=3, column=1)

    tk.Label(root, text="Do you use a mobility device?").grid(row=4, column=0, sticky="e")
    mobility_var = tk.StringVar(value="No")
    mobility_menu = tk.OptionMenu(root, mobility_var, "Yes", "No")
    mobility_menu.grid(row=4, column=1)

    tk.Button(root, text="Submit", command=submit_info).grid(row=5, column=0, columnspan=2, pady=10)
    root.mainloop()

# Call demographic collection
collect_applicant_info()

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
# Shuffle the questions for randomness
randomized_questions = list(questions.items())
random.shuffle(randomized_questions)

responses = {}
current_question_index = 0

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
    justification += f"- Neutral Responses: {middle_count} out of {len(questions)} questions\n"
    justification += f"- Challenges Identified in: {', '.join(classifications) if classifications else 'None'}\n"
    justification += (
        f"- Age vs. Life Expectancy: {applicant_info['Age']} years old, expected lifespan for {applicant_info['Gender']} is {LIFE_EXPECTANCY.get(applicant_info['Gender'], 76)} years.\n"
    )

    return justification

def calculate_and_display_results():
    score, middle_count = calculate_score(responses)
    classifications, category_scores = classify_impairments_and_scores(responses)
    eligibility = determine_eligibility(score, middle_count, len(questions), applicant_info)
    pca_needed = determine_pca(responses)

    justification = generate_justification(score, eligibility, middle_count, classifications, category_scores, applicant_info)

    for widget in frame.winfo_children():
        widget.destroy()

    result_label = tk.Label(
        frame,
        text=f"Overall Score: {score}\nEligibility: {eligibility}\nPCA Required: {pca_needed}",
        wraplength=400,
        justify="left",
    )
    result_label.pack(pady=10)

    breakdown_label = tk.Label(frame, text=justification, wraplength=400, justify="left")
    breakdown_label.pack(pady=10)

    close_button = tk.Button(frame, text="Close", command=root.destroy)
    close_button.pack(pady=20)

def next_question():
    global current_question_index, responses

    selected_option = var.get()
    if selected_option == -1:
        messagebox.showwarning("Input Required", "Please select an option before proceeding.")
        return

    question_key = randomized_questions[current_question_index][0]
    responses[question_key] = selected_option

    current_question_index += 1

    if current_question_index < len(randomized_questions):
        display_question()
    else:
        calculate_and_display_results()

def display_question():
    global current_question_index

    question_data = randomized_questions[current_question_index][1]

    for widget in frame.winfo_children():
        widget.destroy()

    question_label = tk.Label(frame, text=question_data["text"], wraplength=400, justify="left")
    question_label.pack(pady=10)

    global var
    var = tk.IntVar(value=-1)
    for value, option in question_data["options"].items():
        tk.Radiobutton(frame, text=option, variable=var, value=value).pack(anchor="w")

    next_button = tk.Button(frame, text="Next", command=next_question)
    next_button.pack(pady=20)

root = tk.Tk()
root.title("Paratransit Eligibility Questionnaire")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

current_question_index = 0
var = tk.IntVar()

display_question()
root.mainloop()