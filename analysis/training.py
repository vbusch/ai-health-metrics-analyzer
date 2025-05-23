import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler  # For scaling



def train_model(df_merged):

    features = ['dairy_consumed_last_3_days', 'total_sugar_consumed_today', 'time_morning', 'time_afternoon', 'time_evening']
    X = df_merged[features].fillna(0)
    y = df_merged['heart_rate']

    # Scale Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.5, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    #Evaluate Model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse**0.5
    r_squared = r2_score(y_test, y_pred)

    print("Mean Squared Error (MSE):", mse)
    print("Root Mean Squared Error (RMSE):", rmse)
    print("R-squared:", r_squared)

    # Interpret Model
    coefficients = pd.DataFrame({'Feature': features, 'Coefficient': model.coef_})
    print("\nCoefficients:\n", coefficients.to_markdown(index=False, numalign="left", stralign="left"))

    result = f"""
    For the following features {features}
    A LinearRegreasion found:
        Mean Squared Error (MSE): {mse}
        Root Mean Squared Error (RMSE): {rmse}
        R-squared: {r_squared}
        Coefficients:\n", {coefficients.to_markdown(index=False, numalign="left", stralign="left")}
    """
    return result