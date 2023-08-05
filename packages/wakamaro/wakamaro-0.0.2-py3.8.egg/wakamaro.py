# coding: utf-8

# Overview of Data
# the Center for Open Data in the Humanities
# “The Dataset of Pre-Modern Japanese Text (the National Institute of Japanese Literature)
# http://codh.rois.ac.jp/index.html.en

# Data Licensing
# CC BY-SA

# Link to download data
# http://codh.rois.ac.jp/pmjt/package/text.zip

import subprocess as sp
import os
import zipfile
import glob
import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import japanize_matplotlib
import cv2


if os.path.exists('text.zip') == True:
    print('Data already exists')

else:
    sp.call("wget http://codh.rois.ac.jp/pmjt/package/text.zip",shell=True)
    with zipfile.ZipFile('text.zip') as zf:
        for info in zf.infolist():
            info.filename = info.filename.encode('cp437').decode('cp932')
            zf.extract(info, 'text_data')

    path = './text_data/200007092/text/*.txt'

    file_ls = glob.glob(path)

    file_ls.sort()

    file_ls_name_21 = ['01_古今和歌集.txt', '02_後撰和歌集.txt', '03_拾遺和歌集.txt',
                    '04_後拾遺和歌集.txt', '05_金葉和歌集.txt',
                    '06_詞花和歌集.txt', '07_千載和歌集.txt',
                    '08_新古今和歌集.txt', '09_新勅撰和歌集.txt',
                    '10_続後撰和歌集.txt', '11_続古今和歌集.txt',
                    '12_続拾遺和歌集.txt', '13_新後撰和歌集.txt',
                    '14_玉葉和歌集.txt', '15_続千載和歌集.txt',
                    '16_続後拾遺和歌集.txt', '17_風雅和歌集.txt',
                    '18_新千載和歌集.txt', '19_新拾遺和歌集.txt',
                    '20_新後拾遺和歌集.txt','21_新続古今和歌集.txt',
                    '00_二十一代集データについて.txt']
    num = 0
    for file in file_ls:
        os.rename(file, './text_data/200007092/text/' + file_ls_name_21[num])
        num += 1

path = './text_data/200007092/text/*.txt'
file_ls_rename = glob.glob(path)
file_ls_rename.sort()

def text_read(text_koten):
    text_target_read = open(text_koten,'r', encoding="cp932")
    text_target = text_target_read.read()
    text_target_read.close
    text_target

    text_target_split = text_target.split('￥Ｍ',1)
    text_target_split[0]
    text_target_split[1]
    test_text = text_target_split[1]

    test_text_sho = test_text.split('Ｖ')
    test_text_sho_ls = []

    for i in range(len(test_text_sho)):
        test_text_sho_ls_elem = test_text_sho[i].split('\n')
        test_text_sho_ls.append(test_text_sho_ls_elem[0])

    test_text_split = test_text.split('Ｎ')
    test_text_split = test_text_split[1:]
    
    df = pd.DataFrame(test_text_split, columns = [text_koten])
    
    df['N']  = df[text_koten].str.split(pat='\n', expand=True)[0]
    df['K']  = df[text_koten].str.split(pat='Ｋ', expand=True)[1]
    df['L']  = df[text_koten].str.split(pat='Ｌ', expand=True)[1]
    df['H']  = df[text_koten].str.split(pat='Ｈ', expand=True)[1]
    df['I']  = df[text_koten].str.split(pat='Ｉ', expand=True)[1]
    df['W']  = df[text_koten].str.split(pat='Ｗ', expand=True)[1]
    df['X']  = df[text_koten].str.split(pat='Ｘ', expand=True)[1]
    try:
        df['Y']  = df[text_koten].str.split(pat='Ｙ', expand=True)[1]
    except KeyError :
        pass
    try:
        df['Z']  = df[text_koten].str.split(pat='Ｚ', expand=True)[1]
    except KeyError :
        pass
    df['S']  = df[text_koten].str.split(pat='Ｓ', expand=True)[1]
    
    df['K']  = df['K'].str.split(pat='\n', expand=True)[0]    
    df['L']  = df['L'].str.split(pat='\n', expand=True)[0]
    df['H']  = df['H'].str.split(pat='\n', expand=True)[0]
    df['I']  = df['I'].str.split(pat='\n', expand=True)[0]
    df['W']  = df['W'].str.split(pat='\n', expand=True)[0]
    df['X']  = df['X'].str.split(pat='\n', expand=True)[0]
    try:
        df['Y']  = df['Y'].str.split(pat='\n', expand=True)[0]
    except KeyError :
        pass
    try:
        df['Z']  = df['Z'].str.split(pat='\n', expand=True)[0]
    except KeyError :
        pass
    return df

parser = argparse.ArgumentParser()
parser.add_argument('arg1')
parser.add_argument('arg2')
args = parser.parse_args()
print('【waka poetry anthology：'+args.arg1+'】')
print('【appearance more than'+args.arg2+'times】')

text_target_name= file_ls_rename[int(args.arg1)]

df_kokin = text_read(text_target_name)
df_kokin_drop = df_kokin.drop(['K', 'L', 'H', 'X', 'Y', 'Z', 'S'], axis=1)

text_target_name_2 = text_target_name.split('/')
text_target_name_2 = text_target_name_2[4].split('.txt')
text_target_name_2 = text_target_name_2[0]
text_target_name_2

poets_value_counts = df_kokin_drop['I'].value_counts()
df_poets_value_counts = pd.DataFrame(poets_value_counts)
df_poets_value_counts['I']

if_1 = df_poets_value_counts.index[(df_poets_value_counts['I'] <= int(args.arg2))]
df_poets_value_counts.drop(if_1, inplace=True)

fig = plt.figure()
value_counts = df_poets_value_counts['I']
poets=  df_poets_value_counts.index.tolist()
fig = plt.figure(figsize=(20,7))
fig.subplots_adjust(bottom=0.3)
plt.title(text_target_name_2)
plt.xlabel("Waka poets")
plt.ylabel("Number of waka poetry")
plt.bar(poets, value_counts, tick_label= poets, align="center", color='darkcyan')

percent = round(100.*value_counts / value_counts.sum(),1)

def main():
    plt.savefig(text_target_name_2 + '_bar.png')
    plt.show()
    img_color = cv2.imread(text_target_name_2 + '_bar.png')
    cv2.imshow('color', img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

print('【Number of waka poetry by each poet in',text_target_name_2,'】')
print(value_counts)
print('【Percentage of waka poetry by each poet in',text_target_name_2,'】')
print(percent)

if __name__ == "__main__":
    main()
