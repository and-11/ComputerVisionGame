import cv2 as cv
import numpy as np
import os


IMAGE_SIZE = 810
CX, CY, PITCH = IMAGE_SIZE / 2, IMAGE_SIZE / 2, 42.6

def show_image(title, image):
    image = cv.resize(image, (0, 0), fx=0.3, fy=0.3)
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyAllWindows()



    
#  ca la laborator
def extrage_careu(image):

    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    r, g, b = cv.split(image_rgb)

    raw_mask = ((b.astype(np.int16) - r.astype(np.int16)) > 5).astype(np.uint8) * 255

    # show_image('asa', raw_mask)
    #  curata si apoi adauga la loc -> scap de zgomot
    clean_mask = cv.morphologyEx(raw_mask, cv.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # show_image('asa', clean_mask)
    # adauga si apoi curata --> in caz ca bucatile de tabla sunt desprinse
    clean_mask = cv.morphologyEx(clean_mask, cv.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    # show_image('asa', clean_mask)

    # masked_rgb = cv.bitwise_and(image_rgb, image_rgb, mask=clean_mask)
    # show_image("sa", masked_rgb)


    # return image_rgb, clean_mask, masked_rgb




    contours, _ = cv.findContours(clean_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0
    top_left = top_right = bottom_right = bottom_left = None

    for i in range(len(contours)):
        if len(contours[i]) > 3:
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + possible_bottom_right[1]:
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis=1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
            if cv.contourArea(np.array([[possible_top_left], [possible_top_right], [possible_bottom_right], [possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array([[possible_top_left], [possible_top_right], [possible_bottom_right], [possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left


    if top_left is None:
        raise("Have not found the square")
   
    width = IMAGE_SIZE
    height = IMAGE_SIZE
    
    # !
    # image_copy = image.copy()
    # cv.circle(image_copy, tuple(top_left), 20, (0, 0, 255), -1)
    # cv.circle(image_copy, tuple(top_right), 20, (0, 0, 255), -1)
    # cv.circle(image_copy, tuple(bottom_left), 20, (0, 0, 255), -1)
    # cv.circle(image_copy, tuple(bottom_right), 20, (0, 0, 255), -1)
    # show_image("detected corners", image_copy)

    puzzle = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
    destination_of_puzzle = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

    M = cv.getPerspectiveTransform(puzzle, destination_of_puzzle)

    result = cv.warpPerspective(image, M, (width, height))

    return result



# 
def draw_cells(image, cx=CX, cy=CY, pitch=PITCH, scale=0.8):
    rows = [6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6]
    dy = pitch * np.sqrt(3) / 2
    half = int(pitch * scale / 2)

    result = image.copy()
    for r, n in enumerate(rows):
        y = int(round(cy + (r - 5) * dy))
        x0 = cx - (n - 1) * pitch / 2
        for k in range(n):
            x = int(round(x0 + k * pitch))
            cv.rectangle(result, (x - half, y - half), (x + half, y + half), (0, 0, 255), 1)
            cv.circle(result, (x, y), 2, (0, 255, 0), -1)
    return result
# 




def extract_patches(warped, cx=406, cy=404, pitch=42.6, scale=0.9):
    """Returns a dict {(row, col): patch} with a square crop around each cell center."""
    rows = [6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6]
    dy = pitch * np.sqrt(3) / 2
    half = int(pitch * scale / 2)

    patches = {}
    for r, n in enumerate(rows):
        y = int(round(cy + (r - 5) * dy))
        x0 = cx - (n - 1) * pitch / 2
        for k in range(n):
            x = int(round(x0 + k * pitch))
            patches[(r, k)] = warped[y - half:y + half, x - half:x + half].copy()
    return patches


def get_basic_shapes():

    os.makedirs("patches", exist_ok=True)

    for (r, k), p in patches.items():
        cv.imwrite(f"patches/r{r}_c{k}.png", p)









if __name__ == '__main__':



    img = cv.imread('data/train/' + file)
    result = extrage_careu(img)
    # show_image('asta e', result)
    cv.imwrite("see.jpg", draw_cells(result))



    # files = os.listdir('data/train')
    # for file in files:
    #     if file[-3:] == 'jpg':
    #         img = cv.imread('data/train/' + file)
    #         result = extrage_careu(img)
    #         # show_image('asta e', result)

    #         cv.imwrite("see.jpg", draw_cells(result))