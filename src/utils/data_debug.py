def check_data(shift_data, atr_data, month, date_string, year):
    for shift in shift_data:
        s = shift["schedule"];
        # print("===================== DEBUG_ACCESSIONER");
        print(f"Schedule: {s}");
        print("===============");

        for name in shift["employees"]:
            accessioner_stats = atr_data.get(name);
            if accessioner_stats is None: break;
            print(f"----------------------DEBUG_SHIFT {s} for {month}/{date_string}/{year}")
            print(f">>>> Name: {name}");
            
            for stat_item in accessioner_stats:
                accession_date = stat_item["AccessionDate"];
                accession_hour = stat_item["Hour"];
                accession_counts = stat_item["Count"];
                
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")    
                print("1.] Date: ", accession_date);
                print("2.] Hour: ", accession_hour);
                print("3.] Count for that period: ", accession_counts);
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
            
        print("===================== DEBUG_END")