/*
Implements the free cell tableau behavior
*/
use crate::freecell_card::*;

use std::fs::File;
use std::io;
use std::io::BufRead;

#[derive(Clone, Eq, PartialEq)]
pub struct FreeCellBoard {
    pockets: Vec<FreeCellCard>,
    piles: [Vec<FreeCellCard>; 8],
    foundations: [FreeCellCard; 4],
    moves_history: Vec<String>
}

impl FreeCellBoard {
    pub fn new() -> Self {
        let mut full_deck: Vec<FreeCellCard> = Vec::new();

        let mut all_piles: [Vec<FreeCellCard>; 8] = [
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new(),
            Vec::new()
        ];

        let mut starting_foundations: [FreeCellCard; 4] = [
            FreeCellCard { suit: 'S', rank: '-' },
            FreeCellCard { suit: 'H', rank: '-' },
            FreeCellCard { suit: 'D', rank: '-' },
            FreeCellCard { suit: 'C', rank: '-' }
        ];

        return Self {
            pockets: Vec::<FreeCellCard>::new(),
            piles: all_piles,
            foundations: starting_foundations,
            moves_history: Vec::<String>::new()
        }
    }
        
    pub fn print_full_board(&self) {
        println!("\nFREE CELLS: {:?}", self.pockets);
        println!("FOUNDATIONS: {:?}", self.foundations);
        for i in 0..8 {
            println!("CASCADE {}: {:?}", i, self.piles[i]);
        }
    }

    pub fn get_heuristic(&self) -> usize {
        let mut unordered_pairs = 0;
        for row in self.piles.iter() {
            for (i, card) in row[..row.len() - 1].iter().enumerate() {
                if is_unordered(&row[i], &row[i + 1]) { // has a card on top that doesnt match order
                    println!("{} greater than {}", row[i], row[i + 1]);
                    unordered_pairs += 1;
                }
            }
        }

        let mut foundation_cards = 0;
        for suit in 0..4 {
            let foundation_card = self.foundations[suit];
            let rank_index = RANKS.iter().position(|&r| r == foundation_card.rank); // 3 mean -2 etc.

            if rank_index.is_some() {
                println!("here is {}", rank_index.unwrap());
                foundation_cards += rank_index.unwrap();
            }
        }

        // heuristic is totalcards + outofordercards - cardsinfoundation
        return 52 + unordered_pairs - foundation_cards;
    }

    pub fn reached_win(&self) -> bool {
        return self.get_heuristic() <= 40
    }

    fn move_card_pile_to_pile(&mut self, start_row: usize, end_row: usize) {
        assert!(start_row < 8);
        assert!(end_row < 8); 

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.piles[end_row].push(move_card);

        //self.moves_history.push(start_row.to_string() + "~" + &end_row.to_string());
    }

    fn move_card_pile_to_pocket(&mut self, start_row: usize) { // free cells are vec so we don't need the index
        assert!(start_row < 8);

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.pockets.push(move_card);
        
        //self.moves_history.push(start_row.to_string() + "~" + &get_alpha(self.pockets.len()).to_string());
    }

    fn move_card_pocket_to_pile(&mut self, start_pos: usize, end_row: usize) {
        assert!(start_pos < self.pockets.len());
        assert!(end_row < 8);

        let move_card = self.pockets.remove(start_pos);
        self.piles[end_row].push(move_card);

        //self.moves_history.push(get_alpha(start_pos).to_string() + "~" + &end_row.to_string());
    }
    
    fn push_pile_to_foundation(&mut self, start_row: usize, end_pos: usize) {
        assert!(start_row < 8);

        let move_card = self.piles[start_row].pop().expect("No cards found in pile!");
        self.foundations[end_pos] = move_card;

        //self.moves_history.push(start_row.to_string() + "~E");
    }

    fn push_pocket_to_foundation(&mut self, start_pos: usize, end_pos: usize) {
        assert!(start_pos < self.pockets.len());
        
        let move_card = self.pockets.remove(start_pos);
        self.foundations[end_pos] = move_card;
        
        //self.moves_history.push(get_alpha(start_pos).to_string() + "~E");
    }

    pub fn handle_card_move(mut self, card_move: FreeCellMove) {
        match &card_move.category {
            MoveCategory::FreecellToFoundation => self.push_pocket_to_foundation(card_move.start_index, card_move.end_index),
            MoveCategory::CascadeToFoundation => self.push_pile_to_foundation(card_move.start_index, card_move.end_index),
            MoveCategory::FreecellToCascade => self.move_card_pocket_to_pile(card_move.start_index, card_move.end_index),
            MoveCategory::CascadeToFreecell => self.move_card_pile_to_pocket(card_move.start_index),
            MoveCategory::CascadeToCascade => self.move_card_pile_to_pile(card_move.start_index, card_move.end_index),
            _ => panic!("Category not found!")
        }
    }
}

pub fn get_all_valid_moves(board: &FreeCellBoard) -> Vec<FreeCellMove> {
    let mut valid_moves: Vec<FreeCellMove> = Vec::new();
    valid_moves.push(FreeCellMove {
        start_index: 0,
        end_index: 0,
        category: MoveCategory::FreecellToCascade
    });
    return valid_moves;
}

pub fn get_board_from_file(file_path: &str) -> Result<FreeCellBoard, io::Error> {
    let mut new_board = FreeCellBoard::new();

    let file = File::open(file_path)?;
    let reader = io::BufReader::new(file);

    for (i, line) in reader.lines().enumerate() {
        if i > 7 {
            break;
        }

        let value = line?.clone();
        let column: Vec<&str> = value.split_whitespace().collect();
        let tangible: Vec<String> = column.iter().map(|&x| x.into()).collect(); // not sure why we need this
        for card in tangible.iter() {
            let value = FreeCellCard {
                suit: card.chars().nth(0).unwrap(),
                rank: card.chars().nth(1).unwrap()
            };
            new_board.piles[i].push(value);
        }
    }

    return Ok(new_board);
}

