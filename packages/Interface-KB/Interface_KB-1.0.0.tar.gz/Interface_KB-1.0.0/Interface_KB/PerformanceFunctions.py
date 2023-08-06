#interface objects
from .InterfaceObjects import Parameter,PerformanceModel,StopCondition,Constraint,Objective,DecisionVariable,AnalysisModel,ResultMetric,Contact,BoundaryCondition
#import helper functions
from .HelperFunctions import *

#-----------------------------------------------------------------------------------------------------------
#
#   Performance extension
#
#
# -----------------------------------------------------------------------------------------------------------
def getPerformance( OptimizationProblemName,model):
    """
      Function to fetch the complete performance model using the name as identifier.
      The function returns an interface block of the performance model

      :param string OptimizationProblemName: Name identifier of the optimization problem
      :param object model: Metamodel instance model

      :return object PerformanceModel: Interface object of the performance model (-1 = error)
    """

    #define performance model interface object
    pModel = PerformanceModel()
    pModel.clean()  # Flushing the pModel

    found = 0
    if len(model.includesOptimizationProblem.items) != 0:
        # match the assemblySystem by Name
        for optimizationProblem in model.includesOptimizationProblem.items:
            if OptimizationProblemName == optimizationProblem.hasName:
                found = 1
                pModel.Name=optimizationProblem.hasName
                pModel.Description = optimizationProblem.hasDescription

                # fetch the analysysDescription
                pModel.OptimizationMethod=[optimizationProblem.hasOptimizationAnalysisdDescription.hasOptimizationMethod.hasName,optimizationProblem.hasOptimizationAnalysisdDescription.hasOptimizationMethod.hasDescription,optimizationProblem.hasOptimizationAnalysisdDescription.hasOptimizationMethod.hasAlgorithmClass.name]
                StopList = []
                for STP in optimizationProblem.hasOptimizationAnalysisdDescription.hasStopCriterion.items:
                    s = StopCondition(Name=STP.hasName,Description=STP.hasDescription,Value=STP.hasValue,Stopcriteria=STP.hasStopCriterion.name)
                    StopList.append(s)
                pModel.StopConditionList=StopList

                # fetch the Optimization targets
                for designTarget in optimizationProblem.hasOptimizationTargetDescription.hasDesignTarget.items:
                    # check the typing
                    x = str(type(designTarget))
                    if 'Constraint' in x:
                        cstr = Constraint(Name=designTarget.hasName,Description=designTarget.hasDescription)

                        for term in designTarget.hasExpression.hasTerm.items:                       #TODO:this needs to be reworked!
                            TERM = []
                            if "LEFT" in term.hasInfixPosition.name:
                                TERM.append('LEFT')
                            if "RIGHT" in term.hasInfixPosition.name:
                                TERM.append('RIGHT')
                            x = str(type(term))
                            if 'Textual' in x:  # textual term
                                TERM.append(term.hasValue)
                            if 'Numerical' in x:  # numerical term
                                TERM.append(term.hasValue)
                            if 'Variable' in x:  # variable term
                                TERM.append(term.hasDecisionVariable.hasName)
                                TERM.append(term.hasDecisionVariable.hasDescription)
                                TERM.append(term.hasDecisionVariable.hasOptimum)
                            cstr.Expression.append(TERM)
                        #add the expression operator
                        operator  = designTarget.hasExpression.hasExpressionOperator.hasValue
                        cstr.Expression.append(operator)

                        pModel.ConstraintList.append(cstr)

                    if 'Objective' in x:
                        OBJ_O = Objective(Name=designTarget.hasName, Description=designTarget.hasDescription)

                        x = str(type(designTarget.hasTerm))
                        if 'Textual' in x:  # textual term
                            OBJ_O.ObjectiveOption = designTarget.hasTerm.hasValue
                        if 'Numerical' in x:  # numerical term
                            OBJ_O.ObjectiveOption = designTarget.hasTerm.hasValue
                        if 'Variable' in x:  # variable term
                            OBJ_O.ObjectiveOption = [designTarget.hasTerm.hasDecisionVariable.hasName,designTarget.hasTerm.hasDecisionVariable.hasDescription,designTarget.hasTerm.hasDecisionVariable.hasOptimum]
                        pModel.ObjectiveList.append(OBJ_O)

                # fetch the design variables
                for variable in optimizationProblem.hasOptimizationTargetDescription.hasDecisionVariable.items:
                    dv = DecisionVariable(Name=variable.hasName,Description=variable.hasDescription,InitialValue=variable.hasInitialValue,MaxValue=variable.hasMaxValue,MinValue=variable.hasMinValue,Optimum=variable.hasOptimum,Resolution=variable.hasResolution)
                    try:
                        par = Parameter(Name=variable.hasParameter.hasName,Description=variable.hasParameter.hasDescription,Key=variable.hasParameter.hasKey, GUID=variable.hasParameter.hasGUID,Value=variable.hasParameter.hasValue)
                        dv.parameterList.append(par)
                    except:
                        par = []

                    pModel.parameterList.append(dv)



        if found:
            return pModel
        else:
            return -1
    else:
        return -1  # no Optimization Problem!

