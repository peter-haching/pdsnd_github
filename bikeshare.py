import time
import pandas as pd
import numpy as np

# variable definitons

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
MONTH_DATA = { 'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'all': 99 }
DAY_DATA = { 'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6, 'Mon-Fri': 97, 'Sat-Sun': 98, 'all': 99 }
REVERSE_MONTH = { 1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June' }
REVERSE_DAY = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }

#functions



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - number of the month to filter by, or "all" to apply no month filter
        (int) day - number of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    city = ""
    month = ""
    day = ""

    # getting user input - city
    while city not in ['Chicago','New York','New York City','Washington']:
        city = input('Which city would you like to explore - Chicago, New York City, or Washington? ')
        if city == 'New York':
            city = 'New York City'
        if city in ['Washington D. C.', 'Washington, D. C.', 'Washington DC', 'DC']:
                city = 'Washington'
        if city not in ['Chicago','New York','New York City','Washington']:
            print('\nSorry, that does not look like one of the available cities.')

    # getting user input - month
    month_input = ""
    print('\nWhich month should we look at?')
    while month_input not in ['Jan','Feb','Mar','Apr','May','Jun','all']:
        month_input = input('Please enter the first three letters of the month ("Jan", "Feb" etc. through "Jun") or "all". > ')
        if month_input not in ['Jan','Feb','Mar','Apr','May','Jun','all']:
            print('\nSorry, that is not one of the available choices.')
    month = MONTH_DATA[month_input]

    # getting user input - day of week
    day_input = ""
    print('\nWhich day of the week should we look at?')
    while day_input not in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun','Mon-Fri','Sat-Sun','all']:
        day_input = input('Please enter the first three letters of the day (Mon, Tue, etc.), "Mon-Fri", "Sat-Sun", or "all". > ')
        if day_input not in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun','Mon-Fri','Sat-Sun','all']:
            print('\nSorry, that is not one of the available choices.')
    day = DAY_DATA[day_input]

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - number of the month to filter by
        (int) day - number of the day of week to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # creating full dataframe
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour
    df['Trip'] = df['Start Station'] + ' <=> ' + df['End Station']

    # filtering dataframe by month and day of week
    if month < 7:
        df = df[df.Month == month]
    if day < 7:
        df = df[df.Weekday == day]
    elif day == 97:
        df = df[df.Weekday < 5]
    elif day == 98:
        df = df[df.Weekday > 4]

    return df



def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.

    Args:
    (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    (int) month - number of the month to filter by
    (int) day - number of the day of week to filter by

"""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month:')
    if month == 99:
        print('   ' + REVERSE_MONTH[df['Month'].mode()[0]])
    else:
        print('   You selected only a single month.')

    # display the most common day of week
    print('Most common day of the week:')
    if day > 96:
        print('   ' + REVERSE_DAY[df['Weekday'].mode()[0]])
    else:
        print('   You selected only a single day of the week.')

    # display the most common hour
    print('Most common hour of the day:')
    hour_string = str(df['Hour'].mode()[0])
    print('   ' + hour_string + ':00 to ' + hour_string + ':59')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Arg:
    (dataframe) df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most frequently used start station:')
    print('   ' + df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most frequently used end station:')
    print('   ' + df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most frequently used trip (combined start/end stations):')
    print('   ' + df['Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Arg:
    (dataframe) df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    full_time_seconds = int(round(df['Trip Duration'].sum()))
    full_time_format = '00:00:00'
    full_time_format = pd.to_timedelta(full_time_seconds, unit='seconds')
    print('Total travel time:')
    print('   ' + str(full_time_seconds) + ' seconds, or ' + str(full_time_format))

    # display mean travel time
    mean_time_seconds = int(round(df['Trip Duration'].mean()))
    mean_time_format = '00:00:00'
    mean_time_format = pd.to_timedelta(mean_time_seconds, unit='seconds')
    print('Mean travel time:')
    print('   ' + str(mean_time_seconds) + ' seconds, or ' + str(mean_time_format))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users.

    Args:
    (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    (str) city - name of the city to analyze

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print('User type breakdown:')
    user_types = df['User Type'].value_counts()
    print(user_types)

    # display counts of gender (or non-availability message for Washington)
    if city == 'Washington':
        print('\nNo further personal stats on bikeshare users are available for this city.\n')
    else:
        print('\nGender breakdown:')
        user_gender = df['Gender'].value_counts()
        print(user_gender)

    # display earliest, most recent, and most common year of birth (not for Washington)
    if city != 'Washington':
        most_common_year = int(df['Birth Year'].mode()[0])
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())

        print('\nMost common year of birth:')
        print('   ' + str(most_common_year))
        print('Earliest year of birth:')
        print('   ' + str(earliest_year))
        print('Most recent year of birth:')
        print('   ' + str(most_recent_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def raw_data_display(df, city):
    """Allows the user to view the raw data used.

    Args:
    (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    (str) city - name of the city to analyze

    """
    # limit scope (c) to the original columns
    i = 0
    if city == 'Washington':
        c = 7
    else:
        c = 9

    # display raw data in five-line steps if desired
    raw_choice = ""
    raw_choice = input('Would you like to see the raw data for this analysis (5 rows at a time)? Enter yes or no. > ')

    while raw_choice.lower() == 'yes' or raw_choice.lower() == 'y':
        print(df.iloc[i:(i + 5), 0:c])
        raw_choice = input('\nEnter "y" to continue, anything else to abort. > ')
        i += 5



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data_display (df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
