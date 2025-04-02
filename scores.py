import json
from pathlib import Path

class Scores:
    def __init__(self, file_path="scores.json"):
        self.file_path = Path(file_path)
        self.scores = self.load_scores()

    def load_scores(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_scores(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, score):
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores = self.scores[:10]  # Garder les 10 meilleurs scores
        self.save_scores()

    def get_best_score(self):
        return self.scores[0] if self.scores else 0

    def get_scores(self):
        return self.scores