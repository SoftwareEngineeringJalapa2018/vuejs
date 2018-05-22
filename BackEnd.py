from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
from flask_cors import CORS

import json
import datetime
import pymssql


server = 'ALVARO-PC'            #Nombre del Motor SQL
database = 'AdventureWorks2014' #Base De Datos 
username = 'sa'                 #Usario
password = 'gudiel123'          #contrasena

#app = Flask(__name__)

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__,  static_url_path='/static')
CORS(app)

api = Api(app)

class QUERY_2(Resource):
    def get(self):
        conn = pymssql.connect(server, username, password, database)
        result = query_db(conn, "SELECT \
                                    PCS.ProductSubcategoryID, PCS.Name,\
                                    SUM(WO.StockedQty) AS WorkOrderQty, \
                                    SUM(WR.ActualCost* WO.OrderQty) AS WorkOrderCost,\
                                    SUM(CAST(POD.OrderQty  AS bigint)) PurchaseOrderQty,\
                                    SUM(POD.UnitPrice*POD.OrderQty) AS PurchaseOrderCost \
                                    FROM Purchasing.PurchaseOrderDetail POD\
                                    INNER JOIN Production.Product P ON POD.ProductID=POD.ProductID\
                                    INNER JOIN Production.ProductSubcategory PCS ON P.ProductSubcategoryID=PCS.ProductSubcategoryID\
                                    INNER JOIN Production.WorkOrder WO ON P.ProductID=WO.ProductID\
                                    INNER JOIN Production.WorkOrderRouting WR ON WR.WorkOrderID = WO.WorkOrderID\
                                    where year(WO.StartDate)=2014 \
                                    GROUP BY PCS.ProductSubcategoryID, PCS.Name")
        json_result = (json.dumps(result)) 
        return jsonify(result)

class QUERY_1(Resource):
    def get(self):
        conn = pymssql.connect(server, username, password, database)
        result = query_db(conn, "SELECT top 10 \
                                P.ProductID, \
                                P.Name as ProductName, \
                                SUM(PIV.Quantity) AS Stock, \
                                SUM(SOD.OrderQty) AS QuantitySold,\
                                MAX(SOH.OrderDate) AS LastSoldDate,\
                                (select TOP 1 pe.LastName + ' ' + pe.FirstName\
                                from Sales.SalesOrderDetail sd\
                                inner join Sales.SalesOrderHeader soh on sd.SalesOrderID =soh.SalesOrderID\
                                inner join Sales.Customer c on soh.CustomerID=c.CustomerID\
                                inner join Person.Person pe on c.PersonID=pe.BusinessEntityID\
                                where ProductID = P.ProductID\
                                GROUP BY pe.LastName + ' ' + pe.FirstName\
                                ORDER BY COUNT(1) DESC) as BestCustomer\
                                FROM Production.ProductInventory PIV\
                                INNER JOIN Production.Product P ON PIV.ProductID=P.ProductID\
                                INNER JOIN Sales.SalesOrderDetail SOD ON P.ProductID = SOD.ProductID\
                                INNER JOIN Sales.SalesOrderHeader SOH ON SOD.SalesOrderID = SOH.SalesOrderID\
                                GROUP By  P.ProductID, P.Name\
                                ORDER By  Stock asc,QuantitySold desc")
        json_result = (json.dumps(result)) 
        return jsonify(result)
	
       
def query_db(connection, query, args=(), one=False):
    cur = connection.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], str(value)) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

api.add_resource(QUERY_1, '/Produccion/Sales/Money') # Route_1
api.add_resource(QUERY_2, '/Produccion/Sales/Qty') # Route_2

if __name__ == '__main__':
  #app.run(ssl_context=('cert.pem', 'key.pem'),host='localhost', port=5000)
   app.run()
