"""A deterministic, self-contained vector-type newspaper. Python standard library only."""

import base64
import hashlib
import json
import math
import os
import struct
import zlib

# Hershey futural coordinates, ASCII 32..126. Each first pair is the
# left/right bearing; ' R' lifts the pen. Coordinates are relative to 'R'.
SANS_COORDINATES = r"""JZ
MWRFRT RRYQZR[SZRY
JZNFNM RVFVM
H]SBLb RYBRb RLOZO RKUYU
H\PBP_ RTBT_ RYIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX
F^[FI[ RNFPHPJOLMMKMIKIIJGLFNFPGSHVHYG[F RWTUUTWTYV[X[ZZ[X[VYTWT
E_\O\N[MZMYNXPVUTXRZP[L[JZIYHWHUISJRQNRMSKSIRGPFNGMIMKNNPQUXWZY[[[\Z\Y
MWRHQGRFSGSIRKQL
KYVBTDRGPKOPOTPYR]T`Vb
KYNBPDRGTKUPUTTYR]P`Nb
JZRLRX RMOWU RWOMU
E_RIR[ RIR[R
NVSWRXQWRVSWSYQ[
E_IR[R
NVRVQWRXSWRV
G][BIb
H\QFNGLJKOKRLWNZQ[S[VZXWYRYOXJVGSFQF
H\NJPISFS[
H\LKLJMHNGPFTFVGWHXJXLWNUQK[Y[
H\MFXFRNUNWOXPYSYUXXVZS[P[MZLYKW
H\UFKTZT RUFU[
H\WFMFLOMNPMSMVNXPYSYUXXVZS[P[MZLYKW
H\XIWGTFRFOGMJLOLTMXOZR[S[VZXXYUYTXQVOSNRNOOMQLT
H\YFO[ RKFYF
H\PFMGLILKMMONSOVPXRYTYWXYWZT[P[MZLYKWKTLRNPQOUNWMXKXIWGTFPF
H\XMWPURRSQSNRLPKMKLLINGQFRFUGWIXMXRWWUZR[P[MZLX
NVROQPRQSPRO RRVQWRXSWRV
NVROQPRQSPRO RSWRXQWRVSWSYQ[
F^ZIJRZ[
E_IO[O RIU[U
F^JIZRJ[
I[LKLJMHNGPFTFVGWHXJXLWNVORQRT RRYQZR[SZRY
E`WNVLTKQKOLNMMPMSNUPVSVUUVS RQKOMNPNSOUPV RWKVSVUXVZV\T]Q]O\L[JYHWGTFQFNGLHJJILHOHRIUJWLYNZQ[T[WZYYZX RXKWSWUXV
I[RFJ[ RRFZ[ RMTWT
G\KFK[ RKFTFWGXHYJYLXNWOTP RKPTPWQXRYTYWXYWZT[K[
H]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZV
G\KFK[ RKFRFUGWIXKYNYSXVWXUZR[K[
H[LFL[ RLFYF RLPTP RL[Y[
HZLFL[ RLFYF RLPTP
H]ZKYIWGUFQFOGMILKKNKSLVMXOZQ[U[WZYXZVZS RUSZS
G]KFK[ RYFY[ RKPYP
NVRFR[
JZVFVVUYTZR[P[NZMYLVLT
G\KFK[ RYFKT RPOY[
HYLFL[ RL[X[
F^JFJ[ RJFR[ RZFR[ RZFZ[
G]KFK[ RKFY[ RYFY[
G]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF
G\KFK[ RKFTFWGXHYJYMXOWPTQKQ
G]PFNGLIKKJNJSKVLXNZP[T[VZXXYVZSZNYKXIVGTFPF RSWY]
G\KFK[ RKFTFWGXHYJYLXNWOTPKP RRPY[
H\YIWGTFPFMGKIKKLMMNOOUQWRXSYUYXWZT[P[MZKX
JZRFR[ RKFYF
G]KFKULXNZQ[S[VZXXYUYF
I[JFR[ RZFR[
F^HFM[ RRFM[ RRFW[ R\FW[
H\KFY[ RYFK[
I[JFRPR[ RZFRP
H\YFK[ RKFYF RK[Y[
KYOBOb RPBPb ROBVB RObVb
KYKFY^
KYTBTb RUBUb RNBUB RNbUb
JZRDJR RRDZR
I[Ib[b
NVSKQMQORPSORNQO
I\XMX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
H[LFL[ RLPNNPMSMUNWPXSXUWXUZS[P[NZLX
I[XPVNTMQMONMPLSLUMXOZQ[T[VZXX
I\XFX[ RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
I[LSXSXQWOVNTMQMONMPLSLUMXOZQ[T[VZXX
MYWFUFSGRJR[ ROMVM
I\XMX]W`VaTbQbOa RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
I\MFM[ RMQPNRMUMWNXQX[
NVQFRGSFREQF RRMR[
MWRFSGTFSERF RSMS^RaPbNb
IZMFM[ RWMMW RQSX[
NVRFR[
CaGMG[ RGQJNLMOMQNRQR[ RRQUNWMZM\N]Q][
I\MMM[ RMQPNRMUMWNXQX[
I\QMONMPLSLUMXOZQ[T[VZXXYUYSXPVNTMQM
H[LMLb RLPNNPMSMUNWPXSXUWXUZS[P[NZLX
I\XMXb RXPVNTMQMONMPLSLUMXOZQ[T[VZXX
KXOMO[ ROSPPRNTMWM
J[XPWNTMQMNNMPNRPSUTWUXWXXWZT[Q[NZMX
MYRFRWSZU[W[ ROMVM
I\MMMWNZP[S[UZXW RXMX[
JZLMR[ RXMR[
G]JMN[ RRMN[ RRMV[ RZMV[
J[MMX[ RXMM[
JZLMR[ RXMR[P_NaLbKb
J[XMM[ RMMXM RM[X[
KYTBRCQDPFPHQJRKSMSOQQ RRCQEQGRISJTLTNSPORSTTVTXSZR[Q]Q_Ra RQSSUSWRYQZP\P^Q`RaTb
NVRBRb
KYPBRCSDTFTHSJRKQMQOSQ RRCSESGRIQJPLPNQPURQTPVPXQZR[S]S_Ra RSSQUQWRYSZT\T^S`RaPb
F^IUISJPLONOPPTSVTXTZS[Q RISJQLPNPPQTTVUXUZT[Q[O"""

