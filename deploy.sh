#!/bin/bash

# TXAIO_VERSION             : must be set in travis.yml!
export AWS_DEFAULT_REGION=eu-central-1
export AWS_S3_BUCKET_NAME=crossbarbuilder
# AWS_ACCESS_KEY_ID         : must be set in Travis CI build context!
# AWS_SECRET_ACCESS_KEY     : must be set in Travis CI build context!
# WAMP_PRIVATE_KEY          : must be set in Travis CI build context!

set -ev

# TRAVIS_BRANCH, TRAVIS_PULL_REQUEST, TRAVIS_TAG  :  automatically set by Travis CI

# PR => don't deploy and exit
if [ "$TRAVIS_PULL_REQUEST" = "true" ]; then
    echo '[1] deploy script called for PR - exiting ..';
    exit 0;

# direct push to master => deploy
elif [ "$TRAVIS_BRANCH" = "master" -a "$TRAVIS_PULL_REQUEST" = "false" ]; then
    echo '[2] deploy script called for direct push to master: continuing to deploy!';

# tagged release => deploy
elif [ -n "$TRAVIS_TAG" ]; then
    echo '[3] deploy script called for tagged release: continuing to deploy!';

# outside travis? => deploy
else
    echo '[?] deploy script called outside Travis? continuing to deploy!';

fi

# only show number of env vars .. should be 4 on master branch!
# https://docs.travis-ci.com/user/pull-requests/#Pull-Requests-and-Security-Restrictions
# Travis CI makes encrypted variables and data available only to pull requests coming from the same repository.
echo 'aws env vars (should be 4 - but only on master branch!):'
env | grep AWS | wc -l

# set up awscli package
echo 'installing aws tools ..'
pip install awscli
which aws
aws --version

# "aws s3 ls" will return -1 when no files are found! but we don't want our script to exit
aws s3 ls ${AWS_S3_BUCKET_NAME}/wheels/txaio- || true

# build python source dist and wheels
echo 'building package ..'
python setup.py sdist bdist_wheel --universal
ls -la ./dist

# upload to S3: https://s3.eu-central-1.amazonaws.com/crossbarbuilder/wheels/
echo 'uploading package ..'
# aws s3 cp --recursive ./dist s3://${AWS_S3_BUCKET_NAME}/wheels
aws s3 rm s3://${AWS_S3_BUCKET_NAME}/wheels/txaio-${TXAIO_VERSION}-py2.py3-none-any.whl
aws s3 rm s3://${AWS_S3_BUCKET_NAME}/wheels/txaio-latest-py2.py3-none-any.whl

aws s3 cp --acl public-read ./dist/txaio-${TXAIO_VERSION}-py2.py3-none-any.whl s3://${AWS_S3_BUCKET_NAME}/wheels/txaio-${TXAIO_VERSION}-py2.py3-none-any.whl
aws s3 cp --acl public-read ./dist/txaio-${TXAIO_VERSION}-py2.py3-none-any.whl s3://${AWS_S3_BUCKET_NAME}/wheels/txaio-latest-py2.py3-none-any.whl

#aws s3api copy-object --acl public-read \
#    --copy-source wheels/txaio-${TXAIO_VERSION}-py2.py3-none-any.whl --bucket ${AWS_S3_BUCKET_NAME} \
#    --key wheels/txaio-latest-py2.py3-none-any.whl

aws s3 ls ${AWS_S3_BUCKET_NAME}/wheels/txaio-

# tell crossbar-builder about this new wheel push
# get 'wamp' command, always with latest autobahn master
pip install -q -I https://github.com/crossbario/autobahn-python/archive/master.zip#egg=autobahn[twisted,serialization,encryption]

# use 'wamp' to notify crossbar-builder
wamp --max-failures 3 \
     --authid wheel_pusher \
     --url ws://office2dmz.crossbario.com:8008/ \
     --realm webhook call builder.wheel_pushed \
     --keyword name txaio \
     --keyword publish true
