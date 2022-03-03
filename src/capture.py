from PIL import Image
import pyocr
import pyocr.builders


def imageToTexts(filepath):
    allTools = pyocr.get_available_tools()
    tool = allTools[0]
    languages = ['ara', 'ces', 'fas', 'ind', 'ita', 'nld', 'pol', 'por', 'spa', 'tur', 'vie']  
    texts = []  

    for i in range(len(languages)):
        text = tool.image_to_string(
            Image.open(filepath),
            lang = languages[i],
            builder = pyocr.builders.TextBuilder()
        )
        texts.append(text)
    return texts
