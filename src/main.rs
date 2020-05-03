extern crate glob;

use network::encoder::{SimpleGameEncoder, GameLoader, SimpleBoardEncoder, ChunkEncoder};
use std::fs::File;
use protobuf::{Message};
use std::io::Write;
use rand::Rng;
use std::time::{SystemTime, UNIX_EPOCH};

use glob::glob;
use pgn_reader::BufferedReader;
use std::fs;

fn main() {
    let path = "H:\\nn\\ccrl-pgn\\cclr";
    let input_files = format!("{}\\**\\*.pgn", path);
    let mut input_counter = 0;

    for entry in glob(input_files.as_str()).expect("Failed to read") {
        match entry {
            Ok(found_file) => {
                println!("file {}", found_file.display());
                let file = File::open(found_file).expect("fopen");
                let mut reader = BufferedReader::new(file);

                let mut visitor = GameLoader::default();
                let mut chunk_counter = 0;
                let mut chunk_encoder = ChunkEncoder::default();
                while let Some(game) = reader.read_game(&mut visitor).expect("Error") {
                    if chunk_encoder.push(&game) {
                        save(path, &mut chunk_encoder, input_counter, chunk_counter);
                        chunk_counter += 1;
                    }
                }
                save(path, &mut chunk_encoder, input_counter, chunk_counter);
                input_counter += 1;
            }
            Err(e) => println!("{:?}", e),
        }
    }
}

fn save(path: &str, chunk_encoder: &mut ChunkEncoder, file_index: usize, chunk_index: usize) {
    let game_encoder = SimpleGameEncoder::default();
    let board_encoder = SimpleBoardEncoder::default();
    if let Some(chunk) = chunk_encoder.encode(&game_encoder, &board_encoder) {
        let bytes = chunk.write_to_bytes().expect("game_chunk");
        println!("len {}", bytes.len());

        let dir = format!("{}\\custom\\{}", path, file_index);
        fs::create_dir_all(dir.as_str()).expect("Failed to create dir");

        let file = format!("{}\\chunk_{}.chk", dir.as_str(), chunk_index);
        let mut buffer = File::create(file).expect("Failed to create file");
        buffer.write(&bytes).expect("Failed to push ");
    }
}
