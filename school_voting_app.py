
#  SCHOOL VOTING SYSTEM (by Parth)
# Small school election voting app.
# Handles candidates, voters, votes, and saves everything neatly in JSON.

import json
import os   # Using os here mainly to check file presence manually 


class SchoolVoting:
    def __init__(self):
        # store candidates per position
        self.candidates = {}
        self.voters = {}       # voter_id -> has_voted (bool)
        self.results = {}      # position -> {candidate: votes}
        # Note to self: maybe later add timestamps or track vote times

    # ---------- Candidate Management ----------
    def add_candidate(self, name, role):
        '''Add a candidate under a specific role.'''
        if role not in self.candidates:
            self.candidates[role] = []

        if name not in self.candidates[role]:
            self.candidates[role].append(name)
        else:
            print(f"{name} is already listed for {role}.")
        # (Potential future feature: remove or edit candidate info)

    # ---------- Voter Registration ----------
    def register_voter(self, student_id):
        '''Register a student for voting.'''
        if student_id in self.voters:
            print(f"Voter {student_id} already registered.")
            return
        self.voters[student_id] = False   # False means hasn't voted yet
        # Slightly redundant, but keeps the code clear

    # ---------- Voting Process ----------
    def cast_vote(self, voter_id, role, candidate):
        '''Handle a voting action.'''
        # basic validations
        if voter_id not in self.voters:
            return "Error: Voter not registered."

        if self.voters[voter_id]:
            return "Error: This voter has already cast a vote."

        if role not in self.candidates or candidate not in self.candidates[role]:
            return "Error: Invalid candidate or position."

        # update result counts
        if role not in self.results:
            self.results[role] = {}
        if candidate not in self.results[role]:
            self.results[role][candidate] = 0

        self.results[role][candidate] += 1
        self.voters[voter_id] = True

        return f"Vote recorded successfully for {candidate} as {role}!"

    # ---------- Display Results ----------
    def display_results(self):
        print("\n===== FINAL ELECTION RESULTS =====")
        if not self.results:
            print("No votes have been cast yet!")
            return

        for role, scores in self.results.items():
            print(f"\nPosition: {role}")
            sorted_candidates = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for name, vote_count in sorted_candidates:
                print(f"   {name}: {vote_count} votes")
            # TODO: Highlight the winner later (nice-to-have)

    # ---------- Save & Load ----------
    def save_all(self, filename="voting_data.json"):
        '''Save all voting-related data to a JSON file.'''
        data_to_save = {
            "candidates": self.candidates,
            "voters": self.voters,
            "results": self.results
        }

        with open(filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

        print(f"Data saved successfully to {filename}")

    def load_all(self, filename="voting_data.json"):
        '''Load data from JSON file if available.'''
        if not os.path.exists(filename):
            print("No saved data found, starting fresh.")
            return

        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.candidates = data.get("candidates", {})
                self.voters = data.get("voters", {})
                self.results = data.get("results", {})
            print("Data loaded successfully.")
        except json.JSONDecodeError:
            print("Data file seems corrupted. Ignoring and starting fresh.")


# ---------- Example Run ----------
if __name__ == "__main__":
    app = SchoolVoting()

    # Adding candidates
    app.add_candidate("Aarav", "Head Boy")
    app.add_candidate("Vivaan", "Head Boy")
    app.add_candidate("Diya", "Head Girl")
    app.add_candidate("Isha", "Head Girl")

    # Registering voters
    for sid in ["student001", "student002", "student003"]:
        app.register_voter(sid)

    # Casting votes (demo)
    print(app.cast_vote("student001", "Head Boy", "Aarav"))
    print(app.cast_vote("student002", "Head Boy", "Vivaan"))
    print(app.cast_vote("student003", "Head Girl", "Isha"))

    # Display results and save data
    app.display_results()
    app.save_all()
