/*
Implements the A * search algorithm for a solution
*/
use crate::freecell_board::*;
use crate::freecell_card::*;

use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Clone, Eq, PartialEq)]
struct GameState
{
    board: FreeCellBoard,
    heuristic: usize
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

fn get_all_valid_moves(board: &FreeCellBoard) -> Vec<FreeCellMove> {
    let mut valid_moves: Vec<FreeCellMove> = Vec::new();

    // for spot in foundations
    for suit in 0..4 {
        let foundation_card = board.foundations[suit];

        for i in 0..board.pockets.len() {
            if is_foundation_valid(&board.pockets[i], &foundation_card) {
                valid_moves.push(FreeCellMove {
                    start_index: i,
                    end_index: suit,
                    category: MoveCategory::FreecellToFoundation
                });
            }
        }

        for i in 0..8 { // always 8 columns in tableau
            let column_card = board.piles[i].last();
            if column_card.is_some() && is_foundation_valid(&column_card.unwrap(), &foundation_card) {
                valid_moves.push(FreeCellMove {
                    start_index: i,
                    end_index: suit,
                    category: MoveCategory::CascadeToFoundation
                });
            }
        }
    }

    // for column in tableau
    for i in 0..8 {
        if board.piles[i].is_empty() { // anything can go here
            for j in 0..board.pockets.len() {
                valid_moves.push(FreeCellMove {
                    start_index: j,
                    end_index: i,
                    category: MoveCategory::FreecellToCascade
                });
            }

            for j in 0..8 {
                if i != j && !board.piles[j].is_empty() {
                    valid_moves.push(FreeCellMove {
                        start_index: j,
                        end_index: i,
                        category: MoveCategory::CascadeToCascade
                    });
                }
            }
        } else { // validate order (one down and opposite suit)
            let back_card = board.piles[i].last().unwrap();

            for j in 0..board.pockets.len() {
                if is_cascade_valid(&board.pockets[j], &back_card) {
                    valid_moves.push(FreeCellMove {
                        start_index: j,
                        end_index: i,
                        category: MoveCategory::FreecellToCascade
                    });
                }
            }

            for j in 0..8 {
                let front_card = board.piles[j].last();
                if i != j && front_card.is_some() && is_cascade_valid(&front_card.unwrap(), &back_card) {
                    valid_moves.push(FreeCellMove {
                        start_index: j,
                        end_index: i,
                        category: MoveCategory::CascadeToCascade
                    });
                }
            }
        }
    }

    // for open free cell
    if board.pockets.len() < 4 {
        for i in 0..8 {
            if !board.piles[i].is_empty() {
                valid_moves.push(FreeCellMove {
                    start_index: i,
                    end_index: 0, // doesn't matter for this one
                    category: MoveCategory::CascadeToFreecell
                });
            }
        }
    }

    return valid_moves;
}

pub fn show_solution_for(game_board: FreeCellBoard) {
    // using A* algorithm without recursion
    let mut priority_queue: BinaryHeap<GameState> = BinaryHeap::new();
    priority_queue.push(GameState {
        board: game_board.clone(),
        heuristic: game_board.get_heuristic()
    });

    let mut iteration = 0;

    while !priority_queue.is_empty() {
        let current_game_state = priority_queue.pop().unwrap();
        println!("{}", current_game_state.heuristic);
        iteration += 1;

        if current_game_state.board.moves_history.len() == current_game_state.heuristic { // win condition whenn total distance is the current distance
            current_game_state.board.print_full_board();
            println!("CELEBRATE! {:?}", current_game_state.board.moves_history);
            println!("number of iterations: {}", iteration);
            return;
        } else {
            for valid_card_move in get_all_valid_moves(&current_game_state.board) {
                let mut next_board = current_game_state.board.clone();
                next_board.handle_card_move(valid_card_move);
                
                priority_queue.push(GameState {
                    board: next_board.clone(),
                    heuristic: next_board.get_heuristic()
                });
            }
        }
    }

    println!("No solutions found.");
}
