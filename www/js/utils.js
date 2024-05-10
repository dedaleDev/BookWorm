function ConvertTitleToImagePath(imagePath){
    for (let i = 0; i < bannedChar.length; i++) {
        imagePath = imagePath.split(bannedChar[i]).join('_');
    }
    imagePath = imagePath.replace(/à|á|ã|å|ä/g, 'a');
    imagePath = imagePath.replace(/é|è|ë|ê/g, 'e');
    imagePath = imagePath.replace(/î|ï|î/g, 'i');
    imagePath = imagePath.replace(/ô|ö|ò|õ/g, 'o');
    imagePath = imagePath.replace(/û|ü|ù/g, 'u');
    imagePath = imagePath.replace(/ç/g, 'c');
    return imagePath
}