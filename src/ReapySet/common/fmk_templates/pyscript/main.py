# main.py
from datetime import datetime
import numpy as np

def main():
    # Generates a simple data sample using NumPy
    data = np.array([10, 20, 30, 40, 50])
    mean_val = np.mean(data)
    
    current_time = datetime.now().strftime("%H:%M:%S")
    
    print(f"[Python Output - {current_time}]")
    print(f"Sample Array: {data}")
    print(f"Calculated Mean: {mean_val}")

if __name__ == "__main__":
    main()
