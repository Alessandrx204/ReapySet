# main.py
from datetime import datetime
import numpy as np
import numpy.typing as npt

def main() -> None:
    # Generates a simple data sample using NumPy
    data: npt.NDArray[np.int_] = np.array([10, 20, 30, 40, 50])
    mean_val: np.float64 = np.mean(data)
    
    current_time: str = datetime.now().strftime("%H:%M:%S")
    
    print(f"[Python Output - {current_time}]")
    print(f"Sample Array: {data!s}")
    print(f"Calculated Mean: {mean_val}")

if __name__ == "__main__":
    main()
