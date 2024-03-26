from datetime import datetime, timedelta
from collections import defaultdict


# List for dictionary keys, there is no need to put weekend days
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Offset for calculating start of the next weekd
WEEK_MAX_OFFSET = 7


def is_day_weekend(date):
    return True if date.weekday() == 5 or date.weekday() == 6 else False


def get_birthday_per_week(users):
    users_dict = defaultdict(list)
    current_date = datetime.today().date()

    for user in users:
        name = user["name"]
        celebration_day = user["birthday"].date()

        # Change celebration date to actual year
        celebration_day = celebration_day.replace(year=current_date.year)

        celebration_week_start_date = current_date + timedelta(days=WEEK_MAX_OFFSET - current_date.weekday())
        celebration_week_day_offset = (celebration_week_start_date - celebration_day).days

        # If celebration date is older than current, assign it to next year
        # Date year on weekend just before celebration date (in same year) cannot be incremented, because theese dates are assigned to the next week
        if celebration_week_day_offset > 2:    
            celebration_day = celebration_day.replace(year=celebration_day.year + 1)
        
        celebration_day_offset = (celebration_day - celebration_week_start_date).days

        # If the difference is more than 4 (4 == Friday), there is no point for further calculations
        if celebration_day_offset > 4:
            continue
        
        # If the day is on weekend, set it to next Monday
        if(is_day_weekend(celebration_day)):
            celebration_weekend_offset = WEEK_MAX_OFFSET - celebration_day.weekday()
            celebration_day = celebration_day + timedelta(days=celebration_weekend_offset)

        users_dict[WEEK_DAYS[celebration_day.weekday()]].append(name)
    
    if not users_dict:
        return 'No celebration next week :('
    else:
        celebration_string = '\nCelebrations next week:\n'

        for day in WEEK_DAYS:
            if users_dict[day]:
                celebration_string += f'{day:<10}: {', '.join(users_dict[day])}\n'

        
    return celebration_string

