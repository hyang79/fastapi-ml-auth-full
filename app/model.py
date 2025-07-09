import cloudpickle

with open("model/iris_clf.pkl","rb") as f:
    model = cloudpickle.load(f)

def predict(features: list):
    return model.predict([features]).tolist()