def updatePerformance(interfaceObject,model,KBPath):
    """
          Function to update the complete performance model matching the name as identifier.
          The performance interface object is used to interface with the function.
          The function returns whether or not the function is performed correctly

          :param object PerformanceModel: Interface object of the performance model
          :param object model: Metamodel instance model
          :param string KBPath: Absolute path to the metamodel instance model

          :return int Error: -1 = error, 1= function performed correcly
        """

    #find the optimization model
    found = 0
    if len(model.includesOptimizationProblem.items) != 0:
        # match the assemblySystem by Name
        for optimizationProblem in model.includesOptimizationProblem.items:
            if interfaceObject.Name == optimizationProblem.hasName:
                found = 1
                optimizationProblem.hasName=interfaceObject.Name
                optimizationProblem.hasDescription=interfaceObject.Description
                #analysisDescription
                optimizationProblem.hasOptimizationAnalysisdDescription.hasOptimizationMethod.hasName = interfaceObject.OptimizationMethod[0]
                optimizationProblem.hasOptimizationAnalysisdDescription.hasOptimizationMethod.hasDescription = interfaceObject.OptimizationMethod[1]
                optimizationProblem.hasOptimizationAnalysisdDescription.hasOptimizationMethod.hasAlgorithmClass.name = interfaceObject.OptimizationMethod[2]

                StopList = []
                for STP in optimizationProblem.hasOptimizationAnalysisdDescription.hasStopCriterion.items:
                    for STP_NEW in interfaceObject.StopConditionList:
                        if STP_NEW.Name == STP.hasName:
                            STP.hasName=STP_NEW.Name
                            STP.hasDescription=STP_NEW.Description
                            STP.hasValue=STP_NEW.Value
                            STP.hasStopCriterion.name=STP_NEW.StopCriteria

                #Objectives and constraints
                for designTarget in optimizationProblem.hasOptimizationTargetDescription.hasDesignTarget.items:
                    # check the typing
                    x = str(type(designTarget))
                    if 'Constraint' in x:
                        for constraint_new in interfaceObject.ConstraintList:
                            if constraint_new.Name ==designTarget.hasName:
                                designTarget.hasName=constraint_new.Name
                                designTarget.hasDescription=constraint_new.Description
                                for term in designTarget.hasExpression.hasTerm.items:
                                    y=1
                                    #TODO: using the current KB (version6), updating the expressions is not possible! discuss if needed


                    if 'Objective' in x:
                        for obj_new in interfaceObject.ObjectiveList:
                            designTarget.hasName = obj_new.Name
                            designTarget.hasDescription=obj_new.Description
                        x = str(type(designTarget.hasTerm))
                        if 'Textual' in x:  # textual term
                            designTarget.hasTerm.hasValue = obj_new.ObjectiveOption[0]
                        if 'Numerical' in x:  # numerical term
                            designTarget.hasTerm.hasValue = obj_new.ObjectiveOption[0]
                        if 'Variable' in x:  # variable term
                            designTarget.hasTerm.hasDecisionVariable.hasName= obj_new.ObjectiveOption[0]
                            designTarget.hasTerm.hasDecisionVariable.hasDescription= obj_new.ObjectiveOption[1]
                            designTarget.hasTerm.hasDecisionVariable.hasOptimum = obj_new.ObjectiveOption[2]



                #Decision Variables
                for variable in optimizationProblem.hasOptimizationTargetDescription.hasDecisionVariable.items:
                    for variable_new in interfaceObject.parameterList:
                        if variable.hasName == variable_new.Name:
                            variable.hasName=variable_new.Name
                            variable.hasInitialValue=variable_new.InitialValue
                            variable.hasMaxValue=variable_new.MaxValue
                            variable.hasMinValue=variable_new.MinValue
                            variable.hasOptimum=variable_new.Optimum
                            variable.hasResolution=variable_new.Resolution
                            for par in variable_new.parameterList:
                                if variable.hasParameter.hasName==par.Name:
                                    variable.hasParameter.hasName = par.Name
                                    variable.hasParameter.hasDescription = par.Description
                                    variable.hasParameter.hasKey = par.Key
                                    variable.hasParameter.hasGUID = par.GUID
                                    variable.hasParameter.hasValue = str(par.Value)


        if found:
            updateKBv6(KBPath, model)
            return 1
        else:
            return -1
    else:
        return -1  # no Optimization Problem!

