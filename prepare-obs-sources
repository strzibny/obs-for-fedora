#!/bin/sh
# Create open-build-service-%version.tar.xz
#VERSION=$1
OBS_REPO_PATH=~/projects/obs/open-build-service/
CURRENT_PATH=$(pwd)

pushd $OBS_REPO_PATH
#git checkout $VERSION
rm $CURRENT_PATH/open-build-service-2.5.50.tar.gz
mkdir $CURRENT_PATH/open-build-service-2.5.50
cp -r dist/ docs/ src/ AUTHORS COPYING INSTALL README.md TODO $CURRENT_PATH/open-build-service-2.5.50
popd

tar czvf $CURRENT_PATH/open-build-service-2.5.50.tar.gz ./open-build-service-2.5.50

# SystemD files
pushd ./systemd
rm $CURRENT_PATH/open-build-service-2.5.50-systemd.tar.gz
tar czvf $CURRENT_PATH/open-build-service-2.5.50-systemd.tar.gz *
popd
