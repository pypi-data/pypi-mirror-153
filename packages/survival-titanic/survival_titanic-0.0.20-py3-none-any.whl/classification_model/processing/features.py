import re

from sklearn.base import BaseEstimator, TransformerMixin


class ExtractLetterTransformer(BaseEstimator, TransformerMixin):
    # Extract fist letter of variable

    def __init__(self, variables):
        if not isinstance(variables, str):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X[self.variables] = X[self.variables].str[0]

        return X


class ExtractSalutationTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, variables):
        if not isinstance(variables, list):
            raise ValueError("variables should be a string")

        self.variables = variables

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        salutation = list()
        for line in X[self.variables[0]]:
            if re.search("Mrs", line):
                salutation.append("Mrs")
            elif re.search("Mr", line):
                salutation.append("Mr")
            elif re.search("Miss", line):
                salutation.append("Miss")
            elif re.search("Master", line):
                salutation.append("Master")
            else:
                salutation.append("Other")

        X[self.variables[1]] = salutation
        X.drop([self.variables[0]], axis=1, inplace=True)

        return X
