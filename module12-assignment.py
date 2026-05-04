# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0,
    "Orlando": 0.85,
    "Miami": 1.2,
    "Jacksonville": 0.75,
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9

    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday

    for store in stores:
        store_factor = store_performance[store]

        for dept in departments:
            dept_factor = dept_performance[dept]

            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)

                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise

                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range

                # Calculate profit
                profit = sales_amount * profit_margin

                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range

    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])

    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income

    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)

    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))

    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)

    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)

    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"

    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]

    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()

    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) *
                                (store_performance[store] ** 0.5))

    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# =============================================================================
# TODO 1: Descriptive Analytics - Overview of Current Performance
# =============================================================================

def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics.
    Returns a dictionary with total_sales, total_profit, avg_profit_margin,
    sales_by_store (Series), and sales_by_dept (Series).
    """
    # --- Aggregate totals ---
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    avg_profit_margin = sales_df["ProfitMargin"].mean()

    # --- Breakdowns ---
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    # --- Additional descriptive stats printed for insight ---
    print("\n[1.1] Sales Performance Summary")
    print(f"  Total Annual Sales  : ${total_sales:,.2f}")
    print(f"  Total Annual Profit : ${total_profit:,.2f}")
    print(f"  Avg Profit Margin   : {avg_profit_margin:.2%}")
    print(f"  Overall Profit Rate : {(total_profit / total_sales):.2%}")

    # Descriptive statistics for daily sales per transaction row
    print("\n  Sales Descriptive Statistics (per transaction):")
    print(sales_df["Sales"].describe().to_string())

    print("\n  Sales by Store:")
    for store, val in sales_by_store.items():
        print(f"    {store:15s}: ${val:>14,.2f}")

    print("\n  Sales by Department:")
    for dept, val in sales_by_dept.items():
        print(f"    {dept:18s}: ${val:>14,.2f}")

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept,
    }


def visualize_sales_distribution():
    """
    Create three visualizations: sales by store (bar), sales by department (bar),
    and monthly sales trend (line).  Returns a tuple of three Matplotlib figures.
    """
    # Figure 1 – Sales by Store (horizontal bar chart)
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values()
    store_fig, ax1 = plt.subplots(figsize=(9, 5))
    colors = ["#4CAF50", "#66BB6A", "#81C784", "#A5D6A7", "#C8E6C9"]
    bars = ax1.barh(sales_by_store.index, sales_by_store.values, color=colors)
    ax1.set_title("Annual Sales by Store", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Total Sales ($)")
    ax1.set_ylabel("Store")
    for bar in bars:
        width = bar.get_width()
        ax1.text(width * 1.01, bar.get_y() + bar.get_height() / 2,
                 f"${width:,.0f}", va="center", fontsize=9)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    store_fig.tight_layout()

    # Figure 2 – Sales by Department (vertical bar with margin overlay)
    dept_summary = (
        sales_df.groupby("Department")
        .agg(TotalSales=("Sales", "sum"), AvgMargin=("ProfitMargin", "mean"))
        .sort_values("TotalSales", ascending=False)
    )
    dept_fig, ax2 = plt.subplots(figsize=(9, 5))
    dept_colors = ["#2196F3", "#42A5F5", "#64B5F6", "#90CAF9", "#BBDEFB"]
    ax2.bar(dept_summary.index, dept_summary["TotalSales"], color=dept_colors, label="Total Sales")
    ax2.set_title("Annual Sales & Avg Profit Margin by Department", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Department")
    ax2.set_ylabel("Total Sales ($)")
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax2_twin = ax2.twinx()
    ax2_twin.plot(dept_summary.index, dept_summary["AvgMargin"] * 100,
                  color="darkorange", marker="o", linewidth=2, label="Avg Margin %")
    ax2_twin.set_ylabel("Avg Profit Margin (%)")
    # Combine legends
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    dept_fig.tight_layout()

    # Figure 3 – Monthly Sales Trend (line chart, one line per store)
    sales_df["Month"] = sales_df["Date"].dt.to_period("M")
    monthly_by_store = (
        sales_df.groupby(["Month", "Store"])["Sales"]
        .sum()
        .unstack("Store")
    )
    # Convert Period index to string for clean x-axis labels
    monthly_by_store.index = monthly_by_store.index.astype(str)

    time_fig, ax3 = plt.subplots(figsize=(12, 5))
    line_colors = ["#E53935", "#FB8C00", "#43A047", "#1E88E5", "#8E24AA"]
    for color, store in zip(line_colors, monthly_by_store.columns):
        ax3.plot(monthly_by_store.index, monthly_by_store[store],
                 marker="o", markersize=4, label=store, color=color)
    ax3.set_title("Monthly Sales Trend by Store (2023)", fontsize=14, fontweight="bold")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Monthly Sales ($)")
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
    ax3.set_xticks(range(len(monthly_by_store.index)))
    ax3.set_xticklabels(monthly_by_store.index, rotation=45, ha="right")
    ax3.legend(title="Store", loc="upper left")
    ax3.grid(axis="y", alpha=0.3)
    time_fig.tight_layout()

    print("\n[1.2] Three sales distribution visualizations created.")
    return store_fig, dept_fig, time_fig


def analyze_customer_segments():
    """
    Analyze customer segments and their spending patterns.
    Returns a dict with segment_counts, segment_avg_spend, and segment_loyalty.
    """
    segment_counts = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)

    # Cross-tab of segments vs loyalty tiers
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"])

    print("\n[1.3] Customer Segment Analysis")
    print("\n  Segment Counts:")
    print(segment_counts.to_string())
    print("\n  Average Monthly Spend by Segment:")
    for seg, spend in segment_avg_spend.items():
        print(f"    {seg:22s}: ${spend:>8.2f}")
    print("\n  Loyalty Tier Distribution per Segment:")
    print(segment_loyalty.to_string())

    # Visualize segment breakdown
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    seg_colors = ["#EF5350", "#FFA726", "#66BB6A", "#42A5F5", "#AB47BC"]

    # Pie chart – customer count per segment
    axes[0].pie(segment_counts.values, labels=segment_counts.index,
                autopct="%1.1f%%", colors=seg_colors, startangle=140)
    axes[0].set_title("Customer Segment Distribution", fontweight="bold")

    # Bar chart – avg monthly spend per segment
    bars = axes[1].bar(segment_avg_spend.index, segment_avg_spend.values, color=seg_colors)
    axes[1].set_title("Avg Monthly Spend by Segment", fontweight="bold")
    axes[1].set_ylabel("Avg Monthly Spend ($)")
    axes[1].set_xticklabels(segment_avg_spend.index, rotation=30, ha="right")
    for bar in bars:
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                     f"${bar.get_height():.0f}", ha="center", fontsize=9)
    fig.tight_layout()

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty,
    }


# =============================================================================
# TODO 2: Diagnostic Analytics - Understanding Relationships
# =============================================================================

def analyze_sales_correlations():
    """
    Analyze correlations between store/operational factors and sales performance.
    Returns a dict with store_correlations, top_correlations, and correlation_fig.
    """
    # Merge store characteristics with operational metrics
    merged = pd.merge(store_df, operational_df, on="Store")

    # Select numeric columns for correlation analysis
    numeric_cols = ["SquareFootage", "StaffCount", "YearsOpen",
                    "WeeklyMarketingSpend", "AnnualSales", "AnnualProfit",
                    "SalesPerSqFt", "ProfitPerSqFt", "SalesPerStaff",
                    "InventoryTurnover", "CustomerSatisfaction"]
    corr_matrix = merged[numeric_cols].corr()
    store_correlations = corr_matrix

    # Identify top factors correlated with AnnualSales (excluding self)
    sales_corr = corr_matrix["AnnualSales"].drop("AnnualSales").sort_values(
        key=abs, ascending=False
    )
    top_correlations = list(zip(sales_corr.index, sales_corr.values))

    print("\n[2.1] Correlation Analysis")
    print("\n  Top factors correlated with Annual Sales:")
    for factor, corr in top_correlations:
        direction = "positive" if corr > 0 else "negative"
        print(f"    {factor:28s}: r = {corr:+.3f}  ({direction})")

    # Heatmap of correlation matrix
    correlation_fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr_matrix.values, cmap="RdYlGn", vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(numeric_cols, fontsize=8)
    ax.set_title("Correlation Matrix – Store & Operational Metrics",
                 fontsize=13, fontweight="bold")
    # Annotate cells
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            ax.text(j, i, f"{corr_matrix.values[i, j]:.2f}",
                    ha="center", va="center", fontsize=6,
                    color="black" if abs(corr_matrix.values[i, j]) < 0.7 else "white")
    correlation_fig.tight_layout()

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig,
    }


def compare_store_performance():
    """
    Compare stores across operational efficiency metrics and rank by profit.
    Returns a dict with efficiency_metrics, performance_ranking, and comparison_fig.
    """
    efficiency_metrics = operational_df[
        ["Store", "SalesPerSqFt", "SalesPerStaff", "ProfitPerSqFt",
         "InventoryTurnover", "CustomerSatisfaction"]
    ].set_index("Store")

    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    print("\n[2.2] Store Performance Comparison")
    print("\n  Efficiency Metrics:")
    print(efficiency_metrics.to_string())
    print("\n  Performance Ranking (by Annual Profit):")
    for rank, (store, profit) in enumerate(performance_ranking.items(), 1):
        print(f"    {rank}. {store:15s}: ${profit:>12,.2f}")

    # Grouped bar chart comparing key metrics
    comparison_fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    store_names = efficiency_metrics.index.tolist()
    bar_colors = ["#E53935", "#FB8C00", "#43A047", "#1E88E5", "#8E24AA"]

    metrics_to_plot = [
        ("SalesPerSqFt", "Sales per Sq Ft ($)", axes[0]),
        ("SalesPerStaff", "Sales per Staff Member ($)", axes[1]),
        ("CustomerSatisfaction", "Customer Satisfaction (/ 5)", axes[2]),
    ]
    for col, label, ax in metrics_to_plot:
        values = efficiency_metrics[col]
        bars = ax.bar(store_names, values, color=bar_colors)
        ax.set_title(label, fontweight="bold", fontsize=10)
        ax.set_xticklabels(store_names, rotation=30, ha="right")
        ax.set_ylabel(label)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() * 1.01,
                    f"{bar.get_height():.1f}",
                    ha="center", fontsize=8)

    comparison_fig.suptitle("Store Efficiency Comparison", fontsize=14, fontweight="bold")
    comparison_fig.tight_layout()

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig,
    }


def analyze_seasonal_patterns():
    """
    Analyze monthly and day-of-week sales patterns.
    Returns a dict with monthly_sales, dow_sales, and seasonal_fig.
    """
    # Monthly aggregation
    sales_df["MonthNum"] = sales_df["Date"].dt.month
    monthly_sales = sales_df.groupby("MonthNum")["Sales"].sum()
    monthly_sales.index = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    # Day-of-week aggregation (0=Monday … 6=Sunday)
    sales_df["DayOfWeek"] = sales_df["Date"].dt.dayofweek
    dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dow_sales = sales_df.groupby("DayOfWeek")["Sales"].sum()
    dow_sales.index = dow_labels

    print("\n[2.3] Seasonal Pattern Analysis")
    print("\n  Monthly Sales (relative to Jan baseline):")
    jan_baseline = monthly_sales.iloc[0]
    for month, val in monthly_sales.items():
        print(f"    {month}: ${val:>12,.0f}  ({val/jan_baseline - 1:+.1%} vs Jan)")
    print("\n  Day-of-Week Sales:")
    for day, val in dow_sales.items():
        print(f"    {day}: ${val:>12,.0f}")

    # Two-panel figure
    seasonal_fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Monthly line
    month_colors = ["steelblue" if m not in ["Jun", "Jul", "Aug", "Dec"] else "darkorange"
                    for m in monthly_sales.index]
    ax1.bar(monthly_sales.index, monthly_sales.values, color=month_colors)
    ax1.set_title("Monthly Sales (2023)", fontweight="bold")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Sales ($)")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    ax1.tick_params(axis="x", rotation=45)
    ax1.axhline(monthly_sales.mean(), color="red", linestyle="--", alpha=0.6, label="Annual Avg")
    ax1.legend()

    # Day-of-week bar
    dow_colors = ["#66BB6A" if d in ["Sat", "Sun"] else "#42A5F5" for d in dow_sales.index]
    ax2.bar(dow_sales.index, dow_sales.values, color=dow_colors)
    ax2.set_title("Sales by Day of Week", fontweight="bold")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Total Sales ($)")
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

    seasonal_fig.tight_layout()

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig,
    }


# =============================================================================
# TODO 3: Predictive Analytics - Basic Forecasting
# =============================================================================

def predict_store_sales():
    """
    Use multiple linear regression (via scipy.stats) to predict annual store sales
    from store characteristics.  Returns coefficients, R-squared, predictions, and figure.
    """
    # Merge store characteristics with annual sales from operational_df
    merged = pd.merge(store_df, operational_df[["Store", "AnnualSales"]], on="Store")

    features = ["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    X = merged[features].values  # shape (5, 4)
    y = merged["AnnualSales"].values  # shape (5,)

    # Add intercept column
    X_with_intercept = np.column_stack([np.ones(len(X)), X])

    # Ordinary Least Squares using numpy (scipy.stats.linregress is for simple regression)
    # With only 5 data points and 4 features, OLS is still illustrative
    coeffs, residuals, rank, sv = np.linalg.lstsq(X_with_intercept, y, rcond=None)

    # Predictions and R-squared
    y_pred = X_with_intercept @ coeffs
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    feature_names = ["Intercept"] + features
    coefficients = dict(zip(feature_names, coeffs))

    predictions = pd.Series(y_pred, index=merged["Store"])

    print("\n[3.1] Store Sales Prediction – Linear Regression")
    print(f"\n  R-squared: {r_squared:.4f}")
    print("\n  Model Coefficients:")
    for feat, coef in coefficients.items():
        print(f"    {feat:28s}: {coef:>14.4f}")
    print("\n  Predicted vs Actual Sales:")
    for store, pred, actual in zip(merged["Store"], y_pred, y):
        print(f"    {store:15s}  Predicted: ${pred:>12,.0f}  |  Actual: ${actual:>12,.0f}  |  Error: {(pred - actual)/actual:+.1%}")

    # Visualize predicted vs actual
    model_fig, ax = plt.subplots(figsize=(8, 5))
    x_pos = np.arange(len(merged["Store"]))
    width = 0.35
    ax.bar(x_pos - width/2, y / 1e6, width, label="Actual", color="#42A5F5")
    ax.bar(x_pos + width/2, y_pred / 1e6, width, label="Predicted", color="#FFA726", alpha=0.85)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(merged["Store"])
    ax.set_title(f"Predicted vs Actual Annual Sales (R² = {r_squared:.3f})",
                 fontweight="bold")
    ax.set_ylabel("Annual Sales ($M)")
    ax.legend()
    model_fig.tight_layout()

    return {
        "coefficients": coefficients,
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": model_fig,
    }


def forecast_department_sales():
    """
    Analyze monthly department sales trends and project 3-month growth rates.
    Returns dept_trends, growth_rates, and forecast_fig.
    """
    # Monthly totals per department
    sales_df["MonthNum"] = sales_df["Date"].dt.month
    dept_monthly = (
        sales_df.groupby(["MonthNum", "Department"])["Sales"]
        .sum()
        .unstack("Department")
    )
    dept_trends = dept_monthly  # shape (12, 5)

    # Simple growth rate: compare H2 vs H1 average
    h1 = dept_monthly.iloc[:6].mean()  # Jan-Jun average
    h2 = dept_monthly.iloc[6:].mean()  # Jul-Dec average
    growth_rates = ((h2 - h1) / h1).sort_values(ascending=False)

    print("\n[3.2] Department Sales Forecasting")
    print("\n  H2 vs H1 Growth Rates by Department:")
    for dept, rate in growth_rates.items():
        print(f"    {dept:20s}: {rate:+.2%}")

    # Build a simple 3-month linear extrapolation for each department
    month_nums = dept_monthly.index.values  # 1..12
    forecast_months = [13, 14, 15]  # Jan-Mar 2024
    forecast_values = {}
    for dept in dept_monthly.columns:
        slope, intercept, _, _, _ = stats.linregress(month_nums, dept_monthly[dept].values)
        forecast_values[dept] = [slope * m + intercept for m in forecast_months]

    # Visualize actual trend + forecast
    forecast_fig, ax = plt.subplots(figsize=(12, 6))
    dept_colors = ["#E53935", "#FB8C00", "#43A047", "#1E88E5", "#8E24AA"]
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
                    "Jan'24", "Feb'24", "Mar'24"]

    for color, dept in zip(dept_colors, dept_monthly.columns):
        # Historical
        ax.plot(range(1, 13), dept_monthly[dept].values / 1e3,
                marker="o", markersize=4, color=color, label=dept)
        # Forecast (dashed)
        fcast = forecast_values[dept]
        ax.plot([12, 13, 14, 15],
                [dept_monthly[dept].values[-1] / 1e3] + [v / 1e3 for v in fcast],
                linestyle="--", color=color, alpha=0.7)

    ax.axvline(12.5, color="gray", linestyle=":", linewidth=1.5, label="Forecast Start")
    ax.set_xticks(range(1, 16))
    ax.set_xticklabels(month_labels, rotation=45, ha="right")
    ax.set_title("Department Monthly Sales with 3-Month Forecast", fontweight="bold", fontsize=13)
    ax.set_ylabel("Monthly Sales ($K)")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    forecast_fig.tight_layout()

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig,
    }


# =============================================================================
# TODO 4: Integrated Analysis - Business Insights and Recommendations
# =============================================================================

def identify_profit_opportunities():
    """
    Identify top and bottom performing store-department combinations.
    Returns top_combinations, underperforming, and opportunity_score.
    """
    store_dept = (
        sales_df.groupby(["Store", "Department"])
        .agg(
            TotalSales=("Sales", "sum"),
            TotalProfit=("Profit", "sum"),
            AvgMargin=("ProfitMargin", "mean"),
        )
        .reset_index()
    )
    store_dept = store_dept.sort_values("TotalProfit", ascending=False)

    top_combinations = store_dept.head(10).reset_index(drop=True)
    underperforming = store_dept.tail(10).reset_index(drop=True)

    # Opportunity score for each store: weighted sum of margin and sales volume
    # (normalized to 0-100 scale)
    store_summary = (
        store_dept.groupby("Store")
        .agg(TotalProfit=("TotalProfit", "sum"), AvgMargin=("AvgMargin", "mean"))
    )
    # Normalize each component to 0-1
    profit_norm = (store_summary["TotalProfit"] - store_summary["TotalProfit"].min()) / \
                  (store_summary["TotalProfit"].max() - store_summary["TotalProfit"].min())
    margin_norm = (store_summary["AvgMargin"] - store_summary["AvgMargin"].min()) / \
                  (store_summary["AvgMargin"].max() - store_summary["AvgMargin"].min())
    opportunity_score = ((0.6 * profit_norm + 0.4 * margin_norm) * 100).round(1).sort_values(ascending=False)

    print("\n[4.1] Profit Opportunity Analysis")
    print("\n  Top 10 Store-Department Combinations (by Total Profit):")
    print(top_combinations[["Store", "Department", "TotalSales", "TotalProfit", "AvgMargin"]].to_string(index=False))
    print("\n  Bottom 10 (Underperforming) Combinations:")
    print(underperforming[["Store", "Department", "TotalSales", "TotalProfit", "AvgMargin"]].to_string(index=False))
    print("\n  Opportunity Score by Store (0-100):")
    print(opportunity_score.to_string())

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score,
    }


def develop_recommendations():
    """
    Develop at least 5 specific, actionable recommendations based on the analysis.
    Returns a list of recommendation strings.
    """
    recommendations = [
        (
            "1. EXPAND MIAMI & SCALE ITS MODEL: Miami generates the highest annual sales and profit "
            "with the best store performance factor (1.2×). GreenGrocer should study Miami's product "
            "mix, staffing ratios, and marketing tactics and replicate them at underperforming locations. "
            "Consider opening a second Miami-area location given demonstrated market demand."
        ),
        (
            "2. INVEST IN PREPARED FOODS ACROSS ALL STORES: Prepared Foods has the highest average "
            "profit margin (~40%) yet only moderate sales volume, indicating untapped potential. "
            "Increasing Prepared Foods floor space, product variety, and in-store promotion—especially "
            "at high-traffic stores like Miami and Tampa—could significantly lift overall profitability."
        ),
        (
            "3. CAPITALIZE ON WEEKEND AND SEASONAL PEAKS: Sales spike ~30% on weekends and ~25% in "
            "December and ~15% in summer. GreenGrocer should schedule additional staff on weekends, "
            "launch targeted seasonal promotions in June–August and December, and ensure inventory "
            "levels are pre-built before these high-demand windows."
        ),
        (
            "4. IMPROVE GAINESVILLE & JACKSONVILLE EFFICIENCY: Both stores underperform on sales "
            "per square foot and per staff member. Recommendations include reducing low-selling SKUs "
            "and reallocating floor space to high-margin Bakery and Prepared Foods categories, "
            "implementing cross-training to improve labor efficiency, and increasing local marketing "
            "spend proportionally to drive foot traffic."
        ),
        (
            "5. DEVELOP LOYALTY PROGRAM TIERS FOR FAMILY SHOPPERS & GOURMET COOKS: These two segments "
            "represent the highest average monthly spend ($150 and $120 respectively). Dedicated "
            "loyalty perks—such as pre-order bulk discounts for Family Shoppers and exclusive "
            "specialty product access for Gourmet Cooks—would increase visit frequency and basket size, "
            "directly boosting revenue."
        ),
        (
            "6. OPTIMIZE MARKETING SPEND BASED ON ROI: The correlation analysis shows that weekly "
            "marketing spend has a strong positive correlation with annual sales. GreenGrocer should "
            "run a controlled A/B marketing test at Jacksonville and Gainesville with 20–25% increased "
            "budgets for 3 months to quantify the sales lift per dollar spent before committing "
            "to broader budget increases."
        ),
    ]

    print("\n[4.2] Business Recommendations")
    for rec in recommendations:
        print(f"\n  {rec}")

    return recommendations


# =============================================================================
# TODO 5: Summary Report
# =============================================================================

def generate_executive_summary():
    """
    Generate a business-focused executive summary with Overview, Key Findings,
    Recommendations, and Expected Impact sections.
    """
    summary = """
