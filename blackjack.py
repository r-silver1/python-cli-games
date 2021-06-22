


from IPython.display import clear_output
import random
from time import sleep



class Deck:

    def __init__(self, full=False):
        self.deck = []
        if full:
            self.fill_deck()

    @classmethod
    def get_form(cls, card):
        a = card[0]
        card_form = {
            "h": f"""
 ________
/        \\
|{a:2}      |
|  * . * |
|   * *  |
|    *   |
|      {a:2}|
\________/
            """,
            "d": f"""
 ________
/        \\
|{a:2}      |
|    *   |
|   * *  |
|    *   |
|      {a:2}|
\________/
            """,
            "c": f"""
 ________
/        \\
|{a:2}      |
|    *   |
|   *-*  |
|    |   |
|      {a:2}|
\________/
            """,
            "s": f"""
 ________
/        \\
|{a:2}      |
|    ^   |
|   ***  |
|    |   |
|      {a:2}|
\________/
            """,
            "f": """
 ________
/bicycle \\
|--------|
|*.*.*.*.|
|.*.*.*.*|
|--------|
| ǝlɔʎɔᴉq|
\________/
            """
        }
        return card_form[card[1]].split("\n")

    @classmethod
    def print_card(cls, cards, out=True, hide=False):
        l = cards[:]
        if hide:
            l[0] = ('f', 'f')
        big_s = ""
        lines = []
        for c in l:
            lines.append(cls.get_form(c))
        for j in range(len(cls.get_form(("A", "f")))):
            s = ""
            for i in range(len(lines)):
                s+= f"{lines[i][j]:<12}"
            if out:
                print(s)
            big_s+= s+"\n"
        return big_s

    @classmethod
    def get_val(cls, card):
            vals = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7:7, 8:8, 9:9, 10:10, 'J':10, 'Q':10, 'K':10, 'A':11}
            return vals[card]

    def fill_deck(self):
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        suits = ["h", "d", "c", "s"]
        for c in cards:
            self.deck += list(zip([c]*4, suits))

    def shuff_deck(self):
        random.seed()
        random.shuffle(self.deck)

    def deal(self, n=1):
        l = []
        for _ in range(n):
            l.append(self.deck.pop())
        return l

    def reset(self):
        self.deck = []
        self.fill_deck()

    def clear_hand(self):
        self.deck = []

    def score(self):
        tot = 0
        aceCheck = 0
        for k, v in self.deck:
            addVal = Deck.get_val(k)
            #handle ace rules
            if addVal == 11:
                aceCheck +=1
            tot+=addVal
        if tot > 21:
            for _ in range(aceCheck):
                tot-=10
        return tot

    def add_cards(self, cards):
        for c in cards:
            self.deck.append(c)

    def __eq__(self, other):
        if not isinstance(other, Deck) and not isinstance(other, int):
            raise TypeError("cannot compare equality of Deck with not Deck or int")
        else:
            if isinstance(other, Deck):
                return self.score() == other.score()
            else:
                return self.score() == other

    def __lt__(self, other):
        if not isinstance(other, Deck) and not isinstance(other, int):
            raise TypeError("cannot compare equality of Deck with not Deck or int")
        else:
            if isinstance(other, Deck):
                return self.score() < other.score()
            else:
                return self.score() < other

    def __gt__(self, other):
        if not isinstance(other, Deck) and not isinstance(other, int):
            raise TypeError("cannot compare equality of Deck with not Deck or int")
        else:
            if isinstance(other, Deck):
                return self.score() > other.score()
            else:
                return self.score() > other

    def __le__(self, other):
        if not isinstance(other, Deck) and not isinstance(other, int):
            raise TypeError("cannot compare equality of Deck with not Deck or int")
        elif self > other:
            return False
        else:
            return True

    def __ge__(self, other):
        if not isinstance(other, Deck) and not isinstance(other, int):
            raise TypeError("cannot compare equality of Deck with not Deck or int")
        elif self < other:
            return False
        else:
            return True

    def __len__(self):
        return len(self.deck)

    def __repr__(self, hide=False):
        # return f"Deck: {len(self)}"
        return Deck.print_card(self.deck, out=False, hide=hide)


