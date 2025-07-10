# FOIL-Data-Analysis

## Overview

I've decided to take a dual-path approach to the analysis of this data set. During my exporation of the data, I realised that around a quarter of the customerID fields were missing. This meant that, depending on which insights I'm trying to attain, there are two important ways to process the data. 

### Leave the missing CustomerID rows for sales-level insights

Customer ID isn't a data point that is needed for sales-level insights, such as:
- Total revenue
- Product/category analysis
- Top-sellling products
- Time/date based trends
- Location based analysis
- Average order value

It's best to leave them in for this part of the data analysis.

### Drop rows where CustomerID is missing for customer-behaviour insights

Customer ID is an essential column for any customer-behaviour based insight, such as:
- repeat purchases
- customer retention
- average spend per customer