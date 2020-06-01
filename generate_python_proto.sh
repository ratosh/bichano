#!/bin/bash
protoc --proto_path=proto/src/protos --python_out=training proto/src/protos/training_chunk.proto
