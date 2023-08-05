'''
 * this file is wrapper for K3CloudApiSdk
 * version is 3.0
'''
from k3cloud_webapi_sdk.main import K3CloudApiSdk

'''
 * the follow code show the way to test in local mode
'''
# from rderp.main import ErpClient
# from rderp.model import Model

'''
* the follow code show the way to refer inner the package.
* check this setting before publish the code into new package.

'''
from ..main import ErpClient
from ..util import billStatus
from ..util import billQuery_aux
from ..apiAuth import api_getInfo
from ..billModel import BillModel
from .saleDeliveryNotice import SaleDeliveryNotice
import json
'''
* class definition for material object in ERP system
'''


class SaleOutStock(ErpClient):
    def __init__(self, api_token='BEC6002E-C3AE-4947-AD70-212CF2B4218B',
                 meta_token="AD64F20D-6063-4E87-81E8-A24C1751D758",
                 timeout=120):
        self.api_token = api_token
        self.meta_token =meta_token
        data_info = api_getInfo(api_token=self.api_token)
        # print(data_info)
        self.acct_id = data_info['Facct_id']
        self.user_name = data_info['Fuser_name']
        # print(self.user_name)
        self.app_id = data_info['Fapp_id']
        self.app_secret = data_info['Fapp_secret']
        self.server_url = data_info['Fserver_url']
        self.timeout = timeout
        self.token = self.meta_token
        ErpClient.__init__(self, acct_id=self.acct_id, user_name=self.user_name, app_id=self.app_id,
                           app_secret=self.app_secret, server_url=self.server_url, timeout=self.timeout)

    def Meta(self):
        '''
        query the business info or metadata info for material.
        :return:
        '''
        data = {"FormId": "SAL_OUTSTOCK"}
        res = ErpClient.QueryBusinessInfo(self, data=data)
        return (res)

    def View(self, FBillNo='XSCKD2022050001'):
        '''
        * material view / query opration,see the detail infomation each in one material
        :param Number: the number of material
        :param CreateOrgId: the Create orginazation of the material,default is 0
        :param Id: the inner code for material
        :return: the return value is a json formmated data
        '''
        '''
        * to do list:
        * 1. add the function to deal the return value.
        '''
        CreateOrgId = 0
        Id = ""
        self.Number = FBillNo
        self.CreateOrgId = CreateOrgId
        self.Id = Id
        '''
        * create the data for material.View opration
        '''
        data = {
            "CreateOrgId": self.CreateOrgId,
            "Number": self.Number,
            "Id": self.Id}
        res_str = ErpClient.View(self, formid="SAL_OUTSTOCK", data=data)
        res_obj = json.loads(res_str)
        status = res_obj['Result']['ResponseStatus']['IsSuccess']
        res ={}
        if status:
            data = res_obj['Result']['Result']
            data_entry = data['SAL_OUTSTOCKENTRY']
            ncount = len(data_entry)
            # print(data)
            res['status'] = status
            res['data'] = FBillNo
            if ncount >0:
                item = []
                app_sd = SaleDeliveryNotice(api_token=self.api_token,meta_token=self.meta_token)
                for i in range(ncount):
                    cell = {}

                    cell['FId'] = data['Id']
                    cell['FBillNo'] = data['BillNo']
                    cell['FBillTypeID'] = data['BillTypeID']['Id']
                    cell['FBillTypeNumber'] = data['BillTypeID']['Number']
                    cell['FBillTypeName'] = data['BillTypeID']['Name'][0]['Value']
                    cell['FDocumentStatus'] = data['DocumentStatus']
                    cell['FSaleOrgId'] = data['SaleOrgId']['Id']
                    cell['FSaleOrgNumber'] = data['SaleOrgId']['Number']
                    cell['FSaleOrgName'] = data['SaleOrgId']['Name'][0]['Value']
                    cell['FDate'] = data['Date']
                    cell['FStockOrgId'] = data['StockOrgId']['Id']
                    cell['FStockOrgNumber'] = data['StockOrgId']['Number']
                    cell['FStockOrgName'] = data['StockOrgId']['Name'][0]['Value']
                    cell['FCustomerID'] = data['CustomerID']['Id']
                    cell['FCustomerNumber'] = data['CustomerID']['Number']
                    cell['FCustomerName'] = data['CustomerID']['Name'][0]['Value']
                    cell['FSaleDeptId'] = data['CustomerID']['SALDEPTID']['Id']
                    cell['FSaleDeptNumer'] = data['CustomerID']['SALDEPTID']['Number']
                    cell['FSaleDeptName'] = data['CustomerID']['SALDEPTID']['Name'][0]['Value']
                    cell['FSaleGroupId'] = data['CustomerID']['SALGROUPID']['Id']
                    cell['FSaleGroupNumber'] = data['CustomerID']['SALGROUPID']['Number']
                    cell['FSaleGroupName'] = data['CustomerID']['SALGROUPID']['Name'][0]['Value']
                    cell['FSellerId'] = data['CustomerID']['SELLER']['Id']
                    cell['FSellerNumber'] = data['CustomerID']['SELLER']['Number']
                    cell['FSellerName'] = data['CustomerID']['SELLER']['Name'][0]['Value']
                    cell['FPriceListId'] = data['CustomerID']['PRICELISTID']['Id']
                    cell['FPriceListNumber'] = data['CustomerID']['PRICELISTID']['Number']
                    cell['FPriceListName'] = data['CustomerID']['PRICELISTID']['Name'][0]['Value']
                    cell['F_SZSP_KHFL_Id'] = data['CustomerID']['F_SZSP_KHFL']['Id']
                    cell['F_SZSP_KHFL_Number'] = data['CustomerID']['F_SZSP_KHFL']['Number']
                    cell['F_SZSP_KHFL_Name'] = data['CustomerID']['F_SZSP_KHFL']['Name'][0]['Value']
                    cell['FCustTypeId'] = data['CustomerID']['CustTypeId']['Id']
                    cell['FCustTypeNumber'] = data['CustomerID']['CustTypeId']['Number']
                    cell['FCustTypeName'] = data['CustomerID']['CustTypeId']['Name'][0]['Value']
                    cell['FCreateDate'] = data['FCreateDate']
                    cell['FCreatorId'] = data['FCreatorId']['Id']
                    cell['FCreatorName'] = data['FCreatorId']['Name']
                    if data['ApproveDate'] is None:
                        data['ApproveDate'] = '1984-01-01'
                    cell['FApproveDate'] = data['ApproveDate']
                    if data['ApproverID'] is None:
                        cell['FApproverID'] = 0
                        cell['FApproverName'] = ''
                    else:
                        cell['FApproverID'] = data['ApproverID']['Id']
                        cell['FApproverName'] = data['ApproverID']['Name']
                    cell['FBussinessType'] = data['BussinessType']
                    cell['FNote'] = data['Note']
                    if data['F_SZSP_XSLX'] is None:
                        cell['F_SZSP_XSLX'] = ''
                    else:
                        cell['F_SZSP_XSLX'] = data['F_SZSP_XSLX']
                    cell['F_SZSP_Remarks'] = data['F_SZSP_Remarks']
                    cell['FLocalCurrID'] = data['SAL_OUTSTOCKFIN'][0]['LocalCurrID']['Id']
                    cell['FLocalCurrNumber'] = data['SAL_OUTSTOCKFIN'][0]['LocalCurrID']['Number']
                    cell['FLocalCurrName'] = data['SAL_OUTSTOCKFIN'][0]['LocalCurrID']['Name'][0]['Value']
                    cell['FExchangeTypeID'] = data['SAL_OUTSTOCKFIN'][0]['ExchangeTypeID']['Id']
                    cell['FExchangeTypeNumber'] = data['SAL_OUTSTOCKFIN'][0]['ExchangeTypeID']['Number']
                    cell['FExchangeTypeName'] = data['SAL_OUTSTOCKFIN'][0]['ExchangeTypeID']['Name'][0]['Value']
                    cell['FExchangeRate'] = data['SAL_OUTSTOCKFIN'][0]['ExchangeRate']
                    cell['SettleCurrID'] = data['SAL_OUTSTOCKFIN'][0]['SettleCurrID']['Id']
                    cell['SettleCurrNumber'] = data['SAL_OUTSTOCKFIN'][0]['SettleCurrID']['Number']
                    cell['SettleCurrName'] = data['SAL_OUTSTOCKFIN'][0]['SettleCurrID']['Name'][0]['Value']
                    cell['FEntryId'] = data_entry[i]['Id']
                    cell['FSeq'] = data_entry[i]['Seq']
                    cell['FMaterialID'] = data_entry[i]['MaterialID']['Id']
                    cell['FMaterialNumber'] = data_entry[i]['MaterialID']['Number']
                    cell['FMaterialName'] = data_entry[i]['MaterialID']['Name'][0]['Value']
                    cell['FMaterialModel'] = data_entry[i]['MaterialID']['Specification'][0]['Value']
                    cell['FMaterialGroupNumber'] = data_entry[i]['MaterialID']['MaterialGroup']['Number']
                    cell['FMaterialGroupName'] = data_entry[i]['MaterialID']['MaterialGroup']['Name'][0]['Value']
                    cell['F_SZSP_CPDL_Id'] = data_entry[i]['MaterialID']['F_SZSP_CPDL']['Id']
                    cell['F_SZSP_CPDL_Number'] = data_entry[i]['MaterialID']['F_SZSP_CPDL']['Number']
                    cell['F_SZSP_CPDL_Name'] = data_entry[i]['MaterialID']['F_SZSP_CPDL']['Name'][0]['Value']
                    cell['FCategoryID'] = data_entry[i]['MaterialID']['MaterialBase'][0]['CategoryID']['Id']
                    cell['FCategoryNumber'] = data_entry[i]['MaterialID']['MaterialBase'][0]['CategoryID']['Number']
                    cell['FCategoryName'] = data_entry[i]['MaterialID']['MaterialBase'][0]['CategoryID']['Name'][0]['Value']
                    cell['FUnitID'] = data_entry[i]['UnitID']['Id']
                    cell['FUnitNumber'] = data_entry[i]['UnitID']['Number']
                    cell['FUnitName'] = data_entry[i]['UnitID']['Name'][0]['Value']
                    cell['FMustQty'] = data_entry[i]['MustQty']
                    cell['FRealQty'] = data_entry[i]['RealQty']
                    cell['FStockID'] = data_entry[i]['StockID']['Id']
                    cell['FStockNumber'] = data_entry[i]['StockID']['Number']
                    cell['FStockName'] = data_entry[i]['StockID']['Name'][0]['Value']
                    if cell['FStockNumber'] == '1.1.1':
                        cell['FStockLocID'] = data_entry[i]['StockLocID']['F100003']['Id']
                        cell['FStockLocNumber'] = data_entry[i]['StockLocID']['F100003']['Number']
                        cell['FStockLocName'] = data_entry[i]['StockLocID']['F100003']['Name'][0]['Value']
                    cell['FLot'] = data_entry[i]['Lot']['Name'][0]['Value']
                    cell['FIsFree'] =data_entry[i]['IsFree']
                    cell['FPriceUnitId'] = data_entry[i]['PriceUnitId']['Id']
                    cell['FPriceUnitNumber'] = data_entry[i]['PriceUnitId']['Number']
                    cell['FPriceUnitName'] = data_entry[i]['PriceUnitId']['Name'][0]['Value']
                    cell['FPriceUnitQty'] =  data_entry[i]['PriceUnitQty']
                    cell['FPrice'] = data_entry[i]['Price']
                    cell['FTaxPrice'] = data_entry[i]['TaxPrice']
                    cell['FTaxRate'] = data_entry[i]['TaxRate']
                    cell['FAmount'] = data_entry[i]['Amount']
                    cell['FAmount_LC'] = data_entry[i]['Amount_LC']
                    cell['FTaxAmount'] = data_entry[i]['TaxAmount']
                    cell['FTaxAmount_LC'] = data_entry[i]['TaxAmount_LC']
                    cell['FAllAmount'] = data_entry[i]['AllAmount']
                    cell['FAllAmount_LC'] = data_entry[i]['AllAmount_LC']
                    cell['FEntity_Link_RuleId'] =data_entry[i]['FEntity_Link'][0]['RuleId']
                    cell['FEntity_Link_STableName'] = data_entry[i]['FEntity_Link'][0]['STableName']
                    cell['FEntity_Link_SBillId'] = data_entry[i]['FEntity_Link'][0]['SBillId']
                    cell['FEntity_Link_SId'] = data_entry[i]['FEntity_Link'][0]['SId']
                    info_src = app_sd.QueryBillNoByEntryId(FId=cell['FEntity_Link_SBillId'],
                                                                     FEntryId=cell['FEntity_Link_SId'])
                    if info_src['status']:
                        cell['FSrcBillNo'] = info_src['msg'][0]['FBillNo']
                        cell['FSrcSeq'] = info_src['msg'][0]['FSeq']
                    else:
                        cell['FSrcBillNo'] = ''
                        cell['FSrcSeq'] = ''



                    item.append(cell)
                res['msg'] = item

        return (res)

    def Save_demo(self, FNumber='API-01', FName='demo-02'):
        self.FNumber = FNumber
        self.FName = FName
        data = {"Model": {
            "FBillTypeID": {"FNUMBER": "XSDD01_SYS"},
            "FBillNo": "so-api-002",
            "FDate": "2022-04-16 00:00:00",
            "FSaleOrgId": {"FNumber": "100"},
            "FCustId": {"FNumber": "100011"},
            "FHeadDeliveryWay": {"FNumber": "JHFS01_SYS"},
            "FReceiveId": {"FNumber": "100011"},
            "FHEADLOCID": {"FNumber": "BIZ202103081002351"},
            "FSaleDeptId": {"FNumber": "BM000003"},
            "FSaleGroupId": {"FNumber": "XS021"},
            "FSalerId": {"FNumber": "HR043_GW000052_1"},
            "FSettleId": {"FNumber": "100011"},
            "FChargeId": {"FNumber": "100011"},
            # "FISINIT": 'false',
            # "FIsMobile": 'false',
             "F_RQAE_Commission": 'false',
             "F_RQAE_HC": 'false',
             "F_RQAE_AC": 'false',
            "F_SZSP_XSLX": {"FNumber": "1"},
            "F_SZSP_JJCD": {"FNumber": "JJ"},
            "F_SZSP_NMJSY": "个人客户",
            "FSaleOrderFinance": {
                "FSettleCurrId": {"FNumber": "PRE001"},
                "FRecConditionId": {"FNumber": "SKTJ01_SP"},
                "FIsPriceExcludeTax": 'true',
                "FSettleModeId": {"FNumber": "JSFS04_SYS"},
                "FIsIncludedTax": 'true',
                "FExchangeTypeId": {"FNumber": "HLTX01_SYS"}
                #,
                # "FOverOrgTransDirect": 'false'
            },
            "FSaleOrderEntry": [
                {"FRowType": "Standard",
                "FMaterialId": {"FNumber": "300201-1"},
                "FUnitID": {"FNumber": "carton"},
                "FQty": 200.0,
                "FPriceUnitId": {"FNumber": "carton"},
                "FPrice": 442.477876,
                "FTaxPrice": 500.0,
                "FIsFree": 'false',
                "FEntryTaxRate": 13.00,
                "FDeliveryDate": "2022-04-16 17:20:04",
                "FStockOrgId": {"FNumber": "100"},
                "FSettleOrgIds": {"FNumber": "100"},
                "FSupplyOrgId": {"FNumber": "100"},
                "FOwnerTypeId": "BD_OwnerOrg",
                "FOwnerId": {"FNumber": "100"},
                "F_SZSP_YWTC": 50.00,
                "FReserveType": "1",
                "FPriceBaseQty": 200.0,
                # "FStockUnitID": {"FNumber": "carton"},
                # "FStockQty": 200.0,
                # "FStockBaseQty": 200.0,
                # "FOUTLMTUNIT": "SAL",
                # "FOutLmtUnitID": {"FNumber": "carton"},
                "FISMRP": 'false',
                "F_SZSP_FSPC1": 'false',
                "FAllAmountExceptDisCount": 100000.0,
                "F_SZSP_ZLTC": 5.56
                    # ,
                # "FOrderEntryPlan": [{
                #     "FDetailLocId": {"FNumber": "BIZ202103081002351"},
                #     "FPlanDate": "2022-04-16 17:20:04",
                #     "FPlanQty": 200.0
                #     }]
                },
                {
                "FRowType": "Standard",
                "FMaterialId": {"FNumber": "300203-1"},
                "FUnitID": {"FNumber": "carton"},
                "FQty": 400.0,
                "FPriceUnitId": {"FNumber": "carton"},
                "FPrice": 530.973451,
                "FTaxPrice": 600.0,
                "FIsFree": 'false',
                "FEntryTaxRate": 13.00,
                "FDeliveryDate": "2022-04-16 17:20:26",
                "FStockOrgId": {"FNumber": "100"},
                "FSettleOrgIds": {"FNumber": "100"},
                "FSupplyOrgId": {"FNumber": "100"},
                "FOwnerTypeId": "BD_OwnerOrg",
                "FOwnerId": {"FNumber": "100"},
                "F_SZSP_YWTC": 120.00,
                "FReserveType": "1",
                "FPriceBaseQty": 400.0,
                # "FStockUnitID": {"FNumber": "carton"},
                # "FStockQty": 400.0,
                # "FStockBaseQty": 400.0,
                # "FOUTLMTUNIT": "SAL",
                # "FOutLmtUnitID": {"FNumber": "carton"},
                "FISMRP": 'false',
                "F_SZSP_FSPC1": 'false',
                "FAllAmountExceptDisCount": 240000.0,
                "F_SZSP_ZLTC": 13.33
                #    ,
                # "FOrderEntryPlan": [{
                #     "FDetailLocId": {"FNumber": "BIZ202103081002351"},
                #     "FPlanDate": "2022-04-16 17:20:26",
                #     "FPlanQty": 400.0
                #     }]
                }
                ],
                "FSaleOrderPlan": [
                    {
                    "FNeedRecAdvance": 'true',
                    "FRecAdvanceRate": 10.0000000000,
                    "FRecAdvanceAmount": 34000.00,
                    "FIsOutStockByRecamount": 'false'
                    },
                    {
                        "FNeedRecAdvance": 'false',
                        "FRecAdvanceRate": 90.0000000000,
                        "FRecAdvanceAmount": 306000.00,
                        "FIsOutStockByRecamount": 'false'
                    }
                ]
            }
            }
        res = ErpClient.Save(self, formid="SAL_OUTSTOCK", data=data)
        return (res)

    def Save(self, FBillNo='so-api-002'):
        '''
        Save option is new material without materialID.
        :param data:
        :return:
        '''
        self.FBillNo = FBillNo
        app = BillModel(token=self.token, FFormId='SAL_OUTSTOCK', FActionName='Save')
        data = app.dataGen(FBillNo=self.FBillNo)
        print(data)
        res_str = ErpClient.Save(self, formid="SAL_OUTSTOCK", data=data)
        res_obj = json.loads(res_str)
        res = res_obj['Result']['ResponseStatus']['IsSuccess']
        return (res)

    def Modify(self, data):
        '''
        Modify is base on the Save option with aditional part is FMATERIALID
        :param data:
        :return:
        '''
        res = ErpClient.Save(self, formid="SAL_OUTSTOCK", data=data)
        return (res)

    def BillQuery(self, FApproveDate = '2022-05-01'):
        '''
        query the list of material.
        :param FieldKeys:
        :param FilterString:[{"Left":"(","FieldName":"Field1","Compare":"=","Value":"111","Right":")","Logic":"AND"},{"Left":"(","FieldName":"Field2","Compare":"=","Value":"222","Right":")","Logic":""}]
            1、Left：左括号
            2、FieldName：字段名
            3、Compare：比较运算符，如　大于">"、小于"<"、等于"="、包含"like"、左包含"llike"、右包含"rlike"
            4、Value：比较值
            5、Right：右括号
            6、Logic：逻辑运算符，如 "and"、"or"
        :param OrderString:
        :param TopRowCount:
        :param StartRow:
        :param Limit:
        :return:
        '''
        OrderString = ""
        TopRowCount = 0
        StartRow = 0
        Limit = 0
        FilterString ="(FApproveDate is null and FDocumentStatus in ('D')) or (FApproveDate >= '"+FApproveDate+"' and FDocumentStatus in ('C')) "
        self.FieldKeys = "FBillNo,FDate,FApproveDate,FDocumentStatus"
        self.FilterString = FilterString
        self.TopRowCount = TopRowCount
        self.StartRow = StartRow
        self.Limit = Limit
        self.OrderString = OrderString
        data = {
            "FormId": "SAL_OUTSTOCK",
            "FieldKeys": self.FieldKeys,
            "FilterString": self.FilterString,
            "OrderString": self.OrderString,
            "TopRowCount": self.TopRowCount,
            "StartRow": self.StartRow,
            "Limit": self.Limit,
            "SubSystemId": ""
        }
        res_str = ErpClient.ExecuteBillQuery(self, data=data)
        res = billQuery_aux(res_str=res_str)
        return(res)

    def SaveBatch(self, data_list):
        '''
        *save the data in a batch list
        *put multiple save format data into a list
        :param data_list:
        :return:
        '''
        self.data_list = data_list
        save_data = {"Model": self.data_list}
        res = ErpClient.BatchSave(self, formid='SAL_OUTSTOCK', data=save_data)
        return (res)

    def SaveBatchAsync(self, data_list):
        '''
        *save the data in a batch list in Async way.
        *put multiple save format data into a list
        :param data_list:
        :return:
        '''
        self.data_list = data_list
        save_data = {"Model": self.data_list}
        res = ErpClient.BatchSaveQuery(self, formid='SAL_OUTSTOCK', data=save_data)
        return (res)

    def Submit(self, FBillNo):
        '''
        * the material Submit operation just after save.
        :param Numbers: list of material numbers
        :param Ids:   the Ids of material
        :param SelectedPostId: the SelectedPostId of material
        :param NetworkCtrl:  the NetworkCtrl status of material
        :param IgnoreInterationFlag: the Flag of material
        :return: without the return value or the status of Submit after exec.
        '''
        Numbers = [FBillNo]
        Ids = ""
        SelectedPostId = 0
        NetworkCtrl = ""
        IgnoreInterationFlag = ""
        self.Numbers = Numbers
        self.Ids = Ids
        self.SelectedPostId = SelectedPostId
        self.NetworkCtrl = NetworkCtrl
        self.IgnoreInterationFlag = IgnoreInterationFlag
        data = {
            "CreateOrgId": 0,
            "Numbers": self.Numbers,
            "Ids": self.Ids,
            "SelectedPostId": self.SelectedPostId,
            "NetworkCtrl": self.NetworkCtrl,
            "IgnoreInterationFlag": self.IgnoreInterationFlag
        }
        res_str = ErpClient.Submit(self, formid="SAL_OUTSTOCK", data=data)
        res_obj = json.loads(res_str)
        res = res_obj['Result']['ResponseStatus']['IsSuccess']
        return (res)

    def CancelAssign(self, Numbers=[], CreateOrgId=0, Ids="", NetworkCtrl=""):
        '''
        the Cancel operion for submit of material
        :param Numbers: list for number of material
        :param CreateOrgId: the CreateOrgId of material
        :param Ids: the Ids of material
        :param NetworkCtrl: the NetWorkCtrl of material
        :return: the return values
        '''
        self.Numbers = Numbers
        self.CreateOrgId = CreateOrgId
        self.Ids = Ids
        self.NetworkCtrl = NetworkCtrl
        data = {
            "CreateOrgId": self.CreateOrgId,
            "Numbers": self.Numbers,
            "Ids": self.Ids,
            "NetworkCtrl": self.NetworkCtrl
        }
        res = ErpClient.CancelAssign(self, formid="SAL_OUTSTOCK", data=data)
        return (res)

    def UnSubmit(self, Numbers=[], CreateOrgId=0, Ids="", NetworkCtrl=""):
        '''
        the oposite operation for submit
        :param Numbers:
        :param CreateOrgId:
        :param Ids:
        :param NetworkCtrl:
        :return:
        '''
        res = self.CancelAssign(Numbers=Numbers, CreateOrgId=CreateOrgId, Ids=Ids, NetworkCtrl=NetworkCtrl)
        return (res)

    def Audit(self, FBillNo):
        '''
        the Audit or Check operation of material.
        :param Numbers:
        :param CreateOrgId:
        :param Ids:
        :param InterationFlags:
        :param NetworkCtrl:
        :param IsVerifyProcInst:
        :param IgnoreInterationFlag:
        :return:
        '''
        Numbers = [FBillNo]
        CreateOrgId = 0
        Ids = ""
        InterationFlags = ""
        NetworkCtrl = ""
        IsVerifyProcInst = ""
        IgnoreInterationFlag = ""
        self.Numbers = Numbers
        self.CreateOrgId = CreateOrgId
        self.Ids = Ids
        self.InterationFlags = InterationFlags
        self.NetworkCtrl = NetworkCtrl
        self.IsVerifyProcInst = IsVerifyProcInst
        self.IgnoreInterationFlag = IgnoreInterationFlag
        data = {
            "CreateOrgId": self.CreateOrgId,
            "Numbers": self.Numbers,
            "Ids": self.Ids,
            "InterationFlags": self.InterationFlags,
            "NetworkCtrl": self.NetworkCtrl,
            "IsVerifyProcInst": self.IsVerifyProcInst,
            "IgnoreInterationFlag": self.IgnoreInterationFlag
        }
        res_str = ErpClient.Audit(self, formid="SAL_OUTSTOCK", data=data)
        res = billStatus(res_str=res_str,FBillNo=FBillNo,FActionName='审核')
        return (res)

    def Check(self, FBillNo):
        '''
        create the alias for Audit operation of material.
        :param Numbers:
        :param CreateOrgId:
        :param Ids:
        :param InterationFlags:
        :param NetworkCtrl:
        :param IsVerifyProcInst:
        :param IgnoreInterationFlag:
        :return:
        '''
        res = self.Audit(FBillNo=FBillNo)
        return (res)
    def ApiSave(self, FBillNo):
        self.Save(FBillNo=FBillNo)
        self.Submit(FBillNo=FBillNo)
        res = self.Check(FBillNo=FBillNo)
        return(res)
    def ApiDel(self,FBillNo):
        self.UnCheck(FBillNo=FBillNo)
        res = self.Delete(FBillNo=FBillNo)
        return(res)
    def UnAudit(self, FBillNo):
        Numbers = [FBillNo]
        CreateOrgId = 0
        Ids = ""
        InterationFlags = ""
        NetworkCtrl = ""
        IsVerifyProcInst = ""
        IgnoreInterationFlag = ""
        self.Numbers = Numbers
        self.CreateOrgId = CreateOrgId
        self.Ids = Ids
        self.InterationFlags = InterationFlags
        self.NetworkCtrl = NetworkCtrl
        self.IsVerifyProcInst = IsVerifyProcInst
        self.IgnoreInterationFlag = IgnoreInterationFlag
        data = {
            "CreateOrgId": self.CreateOrgId,
            "Numbers": self.Numbers,
            "Ids": self.Ids,
            "InterationFlags": self.InterationFlags,
            "IgnoreInterationFlag": self.IgnoreInterationFlag,
            "NetworkCtrl": self.NetworkCtrl,
            "IsVerifyProcInst": self.IsVerifyProcInst
        }
        res_str = ErpClient.UnAudit(self, formid="SAL_OUTSTOCK", data=data)
        res = billStatus(res_str=res_str,FBillNo=FBillNo,FActionName='反审核')
        return (res)

    def UnCheck(self, FBillNo):
        '''
        create the alias for UnAudit operation of material.
        :param Numbers:
        :param CreateOrgId:
        :param Ids:
        :param InterationFlags:
        :param NetworkCtrl:
        :param IsVerifyProcInst:
        :param IgnoreInterationFlag:
        :return:
        '''
        res = self.UnAudit(FBillNo=FBillNo)
        return (res)

    def Delete(self, FBillNo):
        '''
        the Delete operation of material
        :param Numbers:
        :param CreateOrgId:
        :param Ids:
        :param NetworkCtrl:
        :return:
        '''
        Numbers = [FBillNo]
        CreateOrgId = 0
        Ids = ""
        NetworkCtrl = ""
        self.Numbers = Numbers
        self.CreateOrgId = CreateOrgId
        self.Ids = Ids
        self.NetworkCtrl = NetworkCtrl
        data = {
            "CreateOrgId": self.CreateOrgId,
            "Numbers": self.Numbers,
            "Ids": self.Ids,
            "NetworkCtrl": self.NetworkCtrl
        }
        res_str = ErpClient.Delete(self, formid="SAL_OUTSTOCK", data=data)
        res_obj = json.loads(res_str)
        res = res_obj['Result']['ResponseStatus']['IsSuccess']
        return (res)
    def Push(self,FBillNo):
        data = {
            "Numbers": [FBillNo],
            "EntryIds": "",
            "RuleId": "SaleOrder-DeliveryNotice",
            "TargetBillTypeId": "",
            "TargetOrgId": 0,
            "TargetFormId": "SAL_DELIVERYNOTICE",
            "IsEnableDefaultRule": "false",
            "IsDraftWhenSaveFail": "false",
            "CustomParams": {}
        }
        res_str = ErpClient.Push(self,formid="SAL_OUTSTOCK",data=data)
        res_obj = json.loads(res_str)
        # print(res_obj)
        res = {}
        res['status'] = res_obj['Result']['ResponseStatus']['IsSuccess']
        if res['status']:
            res['data'] = res_obj['Result']['ResponseStatus']['SuccessEntitys'][0]['Number']
        else:
            res['data'] = res_obj['Result']['ResponseStatus']['Errors'][0]['Message']
        return(res)

    def Allocate(self, PrdIdString=0, OrgIdString=""):
        '''
        the Allocation operation of material to other organizations
        :param PrdIdString: the Ids string seperate by comma of material,not a list but a string,such as '333115,333116'
        :param OrgIdString: the Ids string seperate by comma of organizations,not a list but a string,'100201,100202'
        :return: return the status
        '''
        '''
        * to do list
        * 1. test the app Interface. done.
        * data6 =material.Allocate(PrdIdString='333115,333116',OrgIdString='100201,100202')
        * print(data6)
        '''
        self.PkIds = PrdIdString
        self.TOrgIds = OrgIdString
        data = {
            "PkIds": self.PkIds,
            "TOrgIds": self.TOrgIds
        }
        res = ErpClient.Allocate(self, formid="SAL_OUTSTOCK", data=data)
        return (res)

    def CancelAllocate(self, PrdIdString=0, OrgIdString=""):
        '''
        cancel the allocation of matrial.
        :param PrdIdString:
        :param OrgIdString:
        :return:
        '''
        self.PkIds = PrdIdString
        self.TOrgIds = OrgIdString
        data = {
            "PkIds": self.PkIds,
            "TOrgIds": self.TOrgIds
        }
        res = ErpClient.CancelAllocate(self, formid="SAL_OUTSTOCK", data=data)
        return (res)

    def UnAllocate(self, PrdIdString=0, OrgIdString=""):
        res = self.CancelAllocate(PrdIdString=PrdIdString, OrgIdString=OrgIdString)
        return (res)

    def ExcuteOperation(self, opNumber="Forbid", Numbers=[], CreateOrgId=0, Ids="", PkEntryIds=[], NetworkCtrl="",
                        IgnoreInterationFlag=""):
        self.opNumber = opNumber
        self.Numbers = Numbers
        self.CreateOrgId = CreateOrgId
        self.Ids = Ids
        self.PkEntryIds = PkEntryIds
        self.NetworkCtrl = NetworkCtrl
        self.IgnoreInterationFlag = IgnoreInterationFlag
        data = {
            "CreateOrgId": self.CreateOrgId,
            "Numbers": self.Numbers,
            "Ids": self.Ids,
            "PkEntryIds": self.PkEntryIds,
            "NetworkCtrl": self.NetworkCtrl,
            "IgnoreInterationFlag": self.IgnoreInterationFlag
        }
        res = ErpClient.ExcuteOperation(self, formid="SAL_OUTSTOCK", opNumber=self.opNumber, data=data)
        return (res)

    def Disable(self, Numbers=[], CreateOrgId=0, Ids="", PkEntryIds=[], NetworkCtrl="", IgnoreInterationFlag=""):
        '''
        the Disable or Forbid operation of material.
        :param Numbers:
        :param CreateOrgId:
        :param Ids:
        :param PkEntryIds:
        :param NetworkCtrl:
        :param IgnoreInterationFlag:
        :return:
        '''
        res = self.ExcuteOperation(opNumber='Forbid', Numbers=Numbers, CreateOrgId=CreateOrgId, Ids=Ids,
                                   PkEntryIds=PkEntryIds, NetworkCtrl=NetworkCtrl,
                                   IgnoreInterationFlag=IgnoreInterationFlag)
        return (res)

    def Enable(self, Numbers=[], CreateOrgId=0, Ids="", PkEntryIds=[], NetworkCtrl="", IgnoreInterationFlag=""):
        '''
        the Enable of material.
        :param Numbers:
        :param CreateOrgId:
        :param Ids:
        :param PkEntryIds:
        :param NetworkCtrl:
        :param IgnoreInterationFlag:
        :return:
        '''
        res = self.ExcuteOperation(opNumber='Enable', Numbers=Numbers, CreateOrgId=CreateOrgId, Ids=Ids,
                                   PkEntryIds=PkEntryIds, NetworkCtrl=NetworkCtrl,
                                   IgnoreInterationFlag=IgnoreInterationFlag)
        return (res)


if __name__ == '__main__':
    pass