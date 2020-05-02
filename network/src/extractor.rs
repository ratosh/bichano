use shakmaty::{Position, Color, Chess};
use shakmaty::fen::Fen;
use pgn_reader::{BufferedReader, Visitor, SanPlus, Outcome, Skip, RawHeader, San};
use std::{mem};

#[derive(PartialEq)]
enum LoadStep {
    Header,
    Position,
    Moves,
    Result,
}

pub struct Game {
    pub position: Chess,
    pub moves: Vec<San>,
    pub result: Option<Outcome>
}

impl Default for Game {
    fn default() -> Game {
        Game {
            position: Chess::default(),
            moves: Vec::new(),
            result: None
        }
    }
}

pub struct GameExtractor {
    index: usize,
    game: Game,
    step: LoadStep,
    success: bool
}

impl Default for GameExtractor {
    fn default() -> GameExtractor {
        GameExtractor {
            index: 0,
            game: Game::default(),
            step: LoadStep::Header,
            success: true
        }
    }
}

impl Visitor for GameExtractor {
    type Result = Game;

    fn begin_game(&mut self) {
        self.index += 1;
    }

    fn header(&mut self, key: &[u8], value: RawHeader<'_>) {
        // Support games from a non-standard starting position.
        if key == b"FEN" {
            let fen = match Fen::from_ascii(value.as_bytes()) {
                Ok(fen) => {
                    fen
                }
                Err(err) => {
                    eprintln!("invalid fen header in game {}: {} ({:?})", self.index, err, value);
                    return;
                },
            };

            self.game.position = match fen.position() {
                Ok(pos) => {
                    self.step = LoadStep::Position;
                    pos
                },
                Err(err) => {
                    eprintln!("illegal fen header in game {}: {} ({})", self.index, err, fen);
                    return;
                },
            };
        }
    }

    fn end_headers(&mut self) -> Skip {
        return if self.step == LoadStep::Position {
            self.step = LoadStep::Moves;
            Skip(false)
        } else {
            Skip(true)
        }
    }

    fn san(&mut self, san_plus: SanPlus) {
        if self.step == LoadStep::Moves {
            self.game.moves.push(san_plus.san);
        }
    }

    fn begin_variation(&mut self) -> Skip {
        Skip(true)
    }

    fn outcome(&mut self, _outcome: Option<Outcome>) {
        if self.step == LoadStep::Moves {
            self.game.result = _outcome;
        }
    }

    fn end_game(&mut self) -> Self::Result {
        mem::replace(&mut self.game, Game::default())
    }
}