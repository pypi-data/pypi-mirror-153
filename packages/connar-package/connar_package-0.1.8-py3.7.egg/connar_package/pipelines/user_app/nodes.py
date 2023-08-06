import pandas as pd

def predict(instances: pd.DataFrame, model):
    alphas = model.predict(instances)

    # todo: move this to the feature package
    if len(alphas) == 0:
        alphas = pd.DataFrame(columns=['Prediction', 'Signal'])
        alphas.index.name = "Timestamp"
        return alphas

    return alphas
