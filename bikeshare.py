import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hi there! Interested in bikeshare data? Let\'s get started!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('\nWhich city data do you want to explore? chicago, new york city or washington? \n')).lower()
        except:
            continue
        #check whether entered value is one of the three city elements in the CITY_DATA dictionary
        if city not in CITY_DATA:
            print('Sorry, I didn\'t understand that! Please enter one of the three city names!')
            continue
        else:
            #one of the three city names was entered correctly
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('\nWhich month (january to june) do you want to explore or do you want to explore all months? \n')).lower()
        except:
            continue
        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print('Sorry, I didn\'t understand that! Please enter all or the name of the month.')
            continue
        else:
            #a valid month or all was entered correctly
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('\nWhich day of the week do you want to explore or do you want to explore all days? \n')).lower()
        except:
            continue
        if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print('Sorry, I didn\'t understand that! Please enter all or the name of the day of the week.')
            continue
        else:
            #a valid day of the week or all was entered correctly
            break
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
    # load data file into a dataframe = Load the dataset for the specified city.
    # Index the global CITY_DATA dictionary object to get the corresponding filename for the given city name.
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe via bracket indexing
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe via bracket indexing
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # find the most common month
    popular_month = df['month'].mode()[0] #Holt den Index (also die Uhrzeit) aus der Pandas Series popular_hour_count
    print('Most common month:', popular_month)


    # display the most common day of week
    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.day

    # find the most common day (from monday to sunday)
    popular_day = df['day'].mode()[0] #Holt den Index (also die Uhrzeit) aus der Pandas Series popular_hour_count
    print('Most common day:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0] #Holt den Index (also die Uhrzeit) aus der Pandas Series popular_hour_count
    print('Most frequent start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    start_station_count = df.groupby(['Start Station'])['Start Time'].count()
    end_station_count = df.groupby(['End Station'])['End Time'].count()
    stations = {'Start Station': start_station_count, 'End Station': end_station_count}
    # create DataFrame from entire list of stations with NaN values set to 0
    stations = pd.DataFrame(stations).fillna(0).astype(int)
    # create merged Pandas Series in DataFrame
    stations.loc[:,'Cumulated Stations'] = stations.loc[:,'Start Station'].add(stations.loc[:,'End Station'])
    most_popular_station = stations['Cumulated Stations'].idxmax()
    print('Most commonly used station:', most_popular_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average travel time:', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('There are {} subscribers and {} customers.'.format(user_types.iloc[0],user_types.iloc[1]))

    # Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        no_gender_data = df['Gender'].isnull().sum()
        print('There are {} male, {} female and {} with no data available.'.format(user_gender.iloc[0],user_gender.iloc[1], no_gender_data))

    # Display earliest, most recent, and most common year of birth

        user_birth_year_earliest = int(df['Birth Year'].min())
        user_birth_year_most_recent = int(df['Birth Year'].max())
        user_birth_year_most_common = df['Birth Year'].mode()
        no_birth_year_data = df['Birth Year'].isnull().sum()
        print('The earliest birth year was in {}, the most recent in {}, the most common year of birth is {} and there are {} with no data available.'.format(user_birth_year_earliest, user_birth_year_most_recent, user_birth_year_most_common.iloc[0],no_birth_year_data))

    else:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def raw_data(df):
    """Displays raw data."""
    raw_data_start = str(input('\nWould you like to see five rows of raw data? (y/n): \n')).lower()
    if raw_data_start == 'y':
        print('\nDisplaying raw data...\n')

        # display five rows of raw data
        print(df.head(5))
        more_raw_data(df)

def more_raw_data(df):
    """Displays more raw data."""
    i = 0
    while True:
        more_data = input('Would you like to see more data? (y/n): ').lower()
        if more_data != 'y':
            break
        else:
            print(df.iloc[i:i+5])
            i += 5

def descriptive_stats(df):
    """Displays descriptive statistics."""
    desc_stats_start = input('\nWould you like to see descriptive statistics? (y/n): \n').lower()
    if desc_stats_start == 'y':
        print('\nCalculating descriptive statistics...\n')

        # display descriptive stats
        desc_stats = df.describe()
        print(desc_stats)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        descriptive_stats(df)

        restart = input('\nWould you like to restart? (y/n): \n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