# rowmans.jhf shares its letters with futural.jhf. These are every
# differing ASCII glyph in that supplied file, including its punctuation.
ROMAN_COORDINATES = {
    '*': 'JZRFRR RMIWO RWIMO',
    ',': 'MWSZR[QZRYSZS\\R^Q_',
    '.': 'MWRYQZR[SZRY',
    ':': 'MWRMQNROSNRM RRYQZR[SZRY',
    ';': 'MWRMQNROSNRM RSZR[QZRYSZS\\R^Q_',
    '^': 'JZPLRITL RMORJWO RRJR[',
    '_': 'JZJ]Z]',
    '`': 'MWSFRGQIQKRLSKRJ',
}

# Natural Earth 1:110m, 180 by 90 samples packed row-major, high bit first.
MASK_COLS, MASK_ROWS = 180, 90
LANDMASK_B64 = (
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAP//7//wAAAAAAAAAAAAAAAAAAAAAAB///////AA/wDwAAHgAAAAAAAAAAAHf///'
    '///4AB/gAAAAD+AAAAAAAAAAD/v/8////4AA/gAA+ADf4AGAAAAAAAH///4A///4AAAAAH4Af/8AP8AA'
    'AAAAH///+Af//wAAAAAeD////+H4AAwH/gf////4P//wAAD8AeH///////wRw//////9/4P//AAAP/nP'
    '//////////+///////3/H/wuAAf//////////////////////+H/B/AB//////////////Df/////7/8'
    'D8A8AP//////////////A//////gf8B4AAAP/////////////8A/8////wP+AAAAGP5///////////fQ'
    'AHwB///8H/AAAAPD7/////////8B8AAeAB////v/wAAAfD//////////9B8AAAAB//////4AAAfv////'
    '///////B4AAAAAf/////4AAAX////////////AwAAAAAf/////8AAAH////////////gAAAAAAH/////'
    '8AAAH////////////AAAAAAAD/////gAAAB//7////////7gAAAAAAH////8AAAAf//7f///////3gAA'
    'AAAAH////wAAAAfy/////////+HAAAAAAAD///+AAAAAfi/////////+GAAAAAAAD///+AAAAAf/7///'
    '/////+OAAAAAAAB///+AAAAAP/Bz///////n+AAAAAAAA///4AAAAAf/zB///////jwAAAAAAAAf//wA'
    'AAAAf//////////hAAAAAAAAAP/9wAAAAB///////////wAAAAAAAAAP/A8AAAAD///////////gAAAA'
    'AAAAAH/AcAAAAD///////////gAAAAACAAAD/B8AAAAH//////H///+gAAAAADgAAAfPeAAAAH//////'
    'B///wgAAAAABgAAAf+P8AAAH////v+A/j/wwAAAAAAAAAAP+EsAAAH/////+A/B/hwAAAAAAAAAABfgA'
    'AAAH/////4A+B/hwAAAAAAAAAAAPgwAAAH/////wAeAfg4AAAAAAAAAAADj/AAAH/////wAcAXh4AAAA'
    'AAAAAAAB//gAAD/////wAOAbDcAAAAAAAAAAAAf/4AAB/////gAOAcC8AAAAAAAAAAAAH/+AAAfv///g'
    'ACB8HIAAAAAAAAAAAAP/+AAAAD///AAAA8/EAAAAAAAAAAAAf//AAAAD//+AAAAe/+AAAAAAAAAAAAf/'
    '/wAAAD//8AAAAO/38AAAAAAAAAAAf//+AAAD//4AAAAPf//mAAAAAAAAAAf///gAAB//wAAAAHHw/vAA'
    'AAAAAAAAf///gAAA//wAAAAD8AX9wAAAAAAAAAP///gAAA//wAAAAAf8PcYAAAAAAAAAP///AAAA//4A'
    'AAAAA57cMAAAAAAAAAH///AAAA//5wAAAAAH7AAAAAAAAAAAH//+AAAB//7wAAAAAP7gBAgAAAAAAAB/'
    '/+AAAB///wAAAAAf/wBDAAAAAAAAA//+AAAB//jgAAAAB//4ADAAAAAAAAA//8AAAA//HgAAAAH//4DA'
    'AAAAAAAAA//8AAAAf/HAAAAAP//8BAAAAAAAAAA//gAAAAf/HAAAAAP//+AAAAAAAAAAA//AAAAAf+AA'
    'AAAAP//+AAAAAAAAAAA//AAAAAP+AAAAAAH//+AAAAAAAAAAA/+AAAAAP8AAAAAAH//+AAAAAAAAAAA/'
    '8AAAAAP4AAAAAAH8/+AAAAAAAAAAB/8AAAAAGAAAAAAAHQf8AMAAAAAAAAB/wAAAAAAAAAAAAAAAH8AP'
    'AAAAAAAAB/wAAAAAAAAAAAAAAADwAPAAAAAAAAD+AAAAAAAAAAAAAAAAA4AeAAAAAAAAD+AAAAAAAAAA'
    'AAAAAAA4A4AAAAAAAAD8AAAAAAAAAAAAAAAAAABwAAAAAAAAD8AAAAAAAAAAAAAAAAAABgAAAAAAAAD8'
    'AAAAAAAAAADAAAAAAAAAAAAAAAAADxwAAAAAAAAAAAAAAAAAAAAAAAAAAAD5gAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAB8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAH'
    'gAAAAAAAAOAAAGIAQAAAAAAAAAAAAOAAAAAAAAD/+D/////wAAAAAAAAAAA+AAAAAEsH//+///////wA'
    'AAAAAAPAD/AAAA///////////////wAAAAPkP///AAAH///////////////wAAD///////AAAf//////'
    '/////////AAD///////wAgf///////////////+AAP//////+BD4/////////////////AAB////////'
    'v/////////////////4ABAf//////////////////////////g//////////////////////////////'
    '////////////////////////////////////////////////////////////'
)

PAPER = (244, 239, 227)
INK = (27, 27, 27)
RED = (192, 57, 43)
BLUE = (31, 78, 156)
AMBER = (217, 142, 43)
GREY = (88, 82, 74)
RULE = (174, 164, 147)
LAND = (116, 110, 99)
EDGE = 28
WIDTH = 1024 - 2*EDGE
GUTTER = 22
COLUMN = (WIDTH-2*GUTTER)//3
SCALE = 3
SIDE = 1024 * SCALE


