"""Core Skills Drill — Descriptive Analytics

Compute summary statistics, plot distributions, and create a correlation
heatmap for the sample sales dataset.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def compute_summary(df):
    """Task 1: Compute summary statistics for numeric columns."""
    numeric_df = df.select_dtypes(include=['number'])
    
    summary = numeric_df.describe().loc[['count', 'mean', '50%', 'std', 'min', 'max']]
    summary = summary.rename(index={'50%': 'median'})
    
    os.makedirs("output", exist_ok=True)
    summary.to_csv("output/summary.csv")
    print("✅ Summary statistics saved to output/summary.csv")
    
    return summary


def plot_distributions(df, columns, output_path="output/distributions.png"):
    """Create individual distribution plots for each numeric column"""
    n = len(columns)
    
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 6))
    if n == 1:
        axes = [axes]
    
    for i, col in enumerate(columns):
        sns.histplot(data=df, x=col, kde=True, ax=axes[i], color='skyblue')
        axes[i].set_title(f'Distribution of {col}', fontsize=13)
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Distributions plot saved to {output_path}")


def plot_correlation(df, output_path="output/correlation.png"):
    """Task 3: Create correlation heatmap."""
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.shape[1] < 2:
        print("⚠️ Not enough numeric columns for correlation heatmap.")
        return
    
    corr_matrix = numeric_df.corr(method='pearson')
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, 
                annot=True, 
                cmap='coolwarm', 
                vmin=-1, 
                vmax=1, 
                center=0,
                fmt='.2f',
                square=True,
                linewidths=0.5)
    
    plt.title('Correlation Heatmap (quantity vs unit_price)', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Correlation heatmap saved to {output_path}")



def plot_revenue_relationships(df, output_path="output/revenue_relationships.png"):
    """New plot: Relationship between revenue and other variables"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Scatter: Quantity vs Revenue
    sns.scatterplot(data=df, x='quantity', y='revenue', ax=axes[0], alpha=0.7, color='purple')
    axes[0].set_title('Quantity vs Revenue', fontsize=13)
    axes[0].set_xlabel('Quantity')
    axes[0].set_ylabel('Revenue')
    
    # Scatter: Unit Price vs Revenue
    sns.scatterplot(data=df, x='unit_price', y='revenue', ax=axes[1], alpha=0.7, color='orange')
    axes[1].set_title('Unit Price vs Revenue', fontsize=13)
    axes[1].set_xlabel('Unit Price')
    axes[1].set_ylabel('Revenue')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Revenue relationships plot saved to {output_path}")




    
    """Main function"""
    os.makedirs("output", exist_ok=True)

    # Load data
    df = pd.read_csv("data/sample_sales.csv")
    print(f"✅ Data loaded! Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}\n")

    df['revenue'] = df['quantity'] * df['unit_price']
    print(f"✅ Data loaded! Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}\n")

    # Task 1: Summary Statistics
    summary = compute_summary(df)
    print("\nSummary Statistics:\n", summary.round(2))

    # Task 2: Distribution Plots → 
       
    numeric_cols = ['quantity', 'unit_price', 'revenue']

    # Task 3: Correlation Heatmap
    plot_correlation(df)

    print("\n🎉 All tasks completed successfully!")
    print("Check the 'output/' folder for summary.csv, distributions.png, and correlation.png")

def main():
    """Main function"""
    os.makedirs("output", exist_ok=True)

    # Load data
    df = pd.read_csv("data/sample_sales.csv")
    df['revenue'] = df['quantity'] * df['unit_price']   # Derived column
    
    print(f"✅ Data loaded! Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}\n")

    # Task 1: Summary Statistics
    summary = compute_summary(df)
    print("\nSummary Statistics:\n", summary.round(2))

    # Task 2: Distribution Plots for all 3 numeric columns
    numeric_cols = ['quantity', 'unit_price', 'revenue']
    print(f"\nPlotting distributions for: {numeric_cols}")
    plot_distributions(df, numeric_cols)

    # New: Revenue Relationships Plot
    plot_revenue_relationships(df)

    # Task 3: Correlation Heatmap
    plot_correlation(df)

    print("\n🎉 All tasks completed successfully!")
    print("Check the 'output/' folder.")
if __name__ == "__main__":
    main()