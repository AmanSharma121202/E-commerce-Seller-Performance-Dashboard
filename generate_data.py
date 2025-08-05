import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_SELLERS = 500
NUM_ORDERS = 10000
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2023, 12, 31)
SELLER_CATEGORIES = ['Electronics', 'Fashion', 'Home & Kitchen', 'Books', 'Sports', 'Beauty']

# --- 1. Generate Sellers Data ---
print("Generating sellers data...")

sellers_data = []
for i in range(1, NUM_SELLERS + 1):
    # Generate a random join date for each seller
    join_date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
    sellers_data.append({
        'seller_id': f'S{str(i).zfill(4)}',
        'seller_join_date': join_date.strftime('%Y-%m-%d'),
        'seller_category': random.choice(SELLER_CATEGORIES)
    })

sellers_df = pd.DataFrame(sellers_data)
sellers_df['seller_join_date'] = pd.to_datetime(sellers_df['seller_join_date'])

print(f"Generated {len(sellers_df)} sellers.")

# --- 2. Generate Orders Data ---
print("Generating orders data...")

orders_data = []
for i in range(1, NUM_ORDERS + 1):
    # Select a random seller
    random_seller = sellers_df.sample(1).iloc[0]
    seller_id = random_seller['seller_id']
    seller_join_date = random_seller['seller_join_date']
    
    # Order date must be after the seller joined
    max_days_since_join = (END_DATE - seller_join_date).days
    if max_days_since_join <= 0:
        # If seller joined on the last day, order is on the same day
        order_date = seller_join_date
    else:
        order_date = seller_join_date + timedelta(days=random.randint(1, max_days_since_join))

    # Generate order value (e.g., Electronics are generally more expensive)
    category_multipliers = {
        'Electronics': 2.5, 'Fashion': 1.2, 'Home & Kitchen': 1.5, 
        'Books': 0.8, 'Sports': 1.3, 'Beauty': 1.0
    }
    base_value = np.random.gamma(2, 50) # Gamma distribution for a realistic skew
    order_value = round(base_value * category_multipliers[random_seller['seller_category']], 2)

    # Determine if the order was returned (e.g., Fashion has a higher return rate)
    category_return_rates = {
        'Electronics': 0.10, 'Fashion': 0.25, 'Home & Kitchen': 0.08,
        'Books': 0.05, 'Sports': 0.12, 'Beauty': 0.07
    }
    is_returned = 1 if random.random() < category_return_rates[random_seller['seller_category']] else 0
    
    # Calculate profit
    if is_returned:
        # Returned items might have a processing cost, leading to a loss
        profit = -abs(round(order_value * np.random.uniform(0.05, 0.1), 2)) 
    else:
        # Profit margin varies
        profit_margin = np.random.uniform(0.10, 0.40)
        profit = round(order_value * profit_margin, 2)

    orders_data.append({
        'order_id': f'O{str(i).zfill(6)}',
        'seller_id': seller_id,
        'customer_id': f'C{str(random.randint(1, NUM_SELLERS * 5)).zfill(5)}',
        'order_date': order_date.strftime('%Y-%m-%d'),
        'order_value': order_value,
        'is_returned': is_returned,
        'profit': profit
    })

orders_df = pd.DataFrame(orders_data)
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])

print(f"Generated {len(orders_df)} orders.")

# --- 3. Save to CSV ---
sellers_df.to_csv('sellers.csv', index=False)
orders_df.to_csv('orders.csv', index=False)

print("\nData generation complete!")
print("Saved 'sellers.csv' and 'orders.csv' to the current directory.")
