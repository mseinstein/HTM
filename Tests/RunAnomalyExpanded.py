model = createModel(InputName)
    def createModel(InputName):
        """
        Given a model params dictionary, create a CLA Model. Automatically enables
        inference for predicted field.
        :param modelParams: Model params dict
        :return: OPF Model object
        """
        CsvCol,CsvDataTypes,CsvData,csvMin,csvMax,csvStd = getNewParams(InputName)
            def getNewParams(InputName):
                """
                
                """
                INPUT_FILE = "%s.csv" % (InputName)
                CsvData = pd.read_csv(INPUT_FILE)
                CsvCol = CsvData.columns
                CsvDataTypes = CsvData.loc[0].tolist()
                CsvData = CsvData[:][2:]
                csvMax,csvMin,csvStd = [],[],[]
                for Col,ColType in enumerate(CsvDataTypes):
                    if ColType == 'float':
                        CsvData[CsvCol[Col]] = pd.to_numeric(CsvData[CsvCol[Col]])
                        csvMax.append(CsvData[CsvCol[Col]].max())
                        csvMin.append(CsvData[CsvCol[Col]].min())
                        csvStd.append(np.std(CsvData[CsvCol[Col]]))
                    else:
                        csvMax.append(None)
                        csvMin.append(None)
                        csvStd.append(None)
                return [CsvCol,CsvDataTypes,CsvData,csvMin,csvMax,csvStd]
        # Try to find already existing params file
        try:
            params = getModelParamsFromName(InputName)
                def getModelParamsFromName(InputName):
                    """
                    Given a gym name, assumes a matching model params python module exists within the model_params directory and attempts to import it.
                    :param gymName: Gym name, used to guess the model params module name.
                    :return: OPF Model params dictionary
                    """
                    importName = "model_params.%s_model_params" % (InputName.replace(" ", "_").replace("-", "_"))
                    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
                    params = {'modelConfig': importedModelParams}
                    return params
            params["inferenceArgs"] = {'inputPredictedField':'auto','predictionSteps': [1],'predictedField': CsvCol[1]}
        except:    
            print 'swarm file not found, using generic values'
        # Get the new parameters from the csv file
            minResolution = 0.001
            tmImplementation = "cpp"
            # Load model parameters and update encoder params
            if (tmImplementation is "cpp"):
                paramFileRelativePath = os.path.join("anomaly_params_random_encoder","best_single_metric_anomaly_params_cpp.json")
            elif (tmImplementation is "tm_cpp"):
                paramFileRelativePath = os.path.join("anomaly_params_random_encoder","best_single_metric_anomaly_params_tm_cpp.json")
            else:
                raise ValueError("Invalid string for tmImplementation. Try cpp or tm_cpp")        
            with resource_stream(__name__, paramFileRelativePath) as infile:
                params = json.load(infile)
            _fixupRandomEncoderParams(params, CsvCol, CsvDataTypes, CsvData,csvMin, csvMax, csvStd, minResolution)
                def _fixupRandomEncoderParams(params, CsvCol, CsvDataTypes, CsvData, csvMin,csvMax ,csvStd, minResolution):
                    """
                    Given model params, figure out the correct parameters for the
                    RandomDistributed encoder. Modifies params in place.
                    """
                    encDict = (params["modelConfig"]["modelParams"]["sensorParams"]["encoders"])
                    numBuckets = 130.0
                    for Col,ColType in enumerate(CsvDataTypes):
                        if ColType == 'datetime':
                            Nm1 = '%s_timeOfDay' % (CsvCol[Col])
                            encDict[Nm1] = {}
                            encDict[Nm1]['type'] = 'DateEncoder'
                            encDict[Nm1]['timeOfDay'] = [21,9.49]
                            encDict[Nm1]['fieldname'] = CsvCol[Col]
                            encDict[Nm1]['name'] = CsvCol[Col]
                            Nm2 = '%s_dayOfWeek' % (CsvCol[Col])
                            encDict[Nm2] = None
                            Nm3 = '%s_weekend' % (CsvCol[Col])
                            encDict[Nm3] = None
                        elif ColType == 'float':
                            encDict[CsvCol[Col]] = {}
                            encDict[CsvCol[Col]]['name'] = CsvCol[Col]
                            encDict[CsvCol[Col]]['fieldname'] = CsvCol[Col]
                            encDict[CsvCol[Col]]['seed'] = 42
                            encDict[CsvCol[Col]]["type"] =  "RandomDistributedScalarEncoder"
                            maxVal = csvMax[Col]
                            minVal = csvMin[Col]
                            # Handle the corner case where the incoming min and max are the same
                            if minVal == maxVal:
                                maxVal = minVal + 1
                            maxVal = maxVal
                            minVal = minVal
                            resolution = max(minResolution,(maxVal - minVal) / numBuckets)
                            encDict[CsvCol[Col]]["resolution"] = resolution
        params["inferenceArgs"]["predictedField"] = CsvCol[1]
        params['modelConfig']['modelParams']['clEnable'] = True
        model = ModelFactory.create(modelConfig=params["modelConfig"])
            def create(modelConfig, logLevel=logging.ERROR):    ## model_factory.py ##
                """ Create a new model instance, given a description dictionary.
                @param modelConfig (dict) A dictionary describing the current model `described here <../../quick-start/example-model-params.html>`_
                @param logLevel (int) The level of logging output that should be generated
                @exception (Exception) Unsupported model type
                @returns: :class:`nupic.frameworks.opf.model.Model`"""
                logger = ModelFactory.__getLogger()
                logger.setLevel(logLevel)
                logger.debug("ModelFactory returning Model from dict: %s", modelConfig)
                modelClass = None
                if modelConfig['model'] == "HTMPrediction":
                    modelClass = HTMPredictionModel
                        def __init__(self,sensorParams={},inferenceType=InferenceType.TemporalNextStep,spEnable=True,spParams={},trainSPNetOnlyIfRequested=False,tmEnable=True,tmParams={},
                                clEnable=True,clParams={},anomalyParams={},minLikelihoodThreshold=DEFAULT_LIKELIHOOD_THRESHOLD,maxPredictionsPerStep=DEFAULT_MAX_PREDICTIONS_PER_STEP,network=None):
                            if not inferenceType in self.__supportedInferenceKindSet:
                                raise ValueError("{0} received incompatible inference type: {1}".format(self.__class__, inferenceType))
                            # Call super class constructor
                            super(HTMPredictionModel, self).__init__(inferenceType)
                            # self.__restoringFromState is set to True by our __setstate__ method and back to False at completion of our _deSerializeExtraData() method.
                            self.__restoringFromState = False
                            self.__restoringFromV1 = False
                            # Intitialize logging
                            self.__logger = initLogger(self)
                            self.__logger.debug("Instantiating %s." % self.__myClassName)
                            self._minLikelihoodThreshold = minLikelihoodThreshold
                            self._maxPredictionsPerStep = maxPredictionsPerStep
                            # set up learning parameters (note: these may be replaced via enable/disable//SP/TM//Learning methods)
                            self.__spLearningEnabled = bool(spEnable)
                            self.__tpLearningEnabled = bool(tmEnable)
                            # Explicitly exclude the TM if this type of inference doesn't require it
                            if not InferenceType.isTemporal(self.getInferenceType()) or self.getInferenceType() == InferenceType.NontemporalMultiStep:
                                tmEnable = False
                            self._netInfo = None
                            self._hasSP = spEnable
                            self._hasTP = tmEnable
                            self._hasCL = clEnable
                            self._classifierInputEncoder = None
                            self._predictedFieldIdx = None
                            self._predictedFieldName = None
                            self._numFields = None
                            # init anomaly
                            # -----------------------------------------------------------------------
                            if network is not None:
                                self._netInfo = NetworkInfo(net=network, statsCollectors=[])
                            else:
                                # Create the network
                                self._netInfo = self.__createHTMNetwork(sensorParams, spEnable, spParams, tmEnable, tmParams, clEnable,clParams, anomalyParams)
                            # Initialize Spatial Anomaly detection parameters
                            if self.getInferenceType() == InferenceType.NontemporalAnomaly:
                                self._getSPRegion().setParameter("anomalyMode", True)
                            # Initialize Temporal Anomaly detection parameters
                            if self.getInferenceType() == InferenceType.TemporalAnomaly:
                                self._getTPRegion().setParameter("anomalyMode", True)
                            # -----------------------------------------------------------------------
                            # This flag, if present tells us not to train the SP network unless the user specifically asks for the SP inference metric
                            self.__trainSPNetOnlyIfRequested = trainSPNetOnlyIfRequested
                            self.__numRunCalls = 0
                            # Tracks whether finishedLearning() has been called
                            self.__finishedLearning = False
                            self.__logger.debug("Instantiated %s" % self.__class__.__name__)
                            self._input = None
                            return
                elif modelConfig['model'] == "TwoGram":
                    modelClass = TwoGramModel
                elif modelConfig['model'] == "PreviousValue":
                    modelClass = PreviousValueModel
                else:
                    raise Exception("ModelFactory received unsupported Model type: %s" % modelConfig['model'])
                return modelClass(**modelConfig['modelParams'])
        model.enableLearning()
            def enableLearning(self):
                """ Turn Learning on for the current model. """
                self.__learningEnabled = True
                return
        model.enableInference(params["inferenceArgs"])
            def enableInference(self, inferenceArgs=None):
                """ Enable inference for this model.
                :param inferenceArgs: (dict) A dictionary of arguments required for inference. These depend on the InferenceType of the current model"""
                self.__inferenceEnabled = True
                self.__inferenceArgs = inferenceArgs
        return model
