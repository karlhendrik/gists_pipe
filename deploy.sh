#!/bin/bash
set -e
ssh travis@65.21.54.162 -C "cd gists_pipe && git checkout main && git pull && bash build.sh"