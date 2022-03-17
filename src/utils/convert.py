import pandas as pd;

# ================= Accession Tracker Reports ================= 
def atr_csv_to_df(year, month, dateRange):
    # Destructure the day range in order to find the csv.
    start_day, last_day = dateRange;
    
    # Generate the dataframe
    atr_df = pd.read_csv(f'data/AccessionTrackerReports/{year}/{month}/ATR_{month}_{start_day}-{last_day}.csv');
    
    return atr_df;
# ================= TAT Reports ================= 

# ================= Shifts ================= 
def shift_csv_to_df(year, month, shift):
    shift_dict = {
        "Shift 1": "First Shift",
        "Shift 2": "Second Shift",
        "Shift 3": "Third Shift"
    };
    
    # Remove empty first row from incoming dataframe
    shift_df = pd.read_csv(f'data/Shifts/{year}/{month}/{month}_{year} Schedule - {shift_dict[shift]}.csv').iloc[:, 1:];
    
    # Drop all exclusively NaN Columns
    shift_df = shift_df.dropna(axis=1, how='all');
    
    return shift_df

# Detailed list of information
# contains MM/DD worked and at what position
# need to parse key table in order to fully
# flesh out models, not necessary though.  
def get_accessioners_detailed(shift):
    accessioner_list_detailed = shift[shift.isin(["a", "rec", "ov", "la/inc", "M"]).any(axis=1)];
    # print(accessioner_list_detailed);
    
    return accessioner_list_detailed;

def get_non_accessioners_detailed(shift):
    accessioner_list_detailed = shift[shift.isin(["r", "e", "r/e", "rp/r", "pcr", "CR"]).any(axis=1)];
    # print(accessioner_list_detailed);
    
    return accessioner_list_detailed;

# # List of all of the names of all accessioners
# # Does contain special text values such as:
# # # '*', and '()'
# # There is a special designation for 'Lead' wrapped
# # in parentheses like so:
# # # 'firstName lastName (Lead)'
def get_accessioners_names(shift):
    return shift.iloc[:, 0].tolist();