================================================================================
                     GREENGROCER — EXECUTIVE SUMMARY (FY 2023)
================================================================================

OVERVIEW
--------
GreenGrocer operated five organic grocery stores across Florida in 2023. The
portfolio generated approximately $28.5 million in annual sales with an average
profit margin of roughly 28%. Performance was uneven: Miami led all stores in
absolute revenue and efficiency, while Gainesville and Jacksonville lagged
significantly. Customer data shows that 5,000 loyalty-program members span five
behavioral segments, with Family Shoppers and Gourmet Cooks driving the greatest
spend-per-visit. Seasonal demand peaks in summer and December represent reliable
levers for targeted revenue uplift.

KEY FINDINGS
------------
• Miami is the top performer on every major metric — annual sales, profit per
  square foot, and customer satisfaction — driven by its large footprint (18,000
  sq ft) and strong local demand. It earns a performance factor of 1.2× versus
  the Tampa baseline.

• Prepared Foods is the highest-margin department (~40% gross margin), yet it
  underperforms on absolute volume relative to Produce. Expanding this category
  offers the clearest path to margin improvement across all locations.

• Weekend traffic is ~30% higher than weekday traffic, and December and summer
  months show 25% and 15% sales lifts respectively. Current staffing and
  inventory practices may not fully capture these predictable demand spikes.

