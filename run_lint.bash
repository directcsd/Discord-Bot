#!/usr/bin/env bash

rm pep8.log

flake8 . > pep8.log
