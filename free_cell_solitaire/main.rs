/*
Only works with a predefined board in the form of a txt file
*/
mod freecell_card;
mod freecell_board;
mod freecell_solver;

use freecell_board::{FreeCellBoard, get_board_from_file};
use freecell_solver::{show_solution_for};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut game: FreeCellBoard = FreeCellBoard::new();

    // consider advantages of using array vs dictionary for the foundations
    if args.len() > 1 {
        let file_path = &args[1];
        match get_board_from_file(file_path) {
            Ok(result) => game = result,
            Err(e) => eprintln!("Error reading file: {}", e),
        }
        show_solution_for(game);
    } else {
        println!("Please provide the game board txt file as an argument");
    }
}
