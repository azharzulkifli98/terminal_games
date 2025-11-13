/*
For now this will be a mini version that only solves games from the start

possible updates in the future:
allow player to play solitaire too
allow solving from any valid state mid game
allow importing mid game states from a txt file
*/
use std::collections::BinaryHeap;
use std::collections::HashMap;
use std::cmp::Ordering;
use std::env;
use std::fmt;
use std::fs::File;
use std::io;
use std::io::BufRead;

// constants
const SUITS: [char; 4] = ['D', 'S', 'H', 'C'];
const RANKS: [char; 13] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'];
const REDS: &str = "DH";
const BLACKS: &str = "SC";

#[derive(Copy, Clone, Eq, PartialEq)]
struct Card
{
    suit: char,
    rank: char
}

#[derive(Clone, Eq, PartialEq)]
struct FreecellBoard
{
    pockets: Vec<Card>,
    piles: [Vec<Card>; 8],
    foundations: HashMap<char, char>,
    moves_history: Vec<String>
}

#[derive(Clone, Eq, PartialEq)]
struct GameState
{
    board: FreecellBoard,
    heuristic: usize
}

fn get_alpha(index: usize) -> char
{
    let mapping = ['A', 'B', 'C', 'D'];
    return mapping[index];
}

fn get_index(alpha: char) -> usize
{
    let index = match alpha {
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

fn is_valid(front_card: &Card, back_card: &Card) -> bool
{
    return is_opposite(&front_card, &back_card) && is_ordered(&front_card, &back_card);
}

impl fmt::Debug for Card {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result
    {        
        return write!(f, "{}{}", self.suit, self.rank);
    }
}

// The priority queue depends on `Ord`.
// Explicitly implement the trait so the queue becomes a min-heap
// instead of a max-heap.
impl Ord for GameState {
    fn cmp(&self, other: &Self) -> Ordering {
        // Notice that we flip the ordering on costs.
        // In case of a tie we compare positions - this step is necessary
        // to make implementations of `PartialEq` and `Ord` consistent.
        other.heuristic.cmp(&self.heuristic)
            .then_with(|| self.heuristic.cmp(&other.heuristic))
    }
}

// `PartialOrd` needs to be implemented as well.
impl PartialOrd for GameState {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
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
                if !is_ordered(&row[i], &row[i + 1])
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
        return self.get_heuristic() <= 52
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
            if pocket_card.rank == 'A'
            {
                valid_moves.push(get_alpha(i).to_string() + "~E"); // Aces are always valid
            }
            else
            {
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
        }

        for i in 0..8 // pile to foundation
        {
            if self.piles[i].len() > 0 // card exists
            {
                let pile_card = self.piles[i].last().unwrap();
                if pile_card.rank == 'A'
                {
                    valid_moves.push(i.to_string() + "~E"); // Aces are always valid
                }

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
                    valid_moves.push(i.to_string() + "~" + &get_alpha(self.pockets.len()).to_string());
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
                        valid_moves.push(j.to_string() + "~" + &i.to_string());
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
                    if is_valid(&self.pockets[j], &self.piles[i].last().unwrap())
                    {
                        valid_moves.push(get_alpha(j).to_string() + "~" + &i.to_string());
                    }
                }
                for j in 0..8 // pile to pile, must be different columns that both have cards that are valid
                {
                    if  i != j &&
                        self.piles[j].len() > 0
                        && is_valid(&self.piles[j].last().unwrap(), &self.piles[i].last().unwrap())
                    {
                        valid_moves.push(j.to_string() + "~" + &i.to_string());
                    }
                }
            }
        }

        return valid_moves
    }
}

fn get_board_from_file(file_path: &str) -> Result<FreecellBoard, io::Error>
{
    // This example demonstrates the principle for Copy types, not directly for String
    // const EMPTY_STRING: String = String::new(); // This would not compile as String is not Copy
    // let mut string_array: [String; 5] = [EMPTY_STRING; 5];
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

    let file = File::open(file_path)?;
    let reader = io::BufReader::new(file);

    for (i, line) in reader.lines().enumerate()
    {
        if i > 7
        {
            break;
        }

        let tio = line?.clone();

        let cards: Vec<&str> = tio.split_whitespace().collect();
        let tangible: Vec<String> = cards.iter().map(|&x| x.into()).collect();
        for card in tangible.iter()
        {
            let value = Card
            {
                suit: card.chars().nth(0).unwrap(),
                rank: card.chars().nth(1).unwrap() // fix this and look over it again :(
            };
            all_piles[i].push(value);
        }
    }

    let mut starting_foundations: HashMap<char, char> = HashMap::new();

    starting_foundations.insert('D', '-');
    starting_foundations.insert('S', '-');
    starting_foundations.insert('H', '-');
    starting_foundations.insert('C', '-');

    return Ok(FreecellBoard
    {
        pockets: Vec::<Card>::new(),
        piles: all_piles,
        foundations: starting_foundations,
        moves_history: Vec::<String>::new()
    })
}

fn handle_card_move(game_state: GameState, move_notation: String) -> GameState
{
    // consider parameter validators
    let mut updated_game = game_state.board.clone();

    // parse move
    let start_char = move_notation.chars().next().unwrap();
    let end_char = move_notation.chars().last().unwrap();

    // pick move accordingly
    if end_char == 'E'
    {
        if start_char.is_alphabetic()
        {
            updated_game.push_pocket_to_foundation(get_index(start_char));
        }
        else
        {
            updated_game.push_pile_to_foundation(start_char.to_digit(10).unwrap() as usize);
        }
    }
    else if start_char.is_alphabetic()
    {
        updated_game.move_card_pocket_to_pile(get_index(start_char), end_char.to_digit(10).unwrap() as usize);
    }
    else if end_char.is_alphabetic()
    {
        updated_game.move_card_pile_to_pocket(start_char.to_digit(10).unwrap() as usize);
    }
    else
    {
        updated_game.move_card_pile_to_pile(start_char.to_digit(10).unwrap() as usize, end_char.to_digit(10).unwrap() as usize);
    }

    return GameState
    {
        board: updated_game.clone(),
        heuristic: updated_game.get_heuristic()
    }
}

fn show_solution_for(game_board: FreecellBoard)
{
    let start = GameState
    {
        board: game_board.clone(),
        heuristic: game_board.get_heuristic()
    };

    // using A* algorithm without recursion
    let mut priority_queue: BinaryHeap<GameState> = BinaryHeap::new();
    priority_queue.push(start.clone());

    while !priority_queue.is_empty()
    {
        let current_game_state = priority_queue.pop().unwrap();

        if current_game_state.board.reached_win()
        {
            println!("celebrate! {:?}", current_game_state.board.moves_history);
            current_game_state.board.print_full_board();
            return;
        }
        else
        {
            for valid_card_move in current_game_state.board.get_all_valid_moves()
            {
                println!("{}", valid_card_move);
                let new_game_state = handle_card_move(current_game_state.clone(), valid_card_move);
                priority_queue.push(new_game_state.clone());
            }
        }
    }

    println!("No solutions found.");
}

fn main()
{
    let args: Vec<String> = env::args().collect();
    let mut game: FreecellBoard = FreecellBoard::new();

    if args.len() > 1
    {
        let file_path = &args[1];
        match get_board_from_file(file_path)
        {
            Ok(result) => game = result,
            Err(e) => eprintln!("Error reading file: {}", e),
        }
    }
    else
    {
        println!("Using a default board for game.");
    }

    game.print_full_board();

    show_solution_for(game);
}
