playing = True
binAmount = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
playerOne = True
messageCode = 0
giveawayPile = -1
lastRecipient = -1


def evaluate_state(state):
    return state[13] - state[6]


def minimax(state, depth, alpha, beta, maximizingPlayer, isPlayerOneTurn):
    if depth == 0 or game_over(state):
        return evaluate_state(state), None

    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        for child, chosen_bin in generate_children(state, not isPlayerOneTurn):
            eval, _ = minimax(child, depth - 1, alpha, beta, False, not isPlayerOneTurn)
            if eval > maxEval:
                maxEval = eval
                best_move = chosen_bin
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for child, chosen_bin in generate_children(state, isPlayerOneTurn):
            eval, _ = minimax(child, depth - 1, alpha, beta, True, isPlayerOneTurn)
            if eval < minEval:
                minEval = eval
                best_move = chosen_bin
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move


def game_over(state):
    return sum(state[0:6]) == 0 or sum(state[7:13]) == 0


def generate_children(state, playerTwo):
    children = []
    start, end = (7, 13) if playerTwo else (0, 6)
    for i in range(start, end):
        if state[i] > 0:
            new_state, extra_turn = distribute_seeds(state.copy(), i, playerTwo)
            children.append((new_state, i))
    return children


def distribute_seeds(state, chosen_bin, playerTwo):
    seeds = state[chosen_bin]
    state[chosen_bin] = 0
    index = chosen_bin
    while seeds > 0:
        index = (index + 1) % 14
        if index == 13 and playerTwo or index == 6 and not playerTwo:
            continue
        state[index] += 1
        seeds -= 1

    extra_turn = False
    if playerTwo and index == 13 or not playerTwo and index == 6:
        extra_turn = True
    elif 0 <= index < 6 or 7 <= index < 13:
        opposite_index = 12 - index
        if state[index] == 1 and state[opposite_index] > 0:
            state[13 if playerTwo else 6] += state[index] + state[opposite_index]
            state[index] = state[opposite_index] = 0

    return state, extra_turn


def ai_move(state):
    _, best_move = minimax(state, 5, float('-inf'), float('inf'), True, False)  # AI is maximizing player
    return best_move


def print_board(state):
    print("+----+----+----+----+----+----+----+----+")
    print("|    | " + " | ".join(f"{state[i]:2}" for i in range(12, 6, -1)) + " |    |")
    print("| " + f"{state[13]:2}" + " +----+----+----+----+----+----+ " + f"{state[6]:2}" + " |")
    print("|    | " + " | ".join(f"{state[i]:2}" for i in range(6)) + " |    |")
    print("+----+----+----+----+----+----+----+----+")


def main():
    playing = True
    binAmount = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    playerOne = True

    while playing:
        print_board(binAmount)
        if playerOne:
            print("\nPlayer One's Turn...")
            user_input = input("Choose a bin (a-f): ").strip().lower()
            if user_input == 'q':
                print("Game ended by user.")
                break
            chosen_bin = ord(user_input) - ord('a')
            if 0 <= chosen_bin <= 5:
                new_state, extra_turn = distribute_seeds(binAmount, chosen_bin, playerOne)
                if not extra_turn:
                    playerOne = False
            else:
                print("Invalid input. Please select a bin between 'a' and 'f'.")
        else:
            print("\nPlayer Two (AI)'s Turn...")
            ai_bin = ai_move(binAmount)
            if ai_bin is not None:
                print(f"AI chooses bin {chr(ai_bin + 65).lower()}")
                new_state, extra_turn = distribute_seeds(binAmount, ai_bin, playerOne)
                if not extra_turn:
                    playerOne = True

        if game_over(binAmount):
            binAmount[6] += sum(binAmount[:6])
            binAmount[13] += sum(binAmount[7:13])
            for i in list(range(6)) + list(range(7, 13)):
                binAmount[i] = 0
            print_board(binAmount)
            if binAmount[6] > binAmount[13]:
                print("Player One Wins!")
            elif binAmount[6] < binAmount[13]:
                print("Player Two (AI) Wins!")
            else:
                print("It's a Draw!")
            playing = False


if __name__ == "__main__":
    main()