def setPerformance(interfaceObject,model,KBPath,API):
    """
             Function to add a complete performance model to an blank KB (no existing performance part).
             The performance interface object is used to interface with the function.
             The function returns whether or not the function is performed correctly

             :param object PerformanceModel: Interface object of the performance model
             :param object model: Metamodel instance model
             :param string KBPath: Absolute path to the metamodel instance model

             :return int Error: -1 = error, 1= function performed correcly
    """
    # generate a new ASG config and configure
    optimizationProblem = API.create_connected("OptimizationProblem")
    optimizationProblem.hasName=interfaceObject.Name
    optimizationProblem.hasDescription=interfaceObject.Description
    #analysisDescription
    OptimizationAnalysisdDescription = API.create_noPlatformRoot("OptimizationAnalysisDescription")

    #add the method
    OptimizationMethod = API.create_noPlatformRoot("OptimizationMethod")
    OptimizationMethod.hasName = interfaceObject.OptimizationMethod[0]
    OptimizationMethod.hasDescription = interfaceObject.OptimizationMethod[1]
    OptimizationMethod.hasAlgorithmClass.name = interfaceObject.OptimizationMethod[2]
    OptimizationAnalysisdDescription.hasOptimizationMethod = OptimizationMethod

    #add the stop criteria
    for STP_NEW in interfaceObject.StopConditionList:
        StopCriterion = API.create_noPlatformRoot("StopCriterion")
        StopCriterion.hasName = STP_NEW.Name
        StopCriterion.hasDescription = STP_NEW.Description
        StopCriterion.hasValue = STP_NEW.Value
        StopCriterion.hasStopCriterion.name = STP_NEW.StopCriteria
        OptimizationAnalysisdDescription.hasStopCriterion.append(StopCriterion)

    optimizationProblem.hasOptimizationAnalysisdDescription = OptimizationAnalysisdDescription

    OptimizationTargetDescription = API.create_noPlatformRoot("OptimizationTargetDescription")
    #TODO:implement!
    #Objectives and constraints
    for constraint_new in interfaceObject.ConstraintList:
        constraint = API.create_noPlatformRoot("Constraint")
        constraint.hasName=constraint_new.Name
        constraint.hasDescription=constraint_new.Description

        OptimizationTargetDescription.hasDesignTarget.append(constraint)

    for obj_new in interfaceObject.ObjectiveList:
        objective = API.create_noPlatformRoot("Objective")
        objective.hasName = obj_new.Name
        objective.hasDescription=obj_new.Description
        expression = API.create_noPlatformRoot("Expression")

        # TODO: this needs to be updated via the object - no example available to validate
        #expression.hasExpressionOperator = "<"
        #expression.hasValue = double(obj_new.ObjectiveOption[2])
        #expression.hasTerm.append(obj_new.ObjectiveOption[1])
        #objective.hasExpression #TODO: using the current KB (version6), updating the expressions (hasExpression) is not possible! discuss if needed

        OptimizationTargetDescription.hasDesignTarget.append(objective)


    #Decision Variables
    for variable_new in interfaceObject.parameterList:
        variable = API.create_noPlatformRoot("Variable")
        variable.hasName=variable_new.Name
        variable.hasInitialValue=variable_new.InitialValue
        variable.hasMaxValue=variable_new.MaxValue
        variable.hasMinValue=variable_new.MinValue
        variable.hasOptimum=variable_new.Optimum
        variable.hasResolution=variable_new.Resolution
        for par in variable_new.parameterList:
            subvariable = API.create_noPlatformRoot("Variable")
            subvariable.hasName = par.Name
            subvariable.hasDescription = par.Description
            subvariable.hasKey = par.Key
            subvariable.hasGUID = par.GUID
            subvariable.hasValue = str(par.Value)

        OptimizationTargetDescription.hasDecisionVariable.append(variable)

    optimizationProblem.hasOptimizationTargetDescription = OptimizationTargetDescription

    updateKBv6(KBPath, model)
    return 1

