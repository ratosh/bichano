use network::encoder::{SimpleEncoder, NeuralEncoder};
use network::extractor::GameExtractor;
use std::fs::File;
use pgn_reader::BufferedReader;

fn main() {

    let path = "G:\\chess\\epds\\test.pgn";
    let file = File::open(path).expect("fopen");

    let mut reader = BufferedReader::new(file);

    let mut visitor = GameExtractor::default();

    while let Some(game) = reader.read_game(&mut visitor).expect("Error") {
        println!("{}", game.result.is_some());
        let planes = SimpleEncoder::encode(&game.position);
        for plane in planes {
            println!("{}", plane);
        }
    }
}
