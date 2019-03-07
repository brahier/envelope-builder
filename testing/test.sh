#!/bin/bash

curl -H "Content-Type: application/json" -d @test.json -o out.pdf localhost:5000/pdf