runIoThroughNupic(inputData, model, InputName)
    """
    Handles looping over the input data and passing each row into the given model object, as well as extracting the result object and passing it into an output handler.
    :param inputData: file path to input data CSV
    :param model: OPF Model object
    :param InputName: Gym name, used for output handler naming"""
    inputFile = open(inputData, "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows     
    ColNm = csvReader.next()
    csvReader.next()
    csvReader.next()
    output = output_anomaly_generic.NuPICFileOutput(InputName)
        def __init__(self, *args, **kwargs):
            super(NuPICFileOutput, self).__init__(*args, **kwargs)
            self.outputFiles = []
            self.outputWriters = []
            self.lineCount = 0
            headerRow = ['timestamp', 'Ct','prediction', 'anomalyScore', 'anomaly_likelihood']
            outputFileName = "%s_out.csv" % self.name
            print "Preparing to output %s data to %s" % (self.name, outputFileName)
            self.outputFile = open(outputFileName, "w")
            self.outputWriter = csv.writer(self.outputFile)
            self.outputWriter.writerow(headerRow)
    shifter = InferenceShifter()
        def __init__(self):
            self._inferenceBuffer = None
    counter = 0
    for row in csvReader:
        counter += 1
        if (counter % 300 == 0):
            print "Read %i lines..." % counter
        timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
        PredFld = [float(row[Ct]) for Ct in xrange(1,len(ColNm))]
        ResDict = {ColNm[x] : PredFld[x-1] for x in xrange(1,len(ColNm))}
        ResDict["timestamp"] = timestamp
        result = model.run(ResDict)
            def run(self, inputRecord):
                assert not self.__restoringFromState
                assert inputRecord
                results = super(HTMPredictionModel, self).run(inputRecord)
                    def run(self, inputRecord):
                        """
                        Run one iteration of this model.
                        :param inputRecord: (object)
                               A record object formatted according to
                               :meth:`~nupic.data.record_stream.RecordStreamIface.getNextRecord` or
                               :meth:`~nupic.data.record_stream.RecordStreamIface.getNextRecordDict`
                               result format.
                        :returns: (:class:`~nupic.frameworks.opf.opf_utils.ModelResult`)
                                 An ModelResult namedtuple. The contents of ModelResult.inferences depends on the the specific inference type of this model, which can be queried by :meth:`.getInferenceType`. """
                        if hasattr(self, '_numPredictions'):
                            predictionNumber = self._numPredictions
                            self._numPredictions += 1
                        else:
                            predictionNumber = None
                        result = opf_utils.ModelResult(predictionNumber=predictionNumber,rawInput=inputRecord)
                            def __init__(self,predictionNumber=None,rawInput=None,sensorInput=None,inferences=None,metrics=None,predictedFieldIdx=None,predictedFieldName=None,classifierInput=None):
                                self.predictionNumber = predictionNumber
                                self.rawInput = rawInput
                                self.sensorInput = sensorInput
                                self.inferences = inferences
                                self.metrics = metrics
                                self.predictedFieldIdx = predictedFieldIdx
                                self.predictedFieldName = predictedFieldName
                                self.classifierInput = classifierInput
                        return result
                self.__numRunCalls += 1
                if self.__logger.isEnabledFor(logging.DEBUG):
                    self.__logger.debug("HTMPredictionModel.run() inputRecord=%s", (inputRecord))
                results.inferences = {}
                self._input = inputRecord
                # -------------------------------------------------------------------------
                # Turn learning on or off?
                if '_learning' in inputRecord:
                    if inputRecord['_learning']:
                        self.enableLearning()
                            def enableLearning(self):
                                super(HTMPredictionModel, self).enableLearning()
                                    def enableLearning(self):
                                        """ Turn Learning on for the current model. """
                                        self.__learningEnabled = True
                                        return
                                self.setEncoderLearning(True)
                                    def setEncoderLearning(self,learningEnabled):
                                        self._getEncoder().setLearning(learningEnabled)
                                            def _getEncoder(self):
                                                """Returns:  sensor region's encoder for the given network"""
                                                return  self._getSensorRegion().getSelf().encoder
                                                    def _getSensorRegion(self):
                                                        """Returns reference to the network's Sensor region"""
                                                        return self._netInfo.net.regions['sensor']
                    else:
                        self.disableLearning()
                            def disableLearning(self):
                                super(HTMPredictionModel, self).disableLearning()
                                    def disableLearning(self):
                                        """ Turn Learning off for the current model. """
                                        self.__learningEnabled = False
                                        return
                                self.setEncoderLearning(False)
                                    def setEncoderLearning(self,learningEnabled):
                                        self._getEncoder().setLearning(learningEnabled)
                ###########################################################################
                # Predictions and Learning
                ###########################################################################
                self._sensorCompute(inputRecord)
                    def _sensorCompute(self, inputRecord):
                        sensor = self._getSensorRegion()
                            def _getSensorRegion(self):
                                """Returns reference to the network's Sensor region"""
                                return self._netInfo.net.regions['sensor']
                        self._getDataSource().push(inputRecord)
                            def _getDataSource(self):
                                """Returns: data source that we installed in sensor region"""
                                return self._getSensorRegion().getSelf().dataSource
                        sensor.setParameter('topDownMode', False)
                            def setParameter(self, paramName, value):
                                """Set parameter value"""
                                (setter, getter) = self._getParameterMethods(paramName)
                                if setter is None:
                                    import exceptions
                                    raise exceptions.Exception("setParameter -- parameter name '%s' does not exist in region %s of type %s"% (paramName, self.name, self.type))
                                setter(paramName, value)
                        sensor.prepareInputs()
                        try:
                            sensor.compute()
                        except StopIteration as e:
                            raise Exception("Unexpected StopIteration", e,"ACTUAL TRACEBACK: %s" % traceback.format_exc())
                self._spCompute()
                    def _spCompute(self):
                        sp = self._getSPRegion()
                        if sp is None:
                            return
                        sp.setParameter('topDownMode', False)
                        sp.setParameter('inferenceMode', self.isInferenceEnabled())
                        sp.setParameter('learningMode', self.isLearningEnabled())
                        sp.prepareInputs()
                        sp.compute()
                self._tpCompute()
                    def _tpCompute(self):
                        tm = self._getTPRegion()
                        if tm is None:
                            return
                        if (self.getInferenceType() == InferenceType.TemporalAnomaly or self._isReconstructionModel()):
                          topDownCompute = True
                        else:
                          topDownCompute = False
                        tm = self._getTPRegion()
                        tm.setParameter('topDownMode', topDownCompute)
                        tm.setParameter('inferenceMode', self.isInferenceEnabled())
                        tm.setParameter('learningMode', self.isLearningEnabled())
                        tm.prepareInputs()
                        tm.compute()
                results.sensorInput = self._getSensorInputRecord(inputRecord)
                inferences = {}
                # TODO: Reconstruction and temporal classification not used. Remove
                if self._isReconstructionModel():
                    inferences = self._reconstructionCompute()
                elif self._isMultiStepModel():
                    inferences = self._multiStepCompute(rawInput=inputRecord)
                # For temporal classification. Not used, and might not work anymore
                elif self._isClassificationModel():
                    inferences = self._classificationCompute()
                results.inferences.update(inferences)
                inferences = self._anomalyCompute()
                results.inferences.update(inferences)
                # -----------------------------------------------------------------------
                # Store the index and name of the predictedField
                results.predictedFieldIdx = self._predictedFieldIdx
                results.predictedFieldName = self._predictedFieldName
                results.classifierInput = self._getClassifierInputRecord(inputRecord)
                # =========================================================================
                # output
                assert (not self.isInferenceEnabled() or results.inferences is not None), "unexpected inferences: %r" %  results.inferences
                #self.__logger.setLevel(logging.DEBUG)
                if self.__logger.isEnabledFor(logging.DEBUG):
                    self.__logger.debug("inputRecord: %r, results: %r" % (inputRecord,results))
                return results
        result = shifter.shift(result)
        steps = result.inferences["multiStepBestPredictions"].keys()
        prediction = result.inferences["multiStepBestPredictions"][steps[0]]
        anomalyScore = result.inferences["anomalyScore"]
        output.write(timestamp, PredFld[0], prediction, anomalyScore)
    inputFile.close()
    output.close()