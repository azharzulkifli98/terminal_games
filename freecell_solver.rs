use std::io;
use std::io::Write;
use std::fmt;
use std::env;
use std::collections::HashMap;

// constants
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
    foundations: HashMap<char, char>,
    moves_history: Vec<String>
}

struct SolitairePlayer
{
    board: FreecellBoard,
    heuristic: i32
}

fn get_alpha(index: usize) -> char
{
    let mapping = ['A', 'B', 'C', 'D'];
    return mapping[index];
}

fn get_index(alpha: char) -> usize
{
    let mut index = match alpha {
        'A' => 0,
        'B' => 1,
        'C' => 2,
        'D' => 3,
        _ => panic!("Cannot convert to an index")
    };
    return index;
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
            foundations: starting_foundations,
            moves_history: Vec::<String>::new()
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

    fn get_heuristic(&self) -> usize
    {
        let mut unordered_pairs = 0;
        for row in self.piles.iter()
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
            let foundation_rank = self.foundations[suit];
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

    fn move_card_pile_to_pile(&mut self, start_row: usize, end_row: usize)
    {
        assert!(start_row < 8);
        assert!(end_row < 8); 

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.piles[end_row].push(move_card);

        self.moves_history.push(start_row.to_string() + "~" + &end_row.to_string());
    }

    fn move_card_pile_to_pocket(&mut self, start_row: usize)
    {
        assert!(start_row < 8);

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.pockets.push(move_card);
        
        self.moves_history.push(start_row.to_string() + "~" + &get_alpha(self.pockets.len()).to_string());
    }

    fn move_card_pocket_to_pile(&mut self, start_pos: usize, end_row: usize)
    {
        assert!(start_pos < self.pockets.len());
        assert!(end_row < 8);

        let move_card = self.pockets.remove(start_pos);
        self.piles[end_row].push(move_card);

        self.moves_history.push(get_alpha(start_pos).to_string() + "~" + &end_row.to_string());
    }
    
    fn push_pile_to_foundation(&mut self, start_row: usize)
    {
        assert!(start_row < 8);

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.foundations.insert(move_card.suit, move_card.rank);

        self.moves_history.push(start_row.to_string() + "~E");
    }

    fn push_pocket_to_foundation(&mut self, start_pos: usize)
    {
        assert!(start_pos < self.pockets.len());
        
        let move_card = self.pockets.remove(start_pos);
        self.foundations.insert(move_card.suit, move_card.rank);
        
        self.moves_history.push(get_alpha(start_pos).to_string() + "~E");
    }

    fn get_all_valid_moves(&self) -> Vec<String>
    {
        let mut valid_moves = Vec::<String>::new();

        for i in 0..self.pockets.len() // pocket to foundation
        {
            let pocket_card = self.pockets[i];
            let foundation_card = Card
            {
                suit: pocket_card.suit,
                rank: self.foundations[&pocket_card.suit] // TODO: confirm this works ok for '-'
            };
            if is_ordered(&pocket_card, &foundation_card)
            {
                valid_moves.push(get_alpha(i).to_string() + "~E");
            }
        }

        for i in 0..8 // pile to foundation
        {
            if self.piles[i].len() > 0 // card exists
            {
                let pile_card = self.piles[i].last().unwrap();
                let foundation_card = Card
                {
                    suit: pile_card.suit,
                    rank: self.foundations[&pile_card.suit]
                };
                if is_ordered(&pile_card, &foundation_card)
                {
                    valid_moves.push(i.to_string() + "~E");
                }
            }
        }

        if self.pockets.len() < 4 // pile to pocket
        {
            for i in 0..8 // iterate all columns
            {
                if self.piles[i].len() > 0 // card exists in this column
                {
                    valid_moves.push(i.to_string() + "~" + get_alpha(&self.pockets.len()).to_string());
                }
            }
        }

        for i in 0..8
        {
            if self.piles[i].len() == 0 // empty pile is free real estate
            {
                for j in 0..8
                {
                    if self.piles[j].len() > 0 // card exists in this column
                    {
                        valid_moves.push(j.to_string() + "~" &i.to_string());
                    }
                }
                for j in 0..self.pockets.len()
                {
                    valid_moves.push(get_alpha(j).to_string() + "~" + &i.to_string());
                }
            }
            else
            {
                for j in 0..self.pockets.len() // pocket to pile
                {
                    if is_ordered(&self.pockets[j], &self.piles[i].last())
                    {
                        valid_moves.push(get_alpha(j).to_string() + "~" + &i.to_string());
                    }
                }
                for j in 0..8 // pile to pile, must be different columns that both have cards that are valid
                {
                    if i != j && self.piles[j].len() > 0 && is_ordered(&self.pile[j].last(), &self.pile[i].last())
                    {
                        valid_moves.push(j.to_string() + "~" &i.to_string());
                    }
                }
            }
        }

        return valid_moves
    }
}

fn main()
{
    let args: Vec<String> = env::args().collect();

    if args.len() > 1
    {
        let file_path = &args[1];
        println!("{}", file_path.to_string());

        // setup board ( txt file )
    }
    else
    {
        println!("hmmm");

        // setup board
    }

    loop
    {
        print!("> ");
        io::stdout().flush().unwrap();

        let mut player_input = String::new();

        io::stdin().read_line(&mut player_input).expect("Failed to read line");
            // if valid move call Move()

            // if keyword solve call Solve()

            // if keywork quit or game solved, break loop
        break;
    }

    // my_array.iter().any(|&x| x == search_item)
    // let rank_a = front_card.chars().nth(1).expect("front card must have format SR");
}
