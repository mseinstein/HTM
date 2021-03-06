swarmConfig ==  swarmDescriptionJson == SWARM_DESCRIPTION




modelParams = permutations_runner.runWithConfig(swarmConfig,{"maxWorkers": maxWorkers, "overwrite": True},outputLabel=outputLabel,outDir=permWorkDir,permWorkDir=permWorkDir,verbosity=0)
    def runWithConfig(swarmConfig, options,outDir=None, outputLabel="default",permWorkDir=None, verbosity=1): ### permutations_runner.py ###
        global g_currentVerbosityLevel
        g_currentVerbosityLevel = verbosity
        if outDir is None:
            outDir = os.getcwd()
        if permWorkDir is None:
            permWorkDir = os.getcwd()
        _checkOverwrite(options, outDir) 
            def _checkOverwrite(options, outDir): ### permutations_runner.py ###
                overwrite = options["overwrite"]
                if not overwrite:
                    for name in ("description.py", "permutations.py"):
                        if os.path.exists(os.path.join(outDir, name)):
                            raise RuntimeError("The %s file already exists and will be ""overwritten by this tool. If it is OK to overwrite ""this file, use the --overwrite option." % os.path.join(outDir, "description.py"))
                del options["overwrite"]
        _generateExpFilesFromSwarmDescription(swarmConfig, outDir)
            def _generateExpFilesFromSwarmDescription(swarmDescriptionJson, outDir):
                # The expGenerator expects the JSON without newlines for an unknown reason.
                expDescConfig = json.dumps(swarmDescriptionJson)
                expDescConfig = expDescConfig.splitlines()
                expDescConfig = "".join(expDescConfig)
                expGenerator(["--description=%s" % (expDescConfig),"--outDir=%s" % (outDir)])
                    def expGenerator(args):
                        """ Parses, validates, and executes command-line options;     On success: Performs requested operation and exits program normally     On Error:   Dumps exception/error info in JSON format to stdout and exits the program with non-zero status. """
                        # -----------------------------------------------------------------
                        # Parse command line options
                        parser = OptionParser()
                        parser.set_usage("%prog [options] --description='{json object with args}'\n" + "%prog [options] --descriptionFromFile='{filename}'\n" + "%prog [options] --showSchema")
                        parser.add_option("--description", dest = "description", help = "Tells ExpGenerator to generate an experiment description.py and permutations.py file using the given JSON formatted experiment description string.")
                        parser.add_option("--descriptionFromFile", dest = 'descriptionFromFile', help = "Tells ExpGenerator to open the given filename and use it's contents as the JSON formatted experiment description.")
                        parser.add_option("--claDescriptionTemplateFile", dest = 'claDescriptionTemplateFile', default = 'claDescriptionTemplate.tpl', help = "The file containing the template description file for ExpGenerator [default: %default]")
                        parser.add_option("--showSchema", action="store_true", dest="showSchema", help="Prints the JSON schemas for the --description arg.")
                        parser.add_option("--version", dest = 'version', default='v2', help = "Generate the permutations file for this version of hypersearch. Possible choices are 'v1' and 'v2' [default: %default].")
                        parser.add_option("--outDir", dest = "outDir", default=None, help = "Where to generate experiment. If not specified, then a temp directory will be created")
                        (options, remainingArgs) = parser.parse_args(args)
                        # -----------------------------------------------------------------
                        # Check for unprocessed args
                        if len(remainingArgs) > 0:
                            raise _InvalidCommandArgException(_makeUsageErrorStr("Unexpected command-line args: <%s>" % (' '.join(remainingArgs),), parser.get_usage()))
                        # -----------------------------------------------------------------
                        # Check for use of mutually-exclusive options
                        activeOptions = filter(lambda x: getattr(options, x) != None, ('description', 'showSchema'))
                        if len(activeOptions) > 1:
                            raise _InvalidCommandArgException(_makeUsageErrorStr(("The specified command options are mutually-exclusive: %s") % (activeOptions,), parser.get_usage()))
                        # -----------------------------------------------------------------
                        # Process requests
                        if options.showSchema:
                            _handleShowSchemaOption()
                                def _handleShowSchemaOption():  ### ExpGenerator.py ###
                                    """ Displays command schema to stdout and exit program """
                                    print "\n============== BEGIN INPUT SCHEMA for --description =========>>"
                                    print(json.dumps(_getExperimentDescriptionSchema(), indent=_INDENT_STEP*2))
                                        def _getExperimentDescriptionSchema():      ### ExpGenerator.py ###
                                            """Returns the experiment description schema. This implementation loads it in from file experimentDescriptionSchema.json.
                                            Parameters:
                                            --------------------------------------------------------------------------
                                            Returns:    returns a dict representing the experiment description schema."""
                                            installPath = os.path.dirname(os.path.abspath(__file__))
                                            schemaFilePath = os.path.join(installPath, "experimentDescriptionSchema.json")
                                            return json.loads(open(schemaFilePath, 'r').read())
                                    print "\n<<============== END OF INPUT SCHEMA for --description ========"
                                    return
                        elif options.description:
                            _handleDescriptionOption(options.description, options.outDir, parser.get_usage(), hsVersion=options.version, claDescriptionTemplateFile = options.claDescriptionTemplateFile)
                                def _handleDescriptionOption(cmdArgStr, outDir, usageStr, hsVersion, claDescriptionTemplateFile):  ### ExpGenerator.py ###
                                    """ Parses and validates the --description option args and executes the request
                                    Parameters:
                                    -----------------------------------------------------------------------
                                    cmdArgStr:  JSON string compatible with _gExperimentDescriptionSchema
                                    outDir:     where to place generated experiment files
                                    usageStr:   program usage string
                                    hsVersion:  which version of hypersearch permutations file to generate, can be 'v1' or 'v2'
                                    claDescriptionTemplateFile: Filename containing the template description
                                    retval:     nothing """
                                    # convert --description arg from JSON string to dict
                                    try:
                                        args = json.loads(cmdArgStr)
                                    except Exception, e:
                                        raise _InvalidCommandArgException(_makeUsageErrorStr(("JSON arg parsing failed for --description: %s\n" + "ARG=<%s>") % (str(e), cmdArgStr), usageStr))
                                    #print "PARSED JSON ARGS=\n%s" % (json.dumps(args, indent=4))
                                    filesDescription = _generateExperiment(args, outDir, hsVersion=hsVersion, claDescriptionTemplateFile = claDescriptionTemplateFile)
                                        def _generateExperiment(options, outputDirPath, hsVersion, claDescriptionTemplateFile):  ### ExpGenerator.py ###
                                            """ Executes the --description option, which includes:
                                                1. Perform provider compatibility checks
                                                2. Preprocess the training and testing datasets (filter, join providers)
                                                3. If test dataset omitted, split the training dataset into training and testing datasets.
                                                4. Gather statistics about the training and testing datasets.
                                                5. Generate experiment scripts (description.py, permutaions.py)
                                            Parameters:
                                            --------------------------------------------------------------------------
                                            options:  dictionary that matches the schema defined by the return value of _getExperimentDescriptionSchema();  NOTE: this arg may be modified by this function.
                                            outputDirPath:  where to place generated files
                                            hsVersion:  which version of hypersearch permutations file to generate, can be 'v1' or 'v2'
                                            claDescriptionTemplateFile: Filename containing the template description
                                            Returns:    on success, returns a dictionary per _experimentResultsJSONSchema; raises exception on error
                                                Assumption1: input train and test files have identical field metadata"""
                                            _gExperimentDescriptionSchema = _getExperimentDescriptionSchema()
                                            # Validate JSON arg using JSON schema validator
                                            try:
                                                validictory.validate(options, _gExperimentDescriptionSchema)
                                            except Exception, e:
                                                raise _InvalidCommandArgException(("JSON arg validation failed for option --description: " + "%s\nOPTION ARG=%s") % (str(e), pprint.pformat(options)))
                                            # Validate the streamDef
                                            streamSchema = json.load(resource_stream(jsonschema.__name__,'stream_def.json'))
                                            try:
                                                validictory.validate(options['streamDef'], streamSchema)
                                            except Exception, e:
                                                raise _InvalidCommandArgException(("JSON arg validation failed for streamDef " + "%s\nOPTION ARG=%s") % (str(e), json.dumps(options)))
                                            # -----------------------------------------------------------------------
                                            # Handle legacy parameters from JAVA API server
                                            # TODO: remove this!
                                            _handleJAVAParameters(options)
                                            # -----------------------------------------------------------------------
                                            # Get default values
                                            for propertyName in _gExperimentDescriptionSchema['properties']:
                                                _getPropertyValue(_gExperimentDescriptionSchema, propertyName, options)
                                                    def _getPropertyValue(schema, propertyName, options):   ### ExpGenerator.py ###
                                                        """Checks to see if property is specified in 'options'. If not, reads the default value from the schema"""
                                                        if propertyName not in options:
                                                            paramsSchema = schema['properties'][propertyName]
                                                            if 'default' in paramsSchema:
                                                                options[propertyName] = paramsSchema['default']
                                                            else:
                                                                options[propertyName] = None
                                            if options['inferenceArgs'] is not None:
                                                infArgs = _gExperimentDescriptionSchema['properties']['inferenceArgs']
                                                for schema in infArgs['type']:
                                                    if isinstance(schema, dict):
                                                        for propertyName in schema['properties']:
                                                            _getPropertyValue(schema, propertyName, options['inferenceArgs'])
                                            if options['anomalyParams'] is not None:
                                                anomalyArgs = _gExperimentDescriptionSchema['properties']['anomalyParams']
                                                for schema in anomalyArgs['type']:
                                                    if isinstance(schema, dict):
                                                        for propertyName in schema['properties']:
                                                            _getPropertyValue(schema, propertyName, options['anomalyParams'])
                                            # If the user specified nonTemporalClassification, make sure prediction steps is 0
                                            predictionSteps = options['inferenceArgs'].get('predictionSteps', None)
                                            if options['inferenceType'] == InferenceType.NontemporalClassification:
                                                if predictionSteps is not None and predictionSteps != [0]:
                                                    raise RuntimeError("When NontemporalClassification is used, prediction steps must be [0]")
                                            # -------------------------------------------------------------------------
                                            # If the user asked for 0 steps of prediction, then make this a spatial
                                            #  classification experiment
                                            if predictionSteps == [0] and options['inferenceType'] in ['NontemporalMultiStep', 'TemporalMultiStep', 'MultiStep']:
                                                options['inferenceType'] = InferenceType.NontemporalClassification
                                            # If NontemporalClassification was chosen as the inferenceType, then the
                                            #  predicted field can NOT be used as an input
                                            if options["inferenceType"] == InferenceType.NontemporalClassification:
                                                if options["inferenceArgs"]["inputPredictedField"] == "yes" or options["inferenceArgs"]["inputPredictedField"] == "auto":
                                                    raise RuntimeError("When the inference type is NontemporalClassification inputPredictedField must be set to 'no'")
                                                options["inferenceArgs"]["inputPredictedField"] = "no"
                                            # -----------------------------------------------------------------------
                                            # Process the swarmSize setting, if provided
                                            swarmSize = options['swarmSize']
                                            if swarmSize is None:
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "auto"
                                            elif swarmSize == 'small':
                                                if options['minParticlesPerSwarm'] is None:
                                                    options['minParticlesPerSwarm'] = 3
                                                if options['iterationCount'] is None:
                                                    options['iterationCount'] = 100
                                                if options['maxModels'] is None:
                                                    options['maxModels'] = 1
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "yes"
                                            elif swarmSize == 'medium':
                                                if options['minParticlesPerSwarm'] is None:
                                                    options['minParticlesPerSwarm'] = 5
                                                if options['iterationCount'] is None:
                                                    options['iterationCount'] = 4000
                                                if options['maxModels'] is None:
                                                    options['maxModels'] = 200
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "auto"
                                            elif swarmSize == 'large':
                                                if options['minParticlesPerSwarm'] is None:
                                                    options['minParticlesPerSwarm'] = 15
                                                    #options['killUselessSwarms'] = False
                                                    #options['minFieldContribution'] = -1000
                                                    #options['maxFieldBranching'] = 10
                                                    #options['tryAll3FieldCombinations'] = True
                                                options['tryAll3FieldCombinationsWTimestamps'] = True
                                                if options["inferenceArgs"]["inputPredictedField"] is None:
                                                    options["inferenceArgs"]["inputPredictedField"] = "auto"
                                            else:
                                                raise RuntimeError("Unsupported swarm size: %s" % (swarmSize))
                                            # -----------------------------------------------------------------------
                                            # Get token replacements
                                            tokenReplacements = dict()
                                            #--------------------------------------------------------------------------
                                            # Generate the encoder related substitution strings
                                            includedFields = options['includedFields']
                                            if hsVersion == 'v1':
                                                (encoderSpecsStr, permEncoderChoicesStr) = _generateEncoderStringsV1(includedFields)
                                                    def _generateEncoderStringsV1(includedFields):  ### ExpGenerator.py ###
                                                        """ Generate and return the following encoder related substitution variables:
                                                        encoderSpecsStr:
                                                            For the base description file, this string defines the default encoding dicts for each encoder. For example:
                                                                '__gym_encoder' : {   'fieldname': 'gym','n': 13,'name': 'gym','type': 'SDRCategoryEncoder','w': 7},
                                                                '__address_encoder' : {   'fieldname': 'address','n': 13,'name': 'address','type': 'SDRCategoryEncoder','w': 7}
                                                        encoderSchemaStr:
                                                            For the base description file, this is a list containing a DeferredDictLookup entry for each encoder. For example:
                                                                [DeferredDictLookup('__gym_encoder'),DeferredDictLookup('__address_encoder'),DeferredDictLookup('__timestamp_timeOfDay_encoder'),DeferredDictLookup('__timestamp_dayOfWeek_encoder'),DeferredDictLookup('__consumption_encoder')],
                                                        permEncoderChoicesStr:
                                                            For the permutations file, this defines the possible encoder dicts for each encoder. For example:
                                                                '__timestamp_dayOfWeek_encoder': [ None, {'fieldname':'timestamp', 'name': 'timestamp_timeOfDay','type':'DateEncoder''dayOfWeek': (7,1)},
                                                                         {'fieldname':'timestamp','name': 'timestamp_timeOfDay','type':'DateEncoder','dayOfWeek': (7,3)},],
                                                                '__field_consumption_encoder': [None,{'fieldname':'consumption','name': 'consumption','type':'AdaptiveScalarEncoder','n': 13,'w': 7,}]
                                                        Parameters:
                                                        --------------------------------------------------
                                                        includedFields:  item from the 'includedFields' section of the description JSON object. This is a list of dicts, each dict defining the field name, type, and optional min and max values.
                                                        retval:  (encoderSpecsStr, encoderSchemaStr permEncoderChoicesStr)"""
                                                        # ------------------------------------------------------------------------
                                                        # First accumulate the possible choices for each encoder
                                                        encoderChoicesList = []
                                                        for fieldInfo in includedFields:
                                                            fieldName = fieldInfo['fieldName']
                                                            # Get the list of encoder choices for this field
                                                            (choicesList, aggFunction) = _generateEncoderChoicesV1(fieldInfo)
                                                                def _generateEncoderChoicesV1(fieldInfo):  ### ExpGenerator.py ###
                                                                    """ Return a list of possible encoder parameter combinations for the given field and the default aggregation function to use. Each parameter combination is a dict defining the parameters for the encoder. Here is an example return value for the encoderChoicesList:
                                                                    [None,{'fieldname':'timestamp','name': 'timestamp_timeOfDay','type':'DateEncoder''dayOfWeek': (7,1)},
                                                                            {'fieldname':'timestamp','name': 'timestamp_timeOfDay','type':'DateEncoder''dayOfWeek': (7,3)},],
                                                                    Parameters:
                                                                    --------------------------------------------------
                                                                    fieldInfo:      item from the 'includedFields' section of the description JSON object
                                                                    retval:  (encoderChoicesList, aggFunction)
                                                                        encoderChoicesList: a list of encoder choice lists for this field. Most fields will generate just 1 encoder choice list. DateTime fields can generate 2 or more encoder choice lists, one for dayOfWeek, one for timeOfDay, etc.
                                                                        aggFunction: name of aggregation function to use for this field type"""
                                                                    width = 7
                                                                    fieldName = fieldInfo['fieldName']
                                                                    fieldType = fieldInfo['fieldType']
                                                                    encoderChoicesList = []
                                                                    # Scalar?
                                                                    if fieldType in ['float', 'int']:
                                                                        aggFunction = 'mean'
                                                                        encoders = [None]
                                                                        for n in (13, 50, 150, 500):
                                                                            encoder = dict(type='ScalarSpaceEncoder', name=fieldName, fieldname=fieldName, n=n, w=width, clipInput=True,space="absolute")
                                                                            if 'minValue' in fieldInfo:
                                                                                encoder['minval'] = fieldInfo['minValue']
                                                                            if 'maxValue' in fieldInfo:
                                                                                encoder['maxval'] = fieldInfo['maxValue']
                                                                            encoders.append(encoder)
                                                                        encoderChoicesList.append(encoders)
                                                                    # String?
                                                                    elif fieldType == 'string':
                                                                        aggFunction = 'first'
                                                                        encoders = [None]
                                                                        encoder = dict(type='SDRCategoryEncoder', name=fieldName, fieldname=fieldName, n=100, w=width)
                                                                        encoders.append(encoder)
                                                                        encoderChoicesList.append(encoders)
                                                                    # Datetime?
                                                                    elif fieldType == 'datetime':
                                                                        aggFunction = 'first'
                                                                        # First, the time of day representation
                                                                        encoders = [None]
                                                                        for radius in (1, 8):
                                                                            encoder = dict(type='DateEncoder', name='%s_timeOfDay' % (fieldName),fieldname=fieldName, timeOfDay=(width, radius))
                                                                            encoders.append(encoder)
                                                                        encoderChoicesList.append(encoders)
                                                                        # Now, the day of week representation
                                                                        encoders = [None]
                                                                        for radius in (1, 3):
                                                                            encoder = dict(type='DateEncoder', name='%s_dayOfWeek' % (fieldName),fieldname=fieldName, dayOfWeek=(width, radius))
                                                                            encoders.append(encoder)
                                                                        encoderChoicesList.append(encoders)
                                                                    else:
                                                                        raise RuntimeError("Unsupported field type '%s'" % (fieldType))
                                                                    # Return results
                                                                    return (encoderChoicesList, aggFunction)
                                                            encoderChoicesList.extend(choicesList)
                                                        # ------------------------------------------------------------------------
                                                        # Generate the string containing the encoder specs and encoder schema. See the function comments for an example of the encoderSpecsStr and encoderSchemaStr
                                                        #
                                                        encoderSpecsList = []
                                                        for encoderChoices in encoderChoicesList:
                                                            # Use the last choice as the default in the base file because the 1st is often None
                                                            encoder = encoderChoices[-1]
                                                            # Check for bad characters
                                                            for c in _ILLEGAL_FIELDNAME_CHARACTERS:
                                                                if encoder['name'].find(c) >= 0:
                                                                    raise _ExpGeneratorException("Illegal character in field: %r (%r)" % (c, encoder['name']))
                                                            encoderSpecsList.append("%s: \n%s%s" % (_quoteAndEscape(encoder['name']),2*_ONE_INDENT,pprint.pformat(encoder, indent=2*_INDENT_STEP)))
                                                        encoderSpecsStr = ',\n  '.join(encoderSpecsList)
                                                        # ------------------------------------------------------------------------
                                                        # Generate the string containing the permutation encoder choices. See the
                                                        #  function comments above for an example of the permEncoderChoicesStr
                                                        permEncoderChoicesList = []
                                                        for encoderChoices in encoderChoicesList:
                                                            permEncoderChoicesList.append("%s: %s," % (_quoteAndEscape(encoderChoices[-1]['name']),pprint.pformat(encoderChoices, indent=2*_INDENT_STEP)))
                                                        permEncoderChoicesStr = '\n'.join(permEncoderChoicesList)
                                                        permEncoderChoicesStr = _indentLines(permEncoderChoicesStr, 1,indentFirstLine=False)
                                                            def _indentLines(str, indentLevels = 1, indentFirstLine=True):
                                                                """ Indent all lines in the given string
                                                                str:          input string
                                                                indentLevels: number of levels of indentation to apply
                                                                indentFirstLine: if False, the 1st line will not be indented
                                                                Returns:      The result string with all lines indented"""
                                                                indent = _ONE_INDENT * indentLevels
                                                                lines = str.splitlines(True)
                                                                result = ''
                                                                if len(lines) > 0 and not indentFirstLine:
                                                                    first = 1
                                                                    result += lines[0]
                                                                else:
                                                                    first = 0
                                                                for line in lines[first:]:
                                                                    result += indent + line
                                                                return result
                                                        # Return results
                                                        return (encoderSpecsStr, permEncoderChoicesStr)
                                            elif hsVersion in ['v2', 'ensemble']:
                                                (encoderSpecsStr, permEncoderChoicesStr) = _generateEncoderStringsV2(includedFields, options)
                                                    def _generateEncoderStringsV2(includedFields, options):   ### ExpGenerator.py ###
                                                        """ Generate and return the following encoder related substitution variables:
                                                        encoderSpecsStr:
                                                            For the base description file, this string defines the default encoding dicts for each encoder. For example:
                                                                __gym_encoder = {   'fieldname': 'gym','n': 13,'name': 'gym','type': 'SDRCategoryEncoder','w': 7},
                                                                __address_encoder = {   'fieldname': 'address','n': 13,'name': 'address','type': 'SDRCategoryEncoder','w': 7}
                                                        permEncoderChoicesStr:
                                                            For the permutations file, this defines the possible encoder dicts for each encoder. For example:
                                                                '__gym_encoder' : PermuteEncoder('gym', 'SDRCategoryEncoder', w=7,n=100),
                                                                '__address_encoder' : PermuteEncoder('address', 'SDRCategoryEncoder',w=7, n=100),
                                                                '__timestamp_dayOfWeek_encoder' : PermuteEncoder('timestamp','DateEncoder.timeOfDay', w=7, radius=PermuteChoices([1, 8])),
                                                                '__consumption_encoder': PermuteEncoder('consumption', 'AdaptiveScalarEncoder',w=7, n=PermuteInt(13, 500, 20), minval=0,maxval=PermuteInt(100, 300, 25)),
                                                        Parameters:
                                                        --------------------------------------------------
                                                        includedFields:  item from the 'includedFields' section of the description JSON object. This is a list of dicts, each dict defining the field name, type, and optional min and max values.
                                                        retval:  (encoderSpecsStr permEncoderChoicesStr)"""
                                                        width = 21
                                                        encoderDictsList = []
                                                        # If this is a NontemporalClassification experiment, then the the "predicted" field (the classification value) should be marked to ONLY  go to the classifier
                                                        if options['inferenceType'] in ["NontemporalClassification","NontemporalMultiStep", "TemporalMultiStep","MultiStep"]:
                                                            classifierOnlyField = options['inferenceArgs']['predictedField']
                                                        else:
                                                            classifierOnlyField = None
                                                        # ==========================================================================
                                                        # For each field, generate the default encoding dict and PermuteEncoder constructor arguments
                                                        for fieldInfo in includedFields:
                                                            fieldName = fieldInfo['fieldName']
                                                            fieldType = fieldInfo['fieldType']
                                                            # ---------
                                                            # Scalar?
                                                            if fieldType in ['float', 'int']:
                                                                # n=100 is reasonably hardcoded value for n when used by description.py
                                                                # The swarming will use PermuteEncoder below, where n is variable and depends on w
                                                                runDelta = fieldInfo.get("runDelta", False) 
                                                                if runDelta or "space" in fieldInfo:
                                                                    encoderDict = dict(type='ScalarSpaceEncoder', name=fieldName,fieldname=fieldName, n=100, w=width, clipInput=True)
                                                                    if runDelta:
                                                                        encoderDict["runDelta"] = True
                                                                else:
                                                                    encoderDict = dict(type='AdaptiveScalarEncoder', name=fieldName,fieldname=fieldName, n=100, w=width, clipInput=True)
                                                                if 'minValue' in fieldInfo:
                                                                    encoderDict['minval'] = fieldInfo['minValue']
                                                                if 'maxValue' in fieldInfo:
                                                                    encoderDict['maxval'] = fieldInfo['maxValue']
                                                                # If both min and max were specified, use a non-adaptive encoder
                                                                if ('minValue' in fieldInfo and 'maxValue' in fieldInfo) and (encoderDict['type'] == 'AdaptiveScalarEncoder'):
                                                                    encoderDict['type'] = 'ScalarEncoder'                                                          
                                                                # Defaults may have been over-ridden by specifying an encoder type
                                                                if 'encoderType' in fieldInfo:
                                                                    encoderDict['type'] = fieldInfo['encoderType']
                                                                if 'space' in fieldInfo:
                                                                    encoderDict['space'] = fieldInfo['space']
                                                                encoderDictsList.append(encoderDict)
                                                            # ---------
                                                            # String?
                                                            elif fieldType == 'string':
                                                                encoderDict = dict(type='SDRCategoryEncoder', name=fieldName,fieldname=fieldName, n=100+width, w=width)
                                                                if 'encoderType' in fieldInfo:
                                                                    encoderDict['type'] = fieldInfo['encoderType']
                                                                encoderDictsList.append(encoderDict)
                                                            # ---------
                                                            # Datetime?
                                                            elif fieldType == 'datetime':
                                                                # First, the time of day representation
                                                                encoderDict = dict(type='DateEncoder', name='%s_timeOfDay' % (fieldName),fieldname=fieldName, timeOfDay=(width, 1))
                                                                if 'encoderType' in fieldInfo:
                                                                    encoderDict['type'] = fieldInfo['encoderType']
                                                                encoderDictsList.append(encoderDict)
                                                                # Now, the day of week representation
                                                                encoderDict = dict(type='DateEncoder', name='%s_dayOfWeek' % (fieldName),fieldname=fieldName, dayOfWeek=(width, 1))
                                                                if 'encoderType' in fieldInfo:
                                                                    encoderDict['type'] = fieldInfo['encoderType']
                                                                encoderDictsList.append(encoderDict)
                                                                # Now, the day of week representation
                                                                encoderDict = dict(type='DateEncoder', name='%s_weekend' % (fieldName),fieldname=fieldName, weekend=(width))
                                                                if 'encoderType' in fieldInfo:
                                                                    encoderDict['type'] = fieldInfo['encoderType']
                                                                encoderDictsList.append(encoderDict)
                                                            else:
                                                                raise RuntimeError("Unsupported field type '%s'" % (fieldType))
                                                            # -----------------------------------------------------------------------
                                                            # If this was the predicted field, insert another encoder that sends it to the classifier only
                                                            if fieldName == classifierOnlyField:
                                                                clEncoderDict = dict(encoderDict)
                                                                clEncoderDict['classifierOnly'] = True
                                                                clEncoderDict['name'] = '_classifierInput'
                                                                encoderDictsList.append(clEncoderDict)
                                                                # If the predicted field needs to be excluded, take it out of the encoder lists
                                                                if options["inferenceArgs"]["inputPredictedField"] == "no":
                                                                    encoderDictsList.remove(encoderDict)
                                                        # Remove any encoders not in fixedFields
                                                        if options.get('fixedFields') is not None:
                                                            tempList=[]
                                                            for encoderDict in encoderDictsList:
                                                                if encoderDict['name'] in options['fixedFields']:
                                                                    tempList.append(encoderDict)
                                                            encoderDictsList = tempList
                                                        # ==========================================================================
                                                        # Now generate the encoderSpecsStr and permEncoderChoicesStr strings from 
                                                        #  encoderDictsList and constructorStringList
                                                        encoderSpecsList = []
                                                        permEncoderChoicesList = []
                                                        for encoderDict in encoderDictsList:
                                                            if encoderDict['name'].find('\\') >= 0:
                                                                raise _ExpGeneratorException("Illegal character in field: '\\'")
                                                            # Check for bad characters
                                                            for c in _ILLEGAL_FIELDNAME_CHARACTERS:
                                                                if encoderDict['name'].find(c) >= 0:
                                                                    raise _ExpGeneratorException("Illegal character %s in field %r"  %(c, encoderDict['name']))
                                                            constructorStr = _generatePermEncoderStr(options, encoderDict)
                                                                def _generatePermEncoderStr(options, encoderDict):  ### ExpGenerator.py ###
                                                                    """ Generate the string that defines the permutations to apply for a given encoder. 
                                                                    Parameters:
                                                                    -----------------------------------------------------------------------
                                                                    options: experiment params
                                                                    encoderDict: the encoder dict, which gets placed into the description.py
                                                                    For example, if the encoderDict contains:
                                                                        'consumption': {'clipInput': True,'fieldname': u'consumption','n': 100,'name': u'consumption','type': 'AdaptiveScalarEncoder','w': 21},
                                                                    The return string will contain:
                                                                        "PermuteEncoder(fieldName='consumption', encoderClass='AdaptiveScalarEncoder', w=21, n=PermuteInt(28, 521), clipInput=True)" """
                                                                    permStr = ""
                                                                    # If it's the encoder for the classifier input, then it's always present so put it in as a dict in the permutations.py file instead of a  PermuteEncoder().   
                                                                    if encoderDict.get('classifierOnly', False):
                                                                        permStr = "dict("
                                                                        for key, value in encoderDict.items():
                                                                            if key == "name":
                                                                                continue
                                                                            if key == 'n' and encoderDict['type'] != 'SDRCategoryEncoder':
                                                                                permStr += "n=PermuteInt(%d, %d), " % (encoderDict["w"] + 7,encoderDict["w"] + 500)
                                                                            else:
                                                                                if issubclass(type(value), basestring):
                                                                                    permStr += "%s='%s', " % (key, value)
                                                                                else:
                                                                                    permStr += "%s=%s, " % (key, value)
                                                                        permStr += ")" 
                                                                    else:
                                                                        # Scalar encoders
                                                                        if encoderDict["type"] in ["ScalarSpaceEncoder", "AdaptiveScalarEncoder","ScalarEncoder", "LogEncoder"]:
                                                                            permStr = "PermuteEncoder("
                                                                            for key, value in encoderDict.items():
                                                                                if key == "fieldname":
                                                                                    key = "fieldName"
                                                                                elif key == "type":
                                                                                    key = "encoderClass"
                                                                                elif key == "name":
                                                                                    continue
                                                                                if key == "n":
                                                                                    permStr += "n=PermuteInt(%d, %d), " % (encoderDict["w"] + 1, encoderDict["w"] + 500)
                                                                                elif key == "runDelta":
                                                                                    if value and not "space" in encoderDict:
                                                                                        permStr += "space=PermuteChoices([%s,%s]), " % (_quoteAndEscape("delta"), _quoteAndEscape("absolute"))
                                                                                    encoderDict.pop("runDelta")
                                                                                else:
                                                                                    if issubclass(type(value), basestring):
                                                                                        permStr += "%s='%s', " % (key, value)
                                                                                    else:
                                                                                        permStr += "%s=%s, " % (key, value)
                                                                            permStr += ")"
                                                                        # Category encoder          
                                                                        elif encoderDict["type"] in ["SDRCategoryEncoder"]:
                                                                            permStr = "PermuteEncoder("
                                                                            for key, value in encoderDict.items():
                                                                                if key == "fieldname":
                                                                                    key = "fieldName"
                                                                                elif key == "type":
                                                                                    key = "encoderClass"
                                                                                elif key == "name":
                                                                                    continue          
                                                                                if issubclass(type(value), basestring):
                                                                                    permStr += "%s='%s', " % (key, value)
                                                                                else:
                                                                                    permStr += "%s=%s, " % (key, value)
                                                                            permStr += ")"
                                                                        # Datetime encoder
                                                                        elif encoderDict["type"] in ["DateEncoder"]:
                                                                            permStr = "PermuteEncoder("
                                                                            for key, value in encoderDict.items():
                                                                                if key == "fieldname":
                                                                                    key = "fieldName"
                                                                                elif key == "type":
                                                                                    continue
                                                                                elif key == "name":
                                                                                    continue
                                                                                if key == "timeOfDay":
                                                                                    permStr += "encoderClass='%s.timeOfDay', " % (encoderDict["type"])
                                                                                    permStr += "radius=PermuteFloat(0.5, 12), "
                                                                                    permStr += "w=%d, " % (value[0])
                                                                                elif key == "dayOfWeek":
                                                                                    permStr += "encoderClass='%s.dayOfWeek', " % (encoderDict["type"])
                                                                                    permStr += "radius=PermuteFloat(1, 6), "
                                                                                    permStr += "w=%d, " % (value[0])
                                                                                elif key == "weekend":
                                                                                    permStr += "encoderClass='%s.weekend', " % (encoderDict["type"])
                                                                                    permStr += "radius=PermuteChoices([1]),  "
                                                                                    permStr += "w=%d, " % (value)
                                                                                else:
                                                                                    if issubclass(type(value), basestring):
                                                                                        permStr += "%s='%s', " % (key, value)
                                                                                    else:
                                                                                        permStr += "%s=%s, " % (key, value)
                                                                            permStr += ")"
                                                                        else:
                                                                            raise RuntimeError("Unsupported encoder type '%s'" % (encoderDict["type"]))
                                                                      
                                                                  return permStr
                                                            encoderKey = _quoteAndEscape(encoderDict['name'])
                                                            encoderSpecsList.append("%s: %s%s" % (encoderKey,2*_ONE_INDENT,pprint.pformat(encoderDict, indent=2*_INDENT_STEP)))
                                                            # Each permEncoderChoicesStr is of the form:
                                                            #  PermuteEncoder('gym', 'SDRCategoryEncoder', w=7, n=100),
                                                            permEncoderChoicesList.append("%s: %s," % (encoderKey, constructorStr))
                                                        # Join into strings
                                                        encoderSpecsStr = ',\n  '.join(encoderSpecsList)
                                                        permEncoderChoicesStr = '\n'.join(permEncoderChoicesList)
                                                        permEncoderChoicesStr = _indentLines(permEncoderChoicesStr, 1,indentFirstLine=True)
                                                        # Return results
                                                        return (encoderSpecsStr, permEncoderChoicesStr)
                                            else:
                                                raise RuntimeError("Unsupported hsVersion of %s" % (hsVersion))
                                            #--------------------------------------------------------------------------
                                            # Generate the string containing the sensor auto-reset dict.
                                            if options['resetPeriod'] is not None:
                                                sensorAutoResetStr = pprint.pformat(options['resetPeriod'],indent=2*_INDENT_STEP)
                                            else:
                                                sensorAutoResetStr = 'None'
                                            #--------------------------------------------------------------------------
                                            # Generate the string containing the aggregation settings.
                                            aggregationPeriod = {'days': 0,'hours': 0,'microseconds': 0,'milliseconds': 0,'minutes': 0,'months': 0,'seconds': 0,'weeks': 0,'years': 0,}
                                            # Honor any overrides provided in the stream definition
                                            aggFunctionsDict = {}
                                            if 'aggregation' in options['streamDef']:
                                                for key in aggregationPeriod.keys():
                                                    if key in options['streamDef']['aggregation']:
                                                        aggregationPeriod[key] = options['streamDef']['aggregation'][key]
                                                if 'fields' in options['streamDef']['aggregation']:
                                                    for (fieldName, func) in options['streamDef']['aggregation']['fields']:
                                                        aggFunctionsDict[fieldName] = str(func)
                                            # Do we have any aggregation at all?
                                            hasAggregation = False
                                            for v in aggregationPeriod.values():
                                                if v != 0:
                                                    hasAggregation = True
                                                    break
                                            # Convert the aggFunctionsDict to a list
                                            aggFunctionList = aggFunctionsDict.items()
                                            aggregationInfo = dict(aggregationPeriod)
                                            aggregationInfo['fields'] = aggFunctionList
                                            # Form the aggregation strings
                                            aggregationInfoStr = "%s" % (pprint.pformat(aggregationInfo,indent=2*_INDENT_STEP))
                                            # -----------------------------------------------------------------------
                                            # Generate the string defining the dataset. This is basically the
                                            #  streamDef, but referencing the aggregation we already pulled out into the
                                            #  config dict (which enables permuting over it)
                                            datasetSpec = options['streamDef']
                                            if 'aggregation' in datasetSpec:
                                                datasetSpec.pop('aggregation')
                                            if hasAggregation:
                                                datasetSpec['aggregation'] = '$SUBSTITUTE'
                                            datasetSpecStr = pprint.pformat(datasetSpec, indent=2*_INDENT_STEP)
                                            datasetSpecStr = datasetSpecStr.replace("'$SUBSTITUTE'", "config['aggregationInfo']")
                                            datasetSpecStr = _indentLines(datasetSpecStr, 2, indentFirstLine=False)
                                            # -----------------------------------------------------------------------
                                            # Was computeInterval specified with Multistep prediction? If so, this swarm should permute over different aggregations
                                            computeInterval = options['computeInterval']
                                            if computeInterval is not None and options['inferenceType'] in ['NontemporalMultiStep','TemporalMultiStep','MultiStep']:
                                                # Compute the predictAheadTime based on the minAggregation (specified in the stream definition) and the number of prediction steps
                                                predictionSteps = options['inferenceArgs'].get('predictionSteps', [1])
                                                if len(predictionSteps) > 1:
                                                    raise _InvalidCommandArgException("Invalid predictionSteps: %s. When computeInterval is specified, there can only be one stepSize in predictionSteps." % predictionSteps)
                                                if max(aggregationInfo.values()) == 0:
                                                    raise _InvalidCommandArgException("Missing or nil stream aggregation: When computeInterval is specified, then the stream aggregation interval must be non-zero.")
                                                # Compute the predictAheadTime
                                                numSteps = predictionSteps[0]
                                                predictAheadTime = dict(aggregationPeriod)
                                                for key in predictAheadTime.iterkeys():
                                                    predictAheadTime[key] *= numSteps
                                                predictAheadTimeStr = pprint.pformat(predictAheadTime,indent=2*_INDENT_STEP)
                                                # This tells us to plug in a wildcard string for the prediction steps that we use in other parts of the description file (metrics, inferenceArgs, etc.)
                                                options['dynamicPredictionSteps'] = True
                                            else:
                                                options['dynamicPredictionSteps'] = False
                                                predictAheadTimeStr = "None"
                                            # -----------------------------------------------------------------------
                                            # Save environment-common token substitutions
                                            tokenReplacements['\$EXP_GENERATOR_PROGRAM_PATH'] = _quoteAndEscape(os.path.abspath(__file__))
                                            # If the "uber" metric 'MultiStep' was specified, then plug in TemporalMultiStep by default
                                            inferenceType = options['inferenceType']
                                            if inferenceType == 'MultiStep':
                                                inferenceType = InferenceType.TemporalMultiStep
                                            tokenReplacements['\$INFERENCE_TYPE'] = "'%s'" % inferenceType
                                            # Nontemporal classificaion uses only encoder and classifier
                                            if inferenceType == InferenceType.NontemporalClassification:
                                                tokenReplacements['\$SP_ENABLE'] = "False"
                                                tokenReplacements['\$TP_ENABLE'] = "False"
                                            else:
                                                tokenReplacements['\$SP_ENABLE'] = "True"
                                                tokenReplacements['\$TP_ENABLE'] = "True"
                                                tokenReplacements['\$CLA_CLASSIFIER_IMPL'] = ""
                                            tokenReplacements['\$ANOMALY_PARAMS'] = pprint.pformat(options['anomalyParams'], indent=2*_INDENT_STEP)
                                            tokenReplacements['\$ENCODER_SPECS'] = encoderSpecsStr
                                            tokenReplacements['\$SENSOR_AUTO_RESET'] = sensorAutoResetStr
                                            tokenReplacements['\$AGGREGATION_INFO'] = aggregationInfoStr
                                            tokenReplacements['\$DATASET_SPEC'] = datasetSpecStr
                                            if options['iterationCount'] is None:
                                                options['iterationCount'] = -1
                                            tokenReplacements['\$ITERATION_COUNT'] = str(options['iterationCount'])
                                            tokenReplacements['\$SP_POOL_PCT'] = str(options['spCoincInputPoolPct'])
                                            tokenReplacements['\$HS_MIN_PARTICLES'] = str(options['minParticlesPerSwarm'])
                                            tokenReplacements['\$SP_PERM_CONNECTED'] = str(options['spSynPermConnected'])
                                            tokenReplacements['\$FIELD_PERMUTATION_LIMIT'] = str(options['fieldPermutationLimit'])
                                            tokenReplacements['\$PERM_ENCODER_CHOICES'] = permEncoderChoicesStr
                                            predictionSteps = options['inferenceArgs'].get('predictionSteps', [1])
                                            predictionStepsStr = ','.join([str(x) for x in predictionSteps])
                                            tokenReplacements['\$PREDICTION_STEPS'] = "'%s'" % (predictionStepsStr)
                                            tokenReplacements['\$PREDICT_AHEAD_TIME'] = predictAheadTimeStr
                                            # Option permuting over SP synapse decrement value
                                            tokenReplacements['\$PERM_SP_CHOICES'] = ""
                                            if options['spPermuteDecrement'] and options['inferenceType'] != 'NontemporalClassification': 
                                                tokenReplacements['\$PERM_SP_CHOICES'] = _ONE_INDENT +"'synPermInactiveDec': PermuteFloat(0.0003, 0.1),\n"
                                            # The TP permutation parameters are not required for non-temporal networks
                                            if options['inferenceType'] in ['NontemporalMultiStep','NontemporalClassification']:
                                                tokenReplacements['\$PERM_TP_CHOICES'] = ""
                                            else:
                                                tokenReplacements['\$PERM_TP_CHOICES'] = "  'activationThreshold': PermuteInt(12, 16),\n" + "  'minThreshold': PermuteInt(9, 12),\n" + "  'pamLength': PermuteInt(1, 5),\n"
                                            # If the inference type is just the generic 'MultiStep', then permute over temporal/nonTemporal multistep
                                            if options['inferenceType'] == 'MultiStep':
                                                tokenReplacements['\$PERM_INFERENCE_TYPE_CHOICES'] = "  'inferenceType': PermuteChoices(['NontemporalMultiStep', " + "'TemporalMultiStep']),"
                                            else:
                                                tokenReplacements['\$PERM_INFERENCE_TYPE_CHOICES'] = ""
                                          # The Classifier permutation parameters are only required for Multi-step inference types
                                            if options['inferenceType'] in ['NontemporalMultiStep', 'TemporalMultiStep','MultiStep', 'TemporalAnomaly', 'NontemporalClassification']:
                                                tokenReplacements['\$PERM_CL_CHOICES'] = "  'alpha': PermuteFloat(0.0001, 0.1),\n"
                                            else:
                                                tokenReplacements['\$PERM_CL_CHOICES'] = ""
                                            # The Permutations alwaysIncludePredictedField setting. * When the experiment description has 'inputPredictedField' set to 'no', we  simply do not put in an encoder for the predicted field.  * When 'inputPredictedField' is set to 'auto', we include an encoder for the #   predicted field and swarming tries it out just like all the other fields. * When 'inputPredictedField' is set to 'yes', we include this setting in  the permutations file which informs swarming to always use the  predicted field (the first swarm will be the predicted field only) 
                                            tokenReplacements['\$PERM_ALWAYS_INCLUDE_PREDICTED_FIELD'] = "inputPredictedField = '%s'" % (options["inferenceArgs"]["inputPredictedField"])  
                                            # The Permutations minFieldContribution setting
                                            if options.get('minFieldContribution', None) is not None:
                                                tokenReplacements['\$PERM_MIN_FIELD_CONTRIBUTION'] = "minFieldContribution = %d" % (options['minFieldContribution']) 
                                            else:
                                                tokenReplacements['\$PERM_MIN_FIELD_CONTRIBUTION'] = ""
                                            # The Permutations killUselessSwarms setting
                                            if options.get('killUselessSwarms', None) is not None:
                                                tokenReplacements['\$PERM_KILL_USELESS_SWARMS'] = "killUselessSwarms = %r" % (options['killUselessSwarms']) 
                                            else:
                                                tokenReplacements['\$PERM_KILL_USELESS_SWARMS'] = ""
                                            # The Permutations maxFieldBranching setting
                                            if options.get('maxFieldBranching', None) is not None:
                                                tokenReplacements['\$PERM_MAX_FIELD_BRANCHING'] = "maxFieldBranching = %r" % (options['maxFieldBranching']) 
                                            else:
                                                tokenReplacements['\$PERM_MAX_FIELD_BRANCHING'] = ""
                                            # The Permutations tryAll3FieldCombinations setting
                                            if options.get('tryAll3FieldCombinations', None) is not None:
                                                tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS'] = "tryAll3FieldCombinations = %r" % (options['tryAll3FieldCombinations']) 
                                            else:
                                                tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS'] = ""
                                            # The Permutations tryAll3FieldCombinationsWTimestamps setting
                                            if options.get('tryAll3FieldCombinationsWTimestamps', None) is not None:
                                                tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS_W_TIMESTAMPS'] = "tryAll3FieldCombinationsWTimestamps = %r" % (options['tryAll3FieldCombinationsWTimestamps']) 
                                            else:
                                                tokenReplacements['\$PERM_TRY_ALL_3_FIELD_COMBINATIONS_W_TIMESTAMPS'] = ""
                                            # The Permutations fieldFields setting
                                            if options.get('fixedFields', None) is not None:
                                                tokenReplacements['\$PERM_FIXED_FIELDS'] = "fixedFields = %r" % (options['fixedFields']) 
                                            else:
                                                tokenReplacements['\$PERM_FIXED_FIELDS'] = ""
                                            # The Permutations fastSwarmModelParams setting
                                            if options.get('fastSwarmModelParams', None) is not None:
                                                tokenReplacements['\$PERM_FAST_SWARM_MODEL_PARAMS'] = "fastSwarmModelParams = %r" % (options['fastSwarmModelParams']) 
                                            else:
                                                tokenReplacements['\$PERM_FAST_SWARM_MODEL_PARAMS'] = ""
                                            # The Permutations maxModels setting
                                            if options.get('maxModels', None) is not None:
                                                tokenReplacements['\$PERM_MAX_MODELS'] = "maxModels = %r" % (options['maxModels']) 
                                            else:
                                                tokenReplacements['\$PERM_MAX_MODELS'] = ""
                                            # --------------------------------------------------------------------------
                                            # The Aggregation choices have to be determined when we are permuting over aggregations.
                                            if options['dynamicPredictionSteps']:
                                                debugAgg = True
                                                # First, we need to error check to insure that computeInterval is an integer
                                                #  multiple of minAggregation (aggregationPeriod)
                                                quotient = aggregationDivide(computeInterval, aggregationPeriod)
                                                (isInt, multiple) = _isInt(quotient)
                                                if not isInt or multiple < 1:
                                                    raise _InvalidCommandArgException("Invalid computeInterval: %s. computeInterval must be an integer multiple of the stream aggregation (%s)." % (computeInterval, aggregationPeriod))
                                                # The valid aggregation choices are governed by the following constraint,
                                                #   1.) (minAggregation * N) * M = predictAheadTime
                                                #       (minAggregation * N) * M = maxPredictionSteps * minAggregation 
                                                #       N * M = maxPredictionSteps
                                                #   2.) computeInterval = K * aggregation
                                                #       computeInterval = K * (minAggregation * N)
                                                # where: aggregation = minAggregation * N
                                                #        K, M and N are integers >= 1
                                                #          N = aggregation / minAggregation
                                                #          M = predictionSteps, for a particular aggregation
                                                #          K = number of predictions within each compute interval
                                                # Let's build up a a list of the possible N's that satisfy the N * M = maxPredictionSteps constraint
                                                mTimesN = float(predictionSteps[0])
                                                possibleNs = []
                                                for n in xrange(1, int(mTimesN)+1):
                                                    m = mTimesN / n
                                                    mInt = int(round(m))
                                                    if mInt < 1:
                                                        break
                                                    if abs(m - mInt) > 0.0001 * m:
                                                        continue
                                                    possibleNs.append(n)
                                                if debugAgg:
                                                    print "All integer factors of %d are: %s" % (mTimesN, possibleNs)
                                                # Now go through and throw out any N's that don't satisfy the constraint: computeInterval = K * (minAggregation * N)
                                                aggChoices = []
                                                for n in possibleNs:
                                                    # Compute minAggregation * N
                                                    agg = dict(aggregationPeriod)
                                                    for key in agg.iterkeys():
                                                        agg[key] *= n
                                                    # Make sure computeInterval is an integer multiple of the aggregation period
                                                    quotient = aggregationDivide(computeInterval, agg)
                                                    #print computeInterval, agg
                                                    #print quotient
                                                    #import sys; sys.exit()
                                                    (isInt, multiple) = _isInt(quotient)
                                                    if not isInt or multiple < 1:
                                                        continue
                                                    aggChoices.append(agg)
                                                # Only eveluate up to 5 different aggregations
                                                aggChoices = aggChoices[-5:]
                                                if debugAgg:
                                                    print "Aggregation choices that will be evaluted during swarming:"
                                                    for agg in aggChoices:
                                                        print "  ==>", agg
                                                    print
                                                tokenReplacements['\$PERM_AGGREGATION_CHOICES'] = ("PermuteChoices(%s)" % (pprint.pformat(aggChoices, indent=2*_INDENT_STEP)))
                                            else:
                                                tokenReplacements['\$PERM_AGGREGATION_CHOICES'] = aggregationInfoStr
                                            # Generate the inferenceArgs replacement tokens
                                            _generateInferenceArgs(options, tokenReplacements)
                                                def _generateInferenceArgs(options, tokenReplacements):     ### ExpGenerator.py ###
                                                    """ Generates the token substitutions related to the predicted field and the supplemental arguments for prediction"""
                                                    inferenceType = options['inferenceType']
                                                    optionInferenceArgs = options.get('inferenceArgs', None)
                                                    resultInferenceArgs = {}
                                                    predictedField = _getPredictedField(options)[0]
                                                        def _getPredictedField(options):     ### ExpGenerator.py ###
                                                            """ Gets the predicted field and it's datatype from the options dictionary
                                                            Returns: (predictedFieldName, predictedFieldType)"""
                                                            if not options['inferenceArgs'] or not options['inferenceArgs']['predictedField']:
                                                                return None, None
                                                            predictedField = options['inferenceArgs']['predictedField']
                                                            predictedFieldInfo = None
                                                            includedFields = options['includedFields']
                                                            for info in includedFields:
                                                                if info['fieldName'] == predictedField:
                                                                    predictedFieldInfo = info
                                                                    break
                                                            if predictedFieldInfo is None:
                                                                raise ValueError("Predicted field '%s' does not exist in included fields." % predictedField)
                                                            predictedFieldType = predictedFieldInfo['fieldType']
                                                            return predictedField, predictedFieldType
                                                    if inferenceType in (InferenceType.TemporalNextStep,InferenceType.TemporalAnomaly):
                                                        assert predictedField,  "Inference Type '%s' needs a predictedField specified in the inferenceArgs dictionary" % inferenceType
                                                    if optionInferenceArgs:
                                                        # If we will be using a dynamically created predictionSteps, plug in that variable name in place of the constant scalar value
                                                        if options['dynamicPredictionSteps']:
                                                            altOptionInferenceArgs = copy.deepcopy(optionInferenceArgs)
                                                            altOptionInferenceArgs['predictionSteps'] = '$REPLACE_ME'
                                                            resultInferenceArgs = pprint.pformat(altOptionInferenceArgs)
                                                            resultInferenceArgs = resultInferenceArgs.replace("'$REPLACE_ME'",'[predictionSteps]')
                                                        else:
                                                            resultInferenceArgs = pprint.pformat(optionInferenceArgs)
                                                    tokenReplacements['\$INFERENCE_ARGS'] = resultInferenceArgs
                                                    tokenReplacements['\$PREDICTION_FIELD'] = predictedField
                                            # Generate the metric replacement tokens
                                            _generateMetricsSubstitutions(options, tokenReplacements)
                                                def _generateMetricsSubstitutions(options, tokenReplacements):     ### ExpGenerator.py ###
                                                    """Generate the token substitution for metrics related fields.
                                                    This includes:
                                                        \$METRICS
                                                        \$LOGGED_METRICS
                                                        \$PERM_OPTIMIZE_SETTING"""
                                                    # -----------------------------------------------------------------------
                                                    #
                                                    options['loggedMetrics'] = [".*"]
                                                    # -----------------------------------------------------------------------
                                                    # Generate the required metrics
                                                    metricList, optimizeMetricLabel = _generateMetricSpecs(options)
                                                        def _generateMetricSpecs(options):     ### ExpGenerator.py ###
                                                            """ Generates the Metrics for a given InferenceType
                                                            Parameters:
                                                            -------------------------------------------------------------------------
                                                            options: ExpGenerator options
                                                            retval: (metricsList, optimizeMetricLabel)
                                                                metricsList: list of metric string names
                                                                optimizeMetricLabel: Name of the metric which to optimize over"""
                                                            inferenceType = options['inferenceType']
                                                            inferenceArgs = options['inferenceArgs']
                                                            predictionSteps = inferenceArgs['predictionSteps']
                                                            metricWindow = options['metricWindow']
                                                            if metricWindow is None:
                                                                metricWindow = int(Configuration.get("nupic.opf.metricWindow"))
                                                            metricSpecStrings = []
                                                            optimizeMetricLabel = ""
                                                            # -----------------------------------------------------------------------
                                                            # Generate the metrics specified by the expGenerator paramters
                                                            metricSpecStrings.extend(_generateExtraMetricSpecs(options))
                                                                def _generateExtraMetricSpecs(options):     ### ExpGenerator.py ###
                                                                    """Generates the non-default metrics specified by the expGenerator params """
                                                                    global _metricSpecSchema
                                                                    results = []
                                                                    for metric in options['metrics']:
                                                                        for propertyName in _metricSpecSchema['properties'].keys():
                                                                            _getPropertyValue(_metricSpecSchema, propertyName, metric)
                                                                        specString, label = _generateMetricSpecString(field=metric['field'],metric=metric['metric'],params=metric['params'],inferenceElement=metric['inferenceElement'],returnLabel=True)
                                                                            def _generateMetricSpecString(inferenceElement, metric,params=None, field=None,returnLabel=False):     ### ExpGenerator.py ###
                                                                                """ Generates the string representation of a MetricSpec object, and returns the metric key associated with the metric.
                                                                                Parameters:
                                                                                -----------------------------------------------------------------------
                                                                                inferenceElement:An InferenceElement value that indicates which part of the inference thismetric is computed on
                                                                                metric:The type of the metric being computed (e.g. aae, avg_error)
                                                                                params:A dictionary of parameters for the metric. The keys are the parameter names and the values should be the parameter values (e.g. window=200)
                                                                                field:The name of the field for which this metric is being computed
                                                                                returnLabel:If True, returns the label of the MetricSpec that was generated"""
                                                                                metricSpecArgs = dict(metric=metric,field=field,params=params,inferenceElement=inferenceElement)
                                                                                metricSpecAsString = "MetricSpec(%s)" % ', '.join(['%s=%r' % (item[0],item[1])for item in metricSpecArgs.iteritems()])
                                                                                if not returnLabel:
                                                                                    return metricSpecAsString
                                                                                spec = MetricSpec(**metricSpecArgs)
                                                                                metricLabel = spec.getLabel()
                                                                                return metricSpecAsString, metricLabel
                                                                        if metric['logged']:
                                                                            options['loggedMetrics'].append(label)
                                                                        results.append(specString)
                                                                    return results
                                                            # -----------------------------------------------------------------------
                                                            optimizeMetricSpec = None
                                                            # If using a dynamically computed prediction steps (i.e. when swarming over aggregation is requested), then we will plug in the variable predictionSteps in place of the statically provided predictionSteps from the JSON description.
                                                            if options['dynamicPredictionSteps']:
                                                                assert len(predictionSteps) == 1
                                                                predictionSteps = ['$REPLACE_ME']
                                                            # -----------------------------------------------------------------------
                                                            # Metrics for temporal prediction
                                                            if inferenceType in (InferenceType.TemporalNextStep,InferenceType.TemporalAnomaly,InferenceType.TemporalMultiStep,InferenceType.NontemporalMultiStep,InferenceType.NontemporalClassification,'MultiStep'):
                                                                predictedFieldName, predictedFieldType = _getPredictedField(options)
                                                                isCategory = _isCategory(predictedFieldType)
                                                                    def _isCategory(fieldType):    ### ExpGenerator.py ###
                                                                        """Prediction function for determining whether a function is a categorical variable or a scalar variable.  Mainly used for determining the appropriate metrics."""
                                                                        if fieldType == 'string':
                                                                            return True
                                                                        if fieldType == 'int' or fieldType=='float':
                                                                            return False
                                                                metricNames = ('avg_err',) if isCategory else ('aae', 'altMAPE')
                                                                trivialErrorMetric = 'avg_err' if isCategory else 'altMAPE'
                                                                oneGramErrorMetric = 'avg_err' if isCategory else 'altMAPE'
                                                                movingAverageBaselineName = 'moving_mode' if isCategory else 'moving_mean'
                                                                # Multi-step metrics
                                                                for metricName in metricNames:
                                                                    metricSpec, metricLabel = _generateMetricSpecString(field=predictedFieldName,inferenceElement=InferenceElement.multiStepBestPredictions,metric='multiStep',params={'errorMetric': metricName,'window':metricWindow,'steps': predictionSteps},returnLabel=True)
                                                                    metricSpecStrings.append(metricSpec)
                                                                # If the custom error metric was specified, add that
                                                                if options["customErrorMetric"] is not None :
                                                                    metricParams = dict(options["customErrorMetric"])
                                                                    metricParams['errorMetric'] = 'custom_error_metric'
                                                                    metricParams['steps'] = predictionSteps
                                                                    # If errorWindow is not specified, make it equal to the default window
                                                                    if not "errorWindow" in metricParams:
                                                                        metricParams["errorWindow"] = metricWindow
                                                                    metricSpec, metricLabel =_generateMetricSpecString(field=predictedFieldName,inferenceElement=InferenceElement.multiStepPredictions,metric="multiStep",params=metricParams,returnLabel=True)
                                                                    metricSpecStrings.append(metricSpec)
                                                                # If this is the first specified step size, optimize for it. Be sure to escape special characters since this is a regular expression
                                                                optimizeMetricSpec = metricSpec
                                                                metricLabel = metricLabel.replace('[', '\\[')
                                                                metricLabel = metricLabel.replace(']', '\\]')
                                                                optimizeMetricLabel = metricLabel
                                                                if options["customErrorMetric"] is not None :
                                                                    optimizeMetricLabel = ".*custom_error_metric.*"
                                                                # Add in the trivial metrics
                                                                if options["runBaselines"] and inferenceType != InferenceType.NontemporalClassification:
                                                                    for steps in predictionSteps:
                                                                        metricSpecStrings.append(_generateMetricSpecString(field=predictedFieldName,inferenceElement=InferenceElement.prediction,metric="trivial",params={'window':metricWindow,"errorMetric":trivialErrorMetric,'steps': steps}))
                                                                        ##Add in the One-Gram baseline error metric
                                                                        #metricSpecStrings.append(_generateMetricSpecString(field=predictedFieldName,inferenceElement=InferenceElement.encodings,metric="two_gram",params={'window':metricWindow,"errorMetric":oneGramErrorMetric,'predictionField':predictedFieldName,'steps': steps}))
                                                                        #Include the baseline moving mean/mode metric
                                                                        if isCategory:
                                                                            metricSpecStrings.append(_generateMetricSpecString(field=predictedFieldName,inferenceElement=InferenceElement.prediction,metric=movingAverageBaselineName,params={'window':metricWindow,"errorMetric":"avg_err","steps": steps}))
                                                                        else :
                                                                            metricSpecStrings.append(_generateMetricSpecString(field=predictedFieldName,inferenceElement=InferenceElement.prediction,metric=movingAverageBaselineName,params={'window':metricWindow,"errorMetric":"altMAPE","mean_window":200,"steps": steps}))
                                                            # -----------------------------------------------------------------------
                                                            # Metrics for classification
                                                            elif inferenceType in (InferenceType.TemporalClassification):
                                                                metricName = 'avg_err'
                                                                trivialErrorMetric = 'avg_err'
                                                                oneGramErrorMetric = 'avg_err'
                                                                movingAverageBaselineName = 'moving_mode'
                                                                optimizeMetricSpec, optimizeMetricLabel = _generateMetricSpecString(inferenceElement=InferenceElement.classification,metric=metricName,params={'window':metricWindow},returnLabel=True)
                                                                metricSpecStrings.append(optimizeMetricSpec)
                                                                if options["runBaselines"]:
                                                                    # If temporal, generate the trivial predictor metric
                                                                    if inferenceType == InferenceType.TemporalClassification:
                                                                        metricSpecStrings.append(_generateMetricSpecString(inferenceElement=InferenceElement.classification,metric="trivial",params={'window':metricWindow,"errorMetric":trivialErrorMetric}))
                                                                        metricSpecStrings.append(_generateMetricSpecString(inferenceElement=InferenceElement.classification,metric="two_gram",params={'window':metricWindow,"errorMetric":oneGramErrorMetric}))
                                                                        metricSpecStrings.append(_generateMetricSpecString(inferenceElement=InferenceElement.classification,metric=movingAverageBaselineName,params={'window':metricWindow,"errorMetric":"avg_err","mode_window":200}))
                                                                # Custom Error Metric
                                                                if not options["customErrorMetric"] == None :
                                                                    #If errorWindow is not specified, make it equal to the default window
                                                                    if not "errorWindow" in options["customErrorMetric"]:
                                                                        options["customErrorMetric"]["errorWindow"] = metricWindow
                                                                    optimizeMetricSpec = _generateMetricSpecString(inferenceElement=InferenceElement.classification,metric="custom",params=options["customErrorMetric"])
                                                                    optimizeMetricLabel = ".*custom_error_metric.*"  
                                                                    metricSpecStrings.append(optimizeMetricSpec)
                                                            # -----------------------------------------------------------------------
                                                            # If plug in the predictionSteps variable for any dynamically generated prediction steps
                                                            if options['dynamicPredictionSteps']:
                                                                for i in range(len(metricSpecStrings)):
                                                                    metricSpecStrings[i] = metricSpecStrings[i].replace("'$REPLACE_ME'", "predictionSteps")
                                                                optimizeMetricLabel = optimizeMetricLabel.replace("'$REPLACE_ME'", ".*")
                                                            return metricSpecStrings, optimizeMetricLabel
                                                    metricListString = ",\n".join(metricList)
                                                    metricListString = _indentLines(metricListString, 2, indentFirstLine=False)
                                                    permOptimizeSettingStr = 'minimize = "%s"' % optimizeMetricLabel
                                                    # -----------------------------------------------------------------------
                                                    # Specify which metrics should be logged
                                                    loggedMetricsListAsStr = "[%s]" % (", ".join(["'%s'"% ptrn for ptrn in options['loggedMetrics']]))
                                                    tokenReplacements['\$LOGGED_METRICS'] = loggedMetricsListAsStr
                                                    tokenReplacements['\$METRICS'] = metricListString
                                                    tokenReplacements['\$PERM_OPTIMIZE_SETTING'] = permOptimizeSettingStr
                                            # -----------------------------------------------------------------------
                                            # Generate Control dictionary
                                            environment = options['environment']
                                            if environment == OpfEnvironment.Nupic:
                                                tokenReplacements['\$ENVIRONMENT'] = "'%s'"%OpfEnvironment.Nupic
                                                controlTemplate = "nupicEnvironmentTemplate.tpl"
                                            elif environment == OpfEnvironment.Experiment:
                                                tokenReplacements['\$ENVIRONMENT'] = "'%s'"%OpfEnvironment.Experiment
                                                controlTemplate = "opfExperimentTemplate.tpl"
                                            else:
                                                raise _InvalidCommandArgException("Invalid environment type %s"% environment)
                                            # -----------------------------------------------------------------------
                                            if outputDirPath is None:
                                                outputDirPath = tempfile.mkdtemp()
                                            if not os.path.exists(outputDirPath):
                                                os.makedirs(outputDirPath)
                                            print "Generating experiment files in directory: %s..." % (outputDirPath)
                                            descriptionPyPath = os.path.join(outputDirPath, "description.py")
                                            _generateFileFromTemplates([claDescriptionTemplateFile, controlTemplate],descriptionPyPath,tokenReplacements)
                                                def _generateFileFromTemplates(templateFileNames, outputFilePath,replacementDict):    ### ExpGenerator.py ###
                                                    """ Generates a file by applying token replacements to the given template file
                                                    templateFileName: A list of template file names; these files are assumed to be in the same directory as the running ExpGenerator.py script. ExpGenerator will perform the substitution and concanetate the files in the order they are specified
                                                    outputFilePath: Absolute path of the output file
                                                    replacementDict:A dictionary of token/replacement pairs"""
                                                    # Find out where we're running from so we know where to find templates
                                                    installPath = os.path.dirname(__file__)
                                                    outputFile = open(outputFilePath, "w")
                                                    outputLines = []
                                                    inputLines = []
                                                    firstFile = True
                                                    for templateFileName in templateFileNames:
                                                        # Separate lines from each file by two blank lines.
                                                        if not firstFile:
                                                            inputLines.extend([os.linesep]*2)
                                                        firstFile = False
                                                        inputFilePath = os.path.join(installPath, templateFileName)
                                                        inputFile = open(inputFilePath)
                                                        inputLines.extend(inputFile.readlines())
                                                        inputFile.close()
                                                    print "Writing ", len(inputLines), "lines..."
                                                    for line in inputLines:
                                                        tempLine = line
                                                        # Enumerate through each key in replacementDict and replace with value
                                                        for k, v in replacementDict.iteritems():
                                                            if v is None:
                                                                v = "None"
                                                            tempLine = re.sub(k, v, tempLine)
                                                        outputFile.write(tempLine)
                                                    outputFile.close()
                                            permutationsPyPath = os.path.join(outputDirPath, "permutations.py")
                                            if hsVersion == 'v1':
                                                _generateFileFromTemplates(['permutationsTemplateV1.tpl'],permutationsPyPath,tokenReplacements)
                                            elif hsVersion == 'ensemble':
                                                _generateFileFromTemplates(['permutationsTemplateEnsemble.tpl'],permutationsPyPath,tokenReplacements)
                                            elif hsVersion == 'v2':
                                                _generateFileFromTemplates(['permutationsTemplateV2.tpl'],permutationsPyPath,tokenReplacements)
                                            else:
                                                raise(ValueError("This permutation version is not supported yet: %s" %hsVersion))
                                            print "done."
                                    pprint.pprint(filesDescription)
                                    return
                        elif options.descriptionFromFile:
                            _handleDescriptionFromFileOption(options.descriptionFromFile, options.outDir, parser.get_usage(), hsVersion=options.version, claDescriptionTemplateFile = options.claDescriptionTemplateFile)
                                def _handleDescriptionFromFileOption(filename, outDir, usageStr, hsVersion,claDescriptionTemplateFile):    ### ExpGenerator.py ###
                                    """Parses and validates the --descriptionFromFile option and executes the request
                                    Parameters:
                                    -----------------------------------------------------------------------
                                    filename:   File from which we'll extract description JSON
                                    outDir:     where to place generated experiment files
                                    usageStr:   program usage string
                                    hsVersion:  which version of hypersearch permutations file to generate, can be 'v1' or 'v2'
                                    claDescriptionTemplateFile: Filename containing the template description
                                    retval:     nothing """
                                    try:
                                        fileHandle = open(filename, 'r')
                                        JSONStringFromFile = fileHandle.read().splitlines()
                                        JSONStringFromFile = ''.join(JSONStringFromFile)
                                    except Exception, e:
                                        raise _InvalidCommandArgException(_makeUsageErrorStr(("File open failed for --descriptionFromFile: %s\n" + "ARG=<%s>") % (str(e), filename), usageStr))
                                      _handleDescriptionOption(JSONStringFromFile, outDir, usageStr,hsVersion=hsVersion,claDescriptionTemplateFile = claDescriptionTemplateFile)
                                    return
                        else:
                            raise _InvalidCommandArgException(_makeUsageErrorStr("Error in validating command options. No option provided:\n", parser.get_usage()))
        options["expDescConfig"] = swarmConfig
        options["outputLabel"] = outputLabel
        options["outDir"] = outDir
        options["permWorkDir"] = permWorkDir
        runOptions = _injectDefaultOptions(options)
            def _injectDefaultOptions(options):    ### permutations_runner.py ###
                return dict(DEFAULT_OPTIONS, **options)
        _validateOptions(runOptions)
            def _validateOptions(options):    ### permutations_runner.py ###
                if "expDescJsonPath" not in options and "expDescConfig" not in options and "permutationsScriptPath" not in options:
                    raise Exception("Options must contain one of the following: expDescJsonPath, expDescConfig, or permutationsScriptPath.")
        return _runAction(runOptions)
            def _runAction(runOptions):  ### permutations_runner.py ###
                if not os.path.exists(runOptions["outDir"]):
                    os.makedirs(runOptions["outDir"])
                if not os.path.exists(runOptions["permWorkDir"]):
                    os.makedirs(runOptions["permWorkDir"])
                action = runOptions["action"]
                # Print Nupic HyperSearch results from the current or last run
                if action == "report":
                    returnValue = _HyperSearchRunner.generateReport(options=runOptions, replaceReport=runOptions["replaceReport"], hyperSearchJob=None, metricsKeys=None)
                        def generateReport(cls,options,replaceReport,hyperSearchJob,metricsKeys):    ### permutations_runner.py ###
                            """Prints all available results in the given HyperSearch job and emits model information to the permutations report csv.
                            The job may be completed or still in progress.
                            Parameters:
                            ----------------------------------------------------------------------
                            options:        NupicRunPermutations options dict
                            replaceReport:  True to replace existing report csv, if any; False to append to existing report csv, if any
                            hyperSearchJob: _HyperSearchJob instance; if None, will get it from saved jobID, if any
                            metricsKeys:    sequence of report metrics key names to include in report; if None, will pre-scan all modelInfos to generate a complete list of metrics key names.
                            retval:         model parameters"""
                            # Load _HyperSearchJob instance from storage, if not provided
                            if hyperSearchJob is None:
                                hyperSearchJob = cls.loadSavedHyperSearchJob(permWorkDir=options["permWorkDir"],outputLabel=options["outputLabel"])
                            modelIDs = hyperSearchJob.queryModelIDs()
                            bestModel = None
                            # If metricsKeys was not provided, pre-scan modelInfos to create the list; this is needed by _ReportCSVWriter Also scan the parameters to generate a list of encoders and search parameters
                            metricstmp = set()
                            searchVar = set()
                            for modelInfo in _iterModels(modelIDs):
                                if modelInfo.isFinished():
                                    vars = modelInfo.getParamLabels().keys()
                                    searchVar.update(vars)
                                    metrics = modelInfo.getReportMetrics()
                                    metricstmp.update(metrics.keys())
                            if metricsKeys is None:
                                metricsKeys = metricstmp
                            # Create a csv report writer
                            reportWriter = _ReportCSVWriter(hyperSearchJob=hyperSearchJob,metricsKeys=metricsKeys,searchVar=searchVar,outputDirAbsPath=options["permWorkDir"],outputLabel=options["outputLabel"],replaceReport=replaceReport)
                            # Tallies of experiment dispositions
                            modelStats = _ModelStats()
                            #numCompletedOther = long(0)
                            print "\nResults from all experiments:"
                            print "----------------------------------------------------------------"
                            # Get common optimization metric info from permutations script
                            searchParams = hyperSearchJob.getParams()
                                def getParams(self):    ### permutations_runner.py ###
                                    """Semi-private method for retrieving the job-specific params
                                    Parameters:
                                    ----------------------------------------------------------------------
                                    retval:  Job params dict corresponding to the JSON params value returned by ClientJobsDAO.jobInfo()"""
                                    return self.__params
                            (optimizationMetricKey, maximizeMetric) = (_PermutationUtils.getOptimizationMetricInfo(searchParams))
                                def getOptimizationMetricInfo(cls, searchJobParams):    ### permutations_runner.py ###
                                    """Retrives the optimization key name and optimization function.
                                    Parameters:
                                    ---------------------------------------------------------
                                    searchJobParams:
                                        Parameter for passing as the searchParams arg to Hypersearch constructor.
                                    retval: (optimizationMetricKey, maximize)
                                        optimizationMetricKey: which report key to optimize for maximize: True if we should try and maximize the optimizeKey metric. False if we should minimize it."""
                                    if searchJobParams["hsVersion"] == "v2":
                                        search = HypersearchV2(searchParams=searchJobParams)
                                    else:
                                        raise RuntimeError("Unsupported hypersearch version \"%s\"" % (searchJobParams["hsVersion"]))
                                    info = search.getOptimizationMetricInfo()
                                    return info
                            # Print metrics, while looking for the best model
                            formatStr = None
                            # NOTE: we may find additional metrics if HyperSearch is still running
                            foundMetricsKeySet = set(metricsKeys)
                            sortedMetricsKeys = []
                            # pull out best Model from jobs table
                            jobInfo = _clientJobsDB().jobInfo(hyperSearchJob.getJobID())
                            # Try to return a decent error message if the job was cancelled for some
                            # reason.
                            if jobInfo.cancel == 1:
                                raise Exception(jobInfo.workerCompletionMsg)
                            try:
                                results = json.loads(jobInfo.results)
                            except Exception, e:
                                print "json.loads(jobInfo.results) raised an exception.  Here is some info to help with debugging:"
                                print "jobInfo: ", jobInfo
                                print "jobInfo.results: ", jobInfo.results
                                print "EXCEPTION: ", e
                                raise
                            bestModelNum = results["bestModel"]
                            bestModelIterIndex = None
                            # performance metrics for the entire job
                            totalWallTime = 0
                            totalRecords = 0
                            # At the end, we will sort the models by their score on the optimization metric
                            scoreModelIDDescList = []
                            for (i, modelInfo) in enumerate(_iterModels(modelIDs)):
                                # Output model info to report csv
                                reportWriter.emit(modelInfo)
                                # Update job metrics
                                totalRecords+=modelInfo.getNumRecords()
                                format = "%Y-%m-%d %H:%M:%S"
                                startTime = modelInfo.getStartTime()
                                if modelInfo.isFinished():
                                    endTime = modelInfo.getEndTime()
                                    st = datetime.strptime(startTime, format)
                                    et = datetime.strptime(endTime, format)
                                    totalWallTime+=(et-st).seconds
                                # Tabulate experiment dispositions
                                modelStats.update(modelInfo)
                                # For convenience
                                expDesc = modelInfo.getModelDescription()
                                reportMetrics = modelInfo.getReportMetrics()
                                optimizationMetrics = modelInfo.getOptimizationMetrics()
                                if modelInfo.getModelID() == bestModelNum:
                                    bestModel = modelInfo
                                    bestModelIterIndex=i
                                    bestMetric = optimizationMetrics.values()[0]
                                # Keep track of the best-performing model
                                if optimizationMetrics:
                                    assert len(optimizationMetrics) == 1, ("expected 1 opt key, but got %d (%s) in %s" % (len(optimizationMetrics), optimizationMetrics, modelInfo))
                                # Append to our list of modelIDs and scores
                                if modelInfo.getCompletionReason().isEOF():
                                    scoreModelIDDescList.append((optimizationMetrics.values()[0],modelInfo.getModelID(),modelInfo.getGeneratedDescriptionFile(),modelInfo.getParamLabels()))
                                print "[%d] Experiment %s\n(%s):" % (i, modelInfo, expDesc)
                                if (modelInfo.isFinished() and not (modelInfo.getCompletionReason().isStopped or modelInfo.getCompletionReason().isEOF())):
                                    print ">> COMPLETION MESSAGE: %s" % modelInfo.getCompletionMsg()
                                if reportMetrics:
                                    # Update our metrics key set and format string
                                    foundMetricsKeySet.update(reportMetrics.iterkeys())
                                    if len(sortedMetricsKeys) != len(foundMetricsKeySet):
                                        sortedMetricsKeys = sorted(foundMetricsKeySet)
                                        maxKeyLen = max([len(k) for k in sortedMetricsKeys])
                                        formatStr = "  %%-%ds" % (maxKeyLen+2)
                                    # Print metrics
                                    for key in sortedMetricsKeys:
                                        if key in reportMetrics:
                                            if key == optimizationMetricKey:
                                                m = "%r (*)" % reportMetrics[key]
                                            else:
                                                m = "%r" % reportMetrics[key]
                                            print formatStr % (key+":"), m
                                    print
                            # Summarize results
                            print "--------------------------------------------------------------"
                            if len(modelIDs) > 0:
                                print "%d experiments total (%s).\n" % (len(modelIDs),("all completed successfully"if (modelStats.numCompletedKilled + modelStats.numCompletedEOF) ==len(modelIDs) else "WARNING: %d models have not completed or there were errors" % (len(modelIDs) - (modelStats.numCompletedKilled + modelStats.numCompletedEOF +modelStats.numCompletedStopped))))
                                if modelStats.numStatusOther > 0:
                                    print "ERROR: models with unexpected status: %d" % (modelStats.numStatusOther)
                                print "WaitingToStart: %d" % modelStats.numStatusWaitingToStart
                                print "Running: %d" % modelStats.numStatusRunning
                                print "Completed: %d" % modelStats.numStatusCompleted
                                if modelStats.numCompletedOther > 0:
                                    print "    ERROR: models with unexpected completion reason: %d" % (modelStats.numCompletedOther)
                                print "    ran to EOF: %d" % modelStats.numCompletedEOF
                                print "    ran to stop signal: %d" % modelStats.numCompletedStopped
                                print "    were orphaned: %d" % modelStats.numCompletedOrphaned
                                print "    killed off: %d" % modelStats.numCompletedKilled
                                print "    failed: %d" % modelStats.numCompletedError
                                assert modelStats.numStatusOther == 0, "numStatusOther=%s" % (modelStats.numStatusOther)
                                assert modelStats.numCompletedOther == 0, "numCompletedOther=%s" % (modelStats.numCompletedOther)
                            else:
                                print "0 experiments total."
                            # Print out the field contributions
                            print
                            global gCurrentSearch
                            jobStatus = hyperSearchJob.getJobStatus(gCurrentSearch._workers)
                            jobResults = jobStatus.getResults()
                            if "fieldContributions" in jobResults:
                                print "Field Contributions:"
                                pprint.pprint(jobResults["fieldContributions"], indent=4)
                            else:
                                print "Field contributions info not available"
                            # Did we have an optimize key?
                            if bestModel is not None:
                                maxKeyLen = max([len(k) for k in sortedMetricsKeys])
                                maxKeyLen = max(maxKeyLen, len(optimizationMetricKey))
                                formatStr = "  %%-%ds" % (maxKeyLen+2)
                                bestMetricValue = bestModel.getOptimizationMetrics().values()[0]
                                optimizationMetricName = bestModel.getOptimizationMetrics().keys()[0]
                                print
                                print "Best results on the optimization metric %s (maximize=%s):" % (optimizationMetricName, maximizeMetric)
                                print "[%d] Experiment %s (%s):" % (bestModelIterIndex, bestModel, bestModel.getModelDescription())
                                print formatStr % (optimizationMetricName+":"), bestMetricValue
                                print
                                print "Total number of Records processed: %d"  % totalRecords
                                print
                                print "Total wall time for all models: %d" % totalWallTime
                                hsJobParams = hyperSearchJob.getParams()
                            # Were we asked to write out the top N model description files?
                            if options["genTopNDescriptions"] > 0:
                                print "\nGenerating description files for top %d models..." % (options["genTopNDescriptions"])
                                scoreModelIDDescList.sort()
                                scoreModelIDDescList = scoreModelIDDescList[0:options["genTopNDescriptions"]]
                                i = -1
                                for (score, modelID, description, paramLabels) in scoreModelIDDescList:
                                    i += 1
                                    outDir = os.path.join(options["permWorkDir"], "model_%d" % (i))
                                    print "Generating description file for model %s at %s" % (modelID, outDir)
                                    if not os.path.exists(outDir):
                                        os.makedirs(outDir)
                                    # Fix up the location to the base description file.
                                    # importBaseDescription() chooses the file relative to the calling file.
                                    # The calling file is in outDir.
                                    # The base description is in the user-specified "outDir"
                                    base_description_path = os.path.join(options["outDir"],"description.py")
                                    base_description_relpath = os.path.relpath(base_description_path,start=outDir)
                                    description = description.replace("importBaseDescription('base.py', config)","importBaseDescription('%s', config)" % base_description_relpath)
                                    fd = open(os.path.join(outDir, "description.py"), "wb")
                                    fd.write(description)
                                    fd.close()
                                    # Generate a csv file with the parameter settings in it
                                    fd = open(os.path.join(outDir, "params.csv"), "wb")
                                    writer = csv.writer(fd)
                                    colNames = paramLabels.keys()
                                    colNames.sort()
                                    writer.writerow(colNames)
                                    row = [paramLabels[x] for x in colNames]
                                    writer.writerow(row)
                                    fd.close()
                                    print "Generating model params file..."
                                    # Generate a model params file alongside the description.py
                                    mod = imp.load_source("description", os.path.join(outDir,"description.py"))
                                    model_description = mod.descriptionInterface.getModelDescription()
                                    fd = open(os.path.join(outDir, "model_params.py"), "wb")
                                    fd.write("%s\nMODEL_PARAMS = %s" % (getCopyrightHead(),pprint.pformat(model_description)))
                                    fd.close()
                                print
                            reportWriter.finalize()
                            return model_description
                # Run HyperSearch
                elif action in ("run", "dryRun", "pickup"):
                    returnValue = _runHyperSearch(runOptions)
                        def _runHyperSearch(runOptions):        ### permutations_runner.py ###
                            global gCurrentSearch
                            # Run HyperSearch
                            startTime = time.time()
                            search = _HyperSearchRunner(runOptions)
                            # Save in global for the signal handler.
                            gCurrentSearch = search
                            if runOptions["action"] in ("run", "dryRun"):
                                search.runNewSearch()
                                def runNewSearch(self):
                                    """Start a new hypersearch job and monitor it to completion
                                    Parameters:
                                    ----------------------------------------------------------------------
                                    retval:         nothing"""
                                    self.__searchJob = self.__startSearch()
                                        def __startSearch(self):
                                            """Starts HyperSearch as a worker or runs it inline for the "dryRun" action
                                            Parameters:
                                            ----------------------------------------------------------------------
                                            retval:         the new _HyperSearchJob instance representing the HyperSearch job"""
                                            # This search uses a pre-existing permutations script
                                            params = _ClientJobUtils.makeSearchJobParamsDict(options=self._options,forRunning=True)
                                            if self._options["action"] == "dryRun":
                                                args = [sys.argv[0], "--params=%s" % (json.dumps(params))]
                                                print
                                                print "=================================================================="
                                                print "RUNNING PERMUTATIONS INLINE as \"DRY RUN\"..."
                                                print "=================================================================="
                                                jobID = HypersearchWorker.main(args)
                                            else:
                                                cmdLine = _setUpExports(self._options["exports"])
                                                # Begin the new search. The {JOBID} string is replaced by the actual
                                                # jobID returned from jobInsert.
                                                cmdLine += "$HYPERSEARCH"
                                                maxWorkers = self._options["maxWorkers"]
                                                jobID = self.__cjDAO.jobInsert(client="GRP",cmdLine=cmdLine,params=json.dumps(params),minimumWorkers=1,maximumWorkers=maxWorkers,jobType=self.__cjDAO.JOB_TYPE_HS)
                                                cmdLine = "python -m nupic.swarming.HypersearchWorker --jobID=%d" % (jobID)
                                                self._launchWorkers(cmdLine, maxWorkers)
                                            searchJob = _HyperSearchJob(jobID)
                                            # Save search ID to file (this is used for report generation)
                                            self.__saveHyperSearchJobID(permWorkDir=self._options["permWorkDir"],outputLabel=self._options["outputLabel"],hyperSearchJob=searchJob)
                                            if self._options["action"] == "dryRun":
                                                print "Successfully executed \"dry-run\" hypersearch, jobID=%d" % (jobID)
                                            else:
                                                print "Successfully submitted new HyperSearch job, jobID=%d" % (jobID)
                                                _emit(Verbosity.DEBUG,"Each worker executing the command line: %s" % (cmdLine,))
                                            return searchJob
                                    self.monitorSearchJob()
                                        def monitorSearchJob(self):
                                            """Parameters:
                                            ----------------------------------------------------------------------
                                            retval:         nothing"""
                                            assert self.__searchJob is not None
                                            jobID = self.__searchJob.getJobID()
                                            startTime = time.time()
                                            lastUpdateTime = datetime.now()
                                            # Monitor HyperSearch and report progress
                                            # NOTE: may be -1 if it can't be determined
                                            expectedNumModels = self.__searchJob.getExpectedNumModels(searchMethod = self._options["searchMethod"])
                                            lastNumFinished = 0
                                            finishedModelIDs = set()
                                            finishedModelStats = _ModelStats()
                                            # Keep track of the worker state, results, and milestones from the job record
                                            lastWorkerState = None
                                            lastJobResults = None
                                            lastModelMilestones = None
                                            lastEngStatus = None
                                            hyperSearchFinished = False
                                            while not hyperSearchFinished:
                                                jobInfo = self.__searchJob.getJobStatus(self._workers)
                                                # Check for job completion BEFORE processing models; NOTE: this permits us to process any models that we may not have accounted for in the previous iteration.
                                                hyperSearchFinished = jobInfo.isFinished()
                                                # Look for newly completed models, and process them
                                                modelIDs = self.__searchJob.queryModelIDs()
                                                _emit(Verbosity.DEBUG,"Current number of models is %d (%d of them completed)" % (len(modelIDs), len(finishedModelIDs)))
                                                if len(modelIDs) > 0:
                                                    # Build a list of modelIDs to check for completion
                                                    checkModelIDs = []
                                                    for modelID in modelIDs:
                                                        if modelID not in finishedModelIDs:
                                                            checkModelIDs.append(modelID)
                                                    del modelIDs
                                                    # Process newly completed models
                                                    if checkModelIDs:
                                                        _emit(Verbosity.DEBUG,"Checking %d models..." % (len(checkModelIDs)))
                                                        errorCompletionMsg = None
                                                        for (i, modelInfo) in enumerate(_iterModels(checkModelIDs)):
                                                            _emit(Verbosity.DEBUG,"[%s] Checking completion: %s" % (i, modelInfo))
                                                        if modelInfo.isFinished():
                                                            finishedModelIDs.add(modelInfo.getModelID())
                                                            finishedModelStats.update(modelInfo)
                                                            if (modelInfo.getCompletionReason().isError() and not errorCompletionMsg):
                                                                errorCompletionMsg = modelInfo.getCompletionMsg()
                                                            # Update the set of all encountered metrics keys (we will use these to print column names in reports.csv)
                                                            metrics = modelInfo.getReportMetrics()
                                                            self.__foundMetrcsKeySet.update(metrics.keys())
                                                    numFinished = len(finishedModelIDs)
                                                    # Print current completion stats
                                                    if numFinished != lastNumFinished:
                                                        lastNumFinished = numFinished
                                                        if expectedNumModels is None:
                                                            expModelsStr = ""
                                                        else:
                                                            expModelsStr = "of %s" % (expectedNumModels)
                                                        stats = finishedModelStats
                                                        print ("<jobID: %s> %s %s models finished [success: %s; %s: %s; %s: %s; %s: %s; %s: %s; %s: %s; %s: %s]" % (jobID,numFinished,expModelsStr,(stats.numCompletedEOF+stats.numCompletedStopped),"EOF" if stats.numCompletedEOF else "eof",stats.numCompletedEOF,"STOPPED" if stats.numCompletedStopped else "stopped",stats.numCompletedStopped,"KILLED" if stats.numCompletedKilled else "killed",stats.numCompletedKilled,"ERROR" if stats.numCompletedError else "error",stats.numCompletedError,"ORPHANED" if stats.numCompletedError else "orphaned",stats.numCompletedOrphaned,"UNKNOWN" if stats.numCompletedOther else "unknown",stats.numCompletedOther))
                                                        # Print the first error message from the latest batch of completed models
                                                        if errorCompletionMsg:
                                                            print "ERROR MESSAGE: %s" % errorCompletionMsg
                                                    # Print the new worker state, if it changed
                                                    workerState = jobInfo.getWorkerState()
                                                    if workerState != lastWorkerState:
                                                        print "##>> UPDATED WORKER STATE: \n%s" % (pprint.pformat(workerState,indent=4))
                                                        lastWorkerState = workerState
                                                    # Print the new job results, if it changed
                                                    jobResults = jobInfo.getResults()
                                                    if jobResults != lastJobResults:
                                                        print "####>> UPDATED JOB RESULTS: \n%s (elapsed time: %g secs)" % (pprint.pformat(jobResults, indent=4), time.time()-startTime)
                                                        lastJobResults = jobResults
                                                    # Print the new model milestones if they changed
                                                    modelMilestones = jobInfo.getModelMilestones()
                                                    if modelMilestones != lastModelMilestones:
                                                        print "##>> UPDATED MODEL MILESTONES: \n%s" % (pprint.pformat(modelMilestones, indent=4))
                                                        lastModelMilestones = modelMilestones
                                                    # Print the new engine status if it changed
                                                    engStatus = jobInfo.getEngStatus()
                                                    if engStatus != lastEngStatus:
                                                        print "##>> UPDATED STATUS: \n%s" % (engStatus)
                                                        lastEngStatus = engStatus
                                                # Sleep before next check
                                                if not hyperSearchFinished:
                                                    if self._options["timeout"] != None:
                                                        if ((datetime.now() - lastUpdateTime) > timedelta(minutes=self._options["timeout"])):
                                                            print "Timeout reached, exiting"
                                                            self.__cjDAO.jobCancel(jobID)
                                                            sys.exit(1)
                                                    time.sleep(1)
                                            # Tabulate results
                                            modelIDs = self.__searchJob.queryModelIDs()
                                            print "Evaluated %s models" % len(modelIDs)
                                            print "HyperSearch finished!"
                                            jobInfo = self.__searchJob.getJobStatus(self._workers)
                                            print "Worker completion message: %s" % (jobInfo.getWorkerCompletionMsg())
                            else:
                                search.pickupSearch()
                            # Generate reports
                            # Print results and generate report csv file
                            modelParams = _HyperSearchRunner.generateReport(options=runOptions, replaceReport=runOptions["replaceReport"], hyperSearchJob=search.peekSearchJob(), metricsKeys=search.getDiscoveredMetricsKeys())
                            secs = time.time() - startTime
                            hours = int(secs) / (60 * 60)
                            secs -= hours * (60 * 60)
                            minutes = int(secs) / 60
                            secs -= minutes * 60
                            print "Elapsed time (h:mm:ss): %d:%02d:%02d" % (hours, minutes, int(secs))
                            jobID = search.peekSearchJob().getJobID()
                            print "Hypersearch ClientJobs job ID: ", jobID
                    else:
                    raise Exception("Unhandled action: %s" % action)
                return returnValue