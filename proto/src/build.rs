extern crate protoc_rust;

use protoc_rust::Customize;

use std::io;

fn main() -> io::Result<()> {
    // protoc_rust::Codegen::new()
    //     .out_dir("src/protos")
    //     .inputs(&["src/protos/training_chunk.proto"])
    //     .include("protos")
    //     .run()
    // .expect("Running protoc failed.");
    protoc_rust::run(protoc_rust::Args {
        out_dir: "src/protos",
        input: &["src/protos/training_chunk.proto"],
        includes: &["src/protos"],
        customize: Customize {
            ..Default::default()
        },
    })
        .expect("Running protoc failed.");
    Ok(())
}
