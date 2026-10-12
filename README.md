# inclass-hotelapp
# Hotel Booking Dashboard | Team 4

**Team members:** [Add at least four team members]

A Streamlit dashboard for hotel revenue managers to review booking cancellations and demand patterns.

## 1. Dataset and Decision-Maker

**Dataset:** [Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)

The dataset contains real booking records from a city hotel and a resort hotel in Portugal. Each row represents one booking. The records cover arrivals from July 2015 through August 2017. The original data was extracted from the hotels’ property management systems and anonymized. See the [original data article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/).

**Decision-maker:** Hotel revenue manager.

The manager reviews the dashboard weekly and more often during peak periods.

## 2. Why a Dashboard?

The revenue manager repeatedly needs to understand how cancellations vary by hotel, arrival month, and market segment.

**Decision supported:** If the manager sees a hotel’s cancellation rate rise at least 5 percentage points above its comparable seasonal baseline for two weekly reviews in a row, they will investigate the affected booking segments and consider changes to channel mix or booking policies. This is a proposed operating rule; a real hotel should set its threshold using its own history.

Today, the manager might export booking records and compare them in spreadsheets. A dashboard makes those recurring comparisons easier to review. A weekly report could summarize the overall result, but the manager also needs to filter by hotel and year to investigate changes.

## 3. What the Dashboard Shows

The dashboard shows three headline metrics:

- **Bookings:** Number of booking records in the selected filters.
- **Cancellation rate:** Share of those bookings marked as canceled.
- **Room nights in confirmed bookings:** Nights booked in reservations not marked as canceled.

The supporting charts show cancellation rate by arrival month and by market segment. The hotel and arrival-year filters let the manager compare the two hotel types and time periods.

The page puts the headline metrics first, followed by the charts that help explain changes in cancellation rates.

### What We Chose Not to Show

- **Guest-country breakdown:** It adds detail but is less directly tied to the proposed channel and booking-policy decisions.
- **Agent and company ID rankings:** These
