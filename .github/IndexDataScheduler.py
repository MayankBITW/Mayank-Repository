#pip install nselib
import os
from datetime import datetime, timedelta, date
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import holidays
import schedule
import time
from nselib import capital_market


def fetch_and_save_index_data():
    try:
        output_file = "Index_Daily_data.csv"
        in_holidays = holidays.India()
        business_days = CustomBusinessDay(holidays=in_holidays)

        first_date = date(2024, 1, 1)
        today = date.today()
        diff = (today - first_date).days
        end = today
        start = today - timedelta(days=diff)

        Indexlist = capital_market.fno_index_list()
        Indexlist = Indexlist['underlying']

        if os.path.exists(output_file):
            pd.read_csv(output_file).iloc[0:0].to_csv(output_file, index=False)
            print(f"Data deleted successfully: {output_file}")

        new_data = []
        for indexd in Indexlist:
            try:
                df = capital_market.index_data(indexd, start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y"))
                new_data.append(df)
                print(f"Fetched {start.strftime('%d-%m-%Y')} to {end.strftime('%d-%m-%Y')} for {indexd}")
            except Exception as e:
                print(f"No data for {indexd}: {e}")

        if new_data:
            combined = pd.concat(new_data)
            combined.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
            print("✅ Data saved.")
            #send_email("Index Data Fetch Success", f"Successfully fetched and saved index data on {today}")
        else:
            print("⚠️ No new data.")
            #send_email("Index Data Fetch - No New Data", f"No data found for the run on {today}")

    except Exception as e:
        print(f"❌ Error: {e}")
        #send_email("❌ Index Data Fetch Failed", f"An error occurred:\n\n{str(e)}")
