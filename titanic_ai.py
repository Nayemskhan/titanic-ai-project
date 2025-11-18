# titanic_ai.py - Titanic Survival Predictor AI
import random
import json
import datetime

class TitanicAI:
    def __init__(self):
        self.passengers = []
        self.model = None
        self.prediction_history = []
    
    def create_sample_data(self):
        """Create realistic Titanic passenger data"""
        print("Creating sample Titanic dataset...")
        
        survival_rates = {
            ('1', 'female'): 0.97, ('1', 'male'): 0.37,
            ('2', 'female'): 0.86, ('2', 'male'): 0.16,
            ('3', 'female'): 0.49, ('3', 'male'): 0.14
        }
        
        sample_passengers = []
        passenger_id = 1
        
        for pclass in ['1', '2', '3']:
            for sex in ['female', 'male']:
                survival_rate = survival_rates[(pclass, sex)]
                num_passengers = 150 if pclass == '3' else 100
                
                for i in range(num_passengers):
                    if pclass == '1':
                        age = max(5, random.gauss(38, 15))
                        fare = max(0, random.gauss(80, 50))
                    elif pclass == '2':
                        age = max(5, random.gauss(30, 15))
                        fare = max(0, random.gauss(20, 15))
                    else:
                        age = max(5, random.gauss(25, 12))
                        fare = max(0, random.gauss(10, 8))
                    
                    family_size = random.randint(0, 4)
                    survived = 1 if random.random() < survival_rate else 0
                    
                    passenger = {
                        'id': passenger_id,
                        'pclass': pclass,
                        'sex': sex,
                        'age': age,
                        'fare': fare,
                        'family_size': family_size,
                        'survived': survived
                    }
                    
                    sample_passengers.append(passenger)
                    passenger_id += 1
        
        self.passengers = sample_passengers
        print(f"Created {len(self.passengers)} sample passengers")
        return sample_passengers
    
    def analyze_data(self):
        """Basic data analysis"""
        print("\n" + "="*50)
        print("DATA ANALYSIS")
        print("="*50)
        
        if not self.passengers:
            self.create_sample_data()
        
        total = len(self.passengers)
        survived = sum(1 for p in self.passengers if p['survived'] == 1)
        survival_rate = survived / total
        
        print(f"Total passengers: {total}")
        print(f"Survived: {survived}")
        print(f"Overall survival rate: {survival_rate:.2%}")
        
        print("\n--- Survival by Class ---")
        for pclass in ['1', '2', '3']:
            class_passengers = [p for p in self.passengers if p['pclass'] == pclass]
            class_survived = sum(1 for p in class_passengers if p['survived'] == 1)
            rate = class_survived / len(class_passengers)
            print(f"Class {pclass}: {class_survived}/{len(class_passengers)} ({rate:.2%})")
        
        print("\n--- Survival by Gender ---")
        for sex in ['female', 'male']:
            sex_passengers = [p for p in self.passengers if p['sex'] == sex]
            sex_survived = sum(1 for p in sex_passengers if p['survived'] == 1)
            rate = sex_survived / len(sex_passengers)
            print(f"{sex.title()}: {sex_survived}/{len(sex_passengers)} ({rate:.2%})")
    
    def train_model(self):
        """Train AI model"""
        print("\n" + "="*50)
        print("TRAINING AI MODEL")
        print("="*50)
        
        def predict_survival(passenger):
            base_score = 0.0
            
            if passenger['sex'] == 'female':
                base_score += 0.6
            else:
                base_score += 0.1
            
            if passenger['pclass'] == '1':
                base_score += 0.3
            elif passenger['pclass'] == '2':
                base_score += 0.15
            
            age = passenger['age']
            if age < 12:
                base_score += 0.2
            elif age > 60:
                base_score -= 0.1
            
            family_size = passenger.get('family_size', 0)
            if 2 <= family_size <= 4:
                base_score += 0.1
            
            fare = passenger.get('fare', 0)
            if fare > 50:
                base_score += 0.15
            
            return min(0.95, max(0.05, base_score))
        
        self.model = predict_survival
        print("AI Model trained successfully!")
    
    def predict_survival(self, passenger_info):
        """Predict survival for a passenger"""
        if not self.model:
            self.train_model()
        
        probability = self.model(passenger_info)
        prediction = "SURVIVE" if probability > 0.5 else "NOT SURVIVE"
        
        explanation = []
        if passenger_info['sex'] == 'female':
            explanation.append("Female passengers had higher survival rates")
        else:
            explanation.append("Male passengers had lower survival rates")
        
        if passenger_info['pclass'] == '1':
            explanation.append("First class had better lifeboat access")
        elif passenger_info['pclass'] == '3':
            explanation.append("Third class was farthest from lifeboats")
        
        if passenger_info['age'] < 12:
            explanation.append("Children were prioritized")
        
        # Save prediction
        prediction_record = {
            'timestamp': datetime.datetime.now().isoformat(),
            'passenger': passenger_info,
            'prediction': prediction,
            'probability': probability
        }
        self.prediction_history.append(prediction_record)
        
        print(f"\n🎫 PREDICTION RESULTS")
        print(f"Class: {passenger_info['pclass']}")
        print(f"Gender: {passenger_info['sex']}")
        print(f"Age: {passenger_info['age']}")
        print(f"Prediction: {prediction}")
        print(f"Confidence: {probability:.1%}")
        print(f"Reasons: {', '.join(explanation)}")
        
        return prediction, probability

def main():
    """Main function"""
    print("🚢 TITANIC AI SURVIVAL PREDICTOR")
    print("=" * 50)
    
    ai = TitanicAI()
    ai.create_sample_data()
    ai.analyze_data()
    ai.train_model()
    
    # Example predictions
    print("\n" + "="*50)
    print("EXAMPLE PREDICTIONS")
    print("="*50)
    
    examples = [
        {'pclass': '1', 'sex': 'female', 'age': 25, 'fare': 100, 'family_size': 1},
        {'pclass': '3', 'sex': 'male', 'age': 35, 'fare': 10, 'family_size': 1},
        {'pclass': '2', 'sex': 'male', 'age': 8, 'fare': 25, 'family_size': 4},
    ]
    
    for example in examples:
        ai.predict_survival(example)
        print("-" * 30)

if __name__ == "__main__":
    main()