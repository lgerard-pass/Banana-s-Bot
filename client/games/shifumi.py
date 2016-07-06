def shifumi_check(message):
    if message.content == "rock" or message.content == "paper" or message.content == "scissors":
        return True
    else:
        return False


def get_shifumi_winner(p1,p2):
    if p1 == p2:
        return "ties"
    elif p1 == "rock":
        if p2 == "paper":
            return 'loses to'
        elif p2 == "scissors":
            return 'wins against'
    elif p1 == "paper" :
        if p2 == "rock":
            return 'wins against'
        elif p2 == "scissors":
            return 'loses to'
    elif p1 == "scissors":
        if p2 == "rock":
            return 'loses to'
        elif p2 == "paper":
            return 'wins against'
