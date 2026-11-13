#!/bin/sh
# Online Shop repo (../mittu-online-shop) ki latest index.html + img ko Vercel par /mittu-online-shop/ ke liye copy karta hai
set -e
SRC="${1:-../mittu-online-shop}"
mkdir -p mittu-online-shop
cp "$SRC/index.html" mittu-online-shop/index.html
cp -r "$SRC/img" mittu-online-shop/
