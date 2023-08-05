import json
from  pyrdo.dict import list_as_dict
def billStatus(res_str,FBillNo='abc',FActionName='保存'):
    res_obj = json.loads(res_str)
    # print(res_obj)
    flag = res_obj['Result']['ResponseStatus']['IsSuccess']
    if flag:
        msg = "单据" + FBillNo + ""+FActionName+"成功"
        res = {"status": flag, "data": FBillNo, "msg": msg}
    else:
        error = res_obj['Result']['ResponseStatus']['Errors'][0]['Message']
        res = {"status": flag, "data": FBillNo, "msg": error}
    return (res)

def billQuery_aux(res_str):
    res_obj = json.loads(res_str)
    keys = "FBillNo,FDate,FApproveDate,FDocumentStatus"
    keys_list = keys.split(",")
    ncount = len(res_obj)
    res = []
    if ncount >0:
        for item in res_obj:
            cell = list_as_dict(keys_list,item)
            if cell['FApproveDate'] is None:
                cell['FApproveDate'] ='1984-01-01'
            if cell['FDocumentStatus'] == 'C':
                cell['FDocumentStatus'] ='已审核'
            else:
                cell['FDocumentStatus'] = '重新审核'
            res.append(cell)
    return(res)










