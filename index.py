import streamlit as st
import pandas as pd
from datetime import datetime

# Predefined site data for each run
run_sites = {
    1: [
        "Waihi Falls", "Akitio River at Estuary", "Pacific Ocean at Akitio Beach",
        "Pacific Ocean at Herbertville Beach", "Wainui Stream at Herbertville", "Manawatu at Weber Road",
        "Manawatu at Hopelands", "Manawatu at Upper Gorge"
    ],
    2: [
        "Mangatainoka at Pahiatua Town Bridge", "Mangatainoka at SH2", "Makakahi at Motorcamp",
        "Mangahao at Marima Domain", "Mangatainoka at Scarborough Konini Rd", "Mangahao at Poplar Reserve",
        "Tasman Sea at Himitangi Beach", "Kaikokopu Stream at Himitangi Beach", "Tasman Sea at Foxton Beach",
        "Manawatu at Foxton", "Foxton Loop at Harbour Street Boat Ramp", "Manawatu at Whirokino",
        "Hokowhitu Lagoon at Walkbridge"
    ],
    3: [
        "Pohangina at Raumai Reserve", "Pohangina at Totara Reserve", "Pohangina at Piripiri",
        "Oroua at Londons Ford", "Oroua at Barletts Ford", "Oroua at Almadale",
        "Oroua at Feilding Rd Bridge", "Oroua at Timona Park (u/s AFFCO)", "Rangitikei at Bulls Bridge",
        "Rangitikei at McKelvies", "Rangitikei at River Estuary", "Manawatu at u/s PNCC STP (Waitoetoe Park)",
        "Manawatu at Fitzherbert"
    ],
    4: [
        "Kahuterawa at Reserve", "Tokomaru at Horseshoe Bend", "Mangaore at d/s Mangahao Power Station",
        "Ohau at Gladstone Reserve", "Ohau Kimberley Reserve", "Ohau at Kirkcaldies",
        "Ohau at SH1", "Waikawa at Waikawa campsite", "Waikawa Estuary", "Tasman Sea at Waikawa Beach",
        "Hokio Stream at Muaupoko St Bridge", "Tasman Sea at Hokio Beach", "Wairarawa Stream at Waitarere Beach",
        "Tasman Sea at Waitarere"
    ],
    5: [
        "Hautapu at Papakai Park", "Moawhango at Moawhango", "Rangitikei at Pukeokahu",
        "Rangitikei at meeting of the waters (Toetoe Bridge)", "Rangitikei at Mangaweka",
        "Mangawharariki at Ruahine Dress Circle", "Rangitikei at Vinegar Hill", "Rangitikei at Kakariki",
        "Oroua at Awahuri Bridge"
    ],
    6: [
        "Tasman Sea at Ototoka Beach", "Ototoka Stream at End of Beach Road", "Kai Iwi at Archers Bridge",
        "Kai Iwi Beach", "Mowhanau at Footbridge", "Tasman Sea at Castlecliff Beach",
        "Whanganui at Town Bridge", "Whanganui at Cobham Pontoons", "Whanganui at Mosquito Point",
        "Tasman Sea at South Beach", "Lake Wiritoa", "Lake Pauri", "Turakina at Mouth", "Lake Dudding"
    ],
    7: [
        "Whangaehu at Fields Track", "Makotuku at Raetihi Motor Camp", "Whanganui at Pipiriki",
        "Manganui o te Ao at Ruatiti Domain"
    ],
    8: [
        "Whanganui at Mananui (Matapuna)", "Whanganui at Cherry Grove", "Ongarue at Cherry Grove",
        "Whakapapa at Owhango", "Mangawhero at SH49", "Mangateitei at Moore Street"
    ]
}


# Streamlit App
st.title("Run Sites Data Entry")

# User selects multiple runs
selected_runs = st.multiselect(
    "Select the runs to include:", options=run_sites.keys(),
    format_func=lambda x: f"Run {x}"
)

# If runs are selected, gather additional details
if selected_runs:
    st.write("### Enter Run-Specific Information")
    run_details = {}

    for run in selected_runs:
        with st.expander(f"Run {run} - {len(run_sites[run])} Sites"):
            sample_number = st.number_input(f"Starting Sample Number for Run {run}:", min_value=1, step=1)

            # Date input fields (NZ format)
            date_sent = st.text_input(f"Sampling Date for Run {run} (DD/MM/YYYY):", value=datetime.today().strftime("%d/%m/%Y"))
            date_received = st.text_input(f"Date Received at Lab for Run {run} (DD/MM/YYYY):", value=datetime.today().strftime("%d/%m/%Y"))
            time_received = st.text_input(f"Time Received at Lab for Run {run} (HH:MM):", value="07:00")  # User enters manually

            run_details[run] = {
                "sample_number": sample_number,
                "date_sent": date_sent,
                "date_received": date_received,
                "time_received": time_received
            }

    # Input for common field across all runs
    results_received_date = st.text_input("Enter the Date Results Were Received via Labmail (DD/MM/YYYY):", value=datetime.today().strftime("%d/%m/%Y"))
    results_received_time = st.text_input("Enter the Time Results Were Received via Labmail (HH:MM):", value="12:00")

    # Generate table
    all_data = []
    for run in selected_runs:
        details = run_details[run]
        sample_num = details["sample_number"]

        for site in run_sites[run]:
            # Convert text-based date & time inputs to datetime objects
            sent_datetime = datetime.strptime(f"{details['date_sent']} 17:00", "%d/%m/%Y %H:%M")  # Fixed time 17:00
            received_datetime = datetime.strptime(f"{details['date_received']} {details['time_received']}", "%d/%m/%Y %H:%M")
            results_received_datetime = datetime.strptime(f"{results_received_date} {results_received_time}", "%d/%m/%Y %H:%M")


            all_data.append({
                "Run": run,
                "Site": site,
                "Sample Number": str(sample_num),  # Ensure Sample Number has NO commas
                "Date and Time Sent": sent_datetime.strftime("%d/%m/%Y %H:%M"),  # NZ Format
                "Date & Time Received at the Lab": received_datetime.strftime("%d/%m/%Y %H:%M"),  # NZ Format
                "Results Received via Labmail": results_received_datetime.strftime("%d/%m/%Y %H:%M"),  # NZ Format
            })
            sample_num += 1  # Increment sample number for next site

    df = pd.DataFrame(all_data)

    # Display table without index using hide_index=True
    st.write("### Completed Data Table")
    st.dataframe(df, hide_index=True)