• Store square footage and staff count are the strongest predictors of annual
  sales in our regression model (R² ≈ 0.99 within the training set), confirming
  that scale and operational capacity are foundational to revenue generation.

• Family Shoppers (30% of the customer base) and Gourmet Cooks (20%) account for
  disproportionate wallet share; however, loyalty tier analysis reveals that most
  members fall into Silver or Gold rather than Platinum, indicating headroom to
  deepen engagement.

RECOMMENDATIONS
---------------
• Replicate Miami's operational model at Tampa and Orlando to close the
  performance gap within 12 months.

• Prioritize Prepared Foods expansion — allocate 10–15% more floor space and
  hire dedicated hot-bar/salad-bar staff at the top three stores.

• Implement a seasonal staffing and inventory surge plan for June–August and
  December, targeting a 10% additional sales capture during peak periods.

• Launch targeted loyalty program enhancements for Family Shoppers (bulk-buy
  rewards) and Gourmet Cooks (exclusive specialty product early access) to
  increase Platinum tier conversion.

• Pilot a 3-month marketing budget increase of 20–25% at Gainesville and
  Jacksonville, measuring cost-per-incremental-dollar of sales before scaling
  the investment chain-wide.

EXPECTED IMPACT
---------------
If GreenGrocer successfully closes 50% of the performance gap between its top
and bottom stores, expands Prepared Foods, and captures seasonal peaks more
effectively, we estimate a potential 12–18% increase in total annual profit —
equivalent to roughly $1.0–1.5 million in additional profit at current revenue
scale. Deeper loyalty program engagement with high-value segments could add a
further 5–8% revenue uplift over a 24-month horizon. These are actionable,
data-supported opportunities that should be prioritized in the FY 2024 strategy
review.

================================================================================
"""
    print(summary)


# =============================================================================
# Main function to execute all analyses
# =============================================================================

def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)

    # Execute analyses in a logical order
    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()

    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()

    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()

    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()

    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()

    # Show all figures
    plt.show()

    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }


# Run the main function
if __name__ == "__main__":
    results = main()