extern crate protoc_rust;

use protoc_rust::Customize;

use std::io;

fn main() -> io::Result<()> {
    protoc_rust::run(protoc_rust::Args {
        out_dir: "src/protos",
        input: &["src/protos/training_chunk.proto"],
        includes: &["src/protos"],
        customize: Customize {
            ..Default::default()
        },
    })
        .expect("protoc");
    Ok(())
}
