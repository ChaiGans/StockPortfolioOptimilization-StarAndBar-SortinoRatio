import itertools

def calculate_annualized_return(annual_returns):
    """
    Calculate the annualized return given a list of annual returns.

    Parameters:
    annual_returns (list): List of annual returns (expressed as percentages).

    Returns:
    float: The annualized return.
    """
    compounded_return = 1
    for return_percent in annual_returns:
        compounded_return *= (1 + return_percent / 100)
    
    years = len(annual_returns)
    
    return ((compounded_return ** (1 / years)) - 1)*100

def calculate_downside_deviation(downside_rates):
    if not downside_rates:
        return 0  # Avoid division by zero if the list is empty

    mean_rate = sum(downside_rates) / len(downside_rates)
    squared_deviations = [(rate - mean_rate) ** 2 for rate in downside_rates]
    variance = sum(squared_deviations) / (len(downside_rates) - 1)
    return variance ** 0.5  # Square root of variance

def get_sortino_ratio(expected_return, downside_deviation):
    """Calculates the Sortino Ratio for a given expected return and downside deviation."""
    if downside_deviation == 0:
        return float('inf')  # Prevent division by zero
    return (expected_return-2.5) / downside_deviation # 2.5% is risk free rate

def get_user_inputs():
    """Gets and processes user inputs."""
    interested_stocks = input("Enter the stock codes you're interested in (separated by space): ").split()
    total_investment = float(input("Enter your total investment amount: "))
    return interested_stocks, total_investment

def calculate_min_investment(interested_stocks, stock_data, total_investment):
    """Calculates the minimum investment required to optimize the portfolio."""
    min_investment = float('inf')
    for stock in interested_stocks:
        cost_of_100_shares = stock_data[stock]['price'] * 100
        if cost_of_100_shares < min_investment:
            min_investment = cost_of_100_shares
    return total_investment - (total_investment % min_investment)

def generate_combinations(interested_stocks, stock_data, total_investment, min_investment):
    """Generates all possible unique combinations of stock lots within the investment limits."""
    max_lots = {stock: int(total_investment // (stock_data[stock]['price'] * 100)) for stock in interested_stocks}
    all_combinations = []
    unique_combinations = set()

    for combination in itertools.product(*(range(max_lots[stock] + 1) for stock in interested_stocks)):
        total_cost = sum(stock_data[stock]['price'] * 100 * combination[idx] for idx, stock in enumerate(interested_stocks))
        if min_investment <= total_cost <= total_investment:
            formatted_combination = tuple((stock, combination[idx]) for idx, stock in enumerate(interested_stocks))
            if formatted_combination not in unique_combinations:
                unique_combinations.add(formatted_combination)
                all_combinations.append(list(formatted_combination))
    return all_combinations

def find_best_combination(all_combinations, sortino_ratios):
    """Finds the best stock combination based on the highest number of Sortino Ratio."""
    best_combo = None
    best_ratio = -1

    for combo in all_combinations:
        total_lots = sum(lots for _, lots in combo)
        if total_lots == 0:
            continue
        weighted_sortino_ratio = sum(sortino_ratios[stock] * lots for stock, lots in combo) / total_lots
        combo.append(weighted_sortino_ratio)
        ratio = combo[-1]
        if ratio > best_ratio:
            best_ratio = ratio
            best_combo = combo
    return best_combo

# Main code
interested_stocks, total_investment = get_user_inputs()

# Static data setup for each stock
stock_data = {
    # Example: 'STOCK_CODE': {'price': ..., 'DD': ...}
    # DD is last five year downside percentage
    # AR is last five year price movement percentage
    'BBCA': {'price': 8800, 'DD': [0,0,0,0,-0.28], 'AR': [28.56,1.27,7.83,17.12,2.63]},
    'BMRI': {'price': 5800, 'DD': [0,-17.59,0,0,0], 'AR': [4.07,-17.59,11.07,41.28,15.37]},
    'BBNI': {'price': 5225, 'DD': [-10.8,-21.34,0,0,0], 'AR': [-10.8,-21.34,9.31,36.37,10.57]},
    'BBRI': {'price': 5425, 'DD': [0,-5.23,0,0,0], 'AR': [20.22,-5.23,1.03,20.19,10.32]}, 
    'BBTN': {'price': 1265, 'DD': [-28.85,-16.54,-18.63,-19.07,-9.26], 'AR': [-16.54,-18.63,0.29,-19.07,-10.00]},
    'AGRO': {'price': 308, 'DD': [-36.13,0,0,-77.68,-26.24], 'AR': [-36.13,422.73,78.74,-77.68,-27.72]},
    'BJTM': {'price': 615, 'DD': [-0.72,-0.73,0,-5.33,-13.38], 'AR': [-0.72,-0.73,10.29,-5.33,-13.38]},
    'BGTG': {'price': 78, 'DD': [-19.51,0,0,-62.72,-9.2], 'AR': [-19.51,12.12,229.73,-62.72,-9.2]},
    'ASII': {'price': 5725, 'DD': [-15.81,-13.00,-5.39,0,-0.44], 'AR': [-15.81,-13.00,-5.39,0,-0.88]},
    'BRIS': {'price': 1740, 'DD': [-37.14,0,-20.89,-25.69,0], 'AR': [-37.14,581.82,-20.89,-25.69,28.68]},
}

sortino_ratios = {stock: get_sortino_ratio(calculate_annualized_return(stock_data[stock]['AR']), calculate_downside_deviation(stock_data[stock]['DD'])) for stock in stock_data}
min_investment = calculate_min_investment(interested_stocks, stock_data, total_investment)
all_combinations = generate_combinations(interested_stocks, stock_data, total_investment, min_investment)
best_combo = find_best_combination(all_combinations, sortino_ratios)

# Output results
for combo in all_combinations:
    print(combo)
print("Total Combination: ", len(all_combinations)) # Total combinations after filtered with > min_investment
print("Best Combination:", best_combo)
