import requests
from . import app
import mysql.connector

API_KEY=app.config['API_KEY']

cryptomonedas=("EUR","BTC","ETH","USDT","ADA","SOL","XRP","DOT","DOGE","SHIB")
URL ="https://rest.coinapi.io/v1/exchangerate/{orig}/{dest}"

MYSQL_HOST=app.config['MYSQL_HOST']
MYSQL_USER=app.config['MYSQL_USER']
MYSQL_PORT=app.config['MYSQL_PORT']
MYSQL_PASSWORD=app.config['MYSQL_PASSWORD']
MYSQL_DATABASE=app.config['MYSQL_DATABASE']

class CryptoCambio():
    def __init__(self, crypfrom, crypto):
        self.crypfrom = crypfrom
        self.crypto = crypto

    def exchange(self):
         headers = {

            "X-CoinAPI-Key": API_KEY

         }

         url = URL.format(orig=self.crypfrom, dest=self.crypto)
         response=requests.get(url,headers=headers)

         cambio = response.json()['rate']
         
         return cambio   
 
class DBManager :
    def __init__(self, host=MYSQL_HOST, user='kc_user', database='movimientos', password='password', port=MYSQL_PORT,):
        self.host = host
        self.user= user
        self.database= database
        self.password= password
        self.port= port

    def APIError(Exception):
        pass
        
    def ejecutarConParametros(self, sql, val):
        
        conexion = mysql.connector.connect( host=MYSQL_HOST, user=self.user, database=self.database, password=self.password, port=int(MYSQL_PORT) )
        cursor = conexion.cursor()
        resultado=False
        
        try:
            cursor.execute(sql, val)
            conexion.commit()
            resultado=True
        except Exception as  error:
            
            print(error)
            conexion.rollback()
            conexion.close()
    
        return resultado


    def querySQL(self, sql):
        
        conexion = mysql.connector.connect( host=MYSQL_HOST, user=self.user, database=self.database, password=self.password, port=int(MYSQL_PORT) )

        cursor = conexion.cursor()
        cursor.execute(sql)

        self.movimientos = []
        nombre_columna = []
        for tupla in cursor.description:
            nombre_columna.append(tupla[0])

        datos = cursor.fetchall()
        for tupla in datos:
            mov = {}
            indice = 0
            for nombre in nombre_columna:
                mov[nombre] = tupla[indice]
                indice += 1
            self.movimientos.append(mov)
            
        conexion.close()
    
        return self.movimientos

    def Saldo(self):
        saldoAcumulado = []
        for moneda in cryptomonedas:
            saldoMonedas = self.querySQL('''
                            WITH BALANCE 
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM movimientos 
                            WHERE to_currency LIKE "%{}%"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM movimientos 
                            WHERE from_currency LIKE "%{}%"
                            ) 
                            SELECT SUM(saldo)
                            FROM BALANCE;
                            '''.format(moneda,moneda))
            if saldoMonedas[0] == (None,):
                saldoMonedas=0
                saldoAcumulado.append(saldoMonedas)
            
            else:
                saldoAcumulado.append(saldoMonedas[0][0])  
    
        return saldoAcumulado                         

