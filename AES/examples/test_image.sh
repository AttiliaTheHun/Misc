#!/bin/bash

set -ueo pipefail

program="../Program/bin/Debug/net9.0/Program"

cd ../Program

dotnet build

cd ../examples

$program image.jpeg image.jpeg.encrypted wololo e

$program image.jpeg.encrypted image.jpeg.decrypted wololo d

test -f image.jpeg.decrypted && diff image.jpeg image.jpeg.decrypted && echo "Test successful" || echo "Test failed"
