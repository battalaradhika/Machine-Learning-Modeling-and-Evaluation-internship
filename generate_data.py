import pandas as pd
import numpy as np

np.random.seed(42)

n = 10000

# realistic random walk (UP + DOWN movement)
price = 100 + np.cumsum(np.random.randn(n))

df = pd.DataFrame({
    "open": price + np.random.randn(n),
    "high": price + abs(np.random.randn(n)),
    "low": price - abs(np.random.randn(n)),
    "close": price,
    "volume": np.random.randint(1000, 5000, n)
})

df.to_csv("data.csv", index=False)

print("data.csv generated with 10000 rows")