class Validate:
    @staticmethod
    def is_numeric(value, min=None, max=None):
        if not str(value).isnumeric():
            return False
        is_min_numeric = str(min).isnumeric()
        is_max_numeric = str(max).isnumeric()
        if is_min_numeric and is_max_numeric:
            return value >= min and value <= max
        elif is_min_numeric:
            return value >= min
        elif is_max_numeric:
            return value <= max
        return True