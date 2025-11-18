# demo.py - Simple demo version
import random

class SimpleTitanicAI:
    def predict(self, pclass, gender, age):
        """Super simple prediction"""
        score = 0
        
        if gender == "female":
            score += 2
        if pclass == "1":
            score += 1
        if age < 12:
            score += 1
            
        return "SURVIVE" if score >= 2 else "NOT SURVIVE"

# Demo
ai = SimpleTitanicAI()
print("🚢 Titanic AI Demo")
print("First class woman:", ai.predict("1", "female", 25))
print("Third class man:", ai.predict("3", "male", 30))