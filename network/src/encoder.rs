use shakmaty::{Position, Color, Chess};

pub struct SimpleEncoder {
}

pub trait NeuralEncoder {
    fn encode(position: &dyn Position) -> Vec<u64>;
}

impl NeuralEncoder for SimpleEncoder {

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
    fn encode(position: &dyn Position) -> Vec<u64> {
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