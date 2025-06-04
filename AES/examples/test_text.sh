#!/bin/bash

set -ueo pipefail

program="../Program/bin/Debug/net9.0/Program"

cd ../Program

dotnet build

cd ../examples

$program test.txt test.txt.encrypted "Wakanda forever" e

$program test.txt.encrypted test.txt.decrypted "Wakanda forever" d

test -f test.txt.decrypted && diff test.txt test.txt.decrypted && echo "Test successful" || echo "Test failed"
