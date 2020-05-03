use network::encoder::{SimpleGameEncoder, GameLoader, GameEncoder, SimpleBoardEncoder};
use std::fs::File;
use pgn_reader::BufferedReader;
use protobuf::Message;
use std::io::Write;

fn main() {

    let path = "test.pgn";
    let file = File::open(path).expect("fopen");
    let mut buffer = File::create("converted.chk").expect("Failed to create file");

    let mut reader = BufferedReader::new(file);

    let mut visitor = GameLoader::default();

    while let Some(game) = reader.read_game(&mut visitor).expect("Error") {
        let game_chunk = SimpleGameEncoder::default().encode(&game, &SimpleBoardEncoder::default());
        buffer.write(&game_chunk.write_to_bytes().expect("game_chunk"));
    }
}
