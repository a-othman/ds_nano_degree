import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
# , , , , , , , , , , and '

MONTH_2_NUM= {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, \
    'august':8, 'september':9, 'october':10, 'november':11, 'december':12} 

NUM_2_MONTH= {1:'january', 2:'february', 3:'march', 4: 'april', 5:'may', 6:'june', 7:'july', \
    8:'august', 9:'september', 10: 'october', 11:'november', 12:'december'} 

MONTHS= ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', \
        'september', 'october', 'november', 'december']

DAY_2_NUM= {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6 }
NUM_2_DAY= {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday' }
DAYS= ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city= input("\nWould you like to see data for Chicago, New York, or Washington?\n").lower()
        if CITY_DATA.get(city)==None:
            print('Please enter a valid city name (one of the valid names above)')
            continue
        else:
            break
      
    # month_filter= input("Do you want to filter by month?(y/n)").lower()
    # if month_filter=='y':
    # get user input for month (all, january, february, ... , june)
    while True:  
        month= input("\nWhich month (e.g. January)? (Type all if no filter needed\n").lower()
        if month in MONTHS:
            print(f"Looks like you want to filter on {month}")
            break
        elif month=='all':
            print(f"Looks like you don't want a month filter...")
            break
        else:
            print(f"Invalid {month} input, please ensure entering a vlid month")
            continue

    while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day= input("\nWhich day (e.g. Saturday)? Type all if no filter needed\n").lower()
        if day in DAYS:
            print(f"Looks like you want to filter on {day}")
            break
        elif day=='all':
            print(f"Looks like you don't want a day filter...")
            break
        else:
            print(f"Invalid day: {day} input, please ensure entering a vlid day")
            continue

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
    df= pd.read_csv(CITY_DATA[city])
    # casting date objects into datetime
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['End Time']= pd.to_datetime(df['End Time'])

    if month in MONTHS:
        month= MONTH_2_NUM.get(month)
        df= df[df['Start Time'].dt.month==month]
    if day in DAYS:
        df=df[df['Start Time'].dt.dayofweek==DAY_2_NUM[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if df.shape[0]==0:
        print('No filtered data in the selected filters')
        return
    # display the most common month
    most_common_month= df['Start Time'].dt.month.value_counts().sort_values(ascending=False).index[0]
    print(f"Most common month is: {NUM_2_MONTH[most_common_month]}")
    # display the most common day of week
    most_common_dayofweek= df['Start Time'].dt.dayofweek.value_counts().sort_values(ascending=False).index[0]
    print(f"Most common day of the week is: {NUM_2_DAY[most_common_dayofweek]}")
    # display the most common start hour
    most_common_starthour= df['Start Time'].dt.hour.value_counts().sort_values(ascending=False).index[0]
    print(f"Most common start hour is: {most_common_starthour}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if df.shape[0]==0:
        print('No filtered data in the selected filters')
        return
    df['start_end_combination']="start: "+ df['Start Station'] + " end: " + df['End Station']
    
    # display most commonly used start station
    most_common_start_station= df['Start Station'].value_counts().sort_values(ascending=False).index[0]
    freq_most_common_start_station= df['Start Station'].value_counts().sort_values(ascending=False).values[0]
    print(f"Most common start station is: {most_common_start_station} frequency: {freq_most_common_start_station}")

    # display most commonly used end station
    most_common_end_station= df['End Station'].value_counts().sort_values(ascending=False).index[0]
    freq_most_common_end_station= df['End Station'].value_counts().sort_values(ascending=False).values[0]
    print(f"Most common end station is: {most_common_end_station} frequency: {freq_most_common_end_station}")

    # display most frequent combination of start station and end station trip
    most_frquent_combination_start_end_stations= df['start_end_combination'].value_counts().sort_values(ascending=False).index[0]
    freq_most_frquent_combination_start_end_stations= df['start_end_combination'].value_counts().sort_values(ascending=False).values[0]
    print(f"Most frequent combination of start and end is: {most_frquent_combination_start_end_stations} frequency: {freq_most_frquent_combination_start_end_stations}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if df.shape[0]==0:
        print('No filtered data in the selected filters')
        return

    # display total travel time
    print(f"Total travel time is: {df['Trip Duration'].sum()} seconds")

    # display mean travel time
    print(f"Average travel time is: {df['Trip Duration'].mean()} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if df.shape[0]==0:
        print('No filtered data in the selected filters')
        return

    # Display counts of user types
    print(f"Users Type distribution: \n {df['User Type'].value_counts()}")

    # Gender', 'Birth Year
    
    # Display counts of gender
    if 'Gender' in df.columns: 
        print(f"Users Gender distribution: \n{df['Gender'].value_counts()}")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(f"Oldest user was born in: {int(df['Birth Year'].min())}")
        print(f"Youngest user was born in: {int(df['Birth Year'].max())}")
        print(f"Most common year of birth is: {int(df['Birth Year'].value_counts().sort_values(ascending=False).index[0])}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df_generator= (i for i in df.to_dict(orient='records')) #making a generator with all records
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            printing= input("\nwould you like to print row data, enter yes or no?\n")
            if printing=='yes':
                try:
                    for i in range(5):
                        print(f"{next(df_generator)}\n")
                    continue
                except StopIteration:
                    break

            elif printing=='no':
                break
            else:
                print("Invalid input, please write yes or no")
                continue


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
