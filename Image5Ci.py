from PIL import Image
import matplotlib.pyplot as plt
import math

# definisco una classe personale di gestione delle immagini
# in particolare che permetta l'apertura e l'elabolazione di un singolo BMP (bit map)

# Buona abitudine chiamare la classe come nome del file e avere una classe per file
class Image5Ci:
    # costruttore definito come metodo speciale DUNDER (Double underscore)
    # Self AKA riferimento all'oggetto in cui e presente ; deve essere sempre presente al primo posto di ogni metodo
    def __init__(self , ImagePath):
        #Tento di aprire l'immagine il cui percorso e passato come percorso 
        #se non riesco per qualsiasi motivo, sollevo un'eccezione
        # non è un'obbligo dichiarare tutte le variabili all'inizio solo pe rpulizia , possono essere dichiarate quando vogliamo
        self.__myImage = None  # nomenclatura delle variabili private => due underscore + nome var
        self.__ImagePath = ImagePath
        self.__pixels = None
        self.__width = 0
        self.__height = 0

        try:
            #tentativo di apertura
            self.__myImage = Image.open(self.__ImagePath).convert("RGB")
            self.__pixels = self.__myImage.load()
            (self.__width , self.__height) = self.__myImage.size
        
        except Exception as ex:
            raise Exception(f"Attenzione! Qualcosa è andato storto nell'apertura dell'immagine {ImagePath}")

    # Elenco i metodi publici di modifica dell'immagine

    #Negativo 
    def Negative(self , showResult = False , saveResult = False):
        # Creo una nuova immagine per non rovinare quella esistente
        img = Image.new("RGB" , (self.__width , self.__height))

        # Ciclo su ogni pixel e inverto il valore di ogni canale R G B
        for x in range(self.__width):
            for y in range(self.__height):
                r , g , b = self.__pixels[x,y]
                img.putpixel((x,y) , (255 - r , 255 - g , 255 - b))
        
        # Controllo se mostrare l'immagine  
        if showResult:
            img.show() #mostra l'anteprima con l'applicazione di default per le immagine del SO

        # Controllo se salvare l'immagine
        if saveResult:
            img.save("negativo.jpg" , "JPEG" , quality = 100 , optimize = 100 , progressive = True)
    
    # Specchaitura Orizontale
    def HorizontalFlip(self , showResult = False , saveResult = False):
         # Creo una nuova immagine per non rovinare quella esistente
        img = Image.new("RGB" , (self.__width , self.__height))

        # Ciclo su ogni pixel e inverto il valore di ogni canale R G B
        for x in range(self.__width):
            newX = self.__width - 1 - x
            for y in range(self.__height):
                img.putpixel((newX , y) , self.__pixels[x,y])
             

        # Controllo se mostrare l'immagine  
        if showResult:
            img.show() #mostra l'anteprima con l'applicazione di default per le immagine del SO

        # Controllo se salvare l'immagine
        if saveResult:
            img.save("Hflip.jpg" , "JPEG" , quality = 100 , optimize = 100 , progressive = True)
  
    # Specchiatura Verticale 
    def VerticalFlip(self , showResult = False , saveResult = False):
         # Creo una nuova immagine per non rovinare quella esistente
        img = Image.new("RGB" , (self.__width , self.__height))

        # Ciclo su ogni pixel e inverto il valore di ogni canale R G B       
        for y in range(self.__height):
            newY = self.__height - 1 - y
            for x in range(self.__width):
                img.putpixel((x , newY) , self.__pixels[x,y])
             

        # Controllo se mostrare l'immagine  
        if showResult:
            img.show() #mostra l'anteprima con l'applicazione di default per le immagine del SO

        # Controllo se salvare l'immagine
        if saveResult:
            img.save("Hflip.jpg" , "JPEG" , quality = 100 , optimize = 100 , progressive = True)

    def Difference(self , otherImagePath , tolerance = 10 ,showResult = False , saveResult = False):
        # Controllo il valore di tolleranza
        tolerance = tolerance if tolerance > 0 else 0 if tolerance < 255 else 255
        
        otherImage = None
        otherPixels = None
        width , height = (0,0)
        # Tento di aprire l'immagine di cui percorso e stato passato come parametro
        try:
            #tentativo di apertura
            otherImage = Image.open(otherImagePath).convert("RGB")
            otherPixels = otherImage.load()
            width , height = otherImage.size
        except Exception as ex:
            # Questa non è una buona prassi.... ma funziona!
            return
  
        # Se sono arrivato fin qua... tutto è andato bene
        # controllo se le dimensioni sono uguali
        if self.__myImage.size != otherImage.size:
            raise Exception(f"Attenzione L'immaigine {otherImagePath} non ha le dimensioni corrette!")
        
        # Creo una nuova immagine per non rovinare quella esistente
        img = Image.new("RGB" , (self.__width , self.__height))

        #Ciclo su ogni pixel delle due immagini e sottraggo i rispettivi valori per ogni canale
        for x in range(self.__width):
            for y in range(self.__height):
                rA , gA , bA = self.__pixels[x,y]
                rB , gB , bB = otherPixels[x,y]

                # e sufficente che uno dei tre canali sia abbastanza differente per mettere
                # il pixel a bianco

                #tanta roba 3 if su una riga
                value = 255 if abs(rA - rB) >= tolerance or abs(gA - gB) >= tolerance or abs(bA - bB) >= tolerance else 0
                # scrivo il nuovo valore sui tre canali

                img.putpixel((x,y) , (value,value,value))

         # Controllo se mostrare l'immagine  
        if showResult:
            img.show() #mostra l'anteprima con l'applicazione di default per le immagine del SO

        # Controllo se salvare l'immagine
        if saveResult:
            img.save("Difference.jpg" , "JPEG" , quality = 100 , optimize = 100 , progressive = True)

    # Estrazione dei bordi di un'immagine
    def Edges(self , tolerance = 50 ,showResult = False , saveResult = False):
        # Controllo il valore di tolleranza
        tolerance = tolerance if tolerance > 0 else 0 if tolerance < 255 else 255

        # Creo una nuova immagine per non rovinare quella esistente
        img = Image.new("RGB" , (self.__width , self.__height))

        # Ciclo su ogni pixel trascurando per semplicita il rettangolo di bordo di un solo pixel
        x = 1
        while x < self.__width - 1:
            y = 1
            while y < self.__height - 1:
                #considero il pixel corrente
                rA , gA , bA = self.__pixels[ x , y ]
                # considero il pixel sulla diagonale dall'alto sinistra verso il basso a destra
                rB , gB , bB = self.__pixels[ x + 1 , y + 1 ]                
                # considero il pixel sulla diagonale dall'alto destra verso il basso a sinistra
                rC , gC , bC = self.__pixels[ x - 1 , y - 1 ]

                # voglio i bordi neri su sfondo bianco
                value1 = 0 if abs(rA - rB) >= tolerance or abs(gA - gB) >= tolerance or abs(bA - bB) >= tolerance else 255
                value2 = 0 if abs(rA - rC) >= tolerance or abs(gA - gC) >= tolerance or abs(bA - bC) >= tolerance else 255

                value = 0 if value1 == 0 or value2 == 0 else 255

                img.putpixel((x,y) , (value,value,value))
                # incremento il valore di y
                y += 1
                pass
            # incremento il valore di x 
            x += 1

        # Controllo se mostrare l'immagine  
        if showResult:
            img.show() #mostra l'anteprima con l'applicazione di default per le immagine del SO

        # Controllo se salvare l'immagine
        if saveResult:
            img.save("Difference.jpg" , "JPEG" , quality = 100 , optimize = 100 , progressive = True)
     
            
    def gradienteDIGrigio(self, showResult = False, saveResult = False): # Python permette nomenclatura dei parametri, 
    #possiamo mettere in ordine come vogliamo, #posso anche assegnarlo un valore iniziale
    # Creo una nuova immagine per non rovinare quella esistente  
        img = Image.new("RGB",(self.__width,self.__height))
        #Ciclo su ogni pixel e inverto il valore di ogni canale RGB
        for x in range(self.__width):
            for y in range(self.__height):
                
                r,g,b = self.__pixels[x,y]
                # Facciamo la media dei tre canali e li usiamo come parametri
                media = int((r+g+b)/3)
                
                # Lo inverto e lo salvo nella nuova immagine
                img.putpixel((x,y),(media,media,media)) # due tuple uno da 2 elementi e uno da 3 elementi
        # Controllo se mostrare l'immagine negative
        if showResult:
            img.show() # prende il visualizzatore predefinito del sistema operativo e apre immagine
        if saveResult:
            img.save("BN.jpg","JPEG", quality = 100, optimize = 100, progressive = True)

    
    def IstoGrammaLuminosità(self): # Python permette nomenclatura dei parametri, 
    #possiamo mettere in ordine come vogliamo, #posso anche assegnarlo un valore iniziale
    # Creo una nuova immagine per non rovinare quella esistente  
        arrayX = {}
        arrayY = []
        #Ciclo su ogni pixel e inverto il valore di ogni canale RGB
        for x in range(256):
            arrayX = arrayX | {x + 1 : 0}

        for y in range(self.__width * self.__height):
            arrayY.append(y)

        for x in range(self.__width):
            for y in range(self.__height):                
                r,g,b = self.__pixels[x,y]

                value = arrayX[((math.floor((r+g+b)/3))) +1 ]
                arrayX[((math.floor((r+g+b)/3)))+1] =  value + 1
        plt.plot(arrayX, arrayY)
        plt.xlabel('Range Colori')
        plt.ylabel('numero pixel')
        plt.title('Luminosità Generale')

        # Show the plot
        plt.savefig("plot.png")

    pass # no op => comando che non fa niente ma serve per non dare errori in compilazione
