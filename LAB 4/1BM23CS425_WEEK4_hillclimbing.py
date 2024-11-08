import random

def get_user_board(n):
    board = []
    print(f"Enter the initial row positions for each column (0 to {n-1}):")
    for col in range(n):
        row = int(input(f"Column {col + 1}: "))
        if 0 <= row < n:
            board.append(row)
        else:
            print("Invalid input. Row must be between 0 and", n - 1)
            return None
    return board

def heuristic(board):
    n = len(board)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                attacks += 1
    return attacks

def get_neighbors(board):
    neighbors = []
    n = len(board)
    for col in range(n):
        for row in range(n):
            if board[col] != row:
                neighbor = board[:]
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

def print_board(board):
    """Prints the board visually, showing 'Q' for queens and '.' for empty spaces."""
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print("\n")

def hill_climbing_with_restarts(n, initial_board):
    current = initial_board
    restarts = 0
    heuristic_evaluations = 0
    iteration = 1

    while True:
        print(f"\nRestart #{restarts + 1}")
        while True:
            current_heuristic = heuristic(current)
            heuristic_evaluations += 1
            print(f"Iteration {iteration}: Heuristic = {current_heuristic}")
            print_board(current)  # Print the current board visually
            iteration += 1

            if current_heuristic == 0:
                print(f"Solution found!\nTotal restarts: {restarts}\nTotal heuristic evaluations: {heuristic_evaluations}")
                return current

            neighbors = get_neighbors(current)
            best_neighbor = min(neighbors, key=heuristic)
            best_neighbor_heuristic = heuristic(best_neighbor)
            heuristic_evaluations += len(neighbors)

            if best_neighbor_heuristic >= current_heuristic:
                print("Stuck in a local minimum, restarting...\n")
                break  # Local minimum reached, so we restart

            current = best_neighbor

        # Restart with a new random board if stuck
        current = generate_board(n)
        restarts += 1

def generate_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]

# Main execution
n = int(input("Enter the number of queens (e.g., 4 for 4-Queens): "))
initial_board = get_user_board(n)

if initial_board:
    solution = hill_climbing_with_restarts(n, initial_board)
    print("Final Solution:")
    print_board(solution)
    print("Attacking pairs:", heuristic(solution))
else:
    print("Invalid initial board configuration.")
