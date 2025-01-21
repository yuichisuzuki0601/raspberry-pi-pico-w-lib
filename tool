#!/bin/sh
cd `dirname $0`

function ip() {
	ifconfig en0 | awk '$1 == "inet" {print $2}'
}

. ./lib/shell/execute