def parse_glyph(encoded):
    left, right = (ord(c)-82 for c in encoded[:2])
    strokes = []
    for stroke in encoded[2:].split(' R'):
        assert len(stroke) % 2 == 0
        if stroke:
            strokes.append(tuple((ord(stroke[i])-82, ord(stroke[i+1])-82)
                                 for i in range(0, len(stroke), 2)))
    return left, right, tuple(strokes)


SANS = {chr(i+32): parse_glyph(s) for i,s in enumerate(SANS_COORDINATES.splitlines())}
assert len(SANS) == 95
SANS['·'] = (-5, 5, (((-0.7, 0), (0.7, 0)),))
SANS['—'] = (-12, 12, (((-10, 0), (10, 0)),))
ROMAN = dict(SANS)
ROMAN.update({c: parse_glyph(s) for c,s in ROMAN_COORDINATES.items()})


def condensed(width, font=SANS):
    return {c: (left*width,right*width,
                tuple(tuple((x*width,y) for x,y in stroke) for stroke in strokes))
            for c,(left,right,strokes) in font.items()}


TAG = condensed(0.86)

# Rowmans shares its letter skeletons with futural. Give the display faces
# visible serifs at the stem terminals, with room for the stroked ends.
CAP_TERMINALS = {
    'A': ((-8, 9), (8, 9)), 'B': ((-7, -12), (-7, 9)),
    'D': ((-7, -12), (-7, 9)), 'E': ((-6, -12), (-6, 9)),
    'H': ((-7, -12), (7, -12), (-7, 9), (7, 9)),
    'M': ((-8, -12), (8, -12), (-8, 9), (8, 9)),
    'N': ((-7, -12), (7, -12), (-7, 9)),
    'R': ((-7, -12), (-7, 9), (7, 9)), 'T': ((0, 9),),
    'U': ((-7, -12), (7, -12)), 'V': ((-8, -12), (8, -12)),
    'Y': ((-8, -12), (8, -12), (0, 9)), '1': ((1, 9),),
}


def serif_face(terminals, serif_width):
    face = dict(ROMAN)
    for letter, ends in terminals.items():
        left, right, strokes = face[letter]
        serifs = tuple(((x-serif_width, y), (x+serif_width, y)) for x, y in ends)
        face[letter] = (min(left, min(x-serif_width-1 for x, _ in ends)),
                        max(right, max(x+serif_width+1 for x, _ in ends)), strokes+serifs)
    return face


MASTHEAD = condensed(.82, serif_face(CAP_TERMINALS, 3))
EDITORIAL_ROMAN = serif_face({**CAP_TERMINALS,
    'F': ((-6, -12), (-6, 9)), 'I': ((0, -12), (0, 9)), 'J': ((4, -12),),
    'K': ((-7, -12), (-7, 9), (7, -12), (7, 9)), 'L': ((-6, -12),),
    'P': ((-7, -12), (-7, 9)), 'W': ((-10, -12), (0, -12), (10, -12)),
    'X': ((-7, -12), (7, -12), (-7, 9), (7, 9)),
    'a': ((6, 9),), 'b': ((-6, -12),), 'd': ((6, -12), (6, 9)),
    'f': ((0, 9),), 'h': ((-5, -12), (-5, 9), (6, 9)),
    'i': ((0, -5), (0, 9)), 'j': ((1, -5),),
    'k': ((-5, -12), (-5, 9), (6, 9)), 'l': ((0, -12), (0, 9)),
    'm': ((-11, -5), (-11, 9), (0, 9), (11, 9)),
    'n': ((-5, -5), (-5, 9), (6, 9)), 'p': ((-6, -5), (-6, 16)),
    'q': ((6, 16),), 'r': ((-3, -5), (-3, 9)),
    'u': ((-5, -5), (6, -5), (6, 9)), 'v': ((-6, -5), (6, -5)),
    'w': ((-8, -5), (0, -5), (8, -5)), 'y': ((-6, -5), (6, -5)),
}, 2.8)
HEADLINE = condensed(.88, EDITORIAL_ROMAN)
HERO_HEADLINE = condensed(.79, EDITORIAL_ROMAN)


