#!/usr/bin/env bash

find /app -type f -name '*.pyc' -delete

export PATH=/venv/bin:$PATH

if [[ "$MPIVER" = "HPCX" ]]; then
   echo "loading HPCX"
   source $HPCSDK_HOME/comm_libs/hpcx/latest/hpcx-init.sh
   hpcx_load
fi

if [[ "$DEVITO_ARCH" = "icc" ]]; then
   echo "loading Intel icc/mpicc enviroment"
   source $ONEAPI_ROOT/compiler/latest/env/vars.sh
   source $ONEAPI_ROOT/mpi/latest/env/vars.sh
fi

if [[ -z "${DEPLOY_ENV}" ]]; then
    exec "$@"
    ./codecov -t -t ${CODECOV_TOKEN} -F "${DEVITO_ARCH}-${DEVITO-PLATFORM}"
else
    exec "$@"
fi