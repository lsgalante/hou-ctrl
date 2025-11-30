import hou


def vector3Test(kwargs):
    parms = kwargs['parms']
    print(parms[0])
    if len(parms) == 3 \
    and parms[0].parmTemplate().type() == hou.parmTemplateType.Float \
    and parms[1].parmTemplate().type() == hou.parmTemplateType.Float \
    and parms[2].parmTemplate().type() == hou.parmTemplateType.Float:
        return True
    else:
        return False

def setVector3(kwargs, x, y, z):
    parms = kwargs['parms']
    name0 = parms[0].name()
    name1 = parms[1].name()
    name2 = parms[2].name()
    node = parms[0].node()
    node.setParmExpressions({name0: x, name1: y, name2: z})

def vector3XMaster(kwargs):
    name0 = parms[0].name()
    name1 = parms[1].name()
    name2 = parms[2].name()
    node = parms[0].node()
    node.setParmExpressions({name1: 'ch("'+name0+'")', name2: 'ch("'+name0+'")'})
