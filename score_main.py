# coding=utf-8
# Copyright 2019 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Calculates evaluation scores for a prediction TSV file.

The prediction file is produced by predict_main.py and should contain 3 or more
columns:
  1: sources (concatenated)
  2: prediction
  3-n: targets (1 or more)
"""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

from absl import app
from absl import flags
from absl import logging

from easse.report import get_all_scores

import score_lib
from utils import read_lines, get_data_filepath

FLAGS = flags.FLAGS

flags.DEFINE_string(
    'prediction_file', None,
    'TSV file containing source, prediction, and target columns.')
flags.DEFINE_bool(
    'case_insensitive', True,
    'Whether score computation should be case insensitive (in the LaserTagger '
    'paper this was set to True).')


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  flags.mark_flag_as_required('prediction_file')

  sources, predictions, _ = score_lib.read_data(
      FLAGS.prediction_file, FLAGS.case_insensitive)
  ref_filepaths = [get_data_filepath('turkcorpus', 'valid', 'simple.turk', i) for i in range(8)]
  target_lists = [read_lines(ref_filepath) for ref_filepath in ref_filepaths]
  logging.info(f'Read file: {FLAGS.prediction_file}')
  turk_scores = get_all_scores(orig_sents=sources, sys_sents=predictions, refs_sents=target_lists)
  logging.info("[turk] {}".format(turk_scores))
  ref_filepaths = [get_data_filepath('asset', 'valid', 'simp', i) for i in range(10)]
  target_lists = [read_lines(ref_filepath) for ref_filepath in ref_filepaths]
  asset_scores = get_all_scores(orig_sents=sources, sys_sents=predictions, refs_sents=target_lists)
  logging.info("[asset] {}".format(asset_scores))

if __name__ == '__main__':
  app.run(main)
