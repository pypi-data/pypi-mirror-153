"""
    2020 Christian Mollière

    This is a prototype for the model validation feature of the EOQ2 framework.

    It is connected to
    - command/commandrunner.py
    - event/event.py
    The constraint model can be found in
    - mdb/pyecore/constraintmodel/constraintmodel.py
"""
""" imports """
from ..mdb.pyecore.constraintmodel.constraintmodel import Constraint, ConstraintTypeEnum
from ..util.error import EoqError
from ..serialization.textserializer import TextSerializer

"""
    monkey patching constraint class for __str__ representation
"""
def PrettyPrintConstraint(obj):
    return f"CONSTRAINT:\t{obj.name}\n" \
           f"TYPE:\t\t{obj.constraintType}\n"\
           f"TARGET:\t\t{obj.target}\n" \
           f"FEATURE:\t{obj.feature}\n" \
           f"LAW:\t\t{obj.law}\n" \
           f"ANNOTATION:\t{obj.annotation}\n"
def PrettyRepresentConstraint(obj):
    return f"{obj.constraintType} CONSTRAINT:\'{obj.name}\'"
Constraint.__str__  = PrettyPrintConstraint
Constraint.__repr__ = PrettyRepresentConstraint


class ValidationCache:
    """
        Cache to store targets of constraints to ease the computational load.
        The targets are stored in a dictionary using the constraint objects hash as a key.
    """

    def __init__(self):
        self.constraintTargetDict = {}

    def __getitem__(self, constraint):
        # cache can be searched by directly indexing using a constraint object
        constraintHash = str(constraint.__hash__())
        return self.constraintTargetDict[constraintHash]

    def __str__(self):
        return str(self.constraintTargetDict)

    def Contains(self, constraint):
        return str(constraint.__hash__()) in self.constraintTargetDict

    def Update(self, constraint, target):
        constraintHash = str(constraint.__hash__())
        self.constraintTargetDict[constraintHash] = target

    def Clear(self):
        self.constraintTargetDict = {}


