import time
import pandas as pd
import numpy as np
import math

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('_.~"~.'*10)
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    print("Let's get started: Which city's data would you like to explore?\n")
    city = ""
    while city == "":
        # catching weird errors
        try:
            city = input('Type "C" for Chicago, "N" for New York City or "W" for Washington.\n').lower()
        except:
            print('Looks like something went wrong. Enter only a single letter please\n')
            continue
        # check whether the answer is acceptable
        if city in ["c", "n", "w"]:
            cities = {"c": "Chicago", "n": "New York City", "w":"Washington"}
            print("Awesome you chose {}, what a nice city!".format(cities[city]))
            city = cities[city].lower()
        else:
            print("You seem to have entered something else, please try again, with a single letter\n")
            city = ""

    # get user input for month (all, january, february, ... , june)
    print("\n")
    print("-"*40)
    print("Now that we have a city lets look at the months\n")
    month = ""
    # dictionary to translate the numbers
    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:"July", 8:"August", 9:"September",10:"Oktober",11:"November", 12:"December"}
    print('Please type a number from 1 to 6 depending on which month you want to look at. There is sadly no data from July to December\n\
If you want to look at all months enter "all"\n')
    while month == "":
        month = input()
        if month =="all":
            print("Ok, let's look at all months.")
            break
        try:
            if int(month) <= 6 and int(month)>0:
                print("Ok, lets look only at {}.\n".format(months[int(month)]))
            else:
                print("Please enter a number between 1 and 6 or 'all'\n")
                month = ""
        except:
            print("Looks like that wasn't a number or the word 'all'. Please try again.")
            month = ""



    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\n")
    print("-"*40)
    print("Now that we have a month lets look at the days\n")
    day = ""
    while day == "":
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        days_verb = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        week = dict(zip(days, days_verb))

        day = input('Please enter the first two letters of the weekday you want to look at.\n\
If you want to look at all days enter "all"\n')
        if day == "all":
            print("Ok, let's look at all days.")
            return city, month, day
            break
        try:
            if day.title() in days:
                print("Ok, lets look only at {}.\n".format(week[day.title()]))
            else:
                print("Mmh that doesn't look like a day to me. :/\n")
                day = ""
        except:
            print("\nWhoops, I'm expecting two letters of a weekday or 'all'.")
            day = ""

    print('-'*40)

    return city, month, week[day.title()]

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
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month = months.index(month.lower())+1
        #print(month)
        # filter by month to create the new dataframe

        df = df[df["month"] == int(month)]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    # Get a column with the start time
    df['Start Time'] = pd.to_datetime(df["Start Time"], dayfirst = True)
    # extract hour from the Start Time column to create an hour column
    df['hour'] =df["Start Time"].dt.hour

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "all":
        print("Calculating the most common month:")
        common_month = df.month.value_counts().idxmax()
        months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:"July", 8:"August", 9:"September",10:"Oktober",11:"November", 12:"December"}
        print("~~~~~~~")
        print("The most common month is {}".format(months[common_month]))
        print("~~~~~~~\n")
    else:
        print("Calculation of month is skipped because 'all' wasn't selected.\n")



    # display the most common day of week
    if day == "all":
        print("Calculating the most common day:")
        common_day = df.day_of_week.value_counts().idxmax()
        print("~~~~~~~")
        print("The most common day is {}".format(common_day))
        print("~~~~~~~\n")
    else:
        print("Calculation of day is skipped because 'all' wasn't selected.\n")

    # display the most common start hour
    print("Calculating the most common hour:")
    # convert the Start Time column to datetime

    # find the most common hour (from 0 to 23)

    try:
        common_hour = df.hour.value_counts().idxmax()
        print("~~~~~~~")
        print("The most common hour is {}".format(common_hour))
        print("~~~~~~~\n")
    except:
        print("There are no rentals for your filters.")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station= df["Start Station"].value_counts().idxmax()
    visits = df["Start Station"].value_counts().max()
    print("~~~~~~~")
    print("The most commonly used start station is {} with {} visits".format(station, visits))

    # display most commonly used end station
    end_station= df["End Station"].value_counts().idxmax()
    end_visits = df["End Station"].value_counts().max()
    print("The most commonly used end station is {} with {} visits".format(end_station, end_visits))

    # display most frequent combination of start station and end station trip
    #Create a column with start and end stations
    df["Combination"] = df["Start Station"] + " to "+ df["End Station"]
    comb_station= df["Combination"].value_counts().idxmax()
    comb_visits = df["Combination"].value_counts().max()
    print("The most commonly combination of start and end station is {} with {} visits".format(comb_station, comb_visits))
    print("~~~~~~~")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_time = df["Trip Duration"].sum()/3600
    tot_time = round_half_up(tot_time, 2)
    print("~~~~~~~")
    print("The total travel time is {} hours".format(tot_time))
    # display mean travel time
    travel_count = len(df["Trip Duration"])
    #Calculating average and converting back to minutes
    mean = round_half_up(tot_time*60/travel_count,2)
    print("The average travel time is {} minutes".format(mean))
    print("~~~~~~~")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = df["User Type"].unique()
    print("~~~~~~~")
    print("There are {} user types:\n".format(len(types)))
    for type in types:
        amount_type = len(df[df["User Type"]==type])
        print(" {} {}".format(amount_type, type))
    print("~~~~~~~")
    # Display counts of gender
    try:
        genders = df["Gender"].unique()
        print("There are {} genders:\n".format(len(genders)))
        for gender in genders:
            amount_gender = len(df[df["Gender"]==gender])
            print(" {} {}".format(amount_gender, gender))
        print("~~~~~~~")
    except:
        print("No available data on genders for the chosen city.")
        print("~~~~~~~")
    # Display earliest, most recent, and most common year of birth
    try:
        min_birth = int(df["Birth Year"].min())
        max_birth = int(df["Birth Year"].max())
        com_birth = int(df["Birth Year"].value_counts().idxmax())
        print("The oldest customer was born in {} the youngest customer was born in {} and the most common birth year is {}.".format(min_birth, max_birth, com_birth))
    except:
        print("No available data on birth years for the chosen city.")
    print("~~~~~~~")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_me_what_you_got(df):
    """ Displays 5 rows of raw data each time the user prompts the program
    to do so """
    answer = input("Would you like to see some raw data? (y/n)\n")
    start=0
    while str(answer.lower()).startswith("y"):
        stop=start+5
        print(df.iloc[start:stop])
        start=stop
        answer = input("Do you want to see more raw data? (y/n)\n")




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        time.sleep(1)
        station_stats(df)
        time.sleep(1)
        trip_duration_stats(df)
        time.sleep(1)
        user_stats(df)
        time.sleep(1)
        show_me_what_you_got(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('_.~"~.'*10)
            break


if __name__ == "__main__":
	main()
