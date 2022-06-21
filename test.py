import re
def createPolicy():
        print ("Type \"no\" to end add the policy")
        policy = []
        _policy = ""
        _str = ""
        while (True):
            _str = raw_input("Add attribute who can access: ")
            if (_str not in ['no', 'No', 'nO', 'NO']):
                if (_policy != ""):
                    _policy = _policy + " or "
                _policy = _policy + "(" +_str + ")"
                attributes = re.split(r' and ', _str)
                y = []
                for attr in attributes:
                    y.append(attr)
                policy.append(y)
            else:
                break
        return (_policy, str(policy))

(p, _p) = createPolicy()
print(p)
print(_p)