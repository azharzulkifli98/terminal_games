/*
Implements the A * search algorithm for a solution
*/
use crate::freecell_board::*;
use std::collections::BinaryHeap;
use std::collections::HashMap;
use std::cmp::Ordering;
use std::env;
use std::fmt;
use std::fs::File;
use std::io;
use std::io::BufRead;

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

pub fn show_solution_for(game_board: FreeCellBoard) {
    // let start = GameState
    // {
    //     board: game_board.clone(),
    //     heuristic: game_board.get_heuristic()
    // };

    // // using A* algorithm without recursion
    // let mut priority_queue: BinaryHeap<GameState> = BinaryHeap::new();
    // priority_queue.push(start.clone());

    // while !priority_queue.is_empty()
    // {
    //     let current_game_state = priority_queue.pop().unwrap();
    //     current_game_state.board.print_full_board();

    //     if current_game_state.board.reached_win()
    //     {
    //         println!("celebrate! {:?}", current_game_state.board.moves_history);
    //         return;
    //     }
    //     else
    //     {
    //         for valid_card_move in current_game_state.board.get_all_valid_moves()
    //         {
    //             println!("{}", valid_card_move);
    //             let new_game_state = handle_card_move(current_game_state.clone(), valid_card_move);
    //             priority_queue.push(new_game_state.clone());
    //         }
    //     }
    // }

    game_board.print_full_board();
    println!("{}", game_board.get_heuristic());
    println!("{:?}", get_all_valid_moves(&game_board));

    println!("No solutions found.");
}
