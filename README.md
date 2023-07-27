# Real-Estate
https://real-estate-pymn.onrender.com

## Problem Context

Our client is a large Real Estate Investment Trust (REIT).
* They invest in houses, apartments, and condos(complex of buildings) within a small county in New York state.
* As part of their business, they try to predict the fair transaction price of a property before it's sold.
* They do so to calibrate their internal pricing models and keep a pulse on the market.

## Current Solution
The REIT currently employs a third-party appraisal service for estimating the price of the property with their own expertise. In practice, the skill level of individual appraisers vary quite large.

To estimate the mis-priced range, the REIT run a trial run to compare the actual transaction prices to the estimates from the appraiser. It was found that the estimates given by inexperienced appraisers differs $70,000 on average.

## Problem Statement
The REIT has hired us to find a data-driven approach to valuing properties.
* They currently have an untapped dataset of transaction prices for previous properties on the market.
* The data was collected in 2016.
* Our task is to build a real-estate pricing model using that dataset.
* If we can build a model to predict transaction prices with an average error of under US Dollars 70,000, then our client will be very satisfied with the our resultant model.

## Business Objectives and Constraints
* Deliverable: Trained model file
* Win condition: Avg. prediction error < \$70,000
* Model Interpretability will be useful
* No latency requirement
