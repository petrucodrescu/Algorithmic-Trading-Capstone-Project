from sklearn.preprocessing import StandardScaler
from hmmlearn.hmm import GaussianHMM
import numpy as np


def detect_regimes(data, features):
    """
    Detect market regimes using Gaussian Hidden Markov Model (HMM).

    Args:
        data (DataFrame): Data containing relevant features.
        features (list): List of feature column names to use for regime detection.

    Returns:
        DataFrame: Updated DataFrame with a 'Regime' column.
        GaussianHMM: Trained HMM model.
    """

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data[features].dropna())

    model = GaussianHMM(n_components=3, covariance_type='diag', n_iter=1000, random_state=42)
    model.fit(scaled_features)

    data['Regime'] = np.nan
    regimes = model.predict(scaled_features)
    data.loc[data[features].dropna().index, 'Regime'] = regimes

    return data, model