class ValidationManager():
    """
        Runs the constraints to validate their status.
        It is triggered externally by the commandrunner if XXX is executed.
        It shall trigger events and exceptions of constraints are violated.
    """

    def __init__(self, cmdRunner):
        super().__init__()

        # init attributes
        self.constraints = []
        self.cache = ValidationCache()
        
        # connect domain access
        self.cmdRunner = cmdRunner

        # init text serializer
        self.serializer = TextSerializer()
        
        # load constraints from workspace
        self.loadConstraints()

    @staticmethod
    def _StripParenthese(string):
        if string[0] == "(" and string[-1] == ")" and len(string)>2:
            return string[1:-1]

    def _RunCmd(self, cmd, tid):
        """
            untracked execution of cmd to get constraint targets and law
        """
        try:
            evaluator = self.cmdRunner.cmdEvaluators[cmd.cmd]
        except KeyError:
            raise EoqError(0,"Error evaluating command: Unknown command type: %s."%(cmd.cmd))
        return evaluator(cmd.a,tid)

    def _CalculateTarget(self, constraint, tid):
        """
            obtain targets from model
        """
        qry = "GET " + constraint.target
        cmd = self.serializer.Des(qry)
        try:
            return self._RunCmd(cmd, tid)
        except:
            raise EoqError(0,f"Could not resolve target of constraint \'{constraint.name}\'!")

    def _CacheTarget(self, constraint, tid):
        """
            updates cache
        """
        # TODO: review: the cache is always cleared after a ADD or REM was used (see commandrunner.py)
        target = self._CalculateTarget(constraint, tid)
        self.cache.Update(constraint, target)
        return target

    def GetTarget(self, constraint, tid):
        """
            gets constraint target, reads from cache if available
        """
        if self.cache.Contains(constraint):
            return self.cache[constraint]
        else:
            return self._CacheTarget(constraint, tid)

    def GetLawResults(self, constraint, tid):
        """
            evaluate constraint law on all targets
        """
        qry = "GET " + constraint.target + "/" + constraint.feature + constraint.law
        cmd = self.serializer.Des(qry)
        try:
            return self._RunCmd(cmd, tid)
        except:
            raise EoqError(0,f"Could not resolve law of constraint \'{constraint.name}\'")

    def GetLawResultsOnTarget(self, constraint, target, tid):
        """
            evaluate constraint law on single target
        """
        qry = "GET " + self.serializer.Ser(target) + "/" + constraint.feature + constraint.law
        cmd = self.serializer.Des(qry)
        try:
            return self._RunCmd(cmd, tid)
        except:
            raise EoqError(0, f"Could not resolve law of constraint \'{constraint.name}\'")

    def ClearCache(self):
        self.cache.Clear()

    def AddConstraint(self, constraintType, target, feature, law, name=None, annotation=None):
        if type(target) is not str:
            target = self._StripParenthese(self.serializer.Ser(target))
        if type(feature) is not str:
            feature = self._StripParenthese(self.serializer.Ser(feature))
        if type(law) is not str:
            law = self._StripParenthese(self.serializer.Ser(law))
        if name is None:
            name = "untitled constraint"
        if annotation is None:
            annotation = ""
        newConstraint = Constraint(constraintType=constraintType,
                                   target=target,
                                   feature=feature,
                                   law=law,
                                   name=name,
                                   annotation=annotation)
        self.cmdRunner.mdbAccessor.AddConstraint(newConstraint)
        self.constraints.append(newConstraint)
        self.cmdRunner.logger.Info(f"validation: added new constraint \'{newConstraint.name}\'")
        return newConstraint

    def RemoveConstraint(self, constraint):
        idx = self.constraints.index(constraint)
        self.cmdRunner.mdbAccessor.RemoveConstraint(constraint)
        del self.constraints[idx]
        self.cmdRunner.logger.Info(f"validation: removed constraint \'{constraint.name}\'")

    def RemoveAllConstraints(self):
        removed_constraint_target = []
        removed_constraint_feature = []
        removed_constraint_name = []
        for constraint in self.constraints:
            removed_constraint_target.append(constraint.target)
            removed_constraint_feature.append(constraint.feature)
            removed_constraint_name.append(constraint.name)
            self.RemoveConstraint(constraint)
        return removed_constraint_target,removed_constraint_feature,removed_constraint_name

    def GetConstraintsTargeting(self, obj, tid):
        """
            collects all constraints that target obj
        """
        constraintsTargetingObj = []
        if not(isinstance(obj,list)):
            obj = [obj]
        collect_constraints = self.GetObjectStructure(obj,constraintsTargetingObj,tid)
        return collect_constraints
        
    def GetObjectStructure(self, obj, constraintsTargetingObj, tid):
        for index in range(len(obj)):
            if isinstance(obj[index],list):
                emptylist = []
                constraintsTargetingObj.append(emptylist)
                new_obj = obj[index]
                self.GetObjectStructure(new_obj,emptylist,tid)
            else:
                listofconstraints = []
                for constraint in self.constraints:
                    target = self.GetTarget(constraint, tid)
                    if not(isinstance(target.v,list)):
                        target.v = [target.v]
                    if (obj[index] in target.v):
                        listofconstraints.append(constraint)
                constraintsTargetingObj.append(listofconstraints)
        return constraintsTargetingObj

        
    def GetConstraints(self):
        return self.constraints

    def IsConstraint(self, obj):
        return isinstance(obj, Constraint)

    def ValidateConstraint(self, constraint, tid):
        """
            validates a single constraint on all targets
        """
        # get targets
        target = self.GetTarget(constraint, tid)
        # get target/feature/law
        result = self.GetLawResults(constraint, tid)
        # evaluate
        if not(isinstance(result.v,list)):
            result.v = [result.v]
        if not(isinstance(target.v,list)):
            target.v = [target.v]
        if all(result.v):
            return True, target, constraint
        else:
            violatedBy = []
            for idx, res in enumerate(result.v):
                if res is False:
                    violatedBy.append(target.v[idx])
            if constraint.constraintType == "HARD":
                raise EoqError(0,f"validation: {violatedBy} violated hard constraint \'{constraint.name}\'!\nTransaction was cancelled after hard violation.")
            else:
                self.cmdRunner.logger.Warn(f"validation: {violatedBy} violated soft constraint \'{constraint.name}\'!")
            return False, target.v[idx], constraint

    def ValidateTarget(self,target,tid):
        """
            validates all constraints targeting a single target
        """
        # get constraints targeting target
        constraints = self.GetConstraintsTargeting(target, tid)
        # check target
        if isinstance(constraints[0],list):
            constraints = constraints[0]
        for constraint in constraints:
            result = self.GetLawResultsOnTarget(constraint,target, tid)
            if result.v is False:
                if constraint.constraintType == "HARD":
                    raise EoqError(0,f"validation: {target} violated HARD constraint \'{constraint.name}\'!")
                else:
                    self.cmdRunner.logger.Warn(f"validation: {target} violated SOFT constraint \'{constraint.name}\'!")
        return True


    def ValidateAll(self, tid):
        res = []
        result = []
        target = []
        con = []
        for constraint in self.constraints:
            res.append(self.ValidateConstraint(constraint, tid))
        for convert in res:
            result.append(convert[0])
            target.append(convert[1])
            con.append(convert[2])
        if all(result):
            self.cmdRunner.logger.Info(f"validation: successfully validated {len(res)} constraints. no violations found!")
        return result,target,con 
        
    def loadConstraints(self):
        index = None
        for i in range(len(self.cmdRunner.mdbAccessor.root_obj.eContents)):
            if self.cmdRunner.mdbAccessor.root_obj.eContents[i].name == 'cdb.constraintmodel':
                index = i
        if not(index == None):
            for constraint in self.cmdRunner.mdbAccessor.root_obj.eContents[index].eContents[0].constraint:
                self.constraints.append(Constraint(constraintType=str(constraint.constraintType),
                                            target=constraint.target,
                                            feature=constraint.feature,
                                            law=constraint.law,
                                            name=constraint.name,
                                            annotation=constraint.annotation))
        print("constraint list after load:",self.constraints)