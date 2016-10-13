#!/bin/sh
which gnome-autogen.sh || {
    echo "Could not find 'gnome-autgen.sh'. Is gnome-common installed?"
    exit 1
}

NOCONFIGURE=yes . gnome-autogen.sh

##set -x
##autoreconf --verbose --force --install
##intltoolize --copy --force --automake
