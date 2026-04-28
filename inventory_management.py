import datetime
date=datetime.datetime.now()
class Data:
    def __init__(self, sku, name, category, unit, reorderLevel, currentStock, supplierId):
        self.sku = sku
        self.name = name
        self.category = category
        self.unit = unit
        self.reorderLevel = reorderLevel
        self.currentStock = currentStock
        self.supplierId = supplierId
    def __str__(self):
        return f"{self.sku} - {self.name} ({self.currentStock})"
class product:
    def __init__(self):
        self.stock = {}
        self.new_stock = False

    def add_stock(self, sku, name, category, unit, reorderLevel, currentStock, supplierId):
        if sku in self.stock:
            print("Data exists")
        else:
            self.stock[sku] = Data(sku, name, category, unit, reorderLevel, currentStock, supplierId)
            self.new_stock = True
            print("New stock added")

    def update_stock(self, sku, unit, reorderLevel, currentStock):
        if sku in self.stock:
            item = self.stock[sku]
            item.unit = unit
            item.reorderLevel = reorderLevel
            item.currentStock = currentStock
        else:
            print("Data not found")

    def get_stock(self):
        for item in self.stock.values():
            print(item)
class Supplier(product):
    def __init__(self,supplierid,name,contact,email,leadTimeDays):
        product.__init__(self,supplierid,name)
        self.suppliers={}
        self.products=[]
        self.contact=contact
        self.email=email
        self.leadTimeDays=leadTimeDays
    def createPO(self,supplierid,name,contact,email,leadTimeDays):
        if supplierid not in self.suppliers:
            self.products[supplierid]=Supplier.__init__(supplierid,name,contact,email,leadTimeDays,self.products)
        else:
            print("Already exist.")
    def getDeliveryHistory(self,leadTimeDays):
        if leadTimeDays == 'Delivered':
            for i in self.suppliers.values():
                print(i)

class PurchaseOrder():
    def __init__(self,poid,supplierid,status,createDate,approveDate):
        Supplier.__init__(self,supplierid)
        self.poid=poid
        self.status=status
        self.createDate=createDate
        self.approveDate=approveDate
        self.items={}
    def add_data(self,poid,supplierid,status,createDate,approveDate):
        if poid in self.items:
            print("Data exist")
        else:
            self.items[poid]=PurchaseOrder(poid,supplierid,status,createDate,approveDate)
    
    def send(self,poid):
        if poid in self.items:
            self.items[poid].status="send"
    def approve(self,status,poid):
        if status == 0:
            if poid in self.items:
                self.items[poid].status=status
                self.items[poid].approvedDate=date
                self.send(self,status,poid)
        else:
            if status == 1:
                print("product not approved")
    def receive(self,poid):
        self.items[poid].status='received'
    def cancel(self,poid):
         self.items[poid].status='cancel'



class GoodsReceived(PurchaseOrder):
    def __init__(self,grnid,poid,receivedDate,staffid):
        PurchaseOrder.__init__(self,poid)
        self.grnid=grnid
        self.receivedDate=receivedDate
        self.staffid=staffid
        self.receiveditems=[]
        self.grn={}
    def record(self,grnid,receivedDate,staffid,poid):
        self.grn[grnid]=GoodsReceived(grnid,poid,receivedDate,staffid,self.receiveditems)
    def flagDiscrepancy(self,grnid):
        if grnid in self.grn:
            self.receive()
    def close(self,grnid):
        if grnid in self.grn:
            self.cancel()
class StockMovement(product):
    def __init__(self,mid,sku,type,quantity,reason,staffid,timestamp):
        self.mid=mid
        self.type=type
        self.quantity=quantity
        self.reason=reason
        GoodsReceived.__init__(self,staffid)
        product.__init__(self,sku)
        self.timestamp=timestamp
        self.move={}
    def add_move(self,mid,sku,type,quantity,reason,staffid,timestamp):
        self.move[mid]=StockMovement(mid,sku,type,quantity,reason,staffid,timestamp)
    def log(self,unit,recorderLevel,currentStock):
        self.updateStock(unit,recorderLevel,currentStock)
    def getAuditTrail(self,unit,sku,currentStock):
        self.stock[sku].unit=unit-10000
        self.stock[sku].currentStock=currentStock-200

class warehouse(product,Supplier,StockMovement):
    def __init__(self,wid,name,location,products):
        self.wid=wid
        product.__init__(self,name)
        self.location=location
        Supplier.__init__(self,products)
        self.ware={}
    def add(self,wid,name,location,products):
        self.ware[wid]=warehouse(wid,name,location,products)
    def getDashboard(self):
        for i in self.ware.values():
            print(i)
        for i in self.suppliers.values():
            print(i)
        for i in self.stock.values():
            print(i)
    def triggerReorder(self,sku,unit,recorderLevel,currentStock):
        if sku in self.Product:
            if self.stock[sku].unit > 5:
                self.updateStock(unit,recorderLevel,currentStock)  
        else:
            print("no data found")
    def getalerts(self,new_stock,sku,unit,currentStock):
        if new_stock=="True":
            print("New stock have arrived.")
            self.new_stock="False"
        elif sku in self.Product:
            if self.stock[sku].unit > 5:
                self.new_unit=int(input())
                self.new_recorderlevel=input()
                self.new_currentstock=int(input())
                self.updateStock(self.new_unit,self.new_recorderlevel,self.new_currentstock)
            else:
                pass
        elif sku in self.stock:
            if unit > 50000 and currentStock > 500:
                self.getAuditTrail()


def main():
    s1=product()
    s2=Supplier()
    s3=PurchaseOrder()
    s4=GoodsReceived()
    s5=warehouse()