class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = Deck(full=False)

    def make_move(self):
        raise NotImplementedError("makemove not implemented")

    def make_bet(self):
        raise NotImplementedError("make_bet not implemented")

    def win(self):
        raise NotImplementedError("win not implemented")

    def lose(self):
        raise NotImplementedError("lose not implemented")

    def __repr__(self):
        return f"{self.name:10}: ${self.money:.2f}"


class AI(Player):

    def __init__(self, name, money):
        Player.__init__(self, name, money)

    def make_move(self):
        print("in ai make move")
        pass

    def win(self, x):
        self.money+=x

    def lose(self, x):
        self.money-=x

    def __repr__(self):
        return super(AI, self).__repr__() + " (AI)"


class Human(Player):
    def __init__(self, name, money):
        Player.__init__(self, name, money)
        self.wager = 0

    def make_move(self):
        msg = "What is your move? (stay, hit) "
        while True:
            move = input(msg)
            if move in ["quit", "exit", "no"]:
                return "exit"
            elif move in ["stay", "hit"]:
                return move
            else:
                msg = "you must enter stay, hit, or exit to quit "

    def set_wager(self, limit):
        msg = f"Input a wager, at least ${limit:.2f}. {self.name} has ${self.money} to bet "
        while True:
            x = input(msg)
            if x.isdigit():
                x = float(x)
                if x >= limit and x <= self.money:
                    self.wager = x
                    print(f"your wager is {self.wager}")
                    return
            msg = f"You must enter a dollar amount, at least ${limit:.2f} and less than ${self.money:.2f}, i.e 500 or 500.00 "
            continue

    def win(self):
        self.money += self.wager

    def lose(self):
        self.money -= self.wager

    def __repr__(self):
        return super(Human, self).__repr__() + f", Wager: {self.wager}"



