#import di Image5CI
import Image5Ci 

# Alloco un'oggetto di tipo Image5Ci
img = Image5Ci.Image5Ci("Topolino.jpg")

# Applico il negativo
# img.Negative(showResult = True , saveResult = True)

# Specchiatura orizontale 
# img.HorizontalFlip(showResult = True , saveResult = True)

# Differenza tra immagini
img.Difference("Topolino2.jpg", 20 ,showResult=True , saveResult=True)

# mostra i bordi dell'immagine
# img.Edges(tolerance= 35 , showResult=True)

# img.IstoGrammaLuminosità()