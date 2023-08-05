import warnings

import banner.pandas_decorator

warnings.filterwarnings("ignore", message="Pandas doesn't allow columns to be created via a new attribute name")