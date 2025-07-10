# utils.py

import pandas as pd
from typing import List, Dict

def save_to_csv(data: List[Dict], filename: str) -> None:
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
