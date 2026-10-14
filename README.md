# Hotel Booking Dashboard | Team 4

**Team members:** Qiu Yuxin, Sha Xinru, Liu Zeyu

A Streamlit dashboard for hotel revenue managers to review booking cancellations and demand patterns.

## 1. Dataset and Decision-Maker

**Dataset:** [Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)

The dataset contains real booking records from a city hotel and a resort hotel in Portugal. Each row represents one booking. The records cover arrivals from July 2015 through August 2017. The original data was extracted from the hotels’ property management systems and anonymized. The CSV file used for this project is under 25 MB. See the [original data article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/).

**Decision-maker:** Hotel revenue manager.

The manager reviews the dashboard weekly and more often during peak periods.

## 2. Why a Dashboard?

The revenue manager regularly needs to understand how cancellations vary by hotel, arrival month, and market segment.

**Decision supported:** If the manager sees a hotel’s cancellation rate rise at least 5 percentage points above its comparable seasonal baseline for two weekly reviews in a row, they will investigate the affected booking segments and consider changes to the channel mix or booking policies. This is a proposed operating rule, not a result calculated by the current app. A real hotel should set its threshold using its own historical data.

Today, the manager might export booking records, check them, and compare results in spreadsheets. We estimate that this manual process could take about 1–2 hours per week. This is a planning estimate, not a measured result. Manual exports and comparisons may also make it harder to notice a change early.

A dashboard makes these recurring comparisons easier because the manager can filter by hotel and year and investigate changes across arrival months and market segments. A weekly report could summarize the overall results, but it would be less useful for exploring different hotels and time periods. An alert could flag a threshold, while the dashboard would help the manager investigate what may be driving the change.

## 3. What the Dashboard Shows

The dashboard shows three headline metrics:

- **Bookings:** Number of booking records in the selected filters.
- **Cancellation rate:** Share of those bookings marked as canceled.
- **Room nights in confirmed bookings:** Nights booked in reservations not marked as canceled.

The supporting charts show cancellation rates by arrival month and by market segment. The hotel and arrival-year filters let the manager compare the two hotel types and different time periods.

The page puts the headline metrics first, followed by charts that help explain changes in cancellation rates.

### What We Chose Not to Show

- **Guest-country breakdown:** It adds detail but is less directly tied to the proposed channel and booking-policy decisions.
- **Agent and company ID rankings:** These identifiers are anonymized, so a ranking would be difficult to interpret or act on.

### Data Limitations

This is a historical Kaggle snapshot, not live hotel data. Hotel, room, and partner identifiers are anonymized. The dataset does not include room capacity or actual realized revenue, so confirmed room nights should not be interpreted as occupancy or revenue. Patterns from 2015–2017 may not represent current demand.

The current app shows historical cancellation patterns by arrival month. It does not track week-to-week changes in cancellation rates or provide live alerts. The proposed two-week action rule would require regularly refreshed production data.

## 4. Refresh and Review Frequency

In production, booking data should refresh daily from the hotel’s reservation system. The revenue manager should review the dashboard weekly, with additional checks during peak periods or when cancellation rates rise above the proposed threshold.

A week-long data delay could hide a developing cancellation pattern and leave the manager less time to investigate affected booking segments or adjust booking policies. It could also create extra manual work to catch up on changes.

The Kaggle app uses a fixed historical snapshot and does not receive live updates.

**Data period:** July 2015–August 2017, Kaggle snapshot  
**Proposed production refresh:** Daily  
**Suggested review cadence:** Weekly, with additional reviews when the action threshold is reached
