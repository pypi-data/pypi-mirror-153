from MedatechUK.Serial import SerialBase , SerialT , SerialF

class xmlTransactions(SerialBase) :
    
    #region Properties
    @property
    def transactions(self): 
        return self._transactions
    @transactions.setter
    def transactions(self, value):
        self._transactions = []
        for i in range(len(value)):
            if len(value) > 1 :
                self._transactions.append(xmlTransactionsTransaction(**value["transaction"][i]))
            else :
                self._transactions.append(xmlTransactionsTransaction(**value["transaction"]))
    
    #endregion

    #region "ctor"
    def __init__(self,  **kwargs): 

        #region "Property defaults"
        self.transactions = []
        
        #endregion

        #region "Set Meta info"
        SerialBase.__init__(self , SerialF(fname="ZODA_TRANS", rt=1, typename="ORD"), **kwargs)          
        
        SerialT(self, "rt")
        SerialT(self, "bubbleid")
        SerialT(self, "typename")

        #endregion
    
    #endregion

class xmlTransactionsTransaction(SerialBase) :
    
    #region Properties
    @property
    def document(self): 
        return self._document
    @document.setter
    def document(self, value):    
        self._document = {}
        self._document = xmlTransactionsTransactionDocument(**value)
    
    @property
    def date(self): 
        return self._date
    @date.setter
    def date(self, value):
        self._date = value

    @property
    def type(self): 
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def vaultname(self): 
        return self._vaultname
    @vaultname.setter
    def vaultname(self, value):
        self._vaultname = value
    
    #endregion

    #region "ctor"
    def __init__(self,  **kwargs): 

        #region "Property defaults"  
        self._document = {}
        self._date = 0
        self._type = ""
        self._vaultname = ""
        
        #endregion

        #region "Set Meta info"
        SerialBase.__init__(self , SerialF(fname="Transaction", rt=2) , **kwargs)           
        
        SerialT(self, "rt")
        SerialT(self, "date" , pCol="INT1" , pType="INT")
        SerialT(self, "type" , pCol="TEXT2")
        SerialT(self, "vaultname", pCol="TEXT3")

        #endregion
    
    #endregion

class xmlTransactionsTransactionDocument(SerialBase) :
    
    #region Properties
    @property
    def configuration(self): 
        return self._configuration
    @configuration.setter
    def configuration(self, value):        
        self._configuration = xmlTransactionsTransactionDocumentConfiguration(**value)
    
    @property
    def aliasset(self): 
        return self._aliasset
    @aliasset.setter
    def aliasset(self, value):
        self._aliasset = value

    @property
    def id(self): 
        return self._id
    @id.setter
    def id(self, value):
        self._id = value        

    @property
    def idattribute(self): 
        return self._idattribute
    @idattribute.setter
    def idattribute(self, value):
        self._idattribute = value     

    @property
    def idcfgname(self): 
        return self._idcfgname
    @idcfgname.setter
    def idcfgname(self, value):
        self._idcfgname = value  

    @property
    def pdmweid(self): 
        return self._pdmweid
    @pdmweid.setter
    def pdmweid(self, value):
        self._pdmweid = value        


    #endregion

    #region "ctor"
    def __init__(self,  **kwargs): 

        #region "Property defaults"
        self._configuration = {}
        self._aliasset = ""
        self._pdmweid = ""     
        self._id = ""
        self._idattribute = ""
        self._idcfgname = ""

        #endregion

        #region "Set Meta info"
        SerialBase.__init__(self , SerialF(fname="Document", rt=3) , **kwargs)           

        SerialT(self, "rt")
        SerialT(self, "aliasset" , pCol="TEXT1" )
        SerialT(self, "pdmweid" , pCol="TEXT2" )
        SerialT(self, "id" , pCol="TEXT3" )
        SerialT(self, "idattribute" , pCol="TEXT4" )
        SerialT(self, "aliasset" , pCol="TEXT5" )
        SerialT(self, "idcfgname" , pCol="TEXT6" )

        #endregion
    
    #endregion

class xmlTransactionsTransactionDocumentConfiguration(SerialBase) :
    
    #region Properties
    @property
    def attribute(self): 
        return self._attribute
    @attribute.setter
    def attribute(self, value):    
        self._attribute = []   
        for i in range(len(value)):
            try:
                self._attribute.append(xmlTransactionsTransactionDocumentConfigurationAttribute(**value[i]))
            except:
                self._attribute.append(xmlTransactionsTransactionDocumentConfigurationAttribute(**value))

    @property
    def references(self): 
        return self._references
    @references.setter
    def references(self, value):
        self._references = []
        for i in range(len(value["document"])):
            self._references.append(xmlTransactionsTransactionDocument(**value['document'][i]))

    @property
    def name(self): 
        return self._name
    @name.setter
    def name(self, value):
        self._name = value 

    @property
    def quantity(self): 
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        self._quantity = value 

    #endregion

    #region "ctor"
    def __init__(self,  **kwargs): 

        #region "Property defaults"
        self._attribute = []
        self._references = []
        self._name = ""
        self._quantity = 0.0
        
        #endregion

        #region "Set Meta info"
        SerialBase.__init__(self , SerialF(fname="Configuration", rt=4) , **kwargs)   

        SerialT(self, "rt")        
        SerialT(self, "name" , pCol="TEXT1" )
        SerialT(self, "quantity" , pCol="REAL1" , pType="REAL" )

        #endregion
    
    #endregion
    
    #region Methods
    def byName(self, name):
        for a in self._attribute:
            if name.upper() == a.name.upper(): 
                return a.value
        return ''

    def kwargs(self):
        kw = {}
        for a in self._attribute:
            kw[a.name.replace(" ", "_").replace("/","").replace("\\" , "")] = a.value
        return kw

    #endregion
        
class xmlTransactionsTransactionDocumentConfigurationAttribute(SerialBase) :

    #region Properties
    @property
    def name(self): 
        return self._name
    @name.setter
    def name(self, value):
        self._name = value    
    
    @property
    def value(self): 
        return self._value
    @value.setter
    def value(self, value):
        self._value = value   
        
    #endregion 

    #region "ctor"
    def __init__(self,  **kwargs): 

        #region "Property defaults"
        self._name = ''        
        self._value = ''     
        
        #endregion

        #region "Set Meta info"
        SerialBase.__init__(self , SerialF(fname="Attribute", rt=5) , **kwargs)  

        SerialT(self, "rt")         
        SerialT(self, "name" , pCol="TEXT1" )
        SerialT(self, "value" , pCol="TEXT2" )

        #endregion
    
    #endregion
