from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import numpy as np

data = pd.DataFrame.from_dict({
    'x1': np.random.randint(low=1, high=10, size=5),
    'x2': np.random.randint(low=1, high=10, size=5),
    'x3': np.random.randint(low=1, high=10, size=5),
    'x4': np.random.randint(low=1, high=10, size=5),
    # 'y': np.random.randint(low=-1, high=1, size=5),
})

p = PolynomialFeatures(degree=2).fit(data)
print(p.get_feature_names(data.columns))

