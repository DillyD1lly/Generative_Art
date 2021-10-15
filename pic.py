import os
import cairo, PIL, argparse, math, random
from PIL import Image, ImageDraw

list_of_colors = [(145, 185, 141), (229, 192, 121), (210, 191, 88), (140, 190, 178), (255, 183, 10), (189, 190, 220),
 (221, 79, 91), (16, 182, 98), (227, 146, 80), (241, 133, 123), (110, 197, 233), (235, 205, 188), (197, 239, 247), (190, 144, 212),
 (41, 241, 195), (101, 198, 187), (255, 246, 143), (243, 156, 18), (189, 195, 199), (243, 241, 239)]

ocean_colors = [(102, 127, 255), (102, 153, 255), (102, 102, 255), (51, 119, 255), (25, 25, 255), (128, 170, 255)]
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

def draw_curve(cr, x1, y1, xa, ya, xb, yb, x2, y2, r, g, b):
    cr.set_line_width(30)
    cr.set_source_rgb(r, g, b)
    cr.move_to(x1, y1)
    cr.curve_to(xa, ya, xb, yb, x2, y2)
    cr.stroke()

def draw_bird(cr, x1, y1, xa, ya, xb, yb, x2, y2):
    cr.set_line_width(4)
    cr.set_source_rgb(0, 0, 0)
    cr.move_to(x1, y1)
    cr.curve_to(xa, ya, xb, yb, x2, y2)
    cr.stroke()

def draw_wave(cr, x1, y1, w, r, g, b):
    x = x1
    y = y1
    while(x<w):
        draw_curve(cr, x, y, x+20, y-100, x+130, y+100, x+150, y, r, g, b)
        x = x+150


    



def draw_line_circle(cr, radius, j, k, r, g, b):
    radians =  (math.pi)
    rand1 = random.uniform(0, 360)
    rand2 = random.uniform(0, 360)

    x1 = radius * math.cos(rand1) + j
    x2 = radius * math.cos(rand2) + j
    y1 = radius * math.sin(rand1) + k
    y2 = radius * math.sin(rand2) + k
    cr.set_source_rgb(r, g, b)
    cr.set_line_width(4)
    cr.move_to(j, k)
    cr.line_to(x2, y2)
    cr.stroke()

def draw_line(cr, radius, j, k, degree1, degree2):
    
    cr.set_line_width(40)
    cr.set_source_rgb(255, 255, 255)

    x1 = radius * math.cos(degree1) + j
    x2 = radius * math.cos(degree2) + j
    y1 = radius * math.sin(degree1) + k
    y2 = radius * math.sin(degree2) + k

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
    parser.add_argument("-s", "--sunsize", help=".", default=random.randint(0, 500), type=int)
    parser.add_argument("-bs", "--bordersize", help=".", default=50, type=int)
    parser.add_argument("-n", "--noise", help="Texture", default=.4, type=float)
    args = parser.parse_args()

    width, height = args.width, args.height
    border_size = args.bordersize
    sun_size = args.sunsize
    
    sun_center = random.randint(0, height/2)

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    draw_background(cr, .7, .9, 1.0, width, height)

    sun_color = random.choice(list_of_colors)
    sun_r, sun_g, sun_b = sun_color[0]/255.0, sun_color[1]/255.0, sun_color[2]/255.0,
    
    
    

    draw_circle_fill(cr, random.randint(0, width/2), sun_center, sun_size, sun_r, sun_g, sun_b)
    H = height / 2
    while H < height:
        wave_color = random.choice(ocean_colors)
        w_r, w_g, w_b = wave_color[0]/255.0, wave_color[1]/255.0, wave_color[2]/255.0,
        draw_wave(cr, 0, H, width, w_r, w_g, w_b)
        H = H + 30

    s_color = random.choice(list_of_colors)
    s_r, s_g, s_b = s_color[0]/255.0, s_color[1]/255.0, s_color[2]/255.0,

    c = (height/5) * 4
    while c <= height:
        draw_curve(cr, 0, c, 100, c+200, width - 100, c-200, width, c, 236, 231, 215 )
        c = c + 30

    distance_between_planets = 20
    last_center = 0
    last_size = sun_size
    last_color = sun_color


    min_size = 5
    max_size = 70
    
    for x in range(0, 15):
        next_size = random.randint(min_size, max_size)
        next_center = last_center + 10
        next_width_pos = random.randint(0, width)
        draw_wave(cr, 0, next_center, width, 255, 255, 255)

        bx = random.randint(500, width -500)
        by = random.randint(300, height/2 -300)
     

        bmod = random.uniform(100, 300)
        bmody = random.uniform(40, 100)
        draw_bird(cr, bx, by, bx + bmod, by + bmody, bx, by+bmody, bx + bmod, by)


    draw_border(cr, border_size, sun_r, sun_g, sun_b, width, height)

    # os.remove("Generative-Space-Example.png")
    # os.remove("Generative-space-Texture.png")
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
