use std::fmt;
use std::collections::HashMap;

// constants
// const var POCKET_POSITION: string = { 0:"A", 1:"B", 2:"C", 3:"D", "A":0, "B":1, "C":2, "D":3 }
// my_array.iter().any(|&x| x == search_item)
// let rank_a = front_card.chars().nth(1).expect("front card must have format SR");
const SUITS: [char; 4] = ['D', 'S', 'H', 'C'];
const RANKS: [char; 13] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'];
const REDS: &str = "DH";
const BLACKS: &str = "SC";

#[derive(Copy, Clone)]
struct Card
{
    suit: char,
    rank: char
}

#[derive(Clone)]
struct FreecellBoard
{
    pockets: Vec<Card>,
    piles: [Vec<Card>; 8],
    foundations: HashMap<char, char>
}

struct SolitairePlayer
{
    board: FreecellBoard,
    moves_sequence: Vec<String>
}

fn is_opposite(front_card: &Card, back_card: &Card) -> bool
{
    let suit_a: char = front_card.suit;
    let suit_b: char = back_card.suit;

    return (!REDS.contains(suit_a) && REDS.contains(suit_b)) ||
            (!BLACKS.contains(suit_a) && BLACKS.contains(suit_b));
}

fn is_ordered(front_card: &Card, back_card: &Card) -> bool
{
    let rank_a = front_card.rank;
    let rank_b = back_card.rank;
    let index_a = RANKS.iter().position(|&r| r == rank_a).unwrap();
    let index_b = RANKS.iter().position(|&r| r == rank_b).unwrap();

    return index_a == index_b + 1;
}

fn is_valid(front_card: Card, back_card: Card) -> bool
{
    return is_opposite(&front_card, &back_card) && is_ordered(&front_card, &back_card);
}

impl fmt::Display for Card {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result
    {
        return write!(f, "{}{}", self.suit, self.rank);
    }
}

impl fmt::Debug for Card {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result
    {        
        return write!(f, "{}{}", self.suit, self.rank);
    }
}

impl FreecellBoard
{
    fn new() -> Self
    {
        let mut full_deck: Vec<Card> = Vec::new();

        let mut all_piles: [Vec<Card>; 8] =
        [
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new()
        ];

        // all 52 cards
        for i in SUITS.iter()
        {
            for j in RANKS.iter()
            {
                full_deck.push(Card { suit: i.clone(), rank: j.clone() });
            }
        }

        // 24 cards here
        for i in 0..4
        {
            for _j in 0..6
            {
                all_piles[i].push(full_deck.pop().unwrap());
            }
        }

        // 28 cards here
        for i in 4..8
        {
            for _j in 0..7
            {
                all_piles[i].push(full_deck.pop().unwrap());
            }
        }

        let mut starting_foundations: HashMap<char, char> = HashMap::new();

        starting_foundations.insert('D', '-');
        starting_foundations.insert('S', '-');
        starting_foundations.insert('H', '-');
        starting_foundations.insert('C', '-');

        return Self
        {
            pockets: Vec::<Card>::new(),
            piles: all_piles,
            foundations: starting_foundations
        }
    }
        
    fn print_full_board(&self)
    {
        println!("\nFREE CELLS: {:?}", self.pockets);
        println!("FOUNDATIONS: {:?}", self.foundations);
        for i in 0..8
        {
            println!("COLUMN {}: {:?}", i, self.piles[i]);
        }
    }

    fn move_card_pile_to_pile(&mut self, start_row: usize, end_row: usize)
    {
        assert!(start_row < 8);
        assert!(end_row < 8); 

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.piles[end_row].push(move_card);
    }

    fn move_card_pile_to_pocket(&mut self, start_row: usize)
    {
        assert!(start_row < 8);

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.pockets.push(move_card);
    }

    fn move_card_pocket_to_pile(&mut self, start_pos: usize, end_row: usize)
    {
        assert!(start_pos < self.pockets.len());
        assert!(end_row < 8);

        let move_card = self.pockets.remove(start_pos);
        self.piles[end_row].push(move_card);
    }
    
    fn push_pile_to_foundation(&mut self, start_row: usize)
    {
        assert!(start_row < 8);

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.foundations.insert(move_card.suit, move_card.rank);
    }

    fn push_pocket_to_foundation(&mut self, start_pos: usize)
    {
        assert!(start_pos < self.pockets.len());
        
        let move_card = self.pockets.remove(start_pos);
        self.foundations.insert(move_card.suit, move_card.rank);
    }
}

