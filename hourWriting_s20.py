import pandas as pd
import numpy as np
import datetime
import argparse
import os.path
import sys


def get_week_number():
    current_week = datetime.date.today().isocalendar()[1]
    current_date = datetime.date.today()
    parser = argparse.ArgumentParser(description="Enter the week number you wish to update: ")
    parser.add_argument('Week number', metavar="Week", type=int, help = "Week number you wish to update, for current date, use 0.")
    parser.add_argument('--date', action='store_true', help="Do you wish to change data for an other date?")
    parser.add_argument('--show', action='store_true', help="Show the data frame containing work hours")
    parser.add_argument('--summary', action='store_true', help='Show summary data')
    args = parser.parse_args()
    week = vars(args)['Week number']
    date = current_date
    if vars(args)['show']:
        show_df()
        sys.exit()
    if vars(args)['summary']:
        show_summary()
        sys.exit()
    if vars(args)['date']:
        try:
            month = int(input("Enter month: "))
            day = int(input("Enter day: "))
            date = datetime.date(2020, month, day)
            print(date)
        except:
            print("Need integer type")


    if week == 0:
        week = current_week

    input('\n \n Updating hours for week {}.\n\n Press <Enter> to continue \n \n  '.format(week))

    return week, date


def show_df():
    df = pd.read_csv('/home/ida/Dropbox/NTNU/10.semester/annet/hours_s20.csv', index_col=0)
    pd.set_option('display.max_columns', 40)
    print(df)
    return

def show_summary():
    df = pd.read_csv('/home/ida/Dropbox/NTNU/10.semester/annet/hours_s20.csv', index_col=0)
    df["Date"] = df.index
    format = '%Y-%m-%d %H:%M:%S'
    df["Date"] = pd.to_datetime(df["Date"], format=format)
    df = df.set_index(pd.DatetimeIndex(df["Date"]))
    df.drop(["Date"], axis=1, inplace=True)


    summary_df = pd.DataFrame(columns=['week', 'total hours'], index=None)
    # TODO: Aggregate totals for each week
    weekly_df = df.resample('W').sum().reset_index()
    weekly_df.index = weekly_df["Date"].dt.week
    weekly_df.drop(["Date"],axis=1, inplace=True)
    weekly_df.index = weekly_df.index.rename("Week")


    # TODO: Aggregate daily mean for each week and total (Mon-Fri)
    # TODO: Aggregate total sum for each column

    print("\n")
    print("Printing full DataFrame: ")
    summary_df['week'] = weekly_df.index.values
    summary_df['total hours'] = weekly_df.sum(axis=1).values
    summary_df = summary_df.set_index('week')
    print(df)
    print("\n")
    print("Printing summary: ")
    print(summary_df)
    print("\n")
    print(df.sum())
    weekly_df["Daily mean"] = weekly_df.sum(axis=1) / 5
    weekly_df.loc[weekly_df.index.values[-1]]["Daily mean"] = 0
    last_date = np.sort(df.index.values, axis=0)[-1]
    last_date = (last_date - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    last_date = datetime.datetime.utcfromtimestamp(last_date)
    weekly_df.loc[weekly_df.index.values[-1]]["Daily mean"] = weekly_df.loc[weekly_df.index.values[-1]].sum() / min(5,last_date.isoweekday())
    print("\n")
    print(weekly_df)
    pd.set_option('display.max_columns', 40)
    return

def get_hour_data(cols):
    hour_data = np.zeros((1, len(cols)))

    for index, val in enumerate(cols):
        try:
            hours = float(input('How many hours have you worked with: {}\t'.format(val)))
            hour_data[0, index] = hours
        except:
            print("Please enter integer or float type")
    return hour_data

def record_hours(hours, cols, date):
    df = pd.DataFrame(data=None, columns=cols)

    hour_data = np.zeros((1, len(cols)))
    # hour_data[0, 0] = date
    hour_data[0, 1:] = hours
    hour_df = pd.DataFrame(data=hour_data, columns=cols)
    hour_df["Date"] = date
    hour_df.set_index('Date', inplace=True)
    df = df.append(hour_df, sort=True).copy()
    df.drop(columns='Date', inplace=True)

    return df

def save_to_file(df, filename, week):
    hours = df.values[0]
    if not os.path.exists(filename):
        df.to_csv(filename)
        print(df)
        return None
    csv_df = pd.read_csv(filename, index_col=0)
    if str(date) in np.unique(csv_df.index.values):
        new_hours = (csv_df.loc[str(date)].values + hours)

        csv_df.loc[str(date)] = new_hours
    else:
        csv_df = csv_df.append(df).copy()
    try:
     csv_df = csv_df.sort_index()
    except:
        print("Could not sort")
        print("Data is added to df")
        input("Press <Enter> to continue")
    csv_df.to_csv(filename)
    return None

if __name__=='__main__':

    cols = ["Date", "TMA4900 Masteroppgave", "Other projects"]
    week, date = get_week_number()
    hours = get_hour_data(cols[1:])
    df = record_hours(hours, cols, date)
    filename = '/home/ida/Dropbox/NTNU/10.semester/annet/hours_s20.csv'
    save_to_file(df, filename, week)