class Page:
    def __init__(self):
        self.pixels = bytearray(bytes(PAPER) * SIDE * SIDE)
        self.text_boxes = []
        self.rendered = []

    def rect(self, x, y, w, h, color):
        x0,y0,x1,y1 = (round(v*SCALE) for v in (x,y,x+w,y+h))
        assert 0 <= x0 <= x1 <= SIDE and 0 <= y0 <= y1 <= SIDE
        row = bytes(color) * (x1-x0)
        for yy in range(y0,y1):
            start = (yy*SIDE+x0)*3
            self.pixels[start:start+len(row)] = row

    def dot(self, x, y, radius, color):
        for dy in range(-round(radius*SCALE), round(radius*SCALE)+1):
            half_width = math.sqrt(max(0, (radius*SCALE)**2-dy**2))
            span = math.floor(half_width)
            self.rect((round(x*SCALE)-span)/SCALE, (round(y*SCALE)+dy)/SCALE,
                      (2*span+1)/SCALE, 1/SCALE, color)

    def line(self, x0,y0,x1,y1,color,weight):
        return self.polyline(((x0,y0),(x1,y1)),color,max(1,round(weight*SCALE/2)))

    def polyline(self, points, color, weight):
        return self.stroke_pixels(tuple((round(x*SCALE),round(y*SCALE)) for x,y in points),
                                  color,weight)

    def stroke_pixels(self, points, color, weight):
        assert len(points) >= 2 and weight >= 1
        rgb = bytes(color)
        offsets = range(-(weight//2), -(weight//2)+weight)
        radius = weight/2
        left = top = SIDE
        right = bottom = 0

        def pixel(px, py):
            nonlocal left, top, right, bottom
            assert 0 <= px < SIDE and 0 <= py < SIDE
            pos = (py*SIDE+px)*3
            self.pixels[pos:pos+3] = rgb
            left, top = min(left,px), min(top,py)
            right, bottom = max(right,px+1), max(bottom,py+1)

        for (x0,y0),(x1,y1) in zip(points,points[1:]):
            dx,dy = abs(x1-x0),-abs(y1-y0)
            steep = abs(y1-y0) > abs(x1-x0)
            sx,sy = (1 if x0<x1 else -1),(1 if y0<y1 else -1)
            err = dx+dy
            while True:
                for offset in offsets:
                    pixel(x0+offset if steep else x0,y0 if steep else y0+offset)
                if x0==x1 and y0==y1:
                    break
                e = 2*err
                if e >= dy:
                    err += dy
                    x0 += sx
                if e <= dx:
                    err += dx
                    y0 += sy

        # Round caps and joins make each glyph stroke a continuous printed mark.
        extent = math.floor(radius)
        for cx,cy in points:
            for oy in range(-extent,extent+1):
                span = math.floor(math.sqrt(max(0,radius*radius-oy*oy)))
                for ox in range(-span,span+1):
                    pixel(cx+ox,cy+oy)
        return left,top,right,bottom

    def text(self, text,x,y,size,color=INK,weight=2,font=SANS,width=None,tracking=0,
             *, ink_top=False):
        # Size is cap height. By default y is the cap top (F=-12, [=9).
        advance = measure(text,size,font,tracking)
        if width is not None:
            assert advance <= width+0.001, (text,advance,width)
        cursor = x
        scale = size/21
        paths = []
        for ch in text:
            left,right,strokes = font[ch]
            for stroke in strokes:
                pts = [(cursor+(px-left)*scale,(py+12)*scale+(0 if ink_top else y))
                       for px,py in stroke]
                if len(pts) >= 2:
                    paths.append(tuple((round(px*SCALE),round(py*SCALE)) for px,py in pts))
            cursor += (right-left)*scale+tracking
        if paths:
            if ink_top:
                pad = math.floor(weight/2)
                min_y = min(min(py for _,py in path)-pad for path in paths)
                dy = round(y*SCALE)-min_y
                paths = [tuple((px,py+dy) for px,py in path) for path in paths]
            ink = [self.stroke_pixels(path,color,weight) for path in paths]
            bounds = (min(b[0] for b in ink)/SCALE,min(b[1] for b in ink)/SCALE,
                      max(b[2] for b in ink)/SCALE,max(b[3] for b in ink)/SCALE)
            if width is not None:
                assert x <= bounds[0] and bounds[2] <= x+width, (text,bounds,x,width)
            self.text_boxes.append((text,bounds))
        return advance

    def png(self):
        raw = bytearray()
        stride = SIDE*3
        for y in range(1024):
            raw.append(0)
            a = (3*y)*stride
            b = a+stride
            c = b+stride
            for x in range(1024):
                p = x*9
                for channel in range(3):
                    total = (self.pixels[a+p+channel]+self.pixels[a+p+3+channel]+
                             self.pixels[a+p+6+channel]+self.pixels[b+p+channel]+
                             self.pixels[b+p+3+channel]+self.pixels[b+p+6+channel]+
                             self.pixels[c+p+channel]+self.pixels[c+p+3+channel]+
                             self.pixels[c+p+6+channel])
                    raw.append((total+4)//9)
        def chunk(kind,data):
            return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
        return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1024,1024,8,2,0,0,0))+
                chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b''))


def measure(text,size,font=SANS,tracking=0):
    return sum(font[c][1]-font[c][0] for c in text)*size/21+max(0,len(text)-1)*tracking


def wrap(text, size, width, font):
    lines, current = [], ''
    for word in text.split():
        trial = (current + ' ' + word).strip()
        if current and measure(trial, size, font) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    assert all(measure(line, size, font) <= width for line in lines), (text, size, width)
    return lines


HEROES = (
    ('SHENZHEN SUMMIT', 'APEC 2026 · SHENZHEN · FIRST US-CHINA-RUSSIA SUMMIT',
     ('Trump, Xi and Putin', 'hold first three-way summit'),
     'The three leaders met on the sidelines of the APEC gathering in Shenzhen.', 'BY REUTERS'),
    ('WORLD COURT · THE HAGUE', 'THE HAGUE · INTERNATIONAL COURT OF JUSTICE',
     ('World Court: Myanmar', 'committed genocide'),
     "Judges ruled 9-6 in the case over Myanmar's treatment of the Rohingya.", 'FROM THE HAGUE'),
    ('COP31 · ANTALYA', 'ANTALYA · UN CLIMATE TALKS',
     ('COP31 draft drops', 'fossil-fuel aid goal'),
     'A draft deal at the UN climate summit leaves out the goal for fossil-fuel aid.', 'CLIMATE DESK'),
)

FEATURES = (
    ('EUROPE', 'bridge', 'Ukraine strikes Kerch Bridge again',
      'The crossing links Crimea and Russia.', 'BY KYIV INDEPENDENT'),
    ('MIDDLE EAST', 'missile', 'Houthi missiles shot down',
      'The missiles were intercepted in flight.', 'BY AL RASHEED'),
    ('NORTH AMERICA', 'chart', 'Nvidia slides 28% this month',
      'Shares fell as Anthropic went public.', 'BY CNBC'),
    ('NORTH AMERICA', 'game', 'GTA VI goes on sale',
      'Rockstar releases its latest game.', 'FROM LOS ANGELES'),
    ('SOUTH AMERICA', 'fist', 'Colombian unions strike',
      'Protesters take to the streets.', 'FROM BOGOTA'),
    ('OCEANIA', 'medal', 'Champion breaks marathon record',
      'Melbourne gets a new course best.', 'FROM MELBOURNE'),
)

DISPATCHES = (
    ('ASIA', 'Cyclone Alakar heads\nfor India', 'CYCLONE ALAKAR'),
    ('ASIA', 'Court seeks former\nPM Han', 'SEOUL'),
    ('NORTH AMERICA', 'Greenland backs\nArctic pact', 'NUUK'),
    ('NORTH AMERICA', '2,000+ walrus haul\nout in Alaska', 'ANCHORAGE'),
    ('NORTH AMERICA', 'Anthropic rises 17%\nafter $81bn IPO', 'NEW YORK / CNBC'),
)

