#!/bin/bash

ROOT="../../"
export RAPIDMINER_HOME=${ROOT}"/rapidminer"
RAPIDMINER=$RAPIDMINER_HOME

"./"${RAPIDMINER}"/scripts/rapidminer" -f $1
