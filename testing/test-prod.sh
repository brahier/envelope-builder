#!/bin/bash

curl -H "Content-Type: application/json" -d @test.json -o out.pdf https://envelope-builder.app.supcik.net/pdf
