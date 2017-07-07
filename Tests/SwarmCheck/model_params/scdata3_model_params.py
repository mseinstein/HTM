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
                   'clParams': { 'alpha': 0.025075000000000004,
                                 'regionName': 'SDRClassifierRegion',
                                 'steps': '1',
                                 'verbosity': 0},
                   'inferenceType': 'TemporalAnomaly',
                   'sensorParams': { 'encoders': { u'Ct': { 'clipInput': True,
                                                            'fieldname': 'Ct',
                                                            'maxval': 6.0,
                                                            'minval': 0,
                                                            'n': 147,
                                                            'name': 'Ct',
                                                            'type': 'ScalarEncoder',
                                                            'w': 21},
                                                   u'Shift1': { 'clipInput': True,
                                                                'fieldname': 'Shift1',
                                                                'maxval': 6.0,
                                                                'minval': 0,
                                                                'n': 147,
                                                                'name': 'Shift1',
                                                                'type': 'ScalarEncoder',
                                                                'w': 21},
                                                   u'Shift5': None,
                                                   u'timestamp_dayOfWeek': None,
                                                   u'timestamp_timeOfDay': None,
                                                   u'timestamp_weekend': None},
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
                                 'synPermInactiveDec': 0.075075},
                   'tmEnable': True,
                   'tmParams': { 'activationThreshold': 13,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'globalDecay': 0.0,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'maxAge': 0,
                                 'maxSegmentsPerCell': 128,
                                 'maxSynapsesPerSegment': 32,
                                 'minThreshold': 10,
                                 'newSynapseCount': 20,
                                 'outputType': 'normal',
                                 'pamLength': 2,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1960,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0},
                   'trainSPNetOnlyIfRequested': False},
  'predictAheadTime': None,
  'version': 1}