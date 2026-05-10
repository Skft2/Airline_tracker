# Airline Tracker ✈️

A Python-based project to scrape and analyze flight data from the **Flightradar24 endpoint**.  
This tool extracts flight details such as airline, flight number, origin, destination, status, scheduled/actual departure, and arrival times, then organizes them into structured data for further analysis.

---

## 📌 Features
- Scrapes raw flight data from Flightradar24.
- Extracts key fields:
  - Flight ID
  - Airline & Equipment
  - Flight number
  - Origin & Destination (with codes)
  - Status & delay symbol
  - Scheduled vs. Actual departure/arrival times
- Handles missing or malformed data with error handling.
- Outputs structured dictionaries and supports export to CSV/Excel.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- Libraries:
  - `requests`
  - `datetime`
  - `pandas` (for data export)
- Data source: Flightradar24 endpoint (scraped JSON).

---

## ⚙️ Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Skft2/Airline_tracker.git
   cd Airline_tracker
