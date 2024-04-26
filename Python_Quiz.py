import random

class QuizGame:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.options = []
        self.score = 0

    def add_question(self, question, answer, options):
        self.questions.append(question)
        self.answers.append(answer)
        self.options.append(options)

    def display_question(self, index):
        print(self.questions[index])
        options = self.options[index]
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

    def get_user_answer(self):
        return input("Your answer: ")

    def check_answer(self, user_answer, index):
        correct_answer = self.answers[index]
        if user_answer.lower() == correct_answer.lower():
            print("Correct!")
            self.score += 1
        else:
            print("Incorrect. The correct answer is:", correct_answer)

    def run_quiz(self):
        num_questions = len(self.questions)
        order = list(range(num_questions))
        random.shuffle(order)

        print("Welcome to the Quiz Game!\n")
        print("You will be asked", num_questions, "questions.\n")

        for i in order:
            self.display_question(i)
            user_answer = self.get_user_answer()
            self.check_answer(user_answer, i)
            print()  # Add a newline for better readability

        print("\nQuiz completed!")
        print("Your score:", self.score, "out of", num_questions)
        self.show_feedback()

    def show_feedback(self):
        percent_correct = (self.score / len(self.questions)) * 100
        if percent_correct == 100:
            print("Congratulations! You got all questions correct.")
        elif percent_correct >= 75:
            print("Well done! You did a great job.")
        elif percent_correct >= 50:
            print("Not bad! You got more than half of the questions right.")
        else:
            print("Keep practicing! You can improve.")

if __name__ == "__main__":
    quiz = QuizGame()

    # Add questions, answers, and options
    quiz.add_question("What is the capital of France?", "Paris", ["Paris", "London", "Berlin", "Madrid"])
    quiz.add_question("What is 2 * 2?", "4", ["2", "3", "4", "5"])
    quiz.add_question("Who wrote 'Romeo and Juliet'?", "William Shakespeare", ["Charles Dickens", "Mark Twain", "Jane Austen", "William Shakespeare"])
    quiz.add_question("What is the largest planet in our solar system?", "Jupiter", ["Mars", "Saturn", "Jupiter", "Venus"])
    # Add more questions...
    
    # Run the quiz
    quiz.run_quiz()
