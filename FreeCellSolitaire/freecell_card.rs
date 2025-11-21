/*
Implements card behaviors
*/

use std::fmt;

// constants
pub static SUITS: [char; 4] = ['S', 'H', 'D', 'C'];
pub static RANKS: [char; 15] = ['-', 'A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', '+'];
static REDS: &str = "DH";
static BLACKS: &str = "SC";

pub enum MoveCategory {
    FreecellToFoundation,
    CascadeToFoundation,
    FreecellToCascade,
    CascadeToFreecell,
    CascadeToCascade
}

#[derive(Copy, Clone, Eq, PartialEq)]
pub struct FreeCellCard {
    pub suit: char,
    pub rank: char
}

pub struct FreeCellMove {
    pub start_index: usize,
    pub end_index: usize,
    pub category: MoveCategory
}

fn get_alpha(index: usize) -> char {
    let mapping = ['A', 'B', 'C', 'D'];
    return mapping[index];
}

fn get_index(alpha: char) -> usize {
    let index = match alpha {
        'A' => 0,
        'B' => 1,
        'C' => 2,
        'D' => 3,
        _ => panic!("Cannot convert to an index")
    };
    return index;
}

fn is_opposite(front_card: &FreeCellCard, back_card: &FreeCellCard) -> bool {
    let suit_a: char = front_card.suit;
    let suit_b: char = back_card.suit;

    return (!REDS.contains(suit_a) && REDS.contains(suit_b)) ||
            (!BLACKS.contains(suit_a) && BLACKS.contains(suit_b));
}

fn is_rank_up(front_card: &FreeCellCard, back_card: &FreeCellCard) -> bool {
    let rank_a = front_card.rank;
    let rank_b = back_card.rank;
    let index_a = RANKS.iter().position(|&r| r == rank_a).unwrap();
    let index_b = RANKS.iter().position(|&r| r == rank_b).unwrap();

    return index_a == index_b + 1;
}

pub fn is_unordered(front_card: &FreeCellCard, back_card: &FreeCellCard) -> bool {
    let rank_a = front_card.rank;
    let rank_b = back_card.rank;
    let index_a = RANKS.iter().position(|&r| r == rank_a).unwrap();
    let index_b = RANKS.iter().position(|&r| r == rank_b).unwrap();

    return index_a > index_b;
}

pub fn is_valid(front_card: &FreeCellCard, back_card: &FreeCellCard) -> bool {
    return is_opposite(&front_card, &back_card) && is_rank_up(&back_card, &front_card); // order is reversed for cascades
}

impl fmt::Debug for FreeCellCard {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        return write!(f, "{}{}", self.suit, self.rank);
    }
}

impl fmt::Display for FreeCellCard {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        return write!(f, "{}{}", self.suit, self.rank);
    }
}

impl fmt::Debug for FreeCellMove {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.category {
            MoveCategory::FreecellToFoundation => return write!(f, "FC~FD"),
            MoveCategory::CascadeToFoundation => return write!(f, "{}~FD", self.start_index),
            MoveCategory::FreecellToCascade => return write!(f, "FC~{}", self.end_index),
            MoveCategory::CascadeToFreecell => return write!(f, "{}~FC", self.start_index),
            MoveCategory::CascadeToCascade => write!(f, "{}~{}", self.start_index, self.end_index),
            _ => panic!("category not found!")
        }
    }
}

impl fmt::Display for FreeCellMove {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.category {
            MoveCategory::FreecellToFoundation => return write!(f, "FC~FD"),
            MoveCategory::CascadeToFoundation => return write!(f, "{}~FD", self.start_index),
            MoveCategory::FreecellToCascade => return write!(f, "FC~{}", self.end_index),
            MoveCategory::CascadeToFreecell => return write!(f, "{}~FC", self.start_index),
            MoveCategory::CascadeToCascade => write!(f, "{}~{}", self.start_index, self.end_index),
            _ => panic!("category not found!")
        }
    }
}