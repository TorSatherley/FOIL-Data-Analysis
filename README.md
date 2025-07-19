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

## Cancellation rate:

The data set shows a cancellation rate of 10%, which is considerably higher than typical e-commerce benchmarks (2-5%). Resons for this could include: 
- Stock mismanagement (items sold out after order)
- Customer change of mind
- Confusing website/product descriptions
- Poor checkout UX or shipping issues
- Duplicate/mistaken orders

If 10% of orders are cancelled, that means: 
- That’s 10% of logistics and staff time potentially wasted.
- Inventory management and forecasting are affected.
- Revenue projections may be inflated unless cancellations are accounted for.

Investigating the causes of these cancellations could reveal operational inefficiencies or customer experience issues that, if resolved, might significantly improve profitability and customer retention.