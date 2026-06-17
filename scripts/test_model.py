import joblib
import pandas as pd

model = joblib.load("outputs/best_model.pkl")

sample = pd.DataFrame(
    {
        "contributions": [500],
        "days_since_last_commit": [120]
    }
)

prediction = model.predict(sample)

if prediction[0] == 1:
    print("Predicted Status : Active")
else:
    print("Predicted Status : Inactive")