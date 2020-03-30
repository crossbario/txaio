#!/bin/sh

export TXAIO_VERSION=$(grep -E '^(__version__)' ./txaio/_version.py | cut -d ' ' -f3 | sed -e 's|[u"'\'']||g')
export TXAIO_VCS_REF=`git --git-dir="./.git" rev-list -n 1 v${TXAIO_VERSION} --abbrev-commit`
export BUILD_DATE=`date -u +"%Y-%m-%d"`

echo ""
echo "Build environment configured:"
echo ""
echo "  TXAIO_VERSION = ${TXAIO_VERSION}"
echo "  TXAIO_VCS_REF = ${TXAIO_VCS_REF}"
echo "  BUILD_DATE    = ${BUILD_DATE}"
echo ""