def getAnalysisModel(analysisModelName,model):
    """
          Function to fetch the complete analysis model using the name as identifier.
          The function returns an interface block of the analysis model

          :param string OptimizationProblemName: Name identifier of the optimization problem
          :param object model: Metamodel instance model

          :return object PerformanceModel: Interface object of the performance model (-1 = error)
        """

    # define performance model interface object
    aModel = AnalysisModel()
    aModel.clean()  # Flushing the pModel

    found = 0
    if len(model.includesProduct[0].hasAnalysisModel.items) != 0:
        # match the assemblySystem by Name
        for analysisModel in model.includesProduct[0].hasAnalysisModel.items:
            found = 1
            if analysisModel.hasName == analysisModelName:
                aModel.Name = analysisModel.hasName
                aModel.Description = analysisModel.hasDescription
                aModel.Version = analysisModel.hasVersion
                aModel.SubsetNumber = analysisModel.hasSubsetNumber
                aModel.ModelFile = analysisModel.hasModelFile

                #fetch the modelDescription
                aModel.ModelDescription = analysisModel.hasModeldescription

                #fetch the meshes
                meshes=[]
                for m in analysisModel.hasMesh.items:
                    meshes.append(m.hasMeshType)
                aModel.Mesh = meshes

                # -- fetch the analysis elements --

                #fetch result metrics
                results = []
                aModel.AnalysisType = analysisModel.hasAnalysis.hasAnalysisType
                for result in analysisModel.hasAnalysis.hasAnalysisResult.items:
                    metric = ResultMetric(Name=result.hasName,Description=result.hasDescription,Optimum=result.hasOptimum,Unit=result.hasUnit,Value=result.hasValue)
                    results.append(metric)
                aModel.AnalysisResults = results

                # fetch contacts
                contacts = []
                aModel.AnalysisType = analysisModel.hasAnalysis.hasAnalysisType
                for result in analysisModel.hasAnalysis.hasContact.items:
                    contact = Contact(Name=result.hasName, Type=result.hasType,SearchDistance=result.hasSearchDistance)
                    areas = []
                    for area in result.hasApplicationArea:
                        areas.append([area.hasName,area.hasProductPart])    #TODO: check if productpart is present
                    contact.ApplicationAreas = areas
                    contacts.append(contact)
                aModel.Contacts = contacts

                # fetch boundaryConditions
                boundaries = []
                for result in analysisModel.hasAnalysis.hasBoundaryCondition.items:
                    bound = BoundaryCondition(Name=result.hasName,Type=result.hasType,Value=result.hasValue)
                    #direction
                    bound.Direction = [result.hasDirection.hasX,result.hasDirection.hasY,result.hasDirection.hasZ,result.hasDirection.hasRx,result.hasDirection.hasRy,result.hasDirection.hasRz]
                    #DOF
                    bound.DOF = [result.hasDOF.hasDOF1,result.hasDOF.hasDOF2,result.hasDOF.hasDOF3,result.hasDOF.hasDOF4,result.hasDOF.hasDOF5,result.hasDOF.hasDOF6]
                    #ApplicationAreas
                    areas = []
                    for area in result.hasApplicationarea:
                        areas.append([area.hasName, area.hasProductPart])  # TODO: check if productpart is present
                    bound.ApplicationAreas = areas
                    boundaries.append(bound)
                aModel.BoundaryConditions = boundaries

                # fetch ToolDescription
                aModel.ToolDescription = [analysisModel.hasAnalysis.hasTooldescription.hasName,analysisModel.hasAnalysis.hasTooldescription.hasDescription,analysisModel.hasAnalysis.hasTooldescription.hasVersion]

                # fetch response points
                points = []
                for p in analysisModel.hasAnalysis.hasResponsepoint:
                    points.append([p.hasResponseType,[p.position.hasX,p.position.hasY,p.position.hasZ]])
                aModel.Responsepoints=points

                # fetch decision variables
                variables = []
                for var in analysisModel.hasAnalysis.hasDecisionvariable:
                    variable = DecisionVariable(Name=var.hasName,Description=var.hasDescription,InitialValue=var.hasInitialValue,MinValue=var.hasMinValue,MaxValue=var.hasMaxValue,Optimum=var.hasOptimum,Resolution=var.hasResolution,Unit=var.hasUnit)
                    parList = []
                    try:
                        for par in var.hasParameter:
                            p = Parameter(Name=par.hasName,Description=par.hasDescription,Key=par.hasKey, GUID=par.hasGUID,Value=par.hasValue)
                            parList.append(p)
                        variable.parameterList = parList
                    except:
                        x=1

                    variables.append(variable)
                aModel.DecisionVariables = variables

        if found:
            return aModel
        else:
            return -1
    else:
        return -1  # no Optimization Problem!

