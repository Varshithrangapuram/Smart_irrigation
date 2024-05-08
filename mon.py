import serial
import time
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Load the trained Linear Regression model
def load_trained_models(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    # Linear Regression model for rainfall prediction
    X_rainfall = df[['humidity', 'temperature']]
    y_rainfall = df['rainfall']
    model_rainfall = LinearRegression()
    model_rainfall.fit(X_rainfall, y_rainfall)
    
    # Classification model for crop type prediction (using only humidity and temperature)
    X_crop = df[['humidity', 'temperature']]
    y_crop = df['label']  # Assuming 'label' is the column with crop labels
    model_crop = RandomForestClassifier()
    model_crop.fit(X_crop, y_crop)
    
    return model_rainfall, model_crop

# Define the serial port and baud rate
ser = serial.Serial('/dev/cu.usbmodem1101', 9600)  # Update the serial port accordingly

# Load the trained models
csv_file_path = '/Users/varshithrangapuram/Downloads/capstone_ml/Crop_recommendation.csv'
trained_model_rainfall, trained_model_crop = load_trained_models(csv_file_path)

def read_sensor_data():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data.startswith('Humidity'):
                humidity = float(data.split(':')[1].strip().rstrip('%'))
            elif data.startswith('Temperature'):
                temperature = float(data.split(':')[1].strip().rstrip('*C'))
            elif data.startswith('Moisture'):
                moisture = float(data.split(':')[1].strip())
                
                # Check for NaN values in humidity, temperature, or moisture
                if np.isnan(humidity) or np.isnan(temperature) or np.isnan(moisture):
                    print("Skipping prediction due to missing data (NaN)...")
                else:
                    # Predict rainfall using the trained linear regression model
                    predicted_rainfall = trained_model_rainfall.predict([[humidity, temperature]])[0]
                    
                    # Predict crop type using the trained classification model (only humidity and temperature)
                    predicted_crop = trained_model_crop.predict([[humidity, temperature]])[0]
                    
                    print(f"Current Humidity: {humidity} %")
                    print(f"Current Temperature: {temperature} *C")
                    print(f"Predicted Rainfall: {predicted_rainfall:.2f} units")
                    print(f"Predicted Crop Type: {predicted_crop}")
                    
                    # Calculate pump duration based on rainfall prediction
                    pump_duration = 10 if predicted_rainfall < 90.15 else 0  # Adjust as needed
                    
                    # Send pump duration command to Arduino
                    time.sleep(2)
                    ser.write(f"{pump_duration}\n".encode())  # Send pump duration as string with newline

                # Reduce delay for faster responsiveness (optional)
                time.sleep(2)  # Delay before reading sensor data again

try:
    read_sensor_data()

except KeyboardInterrupt:
    ser.close()  # Close the serial connection on Ctrl+C