# Pin coordinates are (longitude, latitude); the index is the printed ticker number.
BULLETINS = (
    ('Xi opens a hall in Shenzhen', (114.1, 22.5)),
    ('Ankara moves to strengthen ties', (32.9, 39.9)),
    ('Sheinbaum addresses tariffs', (-99.1, 19.4)),
    ('Mosque collapses in Jakarta', (106.8, -6.2)),
    ('Korean court proceedings continue', None),
    ('UK inquiry moves forward', (-0.1, 51.5)),
    ('Catalonia in the headlines', None),
    ('Roma author in the spotlight', None),
    ('Cook Islands in the headlines', (-159.8, -21.2)),
    ('Floods hit Spain', None),
    ('US and Venezuela resume military ties', None),
    ('Allies pledge support for Kyiv in Berlin', None),
    ('EU weighs EUR 45bn loan for Ukraine', None),
    ('Putin rejects sea and energy truce', None),
    ('Russian strikes kill 2 and injure 23', None),
    ('Israel ends Gaza operation', None),
    ('Troops mass near Ethiopia-Eritrea border', (39.0, 14.5)),
    ('Bitcoin closes at $62,942', None),
    ('US Senate blocks bid to end Iran war', None),
)

DESK_COLORS = {
    'EUROPE': (31, 78, 156), 'MIDDLE EAST': (136, 82, 20),
    'NORTH AMERICA': (164, 57, 48), 'SOUTH AMERICA': (130, 52, 99),
    'OCEANIA': (39, 104, 91), 'ASIA': (142, 65, 38),
}


def label(page, text, x, y, width, size=8, color=GREY, *, weight=2, font=TAG, tracking=.38):
    # Snap the left edge to the same raster grid used to check glyph bounds.
    left = round(x*SCALE)/SCALE
    return page.text(text, left, y, size, color, weight, font, x+width-left, tracking,
                     ink_top=True)


def centered(page, text, x, y, width, size, color=INK, *, weight=2, font=SANS, tracking=0):
    margin = (width-measure(text, size, font, tracking))/2
    assert margin >= 1, (text, width)
    label(page, text, x+margin, y, width-margin, size, color,
          weight=weight, font=font, tracking=tracking)


def byline(page, text, x, width, card_bottom):
    previous_bottom = page.text_boxes[-1][1][3]
    y = math.ceil((previous_bottom+8)*SCALE)/SCALE
    first = len(page.text_boxes)
    page.rect(x, y+3, 8, 1, RED)
    label(page, text, x+13, y, width-13, 7.2, GREY, weight=2, tracking=.62)
    _, (_,top,_,bottom) = page.text_boxes[first]
    assert top-previous_bottom >= 8, (text,'byline top gap')
    assert card_bottom-bottom >= 10, (text,'byline bottom gap',card_bottom,bottom)
    return bottom


def check_bounds(page, first, x, y, w, h):
    for text, (left, top, right, bottom) in page.text_boxes[first:]:
        assert x <= left < right <= x+w and y <= top < bottom <= y+h, (
            text, 'section bounds', (left, top, right, bottom), (x, y, x+w, y+h))


def column_rules(page, top, bottom):
    assert 3*COLUMN+2*GUTTER == WIDTH
    for index in (1, 2):
        center = EDGE+index*(COLUMN+GUTTER)-GUTTER/2
        page.rect(center-.5, top, 1, bottom-top, RULE)


def desk_chip(page, desk, x, y):
    size, tracking = 7.5, .65
    width = math.ceil(measure(desk, size, TAG, tracking))+12
    page.rect(x, y+4, 5, 5, DESK_COLORS[desk])
    page.rect(x+9, y, width, 13, INK)
    label(page, desk, x+15, y+2.5, width-10, size, (255, 255, 255), tracking=tracking)


def masthead(page, count):
    label(page, f'THE WORLD IN ONE DAY · {count} STORIES · ACROSS THE GLOBE',
          EDGE, 23, 783, 10, RED, tracking=.7)
    label(page, 'WORLD EDITION', 872, 23, 124, 10, GREY, tracking=.7)
    centered(page, 'THURSDAY 19 NOVEMBER 2026', EDGE, 51, WIDTH, 44, weight=6,
             font=MASTHEAD, tracking=1.5)
    page.rect(EDGE, 129, WIDTH, 2, INK)
    page.rect(EDGE, 135, WIDTH, .5, INK)


def stats_bar(page):
    stats = (
        ('3', 'TRILATERAL SUMMIT'), ('9-6', 'WORLD COURT VOTE'),
        ('$120bn', 'COP31 CLIMATE AID'), ('$81bn', 'ANTHROPIC IPO'),
        ('109-0', 'SENATE VOTE'), ('4.9%', 'UNEMPLOYMENT'), ('+2,000', 'ALASKAN WALRUS'),
    )
    cell = WIDTH/len(stats)
    for y, thickness in ((140, 1.5), (144, .5), (198, .5), (202, 1.5)):
        page.rect(EDGE, y, WIDTH, thickness, INK)
    for x in (EDGE, EDGE+WIDTH-.5):
        page.rect(x, 140, .5, 63.5, INK)
    for index, (number, title) in enumerate(stats):
        x = EDGE+index*cell
        first = len(page.text_boxes)
        if index:
            page.rect(x, 145, .5, 53, RULE)
        color = RED if number in ('9-6', '$120bn') else INK
        centered(page, number, x+4, 149, cell-8, 25, color, weight=5, font=HEADLINE)
        centered(page, title, x+4, 185, cell-8, 8, GREY, font=TAG, tracking=.4)
        check_bounds(page, first, x+4, 145, cell-8, 53)


