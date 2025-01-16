import traceback

class Run:
    error = None
    out = None
    errorlst = []

    def reg(errorlst):
        for error in errorlst:
            Run.errorlst.append(error)

    def run(function, args):
        try:
            Run.out = None
            if args:
                Run.out = function(*args)
            else:
                Run.out = function()

        except Exception as ex:
            Run.error = ex

        return Run
    
    def hasreg(error):
        for etype in Run.errorlst:
            if isinstance(error, etype):
                return True
            
        return False

    def onerror(errortype : type, function, args, debug : bool = False):
        if not Run.error:
            return Run
        
        if errortype:
            if isinstance(Run.error, errortype):
                function(*args)

        elif Run.hasreg(Run.error):
            function(*args)

        if debug:
            traceback.print_exception(Run.error)

        return Run


