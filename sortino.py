import itertools

def calculating_sortino_ratio(expected_return, downside_derivation):
    print(expected_return)
    return expected_return / downside_derivation

# User inputs
interested_stocks = input("Enter the stock codes you're interested in (separated by space): ").split()
total_investment = float(input("Enter your total investment amount: "))
target_return = float(input("Enter your target return (in percentage): ")) / 100

# Static data setup for each stock
stock_data = {
    # Example: 'STOCK_CODE': {'price': ..., 'DD': ...}
    # Fill this with static data
    # DD is One last year downside percentage
    'BBCA': {'price': 8800, 'DD': 0.28},
    'BMRI': {'price': 5800, 'DD': -10.31},
    'BBNI': {'price': 5225, 'DD': -13.44},
    'BBRI': {'price': 5425, 'DD': -17.74},
    'BBTN': {'price': 1265, 'DD': 12.47},
    'BBHI': {'price': 1420, 'DD': 39.83},
    'AGRO': {'price': 308, 'DD': 39.61},
    'BJTM': {'price': 615, 'DD': 12.14},
    'BGTG': {'price': 78, 'DD': 21.21},
    'ASII': {'price': 5725, 'DD': 12.26},
    'BRIS': {'price': 1740, 'DD': -26.28},
}

# Calculating Sortino Ratio for each stock
sortino_ratios = {stock: calculating_sortino_ratio(target_return, stock_data[stock]['DD']) for stock in stock_data}

# Calculating minimal investment to optimize portfolio
min_investment = float('inf')  # Start with a very high value
for stock in interested_stocks:
    cost_of_100_shares = stock_data[stock]['price'] * 100
    if cost_of_100_shares < min_investment:
        min_investment = cost_of_100_shares
min_investment = total_investment - (total_investment % min_investment)
print(min_investment)
 
# Calculating maximum lots for each stock
max_lots = {stock: int(total_investment // (stock_data[stock]['price'] * 100) ) for stock in interested_stocks}

# Generating all possible combinations
all_combinations = []
# Use a set to keep track of unique combinations
unique_combinations = set()

# Updated code for generating all possible combinations
for i in range(1, len(interested_stocks) + 1):
    for combination in itertools.product(*(range(max_lots[stock] + 1) for stock in interested_stocks)):
        total_cost = sum(stock_data[interested_stocks[j]]['price'] * 100 * combination[j] for j in range(len(interested_stocks)))
        if total_cost >= min_investment and total_cost <= total_investment:
            formatted_combination = tuple((interested_stocks[j], combination[j]) for j in range(len(interested_stocks)))
            # Check for uniqueness before adding to all_combinations
            if formatted_combination not in unique_combinations:
                unique_combinations.add(formatted_combination)
                all_combinations.append(list(formatted_combination))

# Calculate weighted Sortino Ratio for each unique combination
for combo in all_combinations:
    total_lots = sum(lots for _, lots in combo)
    if total_lots == 0:
        continue
    weighted_sortino_ratio = sum(sortino_ratios[stock] * lots for stock, lots in combo) / total_lots
    combo.append(weighted_sortino_ratio)

# Identifying the best combination
best_combo = None
best_ratio = float('inf')

for combo in all_combinations:
    ratio = combo[-1]
    if (abs(ratio) < abs(best_ratio)) or (ratio == best_ratio and ratio < 0):
        best_ratio = ratio
        best_combo = combo

# Output all unique combinations with Sortino Ratio
for combo in all_combinations:
    print(combo)

# Output the best combination
print("Best Combination:", best_combo)