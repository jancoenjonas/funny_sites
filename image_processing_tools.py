from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import time

# Functie om een rand om de afbeelding te creëren op basis van de randen die in de afbeelding worden gevonden.
def create_outline(image, edge_color=(0, 0, 0)):
    # Vind randen in de afbeelding en zet om naar hoge contrast om de randen duidelijker te maken.
    high_contrast = image.convert('L').filter(ImageFilter.FIND_EDGES)
    outlined_image = Image.new('RGB', image.size, "white")
    outlined_pixel_map = outlined_image.load()

    # Ga door elke pixel en pas de randkleur toe indien nodig.
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if high_contrast.getpixel((x, y)) > 0:  # Als de rand gedetecteerd wordt
                outlined_pixel_map[x, y] = edge_color
            else:  # Behoud de originele pixel of vul met wit als de randkleur is ingesteld
                outlined_pixel_map[x, y] = image.getpixel((x, y)) if edge_color is None else (255, 255, 255)
    return outlined_image

# Functie om het beeld te pixeleren met een gegeven pixelgrootte.
def pixelate(image, pixel_size=10):
    # Verminder de grootte van de afbeelding en vergroot het weer, wat resulteert in een pixel effect.
    image_small = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        resample=Image.NEAREST
    )
    return image_small.resize(image.size, Image.NEAREST)

# Functie om een watermerk toe te voegen aan de afbeelding.
def add_watermark(image, watermark_text, opacity=128):
    # Converteer naar RGBA om met de alpha laag te werken voor de doorzichtigheid.
    if image.mode != 'RGBA':
        image = image.convert("RGBA")

    # Voorbereiding om tekst te tekenen op de afbeelding.
    draw = ImageDraw.Draw(image)
    font_size = 50
    font = ImageFont.truetype("arial.ttf", font_size)
    text_width, text_height = draw.textsize(watermark_text, font=font)

    # Bereken de positie voor het watermerk.
    x = image.width - text_width - 10
    y = image.height - text_height - 10

    # Voeg de tekst toe aan de afbeelding met de gegeven doorzichtigheid.
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, opacity))

    # Converteer terug naar RGB en retourneer de afbeelding.
    return image.convert("RGB")

# Functie om een onscherpe afbeelding scherper te maken.
def deblur(image):
    # Gebruik het SHARPEN-filter van PIL om de afbeelding scherper te maken.
    return image.filter(ImageFilter.SHARPEN)

# Hoofdfunctie om de afbeeldingsverwerking te beheren op basis van de gebruikersinput.
def process_image(img_path, dot_size, mode, outline_mode=False, pixelate_mode=False, deblur_mode=False):
    # Laad de originele afbeelding.
    original_image = Image.open(img_path)

    # Pas de gewenste bewerkingen toe.
    if outline_mode:
        original_image = create_outline(original_image)
    if pixelate_mode:
        original_image = pixelate(original_image, dot_size)
    if deblur_mode:
        original_image = deblur(original_image)

    # Maak een directory indien deze nog niet bestaat.
    directory = '\\image'  
    if not os.path.exists(directory):
        os.makedirs(directory)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_filename = f'dot_matrix_{mode}_{timestamp}.png'
    output_path = os.path.join(directory, output_filename)
    original_image.save(output_path)

    # Retourneer het pad van de opgeslagen afbeelding.
    return output_path

# Startpunt van het script wanneer het als hoofdprogramma wordt uitgevoerd.
if __name__ == "__main__":
    # Verkrijg de modus van de gebruiker via input.
    mode_input = input("Enter the mode: 'bw', 'color', 'random', 'outline', 'pixelate', 'deblur': ").lower()

    # Standaard pixelgrootte voor pixelate-modus.
    dot_size = 10

    # Schakelaars om te bepalen welke bewerkingen worden toegepast.
    outline_mode = False
    pixelate_mode = False
    deblur_mode = False

    # Stel de bewerkingsmodi in op basis van de gebruikersinput.
    if mode_input == 'outline':
        outline_mode = True
    elif mode_input == 'pixelate':
        pixelate_mode = True
        dot_size = int(input("Enter the size for pixelation (larger number for more pixelation): "))
    elif mode_input == 'deblur':
        deblur_mode = True

    # Definieer het pad naar de afbeelding die verwerkt zal worden.
    img_path = 'naar foto'

    # Voer de beeldverwerking uit en sla het resultaat op.
    output_path = process_image(img_path, dot_size, mode_input, outline_mode, pixelate_mode, deblur_mode)
    print(f"Image processed in {mode_input} mode and saved to {output_path}")
