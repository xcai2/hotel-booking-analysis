# Hotel Booking Analysis — Marketing Analytics Project

## Overview

Exploratory data analysis of 119,390 hotel bookings from 2015–2017, designed to surface customer behavior patterns and translate them into actionable marketing questions. The project covers data cleaning, variable exploration, visualization, and integration with public macro datasets to place findings in industry context.

## Project Structure

```
hotel_booking_analysis/
├── README.md                          # Project documentation
├── data/
│   └── hotel_bookings.csv             # Hotel booking dataset (119,390 records)
├── public_data/                       # Public datasets for macro context
│   ├── README.md
│   ├── cpi_data.csv                   # US CPI data (2015–2017)
│   ├── portugal_tourism.csv           # Portugal tourism statistics
│   ├── europe_tourism.csv             # European tourism trends
│   └── seasonal_index.csv             # Travel seasonality index
├── analysis/                          # Analysis scripts and outputs
│   ├── hotel_analysis.py              # Main analysis script
│   ├── download_public_data.py        # Public data downloader
│   ├── hotel_type_stats.csv           # Stats by hotel type
│   ├── monthly_stats.csv              # Monthly stats
│   └── market_segment_stats.csv       # Market segment stats
├── visualizations/                    # Charts and figures
│   ├── cancellation_analysis.png
│   ├── revenue_analysis.png
│   ├── booking_patterns.png
│   ├── customer_source_analysis.png
│   ├── adr_vs_cpi.png
│   └── bookings_vs_seasonal_index.png
└── reports/
    ├── hotel_booking_analysis.Rmd
    └── final_report.md
```

## Data

### Primary dataset: `hotel_bookings.csv`
- **Records:** 119,390 bookings
- - **Time range:** 2015–2017
  - - **Hotel types:** City Hotel and Resort Hotel
    - - **Variables:** 32 columns covering booking, customer, and room information
     
      - ### Public datasets
      - To add macro context to the findings, the analysis integrates four external sources:
      - - **CPI data** (FRED) — to assess price movement against inflation
        - - **Portugal tourism statistics** (INE) — to validate local market trends
          - - **European tourism trends** (Eurostat) — for industry benchmarking
            - - **Seasonality index** — standard tourism seasonal patterns
             
              - ## Key Findings
             
              - ### Core metrics
             
              - | Metric | Value |
              - |---|---|
              - | Overall cancellation rate | 37.04% |
              - | Repeat-customer share | 3.19% |
              - | Average lead time | 104 days |
              - | Average stay length | 3.4 nights |
              - | Average ADR | $101.83 |
             
              - ### Main takeaways
              - - **High cancellation problem.** City Hotel cancellation rate hits 41.7%, and the longer the lead time, the higher the cancellation rate.
                - - **Low customer loyalty.** Only 3.19% of bookings come from repeat customers — retention is a real challenge.
                  - - **Strong seasonality.** Summer (August) is peak season; ADR and booking volume both top out there.
                    - - **Channel dependency.** Over 80% of bookings come from travel agents and tour operators.
                      - - **European market dominance.** Customers are concentrated in Portugal, the UK, and France.
                       
                        - ## Three Core Marketing Questions
                       
                        - **Q1. How do we lower the cancellation rate?**
                        - Implement differentiated deposit policies for City Hotel and long-lead bookings, and offer flexible rescheduling options.
                       
                        - **Q2. How do we improve customer loyalty?**
                        - Build a structured loyalty program, using personalization and service quality to lift the repeat-customer share.
                       
                        - **Q3. How do we optimize pricing and channel strategy?**
                        - Introduce dynamic pricing, build off-season package products, and strengthen the direct-booking channel.
                       
                        - ## Usage
                       
                        - ### Environment
                       
                        - Python:
                        - ```bash
                          pip install pandas numpy matplotlib seaborn
                          ```

                          R (for the R Markdown report):
                          ```r
                          install.packages(c("rmarkdown", "tidyverse", "janitor", "knitr"))
                          ```

                          ### Running the analysis

                          ```bash
                          # Run the main data analysis
                          cd analysis
                          python3 hotel_analysis.py

                          # Download the public datasets
                          python3 download_public_data.py

                          # Generate the R Markdown report (from R)
                          # rmarkdown::render("reports/hotel_booking_analysis.Rmd")
                          ```

                          ## Data Sources

                          - **Primary dataset:** Hotel Booking Demand Dataset
                          - - **CPI:** FRED — Federal Reserve Economic Data
                            - - **Portugal tourism:** INE Portugal
                              - - **European tourism:** Eurostat
                               
                                - ## License
                               
                                - This project is for academic and educational purposes only.
                               
                                - ## Changelog
                               
                                - **2026-02-02** — Initial release
                                - - Completed exploratory data analysis
                                  - - Integrated public datasets
                                    - - Generated visualizations
                                      - - Framed three core marketing questions
                                        - 
