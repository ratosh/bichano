use std::mem;

use pgn_reader::{Outcome, RawHeader, San, SanPlus, Skip, Visitor, Role};
use shakmaty::{Chess, Color, Position, Move, Setup};
use shakmaty::fen::Fen;

use proto::protos::training_chunk::{PositionChunk, PolicyChunk, PositionChunk_PolicyEncodingType, PositionChunk_BoardEncodingType};

pub struct SimpleBoardEncoder {
}

impl Default for SimpleBoardEncoder {
    fn default() -> Self {
        Self {
        }
    }
}

pub trait BoardEncoder {
    fn encoding_type(&self) -> PositionChunk_BoardEncodingType;
    fn encode<T : Position>(&self, position: &T) -> Vec<u64>;
}

impl BoardEncoder for SimpleBoardEncoder {
    fn encoding_type(&self) -> PositionChunk_BoardEncodingType {
        PositionChunk_BoardEncodingType ::SIMPLE_BOARD
    }

    /// 0 - white
    /// 1 - black
    /// 2 - pawns
    /// 3 - knights
    /// 4 - bishops
    /// 5 - rooks
    /// 6 - queens
    /// 7 - kings
    /// 8 - ep square -- Should map impossible EP?
    /// 9 - castling
    fn encode<T : Position>(&self, position: &T) -> Vec<u64> {
        let mut res = Vec::with_capacity(10);
        let color_us = position.turn();
        match color_us {
            Color::White => {
                res.push(position.us().0);
                res.push(position.them().0);
                res.push(position.board().pawns().0);
                res.push(position.board().knights().0);
                res.push(position.board().bishops().0);
                res.push(position.board().rooks().0);
                res.push(position.board().queens().0);
                res.push(position.board().kings().0);
                if let Some(square) = position.ep_square() {
                    res.push(u64::from(square));
                }
                res.push(position.castling_rights().0);
            }
            _ => {
                res.push(position.us().flip_vertical().0);
                res.push(position.them().flip_vertical().0);
                res.push(position.board().pawns().flip_vertical().0);
                res.push(position.board().knights().flip_vertical().0);
                res.push(position.board().bishops().flip_vertical().0);
                res.push(position.board().rooks().flip_vertical().0);
                res.push(position.board().queens().flip_vertical().0);
                res.push(position.board().kings().flip_vertical().0);
                if let Some(square) = position.ep_square() {
                    res.push(u64::from(square.flip_vertical()));
                }
                res.push(position.castling_rights().flip_vertical().0);
            }
        }
        res
    }
}

#[derive(PartialEq)]
enum LoadStep {
    Header,
    Position,
    Moves,
    Result,
}


#[derive(Clone)]
pub struct Game {
    pub position: Chess,
    pub moves: Vec<San>,
    pub result: Option<Outcome>,
}

impl Default for Game {
    fn default() -> Game {
        Game {
            position: Chess::default(),
            moves: Vec::new(),
            result: None,
        }
    }
}

pub struct GameLoader {
    index: usize,
    game: Game,
    step: LoadStep,
}

impl Default for GameLoader {
    fn default() -> GameLoader {
        GameLoader {
            index: 0,
            game: Game::default(),
            step: LoadStep::Header,
        }
    }
}

impl Visitor for GameLoader {
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
                }
            };

            self.game.position = match fen.position() {
                Ok(pos) => {
                    self.step = LoadStep::Position;
                    pos
                }
                Err(err) => {
                    eprintln!("illegal fen header in game {}: {} ({})", self.index, err, fen);
                    return;
                }
            };
        }
        self.step = LoadStep::Position;
    }

    fn end_headers(&mut self) -> Skip {
        return if self.step == LoadStep::Position {
            self.step = LoadStep::Moves;
            Skip(false)
        } else {
            Skip(true)
        };
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
            self.step = LoadStep::Result;
            self.game.result = _outcome;
        }
    }

    fn end_game(&mut self) -> Self::Result {
        mem::replace(&mut self.game, Game::default())
    }
}


pub trait GameEncoder {
    fn encode_move(&self, m: &Move, moving_color: Color) -> u32;
    fn encode(&self, game: &Game, board_encoder: &impl BoardEncoder) -> Vec<PositionChunk>;
}

pub struct SimpleGameEncoder {

}

impl Default for SimpleGameEncoder {
    fn default() -> Self {
        Self {
        }
    }
}

fn convert_outcome(outcome: Outcome) -> f64 {
    match outcome {
        Outcome::Decisive {winner} => {
            match winner {
                Color::White => 0.0,
                _ => 1.
            }
        },
        _ => 0.5
    }
}

impl GameEncoder for SimpleGameEncoder {

    // Simple move encoding (16 bits):
    // - 6 bits for move start position
    // - 6 bits for move end position
    // - 2 bits for promotion
    fn encode_move(&self, m: &Move, moving_color: Color) -> u32 {
        let (from, to, promotion) = match *m {
            Move::EnPassant {from, to} => {
                (from, to, None)
            },
            Move::Castle {king, rook} => {
                (king, rook, None)
            },
            Move::Normal { role: _, from, capture: _, to, promotion } => {
                (from, to, promotion)
            },
            _ => {
                panic!("Invalid move")
            }
        };
        let promotion_index = if let Some(role) = promotion {
            (u32::from(role) - u32::from(Role::Knight)) << 12
        } else {
            0
        };
        return if moving_color == Color::White {
            u32::from(from) + (u32::from(to) << 6) + promotion_index
        } else {
            u32::from(from.flip_vertical()) + u32::from(to.flip_vertical()) + promotion_index
        }
    }

    fn encode(&self, game: &Game, board_encoder: &impl BoardEncoder) -> Vec<PositionChunk> {
        let mut position = game.position.clone();
        let mut positions: Vec<PositionChunk> = Vec::new();

        for san_move in game.moves.iter() {
            let parsed_move = san_move.to_move(&position).expect("Failed to parse move");
            let moving_color = position.turn();

            let mut policies: Vec<PolicyChunk> = Vec::new();
            let mut policy_chunk = PolicyChunk::new();
            policy_chunk.set_value(1.0);
            policy_chunk.set_move_index(self.encode_move(&parsed_move, moving_color));
            policies.push(policy_chunk);

            position.play_unchecked(&parsed_move);
            let board_chunk = board_encoder.encode(&position);

            let mut position_chunk = PositionChunk::new();
            position_chunk.set_policy(policies.into());
            position_chunk.set_planes(board_chunk);
            position_chunk.set_policy_encoding(PositionChunk_PolicyEncodingType::SIMPLE_POLICY);
            position_chunk.set_board_encoding(board_encoder.encoding_type());

            match game.result {
                Some(outcome) => position_chunk.set_result(convert_outcome(outcome)),
                _ => {}
            };
            positions.push(position_chunk);
        }
        positions
    }
}