class Game:
    """       Welcome to the game. In Blackjack you are dealt two cards, one of which you and the dealer
       can see and the other which is known only to you. You can hit (ask for another card) or stay
       (decline to take another card), as can the dealer. At the end, whoever is closest to 21 wins
       the bet. But be careful! If you bust (go over 21) and the dealer doesn't, you lose!
       Note: Face cards count as 10, Aces count as 11 unless you go over 21 in which case they
       count as 1"""

    def __init__(self, limit):
        self.dealer = AI("Hal", 1000000000.00)
        self.players = []
        self.limit = limit
        self.cards = Deck(full=True)
        self.active = False

    def start_game(self):
        name = input("Get ready to play! What is your name? ")
        self.players.append(Human(name, 9000.00))
        self.active = True
        self.new_round()

    def new_round(self):
        self.setup_round()
        input("press enter to start ")
        self.print_turn(hide=True)
        self.make_wagers()
        self.print_turn(hide=True)
        bust = False
        while self.active:
            m = self.check_move()
            self.print_turn(hide=True)
            if m == "bust":
                self.handle_bust(self.players, [self.dealer])
                bust = True
            elif m == "stay":
                print("ok, you chose to stay")
        while self.dealer.hand <= 21 and self.dealer.hand <= self.players[0].hand and not bust:
            self.print_turn(hide=False)
            print("Dealer's Turn")
            sleep(1.2)
            s = self.check_hand(self.dealer)
            if s == "bust":
                self.handle_bust(self.dealer, self.players, isdealer=True)
                bust = True
        if not bust:
            self.print_turn(hide=False)
            winners = self.check_winner()
            if len(winners) == 0:
                print(f"{self.dealer.name} wins! {[p.name for p in self.players]} lost!")
                for p in self.players:
                    p.lose()
                    self.dealer.win(p.wager)
            else:
                print(f"{self.dealer.name} and {[p.name for p in self.players]} have the same score, draw!")

        self.check_continue()

    def setup_round(self):
        for p in self.players:
            p.wager = 0
            p.hand.clear_hand()

        self.dealer.hand.clear_hand()
        self.active = True
        self.cards.reset()
        self.cards.shuff_deck()
        self.first_deals()

    def check_winner(self):
        w = []
        for p in self.players:
            if p.hand >= self.dealer.hand:
                w.append(p)
        return w

    def handle_bust(self, loser, winners, isdealer=False):
        self.print_turn(hide=False)
        if isdealer:
            msg = f"Oh no! {loser.name} busted"
            msg += ", the house pays out! "
            for p in winners:
                p.win()
                self.dealer.lose(p.wager)
        else:
            msg = f"Oh no! "
            self.active = False
            for p in loser:
                p.lose()
                msg += p.name + " "
                self.dealer.win(p.wager)
            msg += "busted, "

        msg += f"{[w.name for w in winners]} wins!"
        print(msg)


    def make_wagers(self):
        for p in self.players:
            p.set_wager(self.limit)


    def first_deals(self):
        self.players[0].hand.add_cards(self.cards.deal(2))
        self.dealer.hand.add_cards(self.cards.deal(2))

    def check_hand(self, plyr):
        plyr.hand.add_cards(self.cards.deal(1))
        if plyr.hand > 21:
            return "bust"
        else:
            return

    def check_move(self):
        s = self.players[0].make_move()
        if not self.checkExit(s):
            return
        else:
            if s == "stay":
                self.active = False
                "stay"
            else:
                return self.check_hand(self.players[0])

    def checkExit(self, s):
        if s in ["exit", "quit", "no", "n"]:
            self.active = False
            return False
        return True

    def check_continue(self):
        if self.players[0].money < self.limit:
            self.handle_exit()
            print("You don't have enough money for this tables limit, maybe check the slots out")
            return
        else:
            msg = "would you like to continue playing? enter (yes, y, continue) or (exit, quit, no) "
            while True:
                b = input(msg)
                if not self.checkExit(b):
                    self.handle_exit()
                    return
                elif b in ["yes", "y", "continue"]:
                    self.new_round()
                else:
                    msg = "you must enter one of the following: yes, y, or continue to keep playing, exit, quit, or no to leave the table "

    def handle_exit(self):
        clear_output()
        self.setup_round()
        Deck.print_card(self.cards.deck[-1:-11:-1], out=True)
        print(f"{'FINAL RESULTS':^120}\n")
        print(self.print_scores())
        print(f"THANK YOU FOR PLAYING! {[p.name for p in self.players]}")
        Deck.print_card([(1, 'f')] * 10, out=True)

    def print_hands(self, hide=True):
        s = ""
        s += f"{'Dealer Hand':^120}\n"
        s += f"{self.dealer.hand.__repr__(hide=hide):120}"
        s += "\n"*2
        s += f"{str(self.players[0].hand):120}"
        s += f"{'Your Hand':^120}\n"
        return s

    def print_scores(self):
        s = ''
        s += f"{'______________________________________________________':^120}\n"
        s += f"{'Dealer:':^30} | {self.dealer }\n"
        s += f"{'Players:':^30} | {self.players}\n\n"
        return s

    def print_turn(self, hide=True):
        clear_output()
        print("\n" * 40)
        print(self.print_scores())
        print(self.print_hands(hide=hide))

    def __repr__(self):
        clear_output()
        s = ""
        s += Deck.print_card(self.cards.deck[-1:-11:-1], out=False)
        s += f"{'BLACKJACK! BLACKJACK! BLACKJACK! BLACKJACK! BLACKJACK!':^120}\n"
        s += self.print_scores()
        s += f"LIMIT: ${self.limit}\n\n"
        s += Game.__doc__+"\n"
        s += Deck.print_card([(1, 'f')]*10, out=False)
        return s


if __name__ == "__main__":
    h = Human("Rob", 9000.00)
    # g = Game(a, h, 500.00)
    clear_output()
    g = Game(500.00)
    print(g)
    g.start_game()