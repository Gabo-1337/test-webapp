import re

def validate_float(value):
    # * Validates a float value, used in 
    value = value or ""
    try:
        float(value)
        if value.startswith("0.") and re.match(r"[0-9]{1,4}\.[0-9]{1,2}$", value):
            if len(value) > 4:
                return False
            else:
                return True
        else:
            return False
    except ValueError:
        return False


def validate_integer(value):
    # * validates an integer, used in number_project_cpf_input
    value = value or ""
    try:
        int(value)
        if 1 <= int(value) <= 10:
            return True
        else:
            return False
    except ValueError:
        return False


def validate_float_range(value):
    # * Validates a float value within a range, used in average_monthly_hours_cpf_input
    value = value or ""
    try:
        float(value)
        if 1 <= float(value) <= 310:
            return True
        else:
            return False
    except ValueError:
        return False


def validate_integer_range(value):
    # * Validates a integer value within a range, used in time_spend_company_cpf_input
    value = value or ""
    try:
        int(value)
        if 1 <= int(value) <= 10:
            return True
        else:
            return False
    except ValueError:
        return False
