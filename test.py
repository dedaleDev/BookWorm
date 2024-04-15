def formatResult(result:list)->list:
    temp = []
    for i in result:#enlève les doublons
        if i not in temp and i != None and i != ( ):
            temp.append(i)
    temp = list(temp[0])
    return temp

print(formatResult([(), (('12, place des clercs 26000 Valence', 'La Licorne', 'https://fr-fr.facebook.com/librairie.lalicorne/', '0475829117'), ('17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\n\n', 'Fnac', 'https://www.fnac.com/Valence/Fnac-Valence/cl51/w-4', '0825020020'), ('31 rue Madier de Montjau\n26000 Valence', "L'Étincelle", 'https://librairieletincelle.wordpress.com/', '0973137597'), ('ZC le Plateau des Couleures\n26000 VALENCE\n07.57.59.94.95', 'Cultura', 'https://www.cultura.com', '0986860293'))]))