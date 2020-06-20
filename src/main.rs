extern crate glob;

use std::fs::File;
use protobuf::{Message};
use std::io::{Write, Read};

use glob::glob;
use pgn_reader::BufferedReader;
use std::fs;
use network::encoder::{BoardEncoder, SimpleBoardEncoder, GameLoader, SimplePolicyEncoder, Game, PolicyEncoder, encode_game};

fn main() {
    let path = "D:\\nn\\ccrl-pgn\\test";
    let input_files = format!("{}\\**\\*.pgn", path);
    let mut input_count = 0;

    for entry in glob(input_files.as_str()).expect("Failed to read") {
        match entry {
            Ok(found_file) => {
                println!("File {}", found_file.display());
                let file = File::open(found_file).expect("fopen");
                let mut reader = BufferedReader::new(file);

                let mut visitor = GameLoader::default();
                let policy_encoder = SimplePolicyEncoder::default();
                let board_encoder = SimpleBoardEncoder::default();
                let mut game_count = 0;
                while let Some(game) = reader.read_game(&mut visitor).expect("Error") {
                    save(path, &game, &policy_encoder, &board_encoder, input_count, game_count);
                    game_count += 1;
                }
                input_count += 1;
            }
            Err(e) => println!("{:?}", e),
        }
    }
}

fn save<PE: PolicyEncoder, BE: BoardEncoder>(path: &str, game: &Game, policy_encoder: &PE, board_encoder: &BE, input_count:u64, game_number: u64) {
    let game_chunk = encode_game(game, policy_encoder, board_encoder);
    let _bytes = game_chunk.write_to_bytes().expect("encoding game");
    let path_name = format!("{}\\s1\\{:016X}", path, input_count);
    fs::create_dir_all(path_name.as_str()).expect("Failed to create dir");
    let file_name = format!("{}\\{:016X}.bch", path_name, game_number);
    let mut file = File::create(file_name).expect("Failed to create file");
    file.write(&_bytes).expect("Failed to push ");
}