MODEL_PARAMS = \
{ 'aggregationInfo': { 'days': 0,
                       'fields': [],
                       'hours': 0,
                       'microseconds': 0,
                       'milliseconds': 0,
                       'minutes': 0,
                       'months': 0,
                       'seconds': 0,
                       'weeks': 0,
                       'years': 0},
  'model': 'HTMPrediction',
  'modelParams': { 'anomalyParams': { u'anomalyCacheRecords': None,
                                      u'autoDetectThreshold': None,
                                      u'autoDetectWaitRecords': None},
                   'clParams': { 'alpha': 0.04997538384508139,
                                 'regionName': 'SDRClassifierRegion',
                                 'steps': '7',
                                 'verbosity': 0},
                   'inferenceType': 'TemporalAnomaly',
                   'sensorParams': { 'encoders': { u'Ct': { 'clipInput': True,
                                                            'fieldname': 'Ct',
                                                            'maxval': 1.0,
                                                            'minval': 0,
                                                            'n': 41,
                                                            'name': 'Ct',
                                                            'type': 'ScalarEncoder',
                                                            'w': 21},
                                                   u'ZIP_10467': { 'clipInput': True,
                                                                   'fieldname': 'ZIP_10467',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'ZIP_10467',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'ZIP_10462': { 'clipInput': True,
                                                                   'fieldname': 'ZIP_10462',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'ZIP_10462',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'ZIP_10475': { 'clipInput': True,
                                                                   'fieldname': 'ZIP_10475',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'ZIP_10475',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'ZIP_10466': { 'clipInput': True,
                                                                   'fieldname': 'ZIP_10466',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'ZIP_10466',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'ZIP_10469': { 'clipInput': True,
                                                                   'fieldname': 'ZIP_10469',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'ZIP_10469',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'DEPT_11': { 'clipInput': True,
                                                                   'fieldname': 'DEPT_11',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'DEPT_11',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'DEPT_24': { 'clipInput': True,
                                                                   'fieldname': 'DEPT_24',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'DEPT_24',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'DEPT_41': { 'clipInput': True,
                                                                   'fieldname': 'DEPT_41',
                                                                   'maxval': 1.0,
                                                                   'minval': 0,
                                                                   'n': 54,
                                                                   'name': 'DEPT_41',
                                                                   'type': 'ScalarEncoder',
                                                                   'w': 21},
                                                   u'timestamp_dayOfWeek': None,
                                                   u'timestamp_timeOfDay': None,
                                                   u'timestamp_weekend': { 'fieldname': 'timestamp',
                                                                           'name': 'timestamp',
                                                                           'type': 'DateEncoder',
                                                                           'weekend': ( 21,
                                                                                        1)}},
                                     'sensorAutoReset': None,
                                     'verbosity': 0},
                   'spEnable': True,
                   'spParams': { 'boostStrength': 0.0,
                                 'columnCount': 2048,
                                 'globalInhibition': 1,
                                 'inputWidth': 0,
                                 'numActiveColumnsPerInhArea': 40,
                                 'potentialPct': 0.8,
                                 'seed': 1956,
                                 'spVerbosity': 0,
                                 'spatialImp': 'cpp',
                                 'synPermActiveInc': 0.05,
                                 'synPermConnected': 0.1,
                                 'synPermInactiveDec': 0.06811521904926},
                   'tmEnable': True,
                   'tmParams': { 'activationThreshold': 16,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'globalDecay': 0.0,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'maxAge': 0,
                                 'maxSegmentsPerCell': 128,
                                 'maxSynapsesPerSegment': 32,
                                 'minThreshold': 9,
                                 'newSynapseCount': 20,
                                 'outputType': 'normal',
                                 'pamLength': 5,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1960,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0},
                   'trainSPNetOnlyIfRequested': False},
  'predictAheadTime': None,
  'version': 1}