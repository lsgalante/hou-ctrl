import hou


def vector3Test(kwargs):
    print(kwargs["parms"][0])
    if len(kwargs["parms"]) == 3\
    and kwargs["parms"][0].parmTemplate().type()==hou.parmTemplateType.Float\
    and kwargs["parms"][1].parmTemplate().type()==hou.parmTemplateType.Float\
    and kwargs["parms"][2].parmTemplate().type()==hou.parmTemplateType.Float:
        return True
    else:
        return False
    

def setVector3(kwargs, x, y, z):
    name0 = kwargs["parms"][0].name()
    name1 = kwargs["parms"][1].name()
    name2 = kwargs["parms"][2].name()
    node = kwargs["parms"][0].node()
    node.setParmExpressions({name0: x, name1: y, name2: z})


def vector3XMaster(kwargs):
    name0 = kwargs["parms"][0].name()
    name1 = kwargs["parms"][1].name()
    name2 = kwargs["parms"][2].name()
    node = kwargs["parms"][0].node()
    node.setParmExpressions({name1: "ch('"+name0+"')", name2: "ch('"+name0+"')"})
