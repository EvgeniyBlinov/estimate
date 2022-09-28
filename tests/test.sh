#!/bin/bash

diff <(cat ./example.txt | estimate) ./expected_result.txt &&
    echo "Test success"