class Illustration:
    def __init__(self, page, x, y, width, height):
        self.page, self.x, self.y = page, x, y
        self.width, self.height = width, height
        self.shapes = 0

    def bounds(self, left, top, right, bottom):
        assert 0 <= left <= right <= self.width and 0 <= top <= bottom <= self.height
        self.shapes += 1
        assert self.shapes <= 60

    def rect(self, x, y, w, h, color):
        self.bounds(x, y, x+w, y+h)
        self.page.rect(self.x+x, self.y+y, w, h, color)

    def dot(self, x, y, r, color):
        self.bounds(x-r, y-r, x+r+.5, y+r+.5)
        self.page.dot(self.x+x, self.y+y, r, color)

    def path(self, points, color, weight=3):
        xs, ys = zip(*points)
        pad = weight/(2*SCALE)+.5
        self.bounds(min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad)
        for (x, y), (xx, yy) in zip(points, points[1:]):
            self.page.line(self.x+x, self.y+y, self.x+xx, self.y+yy, color, weight)

    def polygon(self, points, color):
        xs, ys = zip(*points)
        self.bounds(min(xs), min(ys), max(xs), max(ys))
        edges = list(zip(points, points[1:]+points[:1]))
        for row in range(round(min(ys)*SCALE), round(max(ys)*SCALE)):
            y = (row+.5)/SCALE
            hits = sorted(x+(y-y0)*(xx-x)/(y1-y0) for (x, y0), (xx, y1) in edges
                          if min(y0, y1) <= y < max(y0, y1))
            assert len(hits) % 2 == 0
            for left, right in zip(hits[::2], hits[1::2]):
                self.page.rect(self.x+left, self.y+row/SCALE, right-left, 1/SCALE, color)

    def type(self, text, x, y, width, size, color, font=TAG, weight=2):
        first = len(self.page.text_boxes)
        centered(self.page, text, self.x+x, self.y+y, width, size, color, font=font, weight=weight)
        check_bounds(self.page, first, self.x+x, self.y+y, width, self.height-y)


