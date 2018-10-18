import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def new_super_fast_function():
    """
    A incredible new way to to the calculations
    """
    print(f'MATH: {5+5}')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input(
            'Please select which City you wanna check (Chicago, New York City or Washington):\n').lower()
        if (city in CITY_DATA):
            break
        print('Sorry, City not recognized. Please try again')

    while True:
        month = input(
            'Please define the month you want information for (or all for all of them), currently we have the Data for January to June:\n').lower()
        if (month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']):
            break
        print('Sorry, Month not recognized. Please try again')

    while True:
        day = input(
            'Please define the month you want information for (or all for all of them):\n').lower()
        if (day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']):
            break
        print('Sorry, Day not recognized. Please try again')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, hour and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # using Start and End Station to create a new Combined Station Column
    df['Combined Station'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print(f'The most common month is: {common_month}')

    common_dow = df['day_of_week'].mode()[0]
    print(f'The most common day of the week is: {common_dow}')

    common_hour = df['hour'].mode()[0]
    print(f'The most hour is: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start = df['Start Station'].mode()[0]
    print(f'The most common Start Station is: {common_start}')

    common_end = df['End Station'].mode()[0]
    print(f'The most common End Station is: {common_end}')

    common_combination_start_end = df['Combined Station'].mode()[0]
    print(
        f'The most common combination of Start and End Stations is: {common_combination_start_end}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum()/60
    print(f'The Total Travel Time in Minutes is: {total_travel:.2f}')

    mean_travel = df['Trip Duration'].mean()/60
    print(f'The Mean Travel Time in Minutes is: {mean_travel:.2f}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(f'The different User Types are:\n{user_types}\n')

    if ('Gender' in df.columns) and ('Birth Year'in df.columns):
        genders = df['Gender'].value_counts()
        print(f'The counts of the different genders are:\n{genders}\n')

        earliest_birth_year = df['Birth Year'].min()
        print(f'The earliest Birth year is: {earliest_birth_year:.0f}')

        recent_birth_year = df['Birth Year'].max()
        print(f'The most recent birth year is: {recent_birth_year:.0f}')

        common_birth_year = df['Birth Year'].mode()[0]
        print(f'The most common birth year is: {common_birth_year:.0f}')

    else:
        print('\nThere are no Information about Genders or Birth Years available for the selected City. Sorry')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Asks User if he wants to see raw data of the selected City.
    In packages of 5 rows.
    """
    start = 0

    while True:
        more = ' more' if start > 0 else ''
        user_answer = input(
            f'Would you like to see some{more} raw data (5 rows)? Answer yes or no:\n').lower()

        if user_answer != 'yes':
            break

        print(df[start:start+5])
        start += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
