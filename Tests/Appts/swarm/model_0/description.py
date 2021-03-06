# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------


## This file defines parameters for a prediction experiment.

###############################################################################
#                                IMPORTANT!!!
# This params file is dynamically generated by the RunExperimentPermutations
# script. Any changes made manually will be over-written the next time
# RunExperimentPermutations is run!!!
###############################################################################


from nupic.frameworks.opf.exp_description_helpers import importBaseDescription

# the sub-experiment configuration
config ={
  'aggregationInfo' : {'seconds': 0, 'fields': [], 'months': 0, 'days': 0, 'years': 0, 'hours': 0, 'microseconds': 0, 'weeks': 0, 'minutes': 0, 'milliseconds': 0},
  'modelParams' : {'tmParams': {'minThreshold': 9, 'activationThreshold': 16, 'pamLength': 5}, 'sensorParams': {'encoders': {u'AGE_0_54': None, u'timestamp_weekend': {'name': 'timestamp', 'type': 'DateEncoder', 'fieldname': 'timestamp', 'weekend': (21, 1)}, u'DIST_0_30': {'maxval': 1.0, 'name': 'DIST_0_30', 'clipInput': True, 'minval': 0, 'n': 54, 'fieldname': 'DIST_0_30', 'w': 21, 'type': 'ScalarEncoder'}, u'MARRIED': None, u'timestamp_dayOfWeek': None, u'timestamp_timeOfDay': None, u'MALE': None, u'Ct': {'maxval': 1.0, 'name': 'Ct', 'clipInput': True, 'minval': 0, 'n': 41, 'fieldname': 'Ct', 'w': 21, 'type': 'ScalarEncoder'}}}, 'spParams': {'synPermInactiveDec': 0.06811521904926}, 'clParams': {'alpha': 0.04997538384508139}},

}

mod = importBaseDescription('..\description.py', config)
locals().update(mod.__dict__)
