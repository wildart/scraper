#!/usr/bin/env bash
VENV=venv
BIN=bin
DRIVER=chromedriver_linux64.zip
PYTHON=$VENV/bin/python

# input
URL="https://netforum.avectra.com/eweb/DynamicPage.aspx?Site=KAAR&WebCode=IndResult&FromSearchControl=Yes"
OUT=data

# setup
if [ ! -d "$VENV" ]; then
    echo Setup venv
    python3 -m venv $VENV
    echo Setup libs
    $VENV/bin/pip install selenium
    $VENV/bin/pip install pandas
fi

if [ ! -d "$BIN" ]; then
    curl -O https://chromedriver.storage.googleapis.com/2.40/$DRIVER
    unzip $DRIVER -d $BIN
    rm $DRIVER
fi

echo Scrape
$PYTHON scraper.py $URL $OUT $1
echo Process
$PYTHON parser.py $OUT
rm $OUT.json
