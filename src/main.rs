extern crate glob;

use network::encoder::{SimpleGameEncoder, GameLoader, SimpleBoardEncoder, GameEncoder, Game};
use std::fs::File;
use protobuf::{Message};
use std::io::{Write, Read};

use glob::glob;
use pgn_reader::BufferedReader;
use std::fs;
use proto::protos::training_chunk::{PositionChunk, PolicyChunk};
use std::collections::HashMap;

fn main() {
    let path = "D:\\nn\\ccrl-pgn\\cclr\\train";
    let input_files = format!("{}\\**\\*.pgn", path);
    let mut total_created_files = 0;

    for entry in glob(input_files.as_str()).expect("Failed to read") {
        match entry {
            Ok(found_file) => {
                println!("file {}", found_file.display());
                let file = File::open(found_file).expect("fopen");
                let mut reader = BufferedReader::new(file);

                let mut visitor = GameLoader::default();
                let game_encoder = SimpleGameEncoder::default();
                let mut game_count = 0;
                while let Some(game) = reader.read_game(&mut visitor).expect("Error") {
                    println!("Game {}", game_count);
                    total_created_files += save(path, &game, &game_encoder, total_created_files);
                    game_count += 1;
                }
            }
            Err(e) => println!("{:?}", e),
        }
    }
}

fn save<T: GameEncoder>(path: &str, game: &Game, game_encoder: &T, total_created_files:u64) -> u64 {
    let board_encoder = SimpleBoardEncoder::default();
    let mut created_files = 0;
    for position_chunk in game_encoder.encode(&game, &board_encoder).iter() {
        let mut key:u64 = 0;
        // TODO: Use zobrist key to have a better distribution
        for (index, plane) in position_chunk.get_planes().iter().enumerate() {
            if index < 2 {
                continue;
            }
            key ^= *plane;
        }
        let folder_name = (created_files + total_created_files) / 10240;

        let possible_files = format!("{}\\s1\\{:X}\\**\\{:016X}.bch", path, folder_name, key);
        // println!("Possible {}", possible_files);
        let mut chunk = position_chunk.clone();
        let mut new_file = true;
        let mut file_count = 0;
        for entry in glob(possible_files.as_str()).expect("Failed to read") {
            match entry {
                Ok(found_file) => {
                    // println!("Checking file {}", found_file.display());
                    let mut file = File::open(found_file).expect("Failed to open file");
                    let mut buffer = Vec::new();
                    file.read_to_end(&mut buffer).expect("Failed to read file");
                    let mut found_chunk = PositionChunk::new();
                    found_chunk.merge_from_bytes(&buffer).expect("Protobuf parse error");
                    chunk.set_points(chunk.get_points() + found_chunk.get_points());
                    chunk.set_games(chunk.get_games() + found_chunk.get_games());
                    if found_chunk.get_planes().eq(position_chunk.get_planes()) {
                        chunk.set_policy(merge_policy(&chunk, found_chunk).into());
                        new_file = false;
                        break;
                    } else {
                        file_count += 1;
                    }
                },
                Err(e) => println!("{:?}", e),
            }
        }
        if new_file {
            created_files += 1;
        }

        let _bytes = chunk.write_to_bytes().expect("encoding position");

        let path_name = format!("{}\\s1\\{:X}\\{}", path, folder_name, file_count);
        fs::create_dir_all(path_name.as_str()).expect("Failed to create dir");
        let file_name = format!("{}\\{:016X}.bch", path_name, key);
        // println!("Saving file {}", file_name);
        let mut file = File::create(file_name).expect("Failed to create file");
        file.write(&_bytes).expect("Failed to push ");
    }
    created_files
}

fn merge_policy(c1: &PositionChunk, c2: PositionChunk) -> Vec<PolicyChunk> {
    let mut result = Vec::new();
    let merge : Vec<PolicyChunk> = [c1.get_policy(), c2.get_policy()].concat();
    let mut hash:HashMap<u32, u32> = HashMap::new();
    for entry in merge.iter() {
        match hash.get(&entry.get_move_index()) {
            Some(&number) => hash.insert(entry.get_move_index(), number + entry.get_times_played()),
            _ => hash.insert(entry.get_move_index(), entry.get_times_played()),
        };
    }

    for (key, value) in hash.iter() {
        let mut policy_chunk = PolicyChunk::new();
        policy_chunk.set_move_index(key.clone());
        policy_chunk.set_times_played(value.clone());
        result.push(policy_chunk);
    }

    result
}
