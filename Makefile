SHELL := /bin/bash

.PHONY: build data model map clean

build:
	go build -o bin/resilience ./cmd/resilience

data:
	go run ./cmd/resilience data

model:
	go run ./cmd/resilience model

map:
	go run ./cmd/resilience map

clean:
	rm -rf data/interim/* data/processed/* figures/*