def updateAnalysisModel(interfaceObject,model,KBPath):
    """
          Function to update the complete analysis model matching the name as identifier.
          The analysis interface object is used to interface with the function.
          The function returns whether or not the function is performed correctly

          :param object Analysis Model: Interface object of the analysis model
          :param object model: Metamodel instance model
          :param string KBPath: Absolute path to the metamodel instance model

          :return int Error: -1 = error, 1= function performed correcly
        """
    found = 0
    if len(model.includesProduct[0].hasAnalysisModel.items) != 0:
        # match the assemblySystem by Name
        for analysisModel in model.includesProduct[0].hasAnalysisModel.items:
            found = 1
            if analysisModel.hasName == interfaceObject.Name:
                analysisModel.hasName = interfaceObject.Name
                analysisModel.hasDescription = interfaceObject.Description
                analysisModel.hasVersion = interfaceObject.Version
                analysisModel.hasSubsetNumber = interfaceObject.SubsetNumber
                analysisModel.hasModelFile = interfaceObject.ModelFile

                # update the modelDescription
                analysisModel.hasModeldescription.hasFormalism = interfaceObject.ModelDescription[0]
                analysisModel.hasModeldescription.hasVersion = interfaceObject.ModelDescription[1]
                analysisModel.hasModeldescription.hasCreatedBy = interfaceObject.ModelDescription[2]

                #TODO: [DISCUSS] meshes can only be ADDED, as no identification is provided. Is this sufficient?

                # -- fetch the analysis elements --

                # update result metrics
                for results_update in interfaceObject.AnalysisResults:
                    for result in analysisModel.hasAnalysis.hasAnalysisResult.items:
                        if result.hasName == results_update.Name:
                            result.hasName = results_update.Name
                            result.hasDescription = results_update.Description
                            result.hasOptimum = results_update.Optimum
                            result.hasUnit = results_update.Unit
                            result.hasValue = results_update.Value
                            #analysisModel.hasAnalysis.hasAnalysisType = results_update.Name

                # update contacts
                for results_update in interfaceObject.Contacts:
                    for result in analysisModel.hasAnalysis.hasContact.items:
                        result.hasName = results_update.Name
                        result.hasType = results_update.Type
                        result.hasSearchDistance = results_update.SearchDistance
                        for area_update in results_update.ApplicationAreas:
                            for area in result.hasApplicationArea:
                                if area_update[0]==area.hasName:
                                    area.hasName = area_update[0]
                                    area.hasProductPart = area_update[1]


                # update boundaryConditions
                for results_update in interfaceObject.BoundaryConditions:
                    for result in analysisModel.hasAnalysis.hasBoundaryCondition.items:
                        if result.hasName == results_update.Name:
                            result.hasName = results_update.Name
                            result.hasType = results_update.Type
                            result.hasValue = results_update.Value

                            # direction
                            result.hasDirection.hasX = results_update.Direction[0]
                            result.hasDirection.hasY = results_update.Direction[1]
                            result.hasDirection.hasZ = results_update.Direction[2]
                            result.hasDirection.hasRx = results_update.Direction[3]
                            result.hasDirection.hasRy = results_update.Direction[4]
                            result.hasDirection.hasRz = results_update.Direction[5]

                            # DOF
                            result.hasDOF.hasDOF1 = results_update.DOF[0]
                            result.hasDOF.hasDOF2 = results_update.DOF[1]
                            result.hasDOF.hasDOF3 = results_update.DOF[2]
                            result.hasDOF.hasDOF4 = results_update.DOF[3]
                            result.hasDOF.hasDOF5 = results_update.DOF[4]
                            result.hasDOF.hasDOF6 = results_update.DOF[5]

                            # ApplicationAreas
                            for area_update in results_update.ApplicationAreas:
                                for area in result.hasApplicationarea:
                                    if area_update[0] == area.hasName:
                                        area.hasName = area_update[0]
                                        area.hasProductPart = area_update[1]

                # fetch ToolDescription
                try:
                    analysisModel.hasAnalysis.hasTooldescription.hasName = interfaceObject.ToolDescription[0]
                    analysisModel.hasAnalysis.hasTooldescription.hasDescription = interfaceObject.ToolDescription[1]
                    analysisModel.hasAnalysis.hasTooldescription.hasVersion = interfaceObject.ToolDescription[2]
                except:
                    x=1

                #TODO: [DISCUSS] Response points can only be ADDED, as no identification is provided. Is this sufficient?

                # update decision variables
                for results_update in interfaceObject.DecisionVariables:
                    for result in analysisModel.hasAnalysis.hasDecisionvariable.items:
                        if result.hasName == results_update.Name:
                            result.hasName = results_update.Name
                            result.hasDescription = results_update.Description
                            result.hasInitialValue = results_update.InitialValue
                            result.hasMinValue = results_update.MinValue
                            result.hasMaxValue = results_update.MaxValue
                            result.hasOptimum = results_update.Optimum
                            result.hasResolution = results_update.Resolution
                            result.hasUnit = results_update.Unit

                        for parameter_update in results_update.parameterList:
                            for parameter in result.hasParameter:
                                parameter.hasName = parameter_update.Name
                                parameter.hasDescription = parameter_update.Description
                                parameter.hasKey = parameter_update.Key
                                parameter.hasGUID = parameter_update.GUID
                                parameter.hasValue = parameter_update.Value

        if found:
            updateKBv6(KBPath, model)
            return 1
        else:
            return -1
    else:
        return -1  # no Analysis!

