import os
import glob
import argparse
import cv2

def iconvert():
    parser = argparse.ArgumentParser(prog='iconvert', description='Image convertion utility')
    parser.add_argument('--debayer', action='store_true', help='debayer input')
    parser.add_argument('--glob', action='store_true', help='input name is a glob pattern')
    parser.add_argument('--ofmt', default='tiff', choices=['tiff', 'png', 'jpg', 'bmp'], help='output format')
    parser.add_argument('input')
    args = parser.parse_args()

    if args.glob:
        lst = glob.glob(args.input)
    else:
        lst = [args.input]

    for filename in lst:
        try:
            basename = os.path.basename(os.path.splitext(filename)[0])
            outname = "%s.%s" % (basename, args.ofmt)
            print(filename, '=>', outname)

            img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            if args.debayer:
                img = cv2.cvtColor(img, cv2.COLOR_BayerRG2BGR)
            cv2.imwrite(outname, img)
        except:
            print('ERROR READING',filename)

if __name__ == '__main__':
    iconvert()
