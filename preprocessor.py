import pandas as pd


def preprocess(data):
    dataset = data[1:]

    cleaned_data = []
    for line in dataset:
        try:
            # grab the info and cut it out
            date = line.split(",")[0]
            line2 = line[len(date):]
            time = line2.split("-")[0][2:]
            line3 = line2[len(time):]
            name = line3.split(":")[0][4:]
            line4 = line3[len(name):]
            message = line4[6:-1]  # strip newline character
            cleaned_data.append([date, time, name, message])
        except Exception as e:
            print(f"Error processing line: {line}")
            print(e)
            cleaned_data.append(["", "", "", ""])  # Append empty values to maintain structure

    print("Cleaned data before date check:", cleaned_data)  # Debugging statement

    dte = []
    for i in range(len(cleaned_data)):
        if cleaned_data[i][0] and cleaned_data[i][0][0].isnumeric() and len(cleaned_data[i][0]) <= 8:
            dte.append(cleaned_data[i][0])
        else:
            cleaned_data[i] = [" "]

    cleaned_data = [i for i in cleaned_data if i != [' ']]

    # print("Cleaned data after date check:", cleaned_data)  # Debugging statement

    days = []
    months = []
    years = []
    for i in range(len(cleaned_data)):
        n_date = cleaned_data[i][0]
        n_date = n_date[:6] + '20' + n_date[6:]
        day = n_date[:2]
        days.append(day)
        month = n_date[3:5]
        months.append(month)
        year = n_date[6:]
        years.append(year)

    for i, n in enumerate(days):
        cleaned_data[i] = cleaned_data[i] + [n] + [months[i]] + [years[i]]

    # Create the DataFrame
    df = pd.DataFrame(cleaned_data, columns=['Date', 'Time', 'Name', 'Message', 'day', 'month', 'year'])
    df = df.dropna()
    df['day'] = df['day'].astype('int')
    df['month'] = df['month'].astype('int')

    df['year'] = df['year'].astype('int')

    df = df.drop(index=0)
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)

    hnt = df['Time'].str.split(":")
    hour = {'hour': []}
    minute = {'minute': []}
    zone = {'zone': []}
    for i in hnt:
        hour['hour'].append(i[0])
        minute['minute'].append(i[1].split()[0])
        zone['zone'].append(i[1].split()[1])
    hour_df = pd.DataFrame(hour)
    zone_df = pd.DataFrame(zone)
    minute_df = pd.DataFrame(minute)
    hour_df['hour'] = hour_df['hour'].astype('int')
    minute_df['minute'] = minute_df['minute'].astype('int')
    df1 = hour_df.copy()  # Using hour_df for demonstration

    # Iterate over rows in hour_df and update based on condition
    for index, row in hour_df.iterrows():
        if zone_df.at[index, 'zone'] == 'pm' and hour_df.at[index, 'hour'] < 12:
            df1.at[index, 'hour'] = hour_df.at[index, 'hour'] + 12
    df = pd.concat([df, df1, minute_df], axis=1)
    df = df.drop(columns=['Date', 'Time'], axis=1)

    # Convert to datetime format
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
    df['month_name'] = df['datetime'].dt.month_name()
    df['date'] = df['datetime'].dt.date
    df['day_name'] = df['datetime'].dt.day_name()

    return df
