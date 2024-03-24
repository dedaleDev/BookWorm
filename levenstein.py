
str1 = "Harry Potter"
str2 = "Harry Potter and the Philosopher's Stone"

def levenshtein_distance(str1, str2):
    # Assurez-vous que str1 n'est pas plus long que str2
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    # Créez une liste pour stocker les distances entre les préfixes de str1 et str2
    distances = [0 for i in range(len(str1) + 1)]

    # Parcourez chaque caractère de str2
    for index2, char2 in enumerate(str2):
        # Créez une nouvelle liste pour stocker les distances de la prochaine étape
        new_distances = [index2 + 1]

        # Parcourez chaque caractère de str1
        for index1, char1 in enumerate(str1):
            # Si les caractères sont les mêmes, la distance est la même que pour les préfixes précédents
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                # Sinon, la distance est le minimum entre la suppression, l'insertion et la substitution
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))

        # Mettez à jour la liste des distances
        distances = new_distances

    # La distance de Levenshtein entre str1 et str2 est la dernière distance calculée
    return distances[-1]

print(levenshtein_distance(str1,str2))