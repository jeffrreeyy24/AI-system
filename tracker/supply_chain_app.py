import tkinter as tk
from tkinter import ttk, messagebox
from blockchain import Blockchain
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import IsolationForest
import time
import random



class SupplyChainAIApp:
    def __init__(self, root):
        self.blockchain = Blockchain()
        self.root = root
        self.root.title("Blockchain Supply Chain Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        header = tk.Label(self.root, text="AI Supply Chain Tracker", bg="#004d99", fg="white", font=("Arial", 24))
        header.pack(fill=tk.X)

        self.add_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.add_frame.pack(pady=20)

        tk.Label(self.add_frame, text="Shipment Data:", bg="#f5f5f5", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.data_entry = tk.Entry(self.add_frame, width=40, font=("Arial", 12))
        self.data_entry.grid(row=0, column=1, padx=5)

        add_button = tk.Button(self.add_frame, text="Add Block", bg="#28a745", fg="white", font=("Arial", 12),
                               command=self.add_block)
        add_button.grid(row=0, column=2, padx=5)

        ai_button = tk.Button(self.root, text="AI Prediction & Validation", bg="#007bff", fg="white",
                              font=("Arial", 12), command=self.predict_and_validate)
        ai_button.pack(pady=10)

        # Frame for blockchain visualization
        self.chain_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.SOLID)
        self.chain_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        tk.Label(self.chain_frame, text="Blockchain Visualization:", bg="white", font=("Arial", 14)).pack(anchor="w",
                                                                                                          padx=10)
        self.chain_text = tk.Text(self.chain_frame, wrap=tk.WORD, font=("Courier", 10), state=tk.DISABLED, height=20)
        self.chain_text.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.update_chain_display()

    def add_block(self):
        data = self.data_entry.get()
        if data.strip():
            self.blockchain.add_block(data)
            self.data_entry.delete(0, tk.END)
            self.update_chain_display()
            messagebox.showinfo("Success", "New block added successfully!")
        else:
            messagebox.showwarning("Input Error", "Shipment data cannot be empty.")

    def update_chain_display(self):
        self.chain_text.configure(state=tk.NORMAL)
        self.chain_text.delete("1.0", tk.END)
        for block in self.blockchain.chain:
            block_details = (
                f"Index: {block.index}\n"
                f"Timestamp: {time.ctime(block.timestamp)}\n"
                f"Data: {block.data}\n"
                f"Previous Hash: {block.previous_hash}\n"
                f"Hash: {block.hash}\n{'-' * 50}\n"
            )
            self.chain_text.insert(tk.END, block_details)
        self.chain_text.configure(state=tk.DISABLED)

    def predict_and_validate(self):

        # 1. Predictive Analytics: Predict delays in shipment (using RandomForestRegressor)
        shipment_data = self.collect_shipment_data()

        if len(shipment_data) > 1:
            prediction = self.predict_shipment_delay(shipment_data)
            messagebox.showinfo("Prediction", f"Predicted delay: {prediction} days")

        # 2. Anomaly Detection: Detect any anomalies in the shipment data (using IsolationForest)
        anomalies = self.detect_anomalies(shipment_data)
        if anomalies:
            messagebox.showwarning("Anomaly Detected", "Anomalies found in shipment data!")
        else:
            messagebox.showinfo("Validation", "No anomalies detected in the shipment data.")

        # Blockchain Validation (same as before)
        self.validate_chain()

    def collect_shipment_data(self):
        # Collecting some random shipment data for AI analysis (In real life, this would come from the blockchain)
        # For the sake of the example, we simulate some past shipment data with delays
        data = []
        for i in range(50):
            shipment = {
                'shipment_id': i,
                'distance': random.randint(50, 1000),  # in km
                'shipment_time': random.randint(1, 5),  # in days
                'weather': random.choice(['Clear', 'Rainy', 'Stormy']),
                'delay': random.randint(0, 3),  # predicted delay in days
            }
            data.append(shipment)
        return pd.DataFrame(data)

    def predict_shipment_delay(self, shipment_data):
        # Using a RandomForestRegressor model to predict shipment delays
        features = shipment_data[['distance', 'shipment_time']]
        target = shipment_data['delay']

        model = RandomForestRegressor()
        model.fit(features, target)
        predicted_delay = model.predict([[100, 3]])  # Sample input for prediction (100 km, 3 days shipment time)

        return predicted_delay[0]

    def detect_anomalies(self, shipment_data):
        # Using IsolationForest to detect anomalies in shipment data
        features = shipment_data[['distance', 'shipment_time', 'delay']]

        model = IsolationForest()
        model.fit(features)
        predictions = model.predict(features)

        anomalies = [i for i, x in enumerate(predictions) if x == -1]

        return anomalies

    def validate_chain(self):
        is_valid = self.blockchain.is_chain_valid()
        if is_valid:
            messagebox.showinfo("Validation Result", "The blockchain is valid!")
        else:
            messagebox.showerror("Validation Error", "The blockchain is invalid!")
root = tk.Tk()
app = SupplyChainAIApp(root)
root.mainloop()
