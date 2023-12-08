import itertools

def calculate_proportional_investment(stock_data, stock_combination, total_investment):
    # Calculate the proportion of total investment in each stock
    total_price = sum(stock_data[stock]['price'] for stock in stock_combination)
    return {stock: (stock_data[stock]['price'] / total_price) * total_investment for stock in stock_combination}

def calculate_expected_return(target_return, stock_combination, proportional_investment):
    # Calculate the weighted average of expected returns based on proportional investment
    total_weighted_return = sum(target_return * proportional_investment[stock] for stock in stock_combination)
    return total_weighted_return / total_investment

def calculate_downside_deviation(stock_data, stock_combination, target_return):
    # Calculate the weighted standard deviation of downside risks
    downside_risks = [min(0, stock_data[stock]['downside'] - target_return) for stock in stock_combination]
    if not downside_risks:
        return 0
    mean_downside = sum(downside_risks) / len(downside_risks)
    squared_diffs = [(risk - mean_downside) ** 2 for risk in downside_risks]
    mean_squared_diff = sum(squared_diffs) / len(squared_diffs)
    return mean_squared_diff ** 0.5

def calculate_sortino_ratio(stock_data, stock_combination, total_investment, target_return):
    proportional_investment = calculate_proportional_investment(stock_data, stock_combination, total_investment)
    expected_return = calculate_expected_return(stock_data, stock_combination, proportional_investment)
    downside_deviation = calculate_downside_deviation(stock_data, stock_combination, target_return)

    if downside_deviation == 0:
        return float('inf')  # Avoid division by zero
    
    sortino_ratio = (expected_return - target_return) / downside_deviation
    return sortino_ratio

# User inputs
interested_stocks = input("Enter the stock codes you're interested in (separated by space): ").split()
total_investment = float(input("Enter your total investment amount: "))
max_loss = float(input("Enter your maximum acceptable loss (in percentage): "))
target_return = float(input("Enter your target return (in percentage): "))

# Static data setup for each stock
stock_data = {
    # Example: 'STOCK_CODE': {'price': ..., 'downside': ...}
    # Fill this with static data
    'BBCA': {'price': 8800, '1Ydownside': 0},
    'BMRI': {'price': 5800, '1Ydownside': -14.85},
    'BBNI': {'price': 5225, '1Ydownside': -12.67},
    'BBRI': {'price': 5425, '1Ydownside': -19.76},
    'BBTN': {'price': 1265, '1Ydownside': 12.47},
    'BBHI': {'price': 1420, '1Ydownside': 39.83},
    'AGRO': {'price': 308, '1Ydownside': 39.61},
    'BJTM': {'price': 615, '1Ydownside': 12.14},
    'BGTG': {'price': 78, '1Ydownside': 21.21},
    'ASII': {'price': 5725, '1Ydownside': 12.26},
    'BRIS': {'price': 1740, '1Ydownside': -30.4},
    'INDF': {'price': 6500, '1Ydownside': -0.39},
    'ICBP': {'price': 10650, '1Ydownside': -9.51}
}

# Generating all possible combinations
all_combinations = []
for i in range(1, len(interested_stocks) + 1):
    for combination in itertools.combinations(interested_stocks, i):
        if sum(stock_data[stock]['price'] for stock in combination) <= total_investment:
            all_combinations.append(combination)

# Finding the best combination
best_combination = None
highest_sortino_ratio = -float('inf')

for combination in all_combinations:
    proportional_investment = calculate_proportional_investment(stock_data, combination, total_investment)
    print(proportional_investment)
    expected_return = calculate_expected_return(target_return, combination, proportional_investment)
    downside_deviation = calculate_downside_deviation(stock_data, combination, target_return)
    
    # Convert max_loss to a decimal
    max_loss_decimal = max_loss / 100.0
    # Convert target_return to a decimal
    target_return_decimal = target_return / 100.0

    if downside_deviation <= max_loss_decimal:
        sortino_ratio = calculate_sortino_ratio(stock_data, combination, total_investment, target_return_decimal)
        if sortino_ratio > highest_sortino_ratio:
            highest_sortino_ratio = sortino_ratio
            best_combination = combination

# Output the best combination
print("Best Combination:", best_combination)
print("Highest Sortino Ratio:", highest_sortino_ratio)