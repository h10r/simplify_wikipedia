#!/bin/bash
echo "Downloading articles for $1"
curl "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&&titles=$1" > data/en.$1.txt
curl "http://simple.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&&titles=$1" > data/simple.$1.txt