# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, confusion_matrix, classification_report
import seaborn as sns

# 1. Load a regression dataset (using the Boston housing dataset for example)
data_regression = datasets.load_boston()
X_regression = data_regression.data
y_regression = data_regression.target

# 2. Split the data into training and testing sets
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_regression, y_regression, test_size=0.3, random_state=42)

# 3. Train a regression model (Linear Regression)
model_reg = LinearRegression()
model_reg.fit(X_train_reg, y_train_reg)

# 4. Make predictions
y_pred_reg = model_reg.predict(X_test_reg)

# 5. Compute Regression Metrics
# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test_reg, y_pred_reg)
print(f"Mean Absolute Error (MAE): {mae:.4f}")

# Mean Absolute Percentage Error (MAPE)
mape = np.mean(np.abs((y_test_reg - y_pred_reg) / y_test_reg)) * 100
print(f"Mean Absolute Percentage Error (MAPE): {mape:.4f}%")

# Mean Absolute Scaled Error (MASE)
# Using the in-sample data to compute the denominator
y_train_pred = model_reg.predict(X_train_reg)
mae_base = np.mean(np.abs(y_train_reg - y_train_pred))
mase = mae / mae_base
print(f"Mean Absolute Scaled Error (MASE): {mase:.4f}")

# Root Mean Square Error (RMSE)
rmse = np.sqrt(mean_squared_error(y_test_reg, y_pred_reg))
print(f"Root Mean Square Error (RMSE): {rmse:.4f}")

# --- Now we proceed to classification --- 

# 6. Load a classification dataset (using the Iris dataset as an example)
data_class = datasets.load_iris()
X_class = data_class.data
y_class = data_class.target

# 7. Split the classification dataset into training and testing sets
X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(X_class, y_class, test_size=0.3, random_state=42)

# 8. Train a classifier (Logistic Regression)
model_class = LogisticRegression(max_iter=200)
model_class.fit(X_train_class, y_train_class)

# 9. Make predictions
y_pred_class = model_class.predict(X_test_class)

# 10. Confusion Matrix
cm = confusion_matrix(y_test_class, y_pred_class)

# 11. Print Classification Report (Precision, Recall, F1-score, Accuracy)
print("Classification Report:\n", classification_report(y_test_class, y_pred_class))

# 12. Plot Confusion Matrix
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=data_class.target_names, yticklabels=data_class.target_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
