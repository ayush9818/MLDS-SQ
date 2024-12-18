#!/bin/bash

case "$1" in
    run-pipeline)
        python pipeline.py --config $CONFIG_PATH
        ;;
    test-app)
        pytest
        ;;
    check-lint)
        pylint pipeline.py
        ;;
    *)
        echo "Usage: $0 {pipeline|pytest|pylint}"
        exit 1
esac
