# pip install nselib pandas holidays schedule

import os
import traceback
from datetime import date, timedelta
import pandas as pd
from nselib import capital_market

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "Index_Daily_Data.csv")
LOG_FILE = os.path.join(BASE_DIR, "index_log.txt")
# ----------------------------

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")
    print(msg)


def fetch_and_save_index_data():

    log("----- Job Started -----")

    try:
        first_date = date(2024, 1, 1)
        today = date.today()
        diff = (today - first_date).days
        start = today - timedelta(days=diff)
        end = today

        # Get index list
        try:
            Indexlist = capital_market.fno_index_list()['underlying']
        except Exception as e:
            log(f"Failed to fetch index list: {e}")
            log(traceback.format_exc())
            return

        # Reset file
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
            log("Old file deleted.")

        new_data = []

        # Fetch data for each index
        for indexd in Indexlist:
            try:
                df = capital_market.index_data(
                    indexd,
                    start.strftime("%d-%m-%Y"),
                    end.strftime("%d-%m-%Y")
                )
                if df is not None and not df.empty:
                    new_data.append(df)
                    log(f"Fetched {indexd}")
                else:
                    log(f"No data for {indexd}")

            except Exception as e:
                log(f"Error fetching {indexd}: {e}")
                log(traceback.format_exc())

        # Save output
        if new_data:
            combined = pd.concat(new_data)
            combined.to_csv(OUTPUT_FILE, index=False)
            log("✔ Data saved successfully.")
        else:
            log("⚠ No data fetched.")

    except Exception as e:
        log("❌ Fatal error in job.")
        log(str(e))
        log(traceback.format_exc())

    log("----- Job Finished -----\n")


if __name__ == "__main__":
    fetch_and_save_index_data()
