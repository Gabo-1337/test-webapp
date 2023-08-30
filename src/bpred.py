import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def make_prediction(s_l, n_p, amh, tsc, sal, dep):

# -------------------------------------------------------------------------------------------------------
# * for model accuracy test
    # Implementing Random Forest model
    df = pd.read_csv('https://raw.githubusercontent.com/Lolimipsu/thesis-repository/main/HR_comma_sep.csv')

    # Dropping all duplicate data
    df.drop_duplicates(inplace = True)

    # Initializing inputs and targets
    inputs = df[['satisfaction_level','number_project','average_montly_hours','time_spend_company','Department','salary']]
    target = df.left

    # Setting all salary values in numerical values
    inputs.replace({'salary': {'low':1, 'medium':2, 'high':3}}, inplace=True)

    # One Hot Encoding implementation
    dep_dummies = pd.get_dummies(df['Department'])
    df_with_dummies = pd.concat([inputs,dep_dummies],axis='columns')
    df_with_dummies.drop('Department',axis='columns',inplace=True)
    df_with_dummies.drop('technical',axis='columns',inplace=True)

    # Implementing x and y for prediction model
    x = df_with_dummies
    y = target

    # Implementing the ML Train Test Split Method
    x_train, x_test, y_train, y_test = train_test_split(x,y,train_size=0.8)

# -------------------------------------------------------------------------------------------------------
# * the model itself

    model = joblib.load('employee_model.joblib')

    department_type = dep
    # Custom Prediction
    d_type = []
    if department_type == "IT":
        d_type = [1,0,0,0,0,0,0,0,0]
    elif department_type == "RandD":
        d_type = [0,1,0,0,0,0,0,0,0]
    elif department_type == "accounting":
        d_type = [0,0,1,0,0,0,0,0,0]
    elif department_type == "hr":
        d_type = [0,0,0,1,0,0,0,0,0]
    elif department_type == "management":
        d_type = [0,0,0,0,1,0,0,0,0]
    elif department_type == "marketing":
        d_type = [0,0,0,0,0,1,0,0,0]
    elif department_type == "product_mng":
        d_type = [0,0,0,0,0,0,1,0,0]
    elif department_type == "sales":
        d_type = [0,0,0,0,0,0,0,1,0]
    elif department_type == "support":
        d_type = [0,0,0,0,0,0,0,0,1]
    elif department_type == "technical":
        d_type = [0,0,0,0,0,0,0,0,0]

    # Defining the columns
    columns = ['satisfaction_level','number_project','average_montly_hours','time_spend_company','salary','IT','RandD','accounting','hr','management','marketing','product_mng','sales','support']

    # Initialization of dataframe with the custom prediction data
    prediction_data = pd.DataFrame([[s_l, n_p, amh, tsc, sal] + d_type], columns=columns)

    # Predict
    model_score = str(model.score(x_test,y_test))
    pred_data = model.predict(prediction_data)
    pred_output = "No output yet"
    if pred_data == [0]:
        pred_output = ("The employee is highly likely to retain " + "(value returned was " + str(pred_data) + ")" + " Model Accuracy: " + model_score)
    else:
        pred_output = ("The employee is less likely to retain " + "(value returned was " + str(pred_data) + ")"  +  " Model Accuracy: " + model_score)
  
    return pred_output