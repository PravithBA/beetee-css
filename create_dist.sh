DEST_DIR="dest"
BEETEECSS_PATH="dest/test.btcss"
CSS_PATH="dest/test.css"

if [ -d "$DEST_DIR" ]; then
  echo "Dist directory exists"
else
  echo "Creating nessasary directories"
  mkdir dest
fi
if [ -f "$BEETEECSS_PATH" ]; then
  echo "Beetee css file exists"
else
  echo "Creating beetee css file"
  touch dest/test.btcss
fi
if [ -f "$CSS_PATH" ]; then
  echo "Css file exists"
else
  echo "Creating css file"
  touch dest/test.css
fi