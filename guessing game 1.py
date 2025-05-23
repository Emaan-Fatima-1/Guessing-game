import random
import math
from datetime import datetime

# User class to handle signup and login
class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def signup():
        print("\n--- Signup Time! Let's make you official! ---")
        while True:
            username = input("Pick a cool username: ").strip()
            if User._user_exists(username):
                print("Oops! That username’s taken. Try another one!")
            else:
                password = input("Set a secret password: ").strip()
                with open("users.txt", "a") as f:
                    f.write(f"{username},{password}\n")
                print(f"Sweet! Account created for {username}.\n")
                return User(username)

    @staticmethod
    def login():
        print("\n--- Welcome back! Time to prove who you are! ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if User._validate_credentials(username, password):
            print(f"Alright {username}, you’re in!\n")
            return User(username)
        else:
            print("Nope! Wrong username or password. Try again.\n")
            return None

    @staticmethod
    def _user_exists(username):
        try:
            with open("users.txt", "r") as f:
                for line in f:
                    if line.strip().split(",")[0] == username:
                        return True
        except FileNotFoundError:
            return False
        return False

    @staticmethod
    def _validate_credentials(username, password):
        try:
            with open("users.txt", "r") as f:
                for line in f:
                    u, p = line.strip().split(",")
                    if u == username and p == password:
                        return True
        except FileNotFoundError:
            return False
        return False

# Leaderboard class to save and show scores
class Leaderboard:
    def __init__(self):
        self.scores = self._load_scores()

    def _load_scores(self):
        scores = {}
        try:
            with open("leaderboard.txt", "r") as f:
                for line in f:
                    username, score, timestamp = line.strip().split(",")
                    if username in scores:
                        scores[username].append((int(score), timestamp))
                    else:
                        scores[username] = [(int(score), timestamp)]
        except FileNotFoundError:
            pass
        return scores

    def add_score(self, username, score):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("leaderboard.txt", "a") as f:
            f.write(f"{username},{score},{timestamp}\n")
        if username in self.scores:
            self.scores[username].append((score, timestamp))
        else:
            self.scores[username] = [(score, timestamp)]

    def display(self):
        print("\n--- Leaderboard Time! Who’s the champ? ---")
        if not self.scores:
            print("No scores yet. Time to make your mark!")
            return
        for user, records in self.scores.items():
            total_score = sum(score for score, _ in records)
            rounds = len(records)
            print(f"{user}: Total Score = {total_score}, Rounds Played = {rounds}")
        print()

# Game class with guessing logic
class NumberGuessingGame:
    def __init__(self, user, leaderboard):
        self.user = user
        self.leaderboard = leaderboard

    def play(self):
        while True:
            print("\n--- Set Your Game! Let’s get those numbers right! ---")
            while True:
                try:
                    minimum = int(input("Enter the smallest number you want to guess: "))
                    maximum = int(input("Enter the biggest number you want to guess: "))
                    if minimum >= maximum:
                        print("Hey! Smallest number has to be less than the biggest. Try again.")
                        continue
                    break
                except ValueError:
                    print("Oops! That’s not a number. Try again.")

            while True:
                try:
                    total_attempts = int(input("How many tries do you want? Make it count! "))
                    if total_attempts <= 0:
                        print("You gotta have at least one try, duh!")
                        continue
                    break
                except ValueError:
                    print("Numbers only, please!")

            random_number = random.randint(minimum, maximum)
            total_entries = 0
            wrong_guess_count = 0

            print(f"\nGame on! You’ve got {total_attempts} attempts. Don’t mess it up!")

            while total_attempts > 0:
                try:
                    guess = int(input(f"Your guess (between {minimum} and {maximum}): "))
                except ValueError:
                    print("Numbers, princess! Not letters.")
                    continue

                total_entries += 1

                if guess > random_number:
                    print("Whoa, too high! Lower it down a bit.")
                    wrong_guess_count += 1
                elif guess < random_number:
                    print("Too low! Aim a little higher.")
                    wrong_guess_count += 1
                else:
                    print("Boom! You nailed it!")
                    break

                total_attempts -= 1

            if guess != random_number:
                print(f"Game over! The magic number was {random_number}.")

            score = math.ceil(total_entries - wrong_guess_count + (maximum - minimum)/10)

            print("\n--- Round Recap ---")
            print(f"Total guesses: {total_entries}")
            print(f"Wrong guesses: {wrong_guess_count}")
            print(f"Score this round: {score}")

            self.leaderboard.add_score(self.user.username, score)
            self.leaderboard.display()

            again = input("Wanna play again? (yes/no): ").lower()
            if again != 'yes':
                print("Thanks for playing! You rocked it!")
                break
            else:
                print("Alright, another round coming up!\n")

def main():
    print("Welcome to the Number Guessing Game! Let’s get started!")

    user = None
    while not user:
        action = input("Login or signup? (login/signup): ").lower()
        if action == "login":
            user = User.login()
        elif action == "signup":
            user = User.signup()
        else:
            print("Please type 'login' or 'signup' to continue.")

    leaderboard = Leaderboard()
    game = NumberGuessingGame(user, leaderboard)
    game.play()

if __name__ == "__main__":
    main()
