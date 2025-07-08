import joblib

model = joblib.load("model/iris_clf.pkl")

def predict_species(features: list):
    return int(model.predict([features])[0])