def summit_art(art):
    backdrop = (39, 36, 44)
    cream, gold, scarlet = (252, 242, 221), (242, 185, 79), (219, 70, 53)
    art.rect(0, 0, art.width, art.height, backdrop)
    art.rect(12, 12, art.width-24, 112, (66, 54, 60))
    for y in (16, 20, 102):
        art.rect(16, y, art.width-32, 1, (103, 77, 73))
    for center, name, jacket, halo, skin, hair in (
        (56, 'TRUMP', BLUE, (81, 109, 157), (242, 177, 136), gold),
        (154, 'XI', scarlet, (164, 65, 51), (232, 167, 119), (40, 32, 32)),
        (252, 'PUTIN', BLUE, (92, 118, 159), (235, 188, 158), (180, 156, 133)),
    ):
        def poly(points, color):
            art.polygon(tuple((center+x, y) for x, y in points), color)

        art.dot(center, 57, 41, halo)
        art.rect(center-7, 67, 14, 17, skin)
        poly(((-40, 109), (-35, 88), (-10, 77), (10, 77), (35, 88), (40, 109)), jacket)
        art.rect(center-14, 34, 28, 26, skin)
        art.dot(center, 58, 13.5, skin)
        poly(((-14, 44), (-16, 35), (-7, 27), (11, 26), (16, 32), (13, 42), (9, 35), (-8, 37)), hair)
        art.rect(center-8, 50, 3, 2, INK)
        art.rect(center+5, 50, 3, 2, INK)
        art.path(((center, 51), (center-2, 57), (center+1, 57)), (158, 96, 73), 2)
        art.rect(center-4, 62, 8, 1, (138, 79, 59))
        poly(((-11, 77), (11, 77), (0, 98)), gold if name == 'XI' else cream)
        poly(((0, 82), (3, 89), (0, 104), (-3, 89)), gold if name == 'XI' else scarlet)
        seam = tuple(channel*3//4 for channel in jacket)
        art.path(((center-15, 82), (center-19, 89), (center-8, 102)), seam)
        art.path(((center+15, 82), (center+19, 89), (center+8, 102)), seam)
        if name == 'TRUMP':
            for y, color in ((92, scarlet), (95, cream), (98, scarlet)):
                art.rect(center-28, y, 11, 2, color)
        elif name == 'XI':
            poly(((-23, 87), (-21, 91), (-17, 92), (-21, 95), (-23, 99),
                  (-25, 95), (-29, 92), (-25, 91)), gold)
        else:
            for y, color in ((91, cream), (94, (82, 136, 207)), (97, scarlet)):
                art.rect(center-28, y, 11, 3, color)
        art.rect(center-37, 108, 74, 18, cream)
        art.type(name, center-37, 112, 74, 8.5, INK)


def court_art(art):
    backdrop, field = (31, 46, 58), (39, 63, 79)
    stone, light, gold = (190, 175, 145), (247, 232, 202), (245, 180, 72)
    art.rect(0, 0, art.width, art.height, backdrop)
    art.rect(12, 12, art.width-24, 112, field)
    art.polygon(((29, 57), (113, 20), (197, 57)), light)
    art.polygon(((58, 51), (113, 29), (168, 51)), stone)
    art.dot(113, 43, 4, backdrop)
    art.rect(203, 23, 1, 96, (67, 89, 103))
    art.rect(37, 57, 152, 8, stone)
    for x in (48, 75, 102, 129, 156):
        art.rect(x, 67, 18, 5, light)
        art.rect(x+3, 72, 12, 33, light)
        art.rect(x+12, 72, 3, 33, stone)
        art.rect(x+7, 74, .5, 29, stone)
        art.rect(x, 105, 18, 4, light)
    art.rect(38, 109, 151, 5, light)
    art.rect(31, 114, 165, 5, stone)
    art.rect(23, 119, 181, 5, light)
    art.path(((252, 31), (252, 85)), gold, 5)
    art.path(((230, 42), (274, 42)), gold, 5)
    art.dot(252, 33, 4, light)
    for x in (230, 274):
        art.path(((x-11, 67), (x, 44), (x+11, 67)), light)
        art.polygon(((x-13, 67), (x+13, 67), (x+7, 74), (x-7, 74)), gold)
    art.rect(236, 84, 32, 4, gold)
    art.rect(221, 99, 62, 25, light)
    art.type('9-6', 221, 105, 62, 13, INK, weight=3)


def climate_art(art):
    field, water, leaf = (38, 69, 65), (67, 125, 170), (159, 198, 138)
    white, heat = (250, 231, 191), (226, 76, 53)
    art.rect(0, 0, art.width, art.height, (29, 47, 45))
    art.rect(12, 12, art.width-24, 112, field)
    for y in (33, 54, 75):
        art.path(((27, y), (43, y-4), (59, y+1), (76, y-3)), (70, 106, 96), 2)
    art.dot(129, 60, 42, (73, 100, 85))
    art.dot(129, 60, 38, water)
    art.path(((94, 48), (164, 48)), (138, 174, 190))
    art.path(((92, 68), (166, 68)), (138, 174, 190))
    art.path(((128, 23), (115, 35), (110, 59), (116, 85), (128, 97)), (138, 174, 190))
    art.path(((130, 23), (143, 35), (148, 59), (142, 85), (130, 97)), (138, 174, 190))
    art.polygon(((102, 37), (116, 28), (129, 35), (127, 43), (112, 46), (115, 57),
                 (107, 58), (98, 49)), leaf)
    art.polygon(((114, 56), (129, 60), (135, 70), (126, 82), (120, 91), (115, 78)), leaf)
    art.polygon(((146, 36), (153, 32), (163, 44), (166, 58), (156, 59), (152, 70),
                 (145, 63), (147, 53), (135, 48)), leaf)
    art.dot(208, 79, 14, white)
    art.dot(208, 31, 8, white)
    art.rect(200, 31, 16, 48, white)
    art.rect(205, 48, 6, 32, heat)
    art.dot(208, 79, 9, heat)
    for y in (36, 46, 56, 66):
        art.rect(222, y, 9, 2, white)
    art.path(((246, 70), (258, 59), (270, 59), (281, 44)), (199, 149, 83))
    art.rect(25, 103, art.width-50, 22, white)
    art.rect(25, 103, 3, 22, AMBER)
    first = len(art.page.text_boxes)
    # Pull quote from our own climate brief.
    art.type('"leaves out the goal for fossil-fuel aid"', 33, 108, art.width-66,
             8.5, INK, font=condensed(.9, ROMAN), weight=3)
    check_bounds(art.page, first, art.x+33, art.y+107, art.width-66, 15)


def section_header(page, title, right, y):
    label(page, title, EDGE, y, 400, 10.5, RED, weight=3, tracking=.92)
    width = measure(right, 8.5, TAG, .75)
    label(page, right, EDGE+WIDTH-width-2, y+1, width+2, 8.5, tracking=.75)


def hero_row(page):
    section_header(page, 'THE FRONT PAGE', 'DIPLOMACY · JUSTICE · CLIMATE', 214)
    art_top, bottom = 229, 510
    column_rules(page, art_top, bottom-6)
    for index, ((title, caption, lines, detail, source), draw) in enumerate(zip(
            HEROES, (summit_art, court_art, climate_art))):
        x = EDGE+index*(COLUMN+GUTTER)
        first = len(page.text_boxes)
        draw(Illustration(page, x, art_top, COLUMN, 138))
        copy_start = len(page.text_boxes)
        label(page, title, x, 371, COLUMN, 10, RED, weight=3, tracking=.7)
        label(page, caption, x, 385, COLUMN, 7.3, tracking=.25)
        headline_size = 19.8
        headline_lines = wrap(' '.join(lines), headline_size, COLUMN-5, HERO_HEADLINE)
        assert len(headline_lines) == 2, (title, headline_lines)
        for line_index, line in enumerate(headline_lines):
            label(page, line, x, 395+line_index*30, COLUMN, headline_size, weight=4,
                  font=HERO_HEADLINE, tracking=.15)
        detail_size = 8.5
        detail_lines = wrap(detail, detail_size, COLUMN-3, SANS)
        assert len(detail_lines) == 2, (source, detail_lines)
        for line_index, line in enumerate(detail_lines):
            label(page, line, x, 456+line_index*14, COLUMN, detail_size, font=SANS, tracking=0)
        byline(page, source, x, COLUMN, bottom)
        # Consecutive text blocks must have visible clearance, including descenders.
        copy = page.text_boxes[copy_start:]
        for (a, box), (b, following) in zip(copy, copy[1:]):
            assert round((following[1]-box[3])*SCALE) >= 2, (a, b, box, following)
        check_bounds(page, first, x, art_top, COLUMN, bottom-art_top)
        page.rendered.append(lines[0])


def small_icon(art, icon, color):
    art.rect(0, 0, 49, 49, (232, 223, 205))
    if icon == 'bridge':
        art.rect(6, 28, 37, 4, color)
        for x in (13, 33):
            art.rect(x, 14, 3, 23, color)
        art.path(((7, 25), (14, 15), (24, 25), (34, 15), (42, 25)), color, 4)
        art.path(((8, 40), (41, 40)), color, 2)
    elif icon == 'missile':
        art.polygon(((12, 30), (30, 12), (40, 9), (37, 19), (19, 37), (13, 36)), color)
        art.polygon(((14, 26), (10, 24), (17, 17), (23, 17), (31, 25), (31, 31),
                     (24, 38), (22, 33)), color)
        art.path(((9, 39), (14, 34)), AMBER, 4)
    elif icon == 'chart':
        art.path(((9, 10), (9, 39), (41, 39)), color)
        art.path(((13, 15), (22, 22), (27, 19), (39, 32)), color, 5)
        art.polygon(((32, 32), (40, 25), (40, 34)), color)
    elif icon == 'game':
        art.polygon(((9, 18), (39, 18), (43, 31), (39, 36), (34, 35), (29, 30),
                     (20, 30), (15, 35), (9, 36), (6, 31)), color)
        art.rect(12, 23, 10, 2, PAPER)
        art.rect(16, 19, 2, 10, PAPER)
        art.dot(33, 23, 1.6, PAPER)
        art.dot(37, 27, 1.6, PAPER)
    elif icon == 'fist':
        art.polygon(((16, 37), (16, 29), (10, 23), (10, 18), (14, 16), (18, 21),
                     (18, 13), (35, 13), (38, 18), (38, 26), (32, 33), (32, 37)), color)
        for x, y in ((18, 10), (23, 8), (28, 9), (33, 11)):
            art.rect(x, y, 4, 11, color)
        art.path(((14, 20), (23, 24), (29, 22)), PAPER, 3)
        art.rect(16, 39, 16, 3, color)
    else:
        assert icon == 'medal'
        art.polygon(((12, 8), (20, 8), (28, 27), (19, 29)), color)
        art.polygon(((28, 8), (36, 8), (29, 29), (21, 27)), color)
        art.dot(24, 32, 9, AMBER)
        art.dot(24, 32, 5, color)
        art.rect(23, 29, 2, 6, PAPER)


def secondary_grid(page):
    page.rect(EDGE, 510, WIDTH, 1, INK)
    section_header(page, 'AROUND THE WORLD', 'SIX STORIES IN FOCUS', 521)
    column_rules(page, 535, 722)
    for index, (desk, icon, headline, detail, source) in enumerate(FEATURES):
        row, col = divmod(index, 3)
        x, y = EDGE+col*(COLUMN+GUTTER), 535+row*94
        first = len(page.text_boxes)
        page.rect(x, y, COLUMN, .5, RULE)
        small_icon(Illustration(page, x, y+8, 49, 49), icon, DESK_COLORS[desk])
        tx, inner = x+59, COLUMN-59
        desk_chip(page, desk, tx, y+2)
        headline_size, leading = 12.5, 19
        lines = wrap(headline, headline_size, inner-3, HEADLINE)
        assert 1 <= len(lines) <= 2
        if len(lines) == 2:
            words = headline.split()
            breaks = [(' '.join(words[:i]), ' '.join(words[i:])) for i in range(1, len(words))]
            lines = min(breaks, key=lambda pair: max(measure(line, headline_size, HEADLINE)
                                                     for line in pair))
        for line_index, line in enumerate(lines):
            label(page, line, tx, y+17+line_index*leading, inner, headline_size, INK, weight=3,
                   font=HEADLINE, tracking=.1)
        label(page, detail, tx, y+17+len(lines)*leading, inner, 8.6, font=TAG, tracking=0)
        byline(page, source, tx, inner, y+94)
        check_bounds(page, first, x, y, COLUMN, 94)
        page.rendered.append(headline)


def dispatch_row(page):
    page.rect(EDGE, 727, WIDTH, 1, INK)
    cell = WIDTH/len(DISPATCHES)
    for index, (desk, headline, source) in enumerate(DISPATCHES):
        left = EDGE+index*cell
        x = round((left+(10 if index else 0))*SCALE)/SCALE
        inner = left+cell-x-7
        first = len(page.text_boxes)
        if index:
            page.rect(left, 735, .5, 61, RULE)
        desk_chip(page, desk, x, 734)
        for line_index, line in enumerate(headline.splitlines()):
            label(page, line, x, 750+line_index*17, inner, 11.5, INK, weight=3, font=HEADLINE)
        label(page, source, x, 784, inner, 7.3, tracking=.35)
        check_bounds(page, first, x, 735, inner, 61)
        page.rendered.append(headline)


def dot_map(page, x, y):
    step = 1.45
    mw, mh = MASK_COLS*step, MASK_ROWS*step
    packed = base64.b64decode(LANDMASK_B64, validate=True)
    assert len(packed)*8 == MASK_COLS*MASK_ROWS
    # Sample every other row and column to preserve visible paper between dots.
    for row in range(0, MASK_ROWS, 2):
        for col in range(0, MASK_COLS, 2):
            bit = row*MASK_COLS+col
            if packed[bit//8] & (0x80 >> (bit % 8)):
                page.dot(x+(col+.5)*step, y+(row+.5)*step, .55, LAND)
    pins = []
    for index, (_, location) in enumerate(BULLETINS, 1):
        if location is None:
            continue
        lon, lat = location
        px, py = x+(lon+180)/360*mw, y+(90-lat)/180*mh
        assert all(math.hypot(px-xx, py-yy) >= 13 for xx, yy in pins), (index, 'pin overlap')
        assert x <= px-6.5 and px+6.5 <= x+mw and y <= py-6.5 and py+6.5 <= y+mh
        pins.append((px, py))
        page.dot(px, py, 6.25, PAPER)
        page.dot(px, py, 5, RED)
        centered(page, str(index), px-6, py-2.5, 12, 5, PAPER, font=TAG)


def ticker(page):
    page.rect(EDGE, 799, WIDTH, 1.5, INK)
    section_header(page, 'WHERE IT HAPPENED', 'NEWS IN BRIEF · MAP PINS MATCH STORY NUMBERS', 810)
    dot_map(page, EDGE, 827)
    label(page, 'DOT MAP: NATURAL EARTH 1:110M', EDGE, 959, 260, 6.5, tracking=.35)
    top, row_height, rows = 829, 14, 10
    for col, x in enumerate((307, 654)):
        page.rect(x-9, 827, .5, top+rows*row_height-827, RULE)
        start = col*rows
        for row, (headline, _) in enumerate(BULLETINS[start:start+rows]):
            y = top+row*row_height
            first = len(page.text_boxes)
            label(page, f'{start+row+1:02d}', x, y+1, 22, 8.3, RED, weight=3, tracking=.55)
            label(page, headline, x+25, y, 309, 9.2, INK, font=SANS, tracking=.05)
            check_bounds(page, first, x, y, 334, row_height)
            page.rendered.append(headline)


def footer(page):
    page.rect(EDGE, 971, WIDTH, 1.5, INK)
    page.rect(EDGE, 975, WIDTH, .5, RULE)
    centered(page, 'DATE CHECK: Every story on this paper happened on or before 19 Nov 2026',
             EDGE, 988, WIDTH, 8.8, INK, weight=2, tracking=.22)
    centered(page, 'SOURCES: REUTERS, AP, AFP, BBC, AL JAZEERA, CNN, NBC, TIMES OF INDIA, GUARDIAN, '
             'LE MONDE, KYIV INDEPENDENT, SYDNEY MORNING HERALD — 2026-11-19',
             EDGE, 1004, WIDTH, 7.2, GREY, font=TAG, tracking=.32)


def main():
    page = Page()
    count = sum(map(len, (HEROES, FEATURES, DISPATCHES, BULLETINS)))
    masthead(page, count)
    stats_bar(page)
    hero_row(page)
    secondary_grid(page)
    dispatch_row(page)
    ticker(page)
    footer(page)
    assert len(page.rendered) == len(set(page.rendered)) == count == 33
    # Compare actual glyph ink rectangles, including descenders and stroke width.
    for i,(a,box) in enumerate(page.text_boxes):
        for b,other in page.text_boxes[i+1:]:
            overlap = min(box[2],other[2]) > max(box[0],other[0]) and min(box[3],other[3]) > max(box[1],other[1])
            assert not overlap, ('text overlap',a,b,box,other)
    png = page.png()
    assert len(png) <= 1048576
    output = os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
    os.makedirs(output,exist_ok=True)
    path = os.path.join(output,'entry.png')
    with open(path,'wb') as f:
        f.write(png)
    print(json.dumps({'output':path,'bytes':len(png),'sha256':hashlib.sha256(png).hexdigest(),
                      'stories':len(page.rendered),'text_bounds_checked':len(page.text_boxes),
                        'layout':'The World in One Day newspaper front page'},sort_keys=True))


if __name__ == '__main__':
    main()
