# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Jw_cadの座標コマンドで出力した座標データをCSV形式で出力する。
"""
import csv
import tkinter as tk

def is_float(s):
    """
    入力された文字列がFloatに変換可能ならTrueを返し、
    そうでない場合はFalseを返す。

    Parameters
    ----------
    s : str
        変換できるかどうか確認したい文字列
    """
    try:
        float(s)
    except:
        return False
    return True


def point_counter():
    """
    座標点カウントアップ用のGenerator
    """
    pt = 0
    while True:
        yield pt
        pt += 1


def write_csv(jw_filename, csv_filename):
    """
    座標点名,X座標,Y座標,H座標(0固定)
    というフォーマットでCSVに書き出す

    Parameters
    ----------
    jw_geofile : str
        Jwwから読み出した座標データのテキストファイル名
    csv_name : str
        書き出し用CSVのファイル名
    """
    try:
        with open(jw_filename, 'r') as geo_f, open(csv_filename, 'w') as csv_f:
            writer = csv.writer(csv_f, lineterminator='\n')
            pt_count = point_counter() # 座標点 ex. pt1, pt2, pt3,...
            tr_count = point_counter() # トラバー点 ex. tr1, tr2,...
            pt = []
            tr = []
            for line in geo_f:
                line = line.strip().split()
                if(is_float(line[0])):
                    z = zip(*[iter(line)]*2)
                    for tpl in z:
                        # Jw_cadで出力したデータはY座標,X座標という順番になっているので、X座標,Y座標という順番に入れ替えてCSVへ出力する
                        pt.append([tpl[1], tpl[0], 0])
                elif(line[0] == 'pt'):
                    line[0] = 'Tr' + str(next(tr_count))
                    line[1], line[2] = line[2], line[1]
                    line.append(0)
                    tr.append(line)
            pt = list(map(list, set(map(tuple, pt))))
            for i in range(len(pt)):
                pt[i].insert(0, 'Pt' + str(next(pt_count)))
            writer.writerows(pt)
            writer.writerows(tr)
    except IOError as ex:
        print(ex)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        pass

if __name__ == '__main__':
    jw_file = 'zahyo.txt'
    csv_file = 'geo.csv'
    write_csv(jw_file, csv_file)
    # root = tk.Tk()
    # app = Application(master=root)
    # app.mainloop()