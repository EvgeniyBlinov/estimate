#!/bin/bash

diff <(cat ./example.txt | python3 ../estimate) ./expected_result.txt &&
    echo "Test success"
