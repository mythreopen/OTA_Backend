import re

# # Cleans the accessioner names
# # Allows for easier relational mapping later on.


def clean_names(name):
    return re.sub(' +', ' ', re.sub('\(([^\)]+)\)', '', name.replace('*', '')).rstrip())


def convert_name_to_number(nameDateTime) -> str:
    """Convert 'Month - Day' format into 'MM/DD' format.

    Parameters
    ----------
    nameDateTime: `str`
        Incoming string which is in the 'Month - Date' format.


    Returns 
    -------
    monthDateTime: `str`
        Outgoing string which is converted into the 'MM/DD' format.

    Examples
    --------
    nameDateTime: `str`
        ['30-Jan', '31-Jan', '1-Feb']
    numericalDateTime: `str`
        ['1/30', '1/31', '2/1']
    """
    # If the nameDateTime is already in
    # Numerical MM/DD format then return.
    if "/" in nameDateTime:
        return nameDateTime
    elif not("-" in nameDateTime) or nameDateTime == "--":
        return nameDateTime

    # Get the date time, set it to lowercase
    # and split it into  day and month for
    # further parsing.
    day, month = nameDateTime.lower().split("-")

    # dateTimeDict to convert the month names to month numbers.
    dateTimeDict = {
        'jan': "1",
        'feb': "2",
        'mar': "3",
        'apr': "4",
        'may': "5",
        'jun': "6",
        'jul': "7",
        'aug': "8",
        'sep': "9",
        'oct': "10",
        'nov': "11",
        'dec': "12",
    }

    # Return the string in
    # MM/DD format
    return f"{dateTimeDict[month]}/{day}"


def convert_name_to_shift(acc_name, schedule):
    for shift in schedule:
        schedule_name = shift["schedule"]
        schedule_employees = shift["employees"]

        for employee_name in schedule_employees:
            if acc_name == employee_name:
                return schedule_name

    return "Non-Accessioner"


def search_shift_person(shift_data, name):
    return [person for person in shift_data if name == person]


def clean_atr_name(name):
    # Remove surname from name in order to use it
    # in comparison to the shifts list.
    name_surname_removal = name.replace(
        "Ms. ", "").replace("Mr. ", "").replace("Dr. ", "")

    # Split name into two parts, in the atr menus the format is:
    # "SURNAME. LAST_NAME, FIRST_NAME"
    # We are importing it to:
    # "FIRST_NAME LAST_NAME"
    name_split = name_surname_removal.split(',')

    # Check for instances where the string itself
    # does not get parsed due to the comma not appearing.
    if len(name_split) < 2:
        name_split = name_split[0].split(" ")
        return f"{name_split[0]} {name_split[1]}".strip().title()

    return f"{name_split[1]} {name_split[0]}".strip().title()


def name_fix(name):
    if name == "Jasmin Garcia\n5:00AM-1:30PM":
        return "Jasmin Garcia"
    elif name == "Jia Zhong":
        return "Jiabao Zhong"

    return name


def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1:
            return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:, 1:]) for k, g in grouped}
    return d
