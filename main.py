import random

# Funktion för att validera input string
def input_valid_str(question, error_message, possible_answers):
    answer = input(question)
    while answer not in possible_answers:
        answer = input(f'{error_message}\n{question}')
    return answer

# Funktion för att validera input int
def input_valid_int(question, error_message, min_choice, max_choice):
    while True:
        str_value = input(question)
        if str_value.isdigit() and min_choice <= int(str_value) <= max_choice:
            return int(str_value)
        print(error_message)

# Funktion för att validera input som ska vara ett heltal
def input_question(question, error_message):
    while True:
        try:
            int_value = int(input(question))
            return int_value
        except ValueError:
            print(error_message)

# Hjälpfunktion för att beräkna max antal gånger en fråga kan upprepas
def max_repetitions(number_of_questions):
    if number_of_questions <= 13:
        return 1
    elif 14 <= number_of_questions <= 26:
        return 2
    else:
        return 3

# Funktion som genererar matematiska frågor
def generate_questions(number_of_questions, operator, table_or_divisor):
    questions = []
    number_two = None
    max_reps = max_repetitions(number_of_questions)

    while len(questions) < number_of_questions:
        number_one = random.randint(0, 12)

        if operator == "slumpat":
            generate_operator = random.choice(["//", "*", "%"])
            number_two = random.randint(2, 12) if generate_operator == "*" else random.randint(2, 5)
        else:
            generate_operator = operator  
            number_two = table_or_divisor

        question = (number_one, generate_operator, number_two)
        if questions.count(question) < max_reps:
            questions.append(question)
    return questions

# Funktion som genererar/validerar dörrar
def input_door_question(question_counter, number_of_questions):
    num_doors = number_of_questions - question_counter + 1
    if num_doors > 1:
        zombie_door = random.randint(1, num_doors)
        door_choice = input_valid_int(f"Välj en dörr (1-{num_doors}): ", "Felaktigt val. Försök igen.", 1, num_doors)
        if door_choice == zombie_door:
            return False, zombie_door
        else:
            return True, zombie_door
    return False, 0


proceed = "j"
loser = None
result = None
table_or_divisor = None
question_counter = 0
questions = []
print("Hjäääälp! Du är fast i zombiehuset.")
print("Svara på matematiska frågor och undvik zombies gömda bakom dörrar!")

while proceed == "j":
        number_of_questions = input_valid_int("Välj antal frågor (12 - 39): ", "Felaktigt antal frågor valt. Var god välj ett tal mellan 12 och 39.", 12, 39)
        operator = input_valid_str("Välj räknesätt (*, //, % slumpat): ", "Felaktigt räknesätt. Försök igen.", ["*", "//", "%", "slumpat"])

        if operator == "*":
            table_or_divisor = input_valid_int("Välj tabell (2 - 12): ", "Felaktigt val. Var god välj ett tal mellan 2 och 12.", 2, 12)
        elif operator in ["//", "%"]:
            table_or_divisor = input_valid_int("Välj divisor (2 - 5): ", "Felaktigt val. Var god välj ett tal mellan 2 och 5.", 2, 5)
       
        while question_counter != number_of_questions:
            if question_counter == 0:
                 questions = generate_questions(number_of_questions, operator, table_or_divisor) 
            first_number, chosen_operator, second_number = questions[question_counter] 
            if chosen_operator == "*":
                result = first_number * second_number
            elif chosen_operator == "//":
                result = first_number // second_number
            elif chosen_operator == "%":
                result = first_number % second_number
            user_input = input_question(f"Vad är {first_number} {chosen_operator} {second_number}? ", "Ange ett heltal,")
            if user_input == result:
                question_counter += 1
                if question_counter == number_of_questions:
                    print("Du har klarat alla frågorna! Du har lyckats ta dig ut ur zombiehuset.")
                    proceed = input_valid_str("Vill du spela igen? (j/n): ", "Felaktigt val. Var god välj j eller n.", ["j", "n"])
                    if proceed == "j":
                        question_counter = 0
                        questions = []
                        break
                    else:
                        print("Tack för att du spelade")
                    break 
                print(f"Grattis! Du har svarat rätt på {question_counter} frågor")
                print(f"Antal frågor kvar: {number_of_questions - question_counter}")
                winner, zombie_door = input_door_question(question_counter, number_of_questions)
                if winner:
                    print(f"Zombien va i dörr nummer {zombie_door}")
                    continue
                else:
                    loser = True
            if user_input != result or loser:
                print("Du har svarat fel. Du blir uppäten av zombies!!!")
                proceed = input_valid_str("Vill du spela igen? (j/n): ", "Felaktigt val. Var god välj j eller n.", ["j", "n"])
                if proceed == "j":
                    question_counter = 0
                    questions = []
                else:
                    print("Tack för att du spelade")
                    break

