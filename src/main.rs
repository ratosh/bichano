extern crate glob;

use network::encoder::{SimpleGameEncoder, GameLoader, SimpleBoardEncoder, GameEncoder, Game};
use std::fs::File;
use protobuf::{Message};
use std::io::Write;

use glob::glob;
use pgn_reader::BufferedReader;
use std::fs;

fn main() {
    let path = "D:\\nn\\ccrl-pgn\\cclr";
    let input_files = format!("{}\\**\\*.pgn", path);

    for entry in glob(input_files.as_str()).expect("Failed to read") {
        match entry {
            Ok(found_file) => {
                println!("file {}", found_file.display());
                let file = File::open(found_file).expect("fopen");
                let mut reader = BufferedReader::new(file);

                let mut visitor = GameLoader::default();
                let game_encoder = SimpleGameEncoder::default();
                while let Some(game) = reader.read_game(&mut visitor).expect("Error") {
                    save(path, &game, &game_encoder);
                }
            }
            Err(e) => println!("{:?}", e),
        }
        break;
    }
}

fn save<T: GameEncoder>(path: &str, game: &Game, game_encoder: &T) {
    let board_encoder = SimpleBoardEncoder::default();
    for position_chunk in game_encoder.encode(&game, &board_encoder).iter() {
        let mut key:u64 = 0;
        // TODO: Use zobrist key to have a better distribution
        for (index, plane) in position_chunk.get_planes().iter().enumerate() {
            if index < 2 {
                continue;
            }
            println!("plane {:#016x}", plane);
            key ^= *plane;
        }
        println!("Key {:#016x}", key);

        let dir = format!("{}\\custom\\{:#016x}", path, key);
        fs::create_dir_all(dir.as_str()).expect("Failed to create dir");

        // TODO: Load file and merge equal positions
        // let input_files = format!("{}\\**\\*.bch", dir);
        // for entry in glob(input_files.as_str()).expect("Failed to read") {
        //
        // }

        let bytes = position_chunk.write_to_bytes().expect("encoding position");

        let file = format!("{}\\pos_0.bch", dir.as_str());
        let mut buffer = File::create(file).expect("Failed to create file");
        buffer.write(&bytes).expect("Failed to push ");
    }
}
