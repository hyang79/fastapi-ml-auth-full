from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import cloudpickle
import os

# 데이터 로드
iris = load_iris()
X, y = iris.data, iris.target

# 모델 훈련
clf = RandomForestClassifier()
clf.fit(X, y)

# 저장할 경로 확인
os.makedirs("model", exist_ok=True)
with open("model/iris_clf.pkl", "wb") as f:
    cloudpickle.dump(clf, f)

print("✅ 모델이 model/iris_clf.pkl로 저장되었습니다.")
