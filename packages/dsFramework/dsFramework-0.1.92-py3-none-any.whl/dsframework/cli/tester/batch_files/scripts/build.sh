#!/bin/bash
python ./batch_files/setup.py clean --all
# python ./batch_files/setup.py bdist_wheel
python ./batch_files/setup.py bdist_wheel pipes
python ./batch_files/setup.py bdist_wheel no_pipes