impl SolitairePlayer
{
    fn new() -> Self
    {
        // things missing from the game
        // a way to read in the tableau from a text file
        // a way to play the game as a human
        // a way to solve an existing board and get back the list of moves needed
        // which will require the valid moves list and heuristic and a star algorithm
        return Self
        {
            board: FreecellBoard::new(),
            moves_sequence: Vec::new()
        }
    }

    fn get_heuristic(&self) -> usize
    {
        let mut unordered_pairs = 0;
        for row in self.board.piles.iter()
        {
            for i in 0..row.len() - 1
            {
                if !is_valid(row[i], row[i + 1])
                {
                    unordered_pairs += 1;
                }
            }
        }

        let mut foundation_cards = 0;
        for suit in SUITS.iter()
        {
            let foundation_rank = self.board.foundations[suit];
            let rank_index = RANKS.iter().position(|&r| r == foundation_rank);

            if rank_index.is_some()
            {
                foundation_cards += rank_index.unwrap();
            }
        }

        // heuristic is totalcards + outofordercards - cardsinfoundation
        return 52 + unordered_pairs - foundation_cards;
    }

    fn reached_win(&self) -> bool
    {
        return self.get_heuristic() == 0
    }

    fn get_all_valid_moves(&self) -> Vec<String>
    {
        let valid_moves = Vec::<String>::new();

        // pocket to foundation
        for i in range(len(self.board.pockets)):
            suit_spot = SUITS.index(self.board.pockets[i][0])
            card_rank_index = RANKS.index(self.board.pockets[i][1])
            current_rank = self.board.foundations[suit_spot][1]
            if current_rank == RANKS[card_rank_index - 1]:
                valid_moves.append(POCKET_POSITION[i] + "~E")
        // pile to foundation
        for i in range(len(self.board.piles)):
            if not self.board.piles[i]: # no cards in pile to move
                pass
            suit_spot = SUITS.index(self.board.piles[i][-1][0])
            card_rank_index = RANKS.index(self.board.piles[i][-1][1])
            current_rank = self.board.foundations[suit_spot][1]
            if current_rank == RANKS[card_rank_index - 1]:
                valid_moves.append(str(i) + "~E")
        # pile to pocket
        open_pocket = len(self.board.pockets)
        if open_pocket < 4:
            for i in range(len(self.board.piles)):
                if self.board.piles[i]: # card must exist in order to pocket it
                    valid_moves.append(str(i) + "~" + POCKET_POSITION[open_pocket])
        # pocket to pile
        for i in range(len(self.board.piles)):
            if not self.board.piles[i] and len(self.board.pockets) > 0:
                # any card can go into an empty pile
                for j in range(len(self.board.pockets)):
                    valid_moves.append(POCKET_POSITION[j] + "~" + str(i))
            else:
                # must be opposite color and rank 1 down
                for j in range(len(self.board.pockets)):
                    if IS_VALID(self.board.piles[i][-1], self.board.pockets[j]):
                        valid_moves.append(POCKET_POSITION[j] + "~" + str(i))
        # pile to pile
        for i in range(len(self.board.piles)):
            if not self.board.piles[i]:
                # any card can go into an empty pile
                for j in range(len(self.board.piles)):
                    valid_moves.append(str(j) + "~" + str(i))
            else:
                # must be opposite color and rank 1 down
                for j in range(len(self.board.piles)):
                    if i != j and IS_VALID(self.board.piles[i][-1], self.board.piles[j][-1]):
                        valid_moves.append(str(j) + "~" + str(i))
        
        return valid_moves
        return false
    }

    fn a_star_search(board: FreecellBoard)
    {
        let q = [gameobject]
        while q:
                # get gameobject with best moveset
                gameobject = heapq.heappop(q)

                if gameobject.condition == "win":
                        print(gameobject.previous_moves)
                        print(gameobject.score)
                        gameobject.board.get_board()
                        return True
                else:
                        for dir in ['U', 'R', 'D', 'L']:
                                if gameobject.player.is_valid_move(gameobject.board.truemap, dir):
                                        # simulate doing move before adding to the queue
                                        nextmove = deepcopy(gameobject)
                                        nextmove.game_loop(dir)
                                        nextmove.update_condition()
                                        nextmove.set_heuristic()
                                        if nextmove.condition != "lose":
                                                heapq.heappush(q, nextmove)
    }
}

fn main()
{
    println!("hello.");

    // set up board
    // if arg given parse here

    // ask for input and parse it

    // if valid move call Move()

    // if keyword solve call Solve()

    // if keywork quit break loop

    let mut h = SolitairePlayer::new();
    let winning = h.reached_win();
    println!("{}", h.get_heuristic());
}
