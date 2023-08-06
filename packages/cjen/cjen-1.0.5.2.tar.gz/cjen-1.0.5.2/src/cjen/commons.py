from pyclbr import Function


def __get_annotations__(method):
    if "__closure__" not in dir(method): return None
    if not method.__closure__ and method.__name__ != "__inner__": return method.__annotations__
    for cell in method.__closure__:
        val = __get_annotations__(cell.cell_contents)
        if val: return val
    return None


def _get_method_params(*, method):
    def __wrapper__(func):
        def __inner__(ins, *args, **kwargs):
            # if method.__closure__:
            #     for cell in method.__closure__:
            #         if "__closure__" not in dir(cell.cell_contents) and not cell.cell_contents.__closure__:
            #             kwargs["method.__annotations__"] = cell.cell_contents.__annotations__
            # else:
            #     kwargs["method.__annotations__"] = method.__annotations__
            kwargs["method.__annotations__"] = __get_annotations__(method)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__