def setAnalysisModel(interfaceObject,model,KBPath,API):
    """
                 Function to add a complete analysis model to an blank KB (no existing analysis part).
                 The analysis interface object is used to interface with the function.
                 The function returns whether or not the function is performed correctly

                 :param object AnalysisModel: Interface object of the analysis model
                 :param object model: Metamodel instance model
                 :param string KBPath: Absolute path to the metamodel instance model

                 :return int Error: -1 = error, 1= function performed correcly
        """

    # generate a new ASG config and configure
    analysisModel = API.create_noPlatformRoot("PerformanceModel")
    analysisModel.hasName = interfaceObject.Name
    analysisModel.hasDescription = interfaceObject.Description
    analysisModel.hasVersion = interfaceObject.Version
    analysisModel.hasSubsetNumber = interfaceObject.SubsetNumber
    analysisModel.hasModelFile = interfaceObject.ModelFile

    # add the modelDescription
    Modeldescription = API.create_noPlatformRoot("ModelDescription")
    Modeldescription.hasFormalism = interfaceObject.ModelDescription[0]
    Modeldescription.hasVersion = interfaceObject.ModelDescription[1]
    Modeldescription.hasCreatedBy = interfaceObject.ModelDescription[2]
    analysisModel.hasModeldescription = Modeldescription

    # add meshes
    for mesh in interfaceObject.Mesh:
        m = API.create_noPlatformRoot("Mesh")
        m.hasMeshType = mesh
        analysisModel.hasMesh.append(m)

    # -- fetch the analysis elements --
    Analysis = API.create_noPlatformRoot("Analysis")
    # update result metrics
    for results_update in interfaceObject.AnalysisResults:
        result = API.create_noPlatformRoot("AnalysisResult")
        result.hasName = results_update.Name
        result.hasDescription = results_update.Description
        result.hasOptimum = results_update.Optimum
        result.hasUnit = results_update.Unit
        result.hasValue = results_update.Value
        Analysis.hasAnalysisResult.append(result)

    # add contacts
    for results_update in interfaceObject.Contacts:
        result = API.create_noPlatformRoot("Contact")
        result.hasName = results_update.Name
        result.hasType = results_update.Type
        result.hasSearchDistance = results_update.SearchDistance
        for area_update in results_update.ApplicationAreas:
            area = API.create_noPlatformRoot("ApplicationArea")
            area.hasName = area_update[0]
            area.hasProductPart = area_update[1]
            result.hasApplicationArea.append(area)
        Analysis.hasContact.append(result)

    # update boundaryConditions
    for results_update in interfaceObject.BoundaryConditions:
        result = API.create_noPlatformRoot("BoundaryCondition")
        result.hasName = results_update.Name
        result.hasType = results_update.Type
        result.hasValue = results_update.Value

        # direction
        direction = API.create_noPlatformRoot("Direction")
        direction.hasX = results_update.Direction[0]
        direction.hasY = results_update.Direction[1]
        direction.hasZ = results_update.Direction[2]
        direction.hasRx = results_update.Direction[3]
        direction.hasRy = results_update.Direction[4]
        direction.hasRz = results_update.Direction[5]
        result.hasDirection = direction

        # DOF
        DOF = API.create_noPlatformRoot("DOF")
        DOF.hasDOF1 = results_update.DOF[0]
        DOF.hasDOF2 = results_update.DOF[1]
        DOF.hasDOF3 = results_update.DOF[2]
        DOF.hasDOF4 = results_update.DOF[3]
        DOF.hasDOF5 = results_update.DOF[4]
        DOF.hasDOF6 = results_update.DOF[5]
        result.hasDOF = DOF

        # ApplicationAreas
        for area_update in results_update.ApplicationAreas:
            area = API.create_noPlatformRoot("ApplicationArea")
            area.hasName = area_update[0]
            area.hasProductPart = area_update[1]
            result.hasApplicationarea.append(area)

        Analysis.hasBoundaryCondition.append(result)

    # fetch ToolDescription
    try:
        Tooldescription = API.create_noPlatformRoot("Tooldescription")
        Tooldescription.hasName = interfaceObject.ToolDescription[0]
        Tooldescription.hasDescription = interfaceObject.ToolDescription[1]
        Tooldescription.hasVersion = interfaceObject.ToolDescription[2]
        analysisModel.hasToolDescription = Tooldescription
    except:
        x = 1

    # add response points
    for rp in interfaceObject.Responsepoints:
        m = API.create_noPlatformRoot("ResponsePoint")
        m.hasResponseType = rp
        Analysis.hasResponsepoint.append(m)

    # update decision variables
    for results_update in interfaceObject.DecisionVariables:
        result = API.create_noPlatformRoot("Decisionvariable")
        result.hasName = results_update.Name
        result.hasDescription = results_update.Description
        result.hasInitialValue = results_update.InitialValue
        result.hasMinValue = results_update.MinValue
        result.hasMaxValue = results_update.MaxValue
        result.hasOptimum = results_update.Optimum
        result.hasResolution = results_update.Resolution
        result.hasUnit = results_update.Unit

        for parameter_update in results_update.parameterList:
            parameter = API.create_noPlatformRoot("Parameter")
            parameter.hasName = parameter_update.Name
            parameter.hasDescription = parameter_update.Description
            parameter.hasKey = parameter_update.Key
            parameter.hasGUID = parameter_update.GUID
            parameter.hasValue = parameter_update.Value
            result.hasParameter.append(parameter)

        Analysis.hasDecisionvariables.append(result)


    analysisModel.hasAnalysis = Analysis
    model.includesProduct.items[0].hasAnalysisModel.append(analysisModel)

    updateKBv6(KBPath, model)
    return 1