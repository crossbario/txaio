#!/bin/sh

export TXAIO_BUILD_DATE=`date -u +"%Y-%m-%d"`
export TXAIO_BUILD_ID=$(date --utc +%Y%m%d)-$(git rev-parse --short HEAD)
export TXAIO_VCS_REF=`git rev-parse --short HEAD`
# export TXAIO_VCS_REF=`git --git-dir="./.git" rev-list -n 1 v${TXAIO_VERSION} --abbrev-commit`
export TXAIO_VERSION=$(grep -E '^(__version__)' ./txaio/_version.py | cut -d ' ' -f3 | sed -e 's|[u"'\'']||g')

echo ""
echo "Build environment configured:"
echo ""
echo "  TXAIO_BUILD_DATE = ${TXAIO_BUILD_DATE}"
echo "  TXAIO_BUILD_ID   = ${TXAIO_BUILD_ID}"
echo "  TXAIO_VCS_REF    = ${TXAIO_VCS_REF}"
echo "  TXAIO_VERSION    = ${TXAIO_VERSION}"
echo ""
