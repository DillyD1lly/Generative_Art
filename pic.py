import os
import cairo, PIL, argparse, math, random
from PIL import Image, ImageDraw

list_of_colors = [(145, 185, 141), (229, 192, 121), (210, 191, 88), (140, 190, 178), (255, 183, 10), (189, 190, 220),
 (221, 79, 91), (16, 182, 98), (227, 146, 80), (241, 133, 123), (110, 197, 233), (235, 205, 188), (197, 239, 247), (190, 144, 212),
 (41, 241, 195), (101, 198, 187), (255, 246, 143), (243, 156, 18), (189, 195, 199), (243, 241, 239)]

float_gen = lambda a, b: random.uniform(a, b)

def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height)
    cr.fill()

def draw_circle_fill(cr, x, y, radius, r ,g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.fill()

def draw_orbit(cr, line, x, y, radius, r, g, b):
    cr.set_line_width(line)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.stroke()

def draw_line_circle(cr, radius, j, k, r, g, b):
    radians =  (math.pi)
    randx1 = random.uniform(0, 360)
    randx2 = random.uniform(0, 360)
    randy1 = random.uniform(0, 360)
    randy2 = random.uniform(0, 360)
    x1 = radius * math.cos(randx1) + j
    x2 = radius * math.cos(randx2) + j
    y1 = radius * math.sin(randy1) + k
    y2 = radius * math.sin(randy2) + k
    cr.set_source_rgb(r, g, b)
    cr.set_line_width(4)
    cr.move_to(x1, y1)
    cr.line_to(x2, y2)
    cr.stroke()

def draw_border(cr, size, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, size, height)
    cr.rectangle(0, 0, width, size)
    cr.rectangle(0, height-size, width, size)
    cr.rectangle(width-size, 0, size, height)
    cr.fill()

def main():
    
    print("hello")

    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="Specify Width", default=3000, type=int)
    parser.add_argument("--height", help="Specify Height", default=2000, type=int)
    parser.add_argument("-o", "--orbit", help="Actual Orbits", action="store_true")
    parser.add_argument("-s", "--sunsize", help=".", default=random.randint(200, 400), type=int)
    parser.add_argument("-bs", "--bordersize", help=".", default=50, type=int)
    parser.add_argument("-n", "--noise", help="Texture", default=.4, type=float)
    args = parser.parse_args()

    width, height = args.width, args.height
    border_size = args.bordersize
    sun_size = args.sunsize
    
    sun_center = height - border_size

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    draw_background(cr, .3, .3, .3, width, height)

    sun_color = random.choice(list_of_colors)
    sun_r, sun_g, sun_b = sun_color[0]/255.0, sun_color[1]/255.0, sun_color[2]/255.0,

    draw_circle_fill(cr, width/2, sun_center, sun_size, sun_r, sun_g, sun_b)

    distance_between_planets = 20
    last_center = sun_center
    last_size = sun_size
    last_color = sun_color


    min_size = 5
    max_size = 70

    for x in range(1, 20):
        next_size = random.randint(min_size, max_size)
        next_center = last_center - last_size - (next_size*2)
        next_width_pos = random.randint(0, width)

        if not(next_center - next_size < border_size):
            #orbit lines
            if(args.orbit):
                draw_orbit(cr, random.randint(2, 6), next_width_pos, next_center, next_size + random.randint(100, 200), .6, .6, .6)
            #Transparent planet border
            draw_circle_fill(cr, next_width_pos, next_center, next_size*1.3, .3, .3, .3)

            rand_color = random.choice(list_of_colors)
            while(rand_color is last_color):
                rand_color = random.choice(list_of_colors)

            last_color = rand_color

            r, g, b = rand_color[0]/255.0, rand_color[1]/255.0, rand_color[2]/255.0
            #draw planet
            draw_circle_fill(cr, next_width_pos, next_center, next_size, r,g,b)

            draw_line_circle(cr, next_size, next_width_pos, next_center, 255, 255, 255)
            last_center = next_center
            last_size = next_size

            min_size += 5
            max_size += 5 * x

    draw_border(cr, border_size, sun_r, sun_g, sun_b, width, height)

    os.remove("Generative-Space-Example.png")
    os.remove("Generative-space-Texture.png")
    ims.write_to_png('Generative-Space-Example.png')

    pil_image = Image.open('Generative-Space-Example.png')
    pixels = pil_image.load()

    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):
            r, g, b = pixels[i, j]

            noise = float_gen(1.0 - args.noise, 1.0 + args.noise)
            pixels[i, j] = (int(r*noise), int(g*noise), int(b*noise))

    pil_image.save('Generative-space-Texture.png')


if __name__ == "__main__":
        main()
