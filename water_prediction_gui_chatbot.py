import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pyttsx3

# ========== Voice Engine ==========
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ========== Load & Train ML Model ==========
df = pd.read_csv('water_potability.csv')
df.fillna(df.mean(), inplace=True)

X = df.drop('Potability', axis=1)
y = df['Potability']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# ========== Chatbot ==========
chat_responses = {
    "ph": "pH tells how acidic or basic the water is. Ideal pH is 6.5 to 8.5.",
    "hardness": "Hardness means calcium & magnesium in water. Too much isn't good for pipes.",
    "safe": "If water is potable, it means it's safe to drink.",
    "sulfate": "Sulfates are minerals. High levels can cause stomach issues.",
    "hello": "Hello! Ask me about water parameters like pH, sulfate, etc.",
    "how are you": "I'm great! Ready to help you with water info."
}

def chatbot_response(user_msg):
    msg = user_msg.lower()
    for key in chat_responses:
        if key in msg:
            return chat_responses[key]
    return "Sorry, I don't understand. Ask me about water quality!"

# ========== Prediction Function ==========
def predict_water_quality():
    inputs = [entry.get() for entry in entries]
    labels_range = {
        'pH': (6.5, 8.5),
        'Hardness': (50, 300),
        'Solids': (0, 5000),
        'Chloramines': (0, 4),
        'Sulfate': (0, 400),
        'Conductivity': (0, 600),
        'Organic Carbon': (0, 5),
        'Trihalomethanes': (0, 80),
        'Turbidity': (0, 5)
    }

    try:
        values = [float(val) for val in inputs]
    except:
        messagebox.showerror("Error", "Please enter valid numeric values!")
        speak("Please enter valid numbers")
        return

    for i, val in enumerate(values):
        param = labels[i]
        min_val, max_val = labels_range[param]
        if not (min_val <= val <= max_val):
            msg = f"⚠️ {param} = {val} is outside the safe range ({min_val}-{max_val}).\nWater is NOT safe to drink!"
            messagebox.showwarning("Unsafe Water", msg)
            speak(f"{param} is out of range. Water is not safe to drink.")
            return

    # If all parameters are in safe range, then predict
    sample = np.array([values])
    prediction = model.predict(sample)
    result = "Safe to Drink" if prediction[0] == 1 else "Not Safe to Drink"
    messagebox.showinfo("Prediction", f"✅ All parameters are within range.\nWater is: {result}")
    speak(f"Water is {result}")

# ========== GUI Setup ==========
root = tk.Tk()
root.title("Water Quality + Chatbot + Voice Assistant")
root.geometry("750x700")
root.configure(bg="#F0F8FF")

tk.Label(root, text="Water Quality Prediction", font=("Helvetica", 18, "bold"), bg="#F0F8FF", fg="#1F3A93").pack(pady=20)

# ========== Inputs ==========
labels = ['pH', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 
          'Conductivity', 'Organic Carbon', 'Trihalomethanes', 'Turbidity']
entries = []

input_frame = tk.Frame(root, bg="#F0F8FF")
input_frame.pack()

for i, label in enumerate(labels):
    row = tk.Frame(input_frame, bg="#F0F8FF")
    row.pack(pady=3)
    tk.Label(row, text=label + ":", width=20, anchor='w', font=("Arial", 10), bg="#F0F8FF").pack(side='left')
    entry = tk.Entry(row, width=25)
    entry.pack(side='left')
    entries.append(entry)

tk.Button(root, text="Predict", command=predict_water_quality, bg="#3498DB", fg="white",
          font=("Arial", 12, "bold"), padx=10, pady=5).pack(pady=15)

# ========== Chatbot ==========
tk.Label(root, text="Chat with WaterBot", font=("Helvetica", 14, "bold"), bg="#F0F8FF", fg="#2C3E50").pack(pady=10)

chat_frame = tk.Frame(root, bg="#F0F8FF")
chat_frame.pack()

chat_log = scrolledtext.ScrolledText(chat_frame, width=80, height=8, wrap=tk.WORD, font=("Arial", 10))
chat_log.pack()

user_input = tk.Entry(chat_frame, width=60)
user_input.pack(side='left', padx=5, pady=5)

def handle_chat():
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return
    chat_log.insert(tk.END, "You: " + user_msg + "\n")
    reply = chatbot_response(user_msg)
    chat_log.insert(tk.END, "Bot: " + reply + "\n\n")
    speak(reply)
    user_input.delete(0, tk.END)

tk.Button(chat_frame, text="Send", command=handle_chat, bg="#2ECC71", fg="white", font=("Arial", 10, "bold")).pack(side='left')

root.mainloop()
