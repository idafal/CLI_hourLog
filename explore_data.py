import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn")

df = pd.read_csv("hours_s20.csv")
dates = df[df.columns.values[0]].values
print(df)

def plot_total(df):
    names = df.columns.values[1:]
    print(names)
    plt.bar(x=names, height=df.sum()[1:])
    plt.ylabel("Hours")
    plt.title("Total hours worked during semester", fontsize=15)
    plt.show()
    return None
plot_total(df)

def get_weekly_aggregates(df):
    df = pd.read_csv('/home/ida/Dropbox/NTNU/10.semester/annet/hours_s20.csv', index_col=0)
    df["Date"] = df.index
    format = '%Y-%m-%d %H:%M:%S'
    df["Date"] = pd.to_datetime(df["Date"], format=format)
    df = df.set_index(pd.DatetimeIndex(df["Date"]))
    df.drop(["Date"], axis=1, inplace=True)
    weekly_df = df.resample('W').sum().reset_index()
    weekly_df.index = weekly_df["Date"].dt.week
    weekly_df.drop(["Date"],axis=1, inplace=True)
    weekly_df.index = weekly_df.index.rename("Week")
    return weekly_df


def plot_progress(df):
    df = get_weekly_aggregates(df)
    weeks = df.index.values
    names = df.columns.values
    names=reversed(names)
    fill = 0.85
    print("Weeks", df["TMA4900 Masteroppgave"].mean())
    for course in names:
        plt.fill_between(weeks, y1=df[course], y2=0, alpha=fill, label="{}".format(course))
        fill -= .15
    plt.plot(weeks,[df["TMA4900 Masteroppgave"].mean()] * len(weeks), marker="o", color="grey",alpha=0.5, label="Weekly mean TMA4900 = {}".format(round(df["TMA4900 Masteroppgave"].mean(), 2)))
    plt.legend()
    plt.xlabel("Week", fontsize=12)
    plt.ylabel("Hours", fontsize=12)
    plt.title("Distribution of weekly hours worked", fontsize=15)
    plt.show()

plot_progress(df)

def plot_total_weeks(df):
    df = get_weekly_aggregates(df)
    weeks = df.index.values
    names = df.columns.values
    names=reversed(names)
    fill = 0.95
    total = 0
    for course in names:
        total += df[course]
    plt.plot(weeks, total, alpha=fill, marker=".")
    plt.xlabel("Week", fontsize=12)
    plt.ylabel("Hours", fontsize=12)
    plt.title("Total weekly hours worked", fontsize=15)
    plt.show()



plot_total_weeks(df)