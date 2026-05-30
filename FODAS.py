import tkinter as tk
from tkinter import messagebox
import json
import math
import random
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage,bpm2tempo 
from midi2audio import FluidSynth
import pygame.midi
import pygame.mixer
from time import sleep
import os
import sys
import tempfile
import shutil
import subprocess 
import threading
import time
import os

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# SCRIPT_DIR の内容がコンソールに出力され、パスが正しいか確認できます
print(f"📁 スクリプト実行ディレクトリ: {SCRIPT_DIR}")
pygame.mixer.init(frequency=44100, size=-16, channels=2)
# JSONファイルを開く
with open('data.json', 'r', encoding='utf-8') as file:
    game_data = json.load(file)
with open('save.json', 'r', encoding='utf-8') as file:
    game_save = json.load(file)    
# "achievement" が存在しなければ追加（補完）
if "achievement" not in game_save["resource"][0]:
    game_save["resource"][0]["achievement"] = []

# 変更を保存
    with open('save.json', 'w', encoding='utf-8') as file:
     json.dump(game_save, file, indent=4, ensure_ascii=False)

# 変換したデータを確認
#print(game_data)


root = tk.Tk()#tkinter Tk() Tk()はウィンドウを作る命令

nokakunin=tk.IntVar()
def kakunin():
  root2 = tk.Tk()
  root2.geometry("150x70")
  title = tk.Label(root2,text="ゲームを終了しますか？",font=("Arial",9))
  title.place(x=0,y=0) 
  button=tk.Button(root2,text="はい",font=("Arial",6),command=exit)
  button.place(x=0,y=50)


root.protocol("WM_DELETE_WINDOW", kakunin)
root.resizable(False, False)

#変数
cost=[0,10,50,100,200,300,500,700,1000,1800,3000,4000,13,14,15,16,17,18,19,20,21,22,23,5000,5000,26,27,28,29,9999,9999]
sellingprice=[0,5,25,40,90,150,350,500,700,900,1200,2500,13,14,15,16,17,18,19,20,21,22,23,4000,4000,26,27,28,29,9999,9999]
skillprice=[30,100,1000]
itemsendspot = 0
damagesave= -1
a=0
scene = 0
days = 1
area = 0
act=5
hp = 50
at = 5
df = 3
lv = 1
atex = 0
atex2=0
atex3=0
dfex = 0
dfex2=0
dfex3=0
atdef = 5
dfdef = 3
hpex=0
hpex2=0
hpex3=0
hpdef=50
itemskill1=0
itemskill2=0
itemskill3=0
itemskill4=0
stat=0
enemyskill=0
enemyskillpar=0
skillmess=""
statmess=""
exp = 0
clearflag=0
print(f"クリアしてない！！！！！！！！！{clearflag}")
keynoiti=-1

ename = "null"
ehp = 1
eat = 1
edf = 1
eexp = 1
edrop = 1
edrop2 = 1
elv = 1

critmess = 0
lvdef=1
expdef=0
hpnow = 50
atdefdef = 0
dfdefdef = 0
hpdefdef = 0
ehpnow = 1

attack = 0
defense = 0
damage=0

weapon=-1
weaponname="-"
armor=-1
armorname="-"
accessory1=-1
accessoryname="-"
accessory2=-1
equip=-1
itemtype=-1

turn=0#turn0=自分ターン。

menu_items=['absolute','betray','null','null']
menu_now = 0
menu_decide = 0


root.title("FODAS ~FOurteen DAys Survival~")
root.geometry("400x300")  

item_data = game_data["items"]

enemies = game_data["enemies"]

saves = game_save["itemsave"]

enemy = 0
enemy_data = ['absolute','betray','null','null']
print(enemies)
item = 0
itemname = ""
itemsname=""
itemid = -1
pages = 0

crit=0

iteming = 0
items = ['absolute','betray','null','null']
print(enemies)


skill_no = 0

en_tables={
1:[0,0,0,0,1,1,1,2,2,2],
2:[0,0,0,1,1,1,1,2,2,2],
3:[0,0,0,1,1,1,2,2,2,2],
4:[0,0,1,1,1,2,2,2,3,3],
5:[1,1,1,2,2,2,3,3,3,3],
6:[2,2,2,2,3,3,3,4,4,4],
7:[2,2,3,3,3,4,4,4,4,4],
8:[3,3,3,4,4,4,4,5,5,5],
9:[4,4,4,4,5,5,5,6,6,6],
10:[4,4,5,5,5,6,6,6,7,7],
11:[5,5,5,6,6,6,7,7,7,8],
12:[6,6,6,7,7,7,8,8,8,9],
13:[7,7,7,8,8,8,9,9,9,10],
14:[8,8,8,9,9,9,10,10,10,10],
15:[11],
17:[0,1,2],
18:[3,4,7],
19:[6,5,8],
20:[9,10],
21:[13,14],
22:[3,6,8,15],
23:[16,5,7],
24:[10,10,20],
25:[0,1,2,3,4,5,6,7,8,9,10],
26:[11,11],
27:[21],
28:[0,0,0]
}
item_tables={
1:[0,1,2,3],
2:[0,1,2,3],
3:[0,1,2,3,4,5,6,7,23],
4:[0,1,2,3,4,5,6,7,23],
5:[4,5,6,7,],
6:[4,5,6,7,8,9,10,11,12],
7:[4,5,6,7,8,9,10,11,21,4,5,6,7,8,9,10,11,21,28],
8:[8,9,10,11],
9:[8,9,10,11],
10:[8,9,10,11,12,13,14,15,22],
11:[8,9,10,11,12,13,14,15,22],
12:[12,13,14,15],
13:[12,13,14,15],
14:[12,13,14,15,12,13,14,15,16,17,18,19],
17:[0,1,2,3,22],
18:[0,1,2,3,6,22],
19:[0,1,2,3,6,14,22],
20:[31],
21:[33],
22:[44,45,46],
23:[44,45,41],
24:[45,46,42],
25:[46,44,43],
26:[41,42,43],
27:[47],
28:[0],
}
def tablechange():
  global item_tables
  item_tables={
1:[35,36,37,20],
2:[],
3:[],
4:[],
5:[],
6:[],
7:[],
8:[],
9:[],
10:[],
11:[],
12:[],
13:[],
14:[],
17:[],
18:[],
19:[],

}
weapon_skill_table={
1:[3,5,6],
2:[3,5,6],
3:[3,5,6],
4:[3,5,6],
5:[3,5,6],
6:[3,5,6],
7:[3,5,6],
8:[3,5,6],
9:[3,5,6],
10:[3,5,6],
11:[3,5,6],
12:[3,5,6],
13:[3,5,6],
14:[3,5,6],
}
weapon_skill_table=[3,5,6]
wrare_skill_table=[1,4,8]
accessory_skill_table=[2,7]

loadflag = 0

inventory=[]
inv_data1=[]
inv_data2=[]
inv_data3=[]
inv_data4=[]
inv_star=[]

invmochi=[]
mochi1=[]
mochi2=[]
mochi3=[]
mochi4=[]

myskill=[0,0,0,0]

weaprank=0
armrank=0
accrank=0

itsk1=0
itsk2=0
itsk3=0
itsk4=0
sknm1="-"
sknm2="-"
sknm3="-"
sknm4="-"
skdt1=[]
skdt2=[]
skdt3=[]
skdt4=[]

mochikomiyoubanme=0

rndskill1=0
rndskill2=0
rndskill3=0
rndskill4=0
rndrareskill=0
rndskillX=0

itemtypeinv=0


#inv_data1.append(0)
#inv_data2.append(0)
#inv_data3.append(0)
#inv_data4.append(0)
#inventory.append(25)
def gameend():
   update_scene()
   global clearflag,area,weaprank,armrank,accrank,days,loadflag,inventory,scene,iteming,itemsname,weapon,armor,accessory1,scene,exp,lv,hp,df,at,hpdef,hpex,hpex2,hpex3,hpnow,damagesave,critmess,accessoryname,weaponname,armorname,atex,atex2,atex3,dfex,dfex2,dfex3  ,atdef,dfdef,item_data,item,itemname,itemid,inv_data1,inv_data2,inv_data3,inv_data4,itsk1,itsk2,itsk3,itsk4,itemskill1,itemskill2,itemskill3,itemskill4,sknm1,sknm2,sknm3,sknm4,skdt1,skdt2,skdt3,skdt4,itemtypeinv,rndskill1,rndskill2,rndskill3,rndskill4,rndrareskill,hp,hpnow   ,ehp,eat,edf,ename,at,df,ehpnow,attack,defense,damage,scene,act,exp,eexp,damagesave,pages,myskill,crit,skill_no ,items
 
   if clearflag==1:
    title = tk.Label(root,text="GAME CLEAR!",font=("Arial",20))
    title.place(x=70,y=10)
    title = tk.Label(root,text="島にかかっていた呪いを解いた。",font=("Arial",10))
    title.place(x=10,y=50)
    title = tk.Label(root,text="もう二度と迷い込むものは現れないだろう。",font=("Arial",10))
    title.place(x=10,y=70)
    title = tk.Label(root,text="しかし、封印された歴史を読み解くべく",font=("Arial",10))
    title.place(x=10,y=90)
    title = tk.Label(root,text="私は何度でも島に訪れる。",font=("Arial",10))
    title.place(x=10,y=110)
    title = tk.Label(root,text="呪いの元凶。海底から伸びる朽ち果てた塔。",font=("Arial",10))
    title.place(x=10,y=130)
    title = tk.Label(root,text="これらを解き明かす鍵を見つけるためにも。",font=("Arial",10))
    title.place(x=10,y=150)
    title = tk.Label(root,text="Thank You For Playing!",font=("Arial",15))
    title.place(x=80,y=170)
   else:
    title = tk.Label(root,text="GAME OVER",font=("Arial",20))
    title.place(x=70,y=10)
    title = tk.Label(root,text="島の呪いを解くのは容易ではない。",font=("Arial",10))
    title.place(x=10,y=50)
    title = tk.Label(root,text="だが、知恵と力を駆使し",font=("Arial",10))
    title.place(x=10,y=70)
    title = tk.Label(root,text="挑み続ければ必ず突破口は開ける。",font=("Arial",10))
    title.place(x=10,y=90)
    title = tk.Label(root,text="武器や防具の整備、狩りの計画。",font=("Arial",10))
    title.place(x=10,y=110)
    title = tk.Label(root,text="考え抜いた最適解で生き延び、",font=("Arial",10))
    title.place(x=10,y=130)
    title = tk.Label(root,text="呪いに打ち勝つのだ...!",font=("Arial",10))
    title.place(x=10,y=150)
    title = tk.Label(root,text="To Be Continued...",font=("Arial",15))
    title.place(x=80,y=170)
   scene = 0
   clearflag=0
   damagesave= -1
   area=0
   scene = 0
   days = 1
   loadflag = 0  
   act=5
   hp = 50
   at = 5
   df = 3
   lv = 1
   atex = 0
   atex2=0
   atex3=0
   dfex = 0
   dfex2=0
   dfex3=0
   atdef = 5
   dfdef = 3
   hpex=0
   hpex2=0
   hpex3=0
   hpdef=50
   itemskill1=0
   itemskill2=0
   itemskill3=0
   itemskill4=0

   exp = 0

   ename = "null"
   ehp = 1
   eat = 1
   edf = 1
   eexp = 1
   edrop = 1
   edrop2 = 1
   elv = 1

   critmess = 0

   hpnow = 50

   ehpnow = 1

   attack = 0
   defense = 0
   damage=0

   weapon=-1
   weaponname="-"
   armor=-1
   armorname="-"
   accessory1=-1
   accessoryname="-"
   accessory2=-1
   equip=-1
   itemtype=-1


   item_data = game_data["items"]

   enemies = game_data["enemies"]
   enemy = 0
   enemy_data = ['absolute','betray','null','null']
   print(enemies)
   item = 0
   itemname = ""
   itemsname=""
   itemid = -1
   pages = 0

   crit=0

   iteming = 0
   items = ['absolute','betray','null','null']
   print(enemies)


   skill_no = 0

   inventory=[]
   inv_data1=[]
   inv_data2=[]
   inv_data3=[]
   inv_data4=[]

   myskill=[0,0,0,0]

   itsk1=0
   itsk2=0
   itsk3=0
   itsk4=0
   sknm1="-"
   sknm2="-"
   sknm3="-"
   sknm4="-"
   skdt1=[]
   skdt2=[]
   skdt3=[]
   skdt4=[]

   rndskill1=0
   rndskill2=0
   rndskill3=0
   rndskill4=0
   rndrareskill=0
   rndskillX=0
   weaprank = 0
   armrank = 0
   accrank = 0
   itemtypeinv=0

   button=tk.Button(root,text="OK",font=("Arial",20),command=main)
   button.place(x=30,y=230)  
def gameending():
   update_scene()
   global area,weaprank,armrank,accrank,days,loadflag,inventory,scene,iteming,itemsname,weapon,armor,accessory1,scene,exp,lv,hp,df,at,hpdef,hpex,hpex2,hpex3,hpnow,damagesave,critmess,accessoryname,weaponname,armorname,atex,atex2,atex3,dfex,dfex2,dfex3  ,atdef,dfdef,item_data,item,itemname,itemid,inv_data1,inv_data2,inv_data3,inv_data4,itsk1,itsk2,itsk3,itsk4,itemskill1,itemskill2,itemskill3,itemskill4,sknm1,sknm2,sknm3,sknm4,skdt1,skdt2,skdt3,skdt4,itemtypeinv,rndskill1,rndskill2,rndskill3,rndskill4,rndrareskill,hp,hpnow   ,ehp,eat,edf,ename,at,df,ehpnow,attack,defense,damage,scene,act,exp,eexp,damagesave,pages,myskill,crit,skill_no ,items
   global clearflag
   pulloff()
   sending = {
      "itemid":29,
      "skill1":lvdef,
      "skill2":expdef,
      "skill3":days,  
      "skill4":0
      }
   if clearflag == 1:
    sending = {
      "itemid":48,
      "skill1":0,
      "skill2":0,
      "skill3":0,  
      "skill4":0
      }
   game_save["itemsave"].append(sending)
   with open("save.json", "w", encoding="utf-8") as f:
       json.dump(game_save, f, indent=4, ensure_ascii=False)
   if weapon != -1:
     itemsave(0)
   if armor != -1:
     itemsave(1)
   if accessory1 != -1:
     itemsave(2)
   global inventorytt,inv_data1tt,inv_data2tt,inv_data3tt,item
   inventorytt=[]
   inv_data1tt=[]
   inv_data2tt=[]
   inv_data3tt=[]
   if len(inventory) >0:
    print(inventory)
    print("こ↑こ↓")
    a=0
    sendinging=[]
    for a in range(len(inventory)):
      
      new_item = {
       "itemid": inventory[a],
       "skill1": inv_data1[a],
       "skill2": inv_data2[a],
       "skill3": inv_data3[a],  
       "skill4": inv_data4[a]
       }
      if inventory[a] != 30:
       sendinging.append(new_item)



    game_save["itemsave"].extend(sendinging)
    with open("save.json", "w", encoding="utf-8") as f:
       json.dump(game_save, f, indent=4, ensure_ascii=False)
   scene = 0
   damagesave= -1
   area=0
   scene = 0
   days = 1
   loadflag = 0  
   act=5
   hp = 50
   at = 5
   df = 3
   lv = 1
   atex = 0
   atex2=0
   atex3=0
   dfex = 0
   dfex2=0
   dfex3=0
   atdef = 5
   dfdef = 3
   hpex=0
   hpex2=0
   hpex3=0
   hpdef=50
   itemskill1=0
   itemskill2=0
   itemskill3=0
   itemskill4=0

   exp = 0
   
   ename = "null"
   ehp = 1
   eat = 1
   edf = 1
   eexp = 1
   edrop = 1
   edrop2 = 1
   elv = 1

   critmess = 0

   hpnow = 50

   ehpnow = 1

   attack = 0
   defense = 0
   damage=0

   weapon=-1
   weaponname="-"
   armor=-1
   armorname="-"
   accessory1=-1
   accessoryname="-"
   accessory2=-1
   equip=-1
   itemtype=-1


   item_data = game_data["items"]

   enemies = game_data["enemies"]
   enemy = 0
   enemy_data = ['absolute','betray','null','null']
   print(enemies)
   item = 0
   itemname = ""
   itemsname=""
   itemid = -1
   pages = 0

   crit=0

   iteming = 0
   items = ['absolute','betray','null','null']
   print(enemies)


   skill_no = 0

   inventory=[]
   inv_data1=[]
   inv_data2=[]
   inv_data3=[]
   inv_data4=[]

   myskill=[0,0,0,0]

   itsk1=0
   itsk2=0
   itsk3=0
   itsk4=0
   sknm1="-"
   sknm2="-"
   sknm3="-"
   sknm4="-"
   skdt1=[]
   skdt2=[]
   skdt3=[]
   skdt4=[]

   rndskill1=0
   rndskill2=0
   rndskill3=0
   rndskill4=0
   rndrareskill=0
   rndskillX=0
   weaprank = 0
   armrank = 0
   accrank = 0
   itemtypeinv=0

   scene=0
   if clearflag==1:
    title = tk.Label(root,text="GAME COMPLETE!!!!",font=("Arial",20))
    title.place(x=70,y=10)
    title = tk.Label(root,text="呪いの元凶を打ち破った。",font=("Arial",10))
    title.place(x=10,y=50)
    title = tk.Label(root,text="黒い雲で覆われていた塔の周りも",font=("Arial",10))
    title.place(x=10,y=70)
    title = tk.Label(root,text="今では虹がかかっている。",font=("Arial",10))
    title.place(x=10,y=90)
    title = tk.Label(root,text="穏やかな海になったことだろう。",font=("Arial",10))
    title.place(x=10,y=110)
    title = tk.Label(root,text="しかし、どうやってあの島や塔が",font=("Arial",10))
    title.place(x=10,y=130)
    title = tk.Label(root,text="生まれ、呪われたのかは今でも謎のままだ。",font=("Arial",10))
    title.place(x=10,y=150)
    title = tk.Label(root,text="Thank You For Playing!!!!!!",font=("Arial",15))
    title.place(x=80,y=170)
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)  
    clearflag=0
   else:
    main()
# pygame.mixer の初期化コードもここに配置されていると仮定します
def pageinc():
    global page
    page = page + 1
    print(page)
    main()
    
def pagedec():
    global page
    page = page - 1
    print(page)
    main()
    
def octinc():
    global octave
    octave = octave + 1
    print(octave)
    main()
    
def octdec():
    global octave
    octave = octave - 1
    print(octave)
    main()

def bpmchanging():
    global entry
    global BPM 
    # NOTE: entry.get() を呼び出す前に entry が存在することを確認してください
    if entry:
        BPM = entry.get()
        print(f"BPM changed to: {BPM}")
    main()

def backing():
    global scene
    scene = 5
    attacking()
# SCRIPT_DIR の定義をファイルの先頭に移動
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SOUNDFONT_FILE_NAME = 'soundfont.sf2' 



def play_midi_direct():
    fluidsynth_exe = os.path.join(SCRIPT_DIR, 'fluidsynth-2.4.6-win10-x64/bin/fluidsynth.exe').replace('\\','/')
    soundfont = os.path.join(SCRIPT_DIR, SOUNDFONT_FILE_NAME).replace('\\','/')
    midi_file = os.path.join(SCRIPT_DIR, 'output.mid').replace('\\','/')

    mid = mido.MidiFile(midi_file)

    # tempo を取得（最初の set_tempo があればそれを使う）
    tempo = 500000  # デフォルト 120BPM
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                break
        if tempo != 500000:
            break

    # MIDI全体の長さを秒で計算
    total_seconds = sum(mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
                        for track in mid.tracks
                        for msg in track)

    try:
        # FluidSynthを起動
        p = subprocess.Popen([fluidsynth_exe, '-ni', soundfont, midi_file], cwd=SCRIPT_DIR)
        time.sleep(total_seconds)  # MIDIの長さだけ待機
        p.terminate()              # 再生終了
        p.wait()
        print("▶️ 正確にMIDI再生完了（休符も考慮済み）")
    except Exception as e:
        print(f"❌ 再生中にエラー: {e}")
        
# MIDI保存後にスレッドで再生
def midsave():
    global mid,risting,BPM  # 既存のMIDIオブジェクト
    # ノート情報をMIDIに追加
    print(risting)
    mid.tracks=[]
    track1 = MidiTrack()#トラック作って
    mid.tracks.append(track1)#追加
    print(track1)
    microseconds_per_beat = int(60000000 / int(BPM))  # BPM → マイクロ秒/拍
    track1.insert(0, MetaMessage('set_tempo', tempo=microseconds_per_beat))
    
    for i in range(len(risting)):
     if risting[i] != -1:
         track1.append(Message('note_on', note=risting[i], velocity=64, time=0))
         track1.append(Message('note_off', note=risting[i], velocity=0, time=120))
     else:
         # 休符の時間を進める
         track1.append(Message('note_on', note=60, velocity=0, time=120))
    for i in range(4):
      track1.append(Message('note_on', note=60, velocity=0, time=120))   
    midi_file_name = 'output.mid'
    midi_abs_path = os.path.join(SCRIPT_DIR, midi_file_name)
    mid.save(midi_abs_path)
    print("✅ MIDIファイル output.mid を保存しました。")

    t = threading.Thread(target=play_midi_direct)
    t.daemon = True
    t.start()
def enRndm():#敵ランダム
  global days
  global enemy
  global enemy_data
  enemy = random.choice(en_tables[days])
  if days == 7:
    if accessory1 == 39:
      check = random.choice([0,1])
      print(check)
      print("；ヵｓｄｆｋｌｊはｓｄｆｋｌｊｈさｄｆｌｋｊｈさｄｆｋｊ")
      if check == 0:
        enemy = 12

  if area == 2 and days != 28:
    enemy=en_tables[days][len(en_tables[days])-act]
  print(enemy)

  enemy_data = game_data["enemies"][enemy]
  
def itemRndm():#探索アイテムランダム
  global days,iteming,items,item_data,itemsname,itemtypeinv
  iteming = random.choice(item_tables[days])
  print(iteming)
  items = game_data["items"][iteming]
  itemsname = items['name']
  itemtypeinv = items['type']
  

def itemsend(a):
   global scene
   global itemsendspot
   scene = 30
   itemsendspot = a
   main()

def itemseisei():
     global scene
     scene=777
     main()
def daw():
  global scene,page,octave,mid,track1,track2,track3,track4,BPM,risting
  risting=[]
  BPM = 120
  mid = MidiFile(ticks_per_beat=480,type=1)#midiをつくって
  page=0
  octave=3
  scene=222.22
  main()
def ited():
  global aur,aur2,aur3,aur4,aur5,scene,aaa,iyaabaf,iyaabaf2
  iyaabaf=0
  iyaabaf2=0
  aaa=0
  aur=0
  aur2=0
  aur3=0
  aur4=0
  aur5=0

  scene=300
  main()
def itemsave(a):
   global saves,scene,equip,weapon,armor,accessory1,accessory2,inventory,inv_data1,inv_data2,inv_data3,inv_data4,itemskill1,itemskill2,itemskill3,itemskill4,myskill,pages,itemtype,item_data,itemid,atex,atex2,atex3,dfex,dfex2,dfex3,at,df,hp,atdef,atdef,hpex,hpex2,hpex3,weaponname,armorname,accessoryname,rndskill1,rndskill2,rndskill3,rndskill4,rndrareskill,rndskillX,myskill,hpnow,weaprank,armrank,accrank
   scene = 13
   if a == 0:
     sending = {
     "itemid":weapon,
     "skill1":itemskill1,
     "skill2":itemskill2,
     "skill3":itemskill3,  
     "skill4":0
     }
     game_save["itemsave"].append(sending)
     with open("save.json", "w", encoding="utf-8") as f:
      json.dump(game_save, f, indent=4, ensure_ascii=False)
     weapon=-1
     weaponname = "-"
     atex=0
     dfex=0 
     hpex=0     
     weaprank=0
     itemskill1 = 0
     itemskill2 = 0
     itemskill3 = 0
     hp=hpdef+hpex+hpex2+hpex3
     if hpnow > hp:
       hpnow=hp 
   elif a == 1:
     sending = {
     "itemid":armor,
     "skill1":0,
     "skill2":0,
     "skill3":0,  
     "skill4":0
     }
     game_save["itemsave"].append(sending)
     with open("save.json", "w", encoding="utf-8") as f:
      json.dump(game_save, f, indent=4, ensure_ascii=False)
     armor=-1
     armorname = "-"
     atex2=0
     dfex2=0 
     hpex2=0     
     armrank=0
     hp=hpdef+hpex+hpex2+hpex3
     if hpnow > hp:
       hpnow=hp 
   elif a == 2:
     sending = {
     "itemid":accessory1,
     "skill1":0,
     "skill2":0,
     "skill3":0,  
     "skill4":itemskill4
     }
     game_save["itemsave"].append(sending)
     with open("save.json", "w", encoding="utf-8") as f:
      json.dump(game_save, f, indent=4, ensure_ascii=False)
     accessory1=-1
     accessoryname = "-"
     itemskill4 = 0
     atex3=0
     dfex3=0 
     hpex3=0     
     accrank=0
     hp=hpdef+hpex+hpex2+hpex3
     if hpnow > hp:
       hpnow=hp 
     
   myskill=[itemskill1,itemskill2,itemskill3,itemskill4,]
   scene = 32
   main()

def enskactivation(ensk):
   global ename,weapon,enemy_data,stat,skillmess,skillcom,edf,hp,weapon,ehpnow,hpnow
   skillcompre = game_data["en_skills"][ensk]
   skillcom = skillcompre["name"]
   skillcom2 = skillcompre["comment"]
   skillmess = f"{ename}の{skillcom}！{skillcom2}"
   if weapon == 28 and ensk == 4:
        skillmess = f"{ename}の{skillcom}！虹の力を吸収された......"
   if ensk == 1:#猛毒液の処理
     stat = 1
   if ensk == 2:#スーパーアーマーの処理
     edf=edf+50
   if ensk == 3:#骸骨の呪いの処理
     stat = 2
   if ensk == 4:#ナイトメアドレインの処理
     a = round((hp*hp)*0.004)
     if weapon == 28:
       a=a*3
     print(a,(hp),(hp*hp))
     ehpnow+=a
     if hpnow < 11:
       hpnow-=1
     else:
       hpnow-=round((hpnow*0.1))
   
   
   
   if 28 in myskill and stat != 0:#スーパーレアスキル 龍の護りの処理 
        stat=0     
        skillmess=f"龍の護りで状態異常を無効化した！"
   if 30 in myskill and armor == 31 and accessory1 == 32 and stat != 0:#スーパーレアスキル 龍の護りの処理 
        stat=0     
        skillmess=f"狐火が災いを祓った。"
         
 

def calculate_damage(attack, defense,doch):
    global crit
    global critmess
    if attack < 2:
     attack = 2
    if defense < 2:
     defense = 2
    # 計算式に基づくダメージを計算
    hosei = random.uniform(0.6, 1.4)

    
    if 21 in myskill:#スキル 疾風怒濤の処理
     hosei = random.uniform(0.1, 2.2)
    print(hosei)
    #damage = ((attack*attack) / (defense+attack)) * (math.log(defense, attack))* hosei
    #↑ダメージ計算式バージョン1
    #damage = ((attack*1.5) / (defense*1.2)) * hosei
    #↑ダメージ計算式バージョン2

    damage=((((attack/3)/(defense/2))*(defense**(0.7)))*1.2)*hosei
    #↑ダメージ計算式バージョン3
    print(hosei)
    print("補正だよ～ん")
    if 22 in myskill:#スキル 諸刃の剣の処理
     damage=damage*1.2
    
    #クリティカルの処理は個別に移動した
    if crit == 1:
       critmess = 1
       damage=damage*3
       print("クリティカルヒット")
       return damage
    elif crit!=1:
       print(critmess)
       print("あああ")
       if critmess == 0:
        print("ううううううう")
        critmess = 0
       return damage
def mochikomi(a,mochiban):
  update_scene()
  global scene
  global game_data
  global money,nokakunin
  scene=13
  
  mochibanban = inventory[mochiban]
  ii=game_data["items"][mochibanban]
  ii2=ii['name']
  itemranki=ii['rank']
#  あｓｄふぁｓｄｆ=012012fasdljhkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkj
  title = tk.Label(root,text=f"{ii2}を持ち込みますか？",font=("Arial",15))
  title.place(x=40,y=10)
  title = tk.Label(root,text=f"持ち込みコスト:{cost[itemranki]}",font=("Arial",15))
  title.place(x=40,y=50)

  button=tk.Button(root,text="いいえ",font=("Arial",20),command=main)
  button.place(x=280,y=230)
  if money >= cost[itemranki]:
   button=tk.Button(root,text="はい",font=("Arial",20),command=lambda b=0:mochikomisave(mochiban,cost[itemranki]))
   button.place(x=30,y=230)
   print(nokakunin.get())
   if nokakunin.get() == 1:
    print("勝手にやっちゃうZE")
    mochikomisave(mochiban,cost[itemranki])
  else:
   title = tk.Label(root,text=f"資金が{(cost[itemranki])-money}足りない",font=("Arial",15))
   title.place(x=30,y=230)
def mochikomisave(mochiban,monemone):
      print (mochiban)

      global scene,game_save,inventory,inv_data1,inv_data2,inv_data3,inv_data4,invmochi,mochi1,mochi2,mochi3,mochi4
      print(inventory)

      
      moneyindec(0,monemone)

      i=inventory[mochiban]
      i1= inv_data1[mochiban]
      i2= inv_data2[mochiban]
      i3= inv_data3[mochiban]
      i4= inv_data4[mochiban]
      invmochi.append(i)
      mochi1.append(i1)
      mochi2.append(i2)
      mochi3.append(i3)
      mochi4.append(i4)
      del inventory[mochiban]
      del inv_data1[mochiban]
      del inv_data2[mochiban]
      del inv_data3[mochiban]
      del inv_data4[mochiban]
      game_save["itemsave"].pop(mochiban)
      with open("save.json", "w", encoding="utf-8") as f:
       json.dump(game_save, f, indent=4, ensure_ascii=False)
      scene=13
      main()

def moneyindec(inc,dec):#お金増減(増える量を左に、減る量を右に)
  global money
  global game_save
  money = money+inc-dec
  game_save["resource"][0]["money"]=money
  with open("save.json", "w", encoding="utf-8") as f:
    json.dump(game_save, f, indent=4, ensure_ascii=False)

def Shosai(a):
   update_scene()
   global rainbowing

   rainbowing=0
   def rainbow():
     global rainbowing
     if not rbutton.winfo_exists():
      return
     rainbowing=rainbowing+1
     if rainbowing > 6:
      rainbowing=0
     rainbow_colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'magenta']
     current_color = rainbow_colors[rainbowing]
     rbutton.config(bg=current_color, activebackground=current_color)
     root.after(77, rainbow)


   global inventory,inv_data1,inv_data2,inv_data3,inv_data4,item_data,scene
   itemid = inventory[a]
   item_data = game_data["items"][itemid] 
   itemtype = item_data['type']
   if itemtype == 0:
    typename="武器"
   elif itemtype == 1:
    typename="防具"
   elif itemtype == 2:
    typename="アクセサリー"
   else :
    typename="その他" 
  
   itemname = item_data['name']

   itemat = item_data['attack']
   itemdf = item_data['defense']
   itemhp = item_data['hp']

   itemcomment = item_data['comment']
   itsk1 = inv_data1[a]
   itsk2 = inv_data2[a]
   itsk3 = inv_data3[a]
   itsk4 = inv_data4[a]

   if itemid != 29:
    skdt1=game_data["skills"][itsk1]
    skdt2=game_data["skills"][itsk2]
    skdt3=game_data["skills"][itsk3]
    skdt4=game_data["skills"][itsk4]
   
    sknm1=skdt1['fullname']
    sknm2=skdt2['fullname']
    sknm3=skdt3['fullname']
    sknm4=skdt4['fullname']   
 
    skcm1=skdt1['comment']
    skcm2=skdt2['comment'] 
    skcm3=skdt3['comment']
    skcm4=skdt4['comment']     
   itrank=item_data['rank']     

   if itsk3 == 0:
     title = tk.Label(root,text=f"名前:{itemname}[{typename}]",font=("Arial",9))
     title.place(x=10,y=5)
   if itsk3 != 0:
     if itemid != 29:
      title = tk.Label(root,text=f"名前:{itemname}☆[{typename}]",font=("Arial",9))
      title.place(x=10,y=5)
     else:
      title = tk.Label(root,text=f"名前:{itemname}[{typename}]",font=("Arial",9))
      title.place(x=10,y=5)       
   
   title = tk.Label(root,text=f"・{itemcomment}",font=("Arial",8))
   title.place(x=20,y=25)     
   if typename != "その他":
    title = tk.Label(root,text=f"AT + ( {itemat} ), DF + ( {itemdf} ), HP + ( {itemhp} )",font=("Arial",10))
    title.place(x=20,y=55)     
   if itemid != 29:
    if itsk1 != 0:
     title = tk.Label(root,text=f"スキル1:{sknm1}",font=("Arial",10))
     title.place(x=2,y=95)   
     title = tk.Label(root,text=f"効果:{skcm1}",font=("Arial",9))
     title.place(x=2,y=115)   
    if itsk2 != 0:
     title = tk.Label(root,text=f"スキル2:{sknm2}",font=("Arial",10))
     title.place(x=2,y=135)  
     title = tk.Label(root,text=f"効果:{skcm2}",font=("Arial",9))
     title.place(x=2,y=155)    
    if itsk3 != 0:
     title = tk.Label(root,text=f"スキル☆:{sknm3}",font=("Arial",10))
     title.place(x=0,y=175)   
     title = tk.Label(root,text=f"効果:{skcm3}",font=("Arial",9))
     title.place(x=2,y=195) 
    if itsk4 != 0:
     title = tk.Label(root,text=f"スキル:{sknm4}",font=("Arial",10))
     title.place(x=2,y=75)   
     title = tk.Label(root,text=f"効果:{skcm4}",font=("Arial",9))
     title.place(x=2,y=100) 
    if itemid == 28 and money >= 7777:
     rbutton=tk.Button(root,text="アイテム生成(コスト:7777)",font=("Arial",8),command=itemseisei)
     rbutton.place(x=150,y=270) 
     rainbow()
   else:
     if itsk3 != 0:
      title = tk.Label(root,text=f"到達:{itsk3-16}階層",font=("Arial",15))
      title.place(x=2,y=95)  
     
   bbbb  = sellingprice[itrank]
   scene = 13
   if loadflag == 1:
    button=tk.Button(root,text=f"売却:{sellingprice[itrank]}",font=("Arial",10),command=lambda a=a:sell(bbbb,a))
    button.place(x=150,y=230)   

   button=tk.Button(root,text="OK",font=("Arial",20),command=main)
   button.place(x=30,y=230)


def itemkobetsu():
   a=0#没になったよ。詳細右 絶対消していいけど、なんかあったらやだから一応残しておく アイテム名に対応した処理を行う。例えば、剣なら剣の枠に装備。未実装なのでとりあえずa=0を置いてるffffffffffffffff

def sell(ab,uwaa):
 global inv_data1,inv_data2,inv_data3,inv_data4,inventory,pages
 moneyindec(ab,0)
 print (f"{(pages+1)*uwaa}aaasdaffdsaadfsadffads")
 print(f"{inventory}うおゆいｒちゆｒてうぃゆおｔｒうぇいうよｗｒていうよえｔｗるいぇｔｒうｙｒとぅｙｒｔｗｙｔｒｙｗｙｒｔｗｙｒつｙつｙｒｔｙｒｔｒｔｔｙｒｔｙｔｙS")
 del inventory[uwaa]
 del inv_data1[uwaa]
 del inv_data2[uwaa]
 del inv_data3[uwaa]
 del inv_data4[uwaa]
 game_save["itemsave"].pop(uwaa)
 print(game_save)
 with open("save.json", "w", encoding="utf-8") as f:
  json.dump(game_save, f, indent=4, ensure_ascii=False)
 main()

def update_scene():
    #画面の初期化
    for widget in root.winfo_children():
        widget.destroy()

def encount():#エンカウント
  global ehp,ehpnow,eat,edf,eexp,ename,elv,enemyskill,enemyskillpar
  enRndm()
  ehp=enemy_data['hp']
  ehpnow=ehp
  eat=enemy_data['attack']
  edf=enemy_data['defense']
  eexp=enemy_data['exp']
  ename=enemy_data['name']
  elv = 1
  enemyskill=enemy_data['skill']
  if enemyskill != 0:
    enemyskillpar = enemy_data['skillpar']
def start():#ゲーム開始処理
    global scene
    scene=1
    
    main()

def dataload():#ロード処理
    global scene,inventory,inv_data1,inv_data2,inv_data3,inv_data4



    inventory =[]
    inv_data1=[]
    inv_data2=[]
    inv_data3=[]
    inv_data4=[]    
    scene=40
    main()

def exit():#ゲーム終了処理
    root.quit()

def letsgo():#本編開始
    global scene,act,days,mochi1,mochi2,mochi3,mochi4,invmochi,inventory,inv_data1,inv_data2,inv_data3,inv_data4,hpnow
    global pages
    pages=0
    inventory =[]
    inv_data1=[]
    inv_data2=[]
    inv_data3=[]
    inv_data4=[]    
    if invmochi:
     for a in range(len(invmochi)):
      inventory.append(invmochi[a])
      inv_data1.append(mochi1[a])
      inv_data2.append(mochi2[a])
      inv_data3.append(mochi3[a])
      inv_data4.append(mochi4[a])
    invmochi=[]
    mochi1=[]
    mochi2=[]
    mochi3=[]
    mochi4=[]

    days = 1
    act = 5
    scene=3
    hpnow = 50
    main()

def yada():#断った場合
     global scene
     scene=4
     main()

def yadaex():#タイトルに戻る
     global scene
     scene=0
     main()

def back():#インベントリ画面などから遷移
     global scene
     scene=3
     main()
def back2():#持ち込み画面から遷移
     global scene
     global pages
     pages=0
     scene=0
     main()

def hunt():#狩り
     global act
     if area == 0:
      act = act-1
     global scene
     global days
     if days == 16:
      scene=24
      main()
     elif days == 28:
      scene=999
      main()    
     else:
      encount()
      scene=5
      main()

def search():#探索
     global act
     global days
     global scene
     if days == 15:
      scene=21
      main()
     elif days == 16:
      scene=24
      main()   
     elif area == 1:
      scene=23
      main()   
     elif area == 2:
      scene=23.5
      main()   
     else:
      act = act-1
 
      scene=6
      main()

def rest():#休憩
     global act,hp,hpnow,stat,lv,lvdef,exp,expdef,atdef,dfdef,hpdef
     if area != 2:
      if hpnow < hp:
       if days != 16:
        act = act-1
   
     global scene
     scene=3      
     if area != 2:
      hpnow = hp
      stat = 0
     elif area == 2:
       if act==len(en_tables[days]):
        print(f'{lvdef}おｓふぁｄｈｊｋｌｇｓｄふぁｊｋｈｌｆだｓｋｈｊｌｄｆさｈｊｋｓｄｆｌｈｊかｆｓｄ')
        hpnow = hp
        stat = 0
        lv=lvdef
        exp=expdef
       else:
        scene=44.4
                 
 
     main()

def inv():#インベントリ閲覧
    global scene
    global loadflag
    scene=13
    loadflag = 0
    main()

def attacking():#こっちの攻撃
     global hp,hpnow   ,ehp,eat,edf,ename,at,df,ehpnow,attack,defense,damage,scene,act,exp,eexp,damagesave,pages,myskill,crit,skill_no,armor,weapon,accessory1,stat
     global critmess
     critmess=0
     attack = at
     defense=edf

     if 8 in myskill:#レアスキル ピンチブーストの処理
        if hpnow < hp*0.2:
           attack=attack*1.5
    
     crit = random.uniform(0,24)
     crit = round(crit)
     if 5 in myskill:#スキル CRT率アップの処理
            crit = random.uniform(0,12)
            crit = round(crit)
     if 18 in myskill:#スーパーレアスキル 確定クリティカルの処理
            crit = 1
            critmess=1
            print("確定")
     print(f'{crit}')  
     damage = calculate_damage(attack,defense,0)#ダメ計

     if 3 in myskill:#スキル ダメージアップ+1の処理
        damage=damage+1
     if 4 in myskill:#レアスキル ライフドレインの処理
        hpnow = hpnow+(damage*0.05)
        hpnow=round(hpnow)
        if hpnow > hp:
              hpnow=hp
     if 11 in myskill:#スーパーレアスキル ライフドレイン+の処理
        print("rareskill")
        damage=damage*0.9
        damage=round(damage)
        hpnow = hpnow+(damage*0.15)
        hpnow=round(hpnow)
        if hpnow > hp:
              hpnow=hp
     if 6 in myskill:#スキル ダメージアップ+10%の処理
        damage=damage*1.1
     if 39 in myskill:#スーパーレアスキル Quartz GodRayの処理
        if ehp >= 600:
         damage=damage*2

     if 12 in myskill:#レアスキル ダメージアップ+25%の処理
        damage=damage*1.25
     if 40 in myskill:#スーパーレアスキル Infinity Forceの処理
        damage=88888888888888888888888888888888888
     if 15 in myskill:#スキル 血気盛んの処理
        damage=damage*1.05

     if skill_no == 10:#スキル 強攻撃の処理
        print(f'もともと{damage}')
        damage=damage*3
        skill_no =0
        print(f'強いぜ{damage}')     
     if skill_no == 20:#スキル 力任せの一撃の処理
        print(f'もともと{damage}')
        f = random.uniform(1,10)
        if f < 4:
         damage=0
        else:
         damage=damage*2
        skill_no =0
        print(f'強いぜ{damage}') 
     if skill_no == 30:#スキル スカルフレイムの処理
        print(f'もともと{damage}')
        print(enemy_data)
        if enemy_data['type'] == "undead":
         damage=damage*3
         print("こいつはアンデッドだぜ")
        skill_no =0
        print(f'強いぜ{damage}') 
     if skill_no == 38:#スーパーレアスキル ドラゴンウェーブの処理
         damage=damage*1.5
         skill_no =0
       
     if 23 in myskill:#スキル ファイナルブローの処理
      if ehpnow <= ehp*0.2:
       damage=damage*1.2
     if 25 in myskill:#スーパーレアスキル 逆鱗の処理
      if hpnow <= hp*0.2:
       damage=damage*2
     if 26 in myskill:#スーパーレアスキル Rainbow Rushの処理
       if 37 in myskill:#スーパーレアスキル 虹の夢の処理
        damage=damage*2.77
       else:
        damage=damage*1.77
     if 29 in myskill:#レアスキル 裁きの炎の処理
        damage=damage*1.1
        hpnow = hpnow+round(damage*0.1)
        if hpnow > hp:
          hpnow=hp


               
     damage = round(damage)#一番最後に切り上げ処理
     if damage < 1:
        damage=1
     ehpnow = ehpnow-damage

     if ehpnow < 1:
          exp=exp+eexp

          if 17 in myskill:#スキル 治癒の祈りの処理
           hpnow = hpnow+(hp*0.05)
           hpnow=round(hpnow)
           if hpnow > hp:
              hpnow=hp
          if 29 in myskill:#レアスキル 裁きの炎の処理
           stat=0

          scene = 10
          main()
     elif ehpnow > 0:
      damagesave = damage
      main()
      damaging()
 

def damaging():#敵の攻撃
     global skillmess,enemyskill,enemyskillpar,hp,hpnow   ,ehp,eat,edf,ename,at,df,ehpnow,attack,defense,damage,scene,act,myskill,crit,stat,statmess
     attack = eat
     defense=df

     if 8 in myskill:#レアスキル ピンチブーストの処理
        if hpnow < hp*0.2:
           defense=defense*1.5
    
     crit = random.uniform(0,24)#クリティカル
     crit = round(crit)
     if 19 in myskill:#レアスキル クリティカルガードの処理
        crit = 222.22

     damage = calculate_damage(attack,defense,1)

     if 2 in myskill:#スキル ダメージカット-1の処理
        damage=damage-1
     if 7 in myskill:#スキル ダメージカット-5%の処理
        damage=damage*0.95
     if 36 in myskill:#スキル ウェポンガードの処理
        damage=damage*0.95
     if 13 in myskill:#レアスキル ダメージカット-35%の処理
        damage=damage*0.65
     if 28 in myskill:#スーパーレアスキル 龍の護りの処理
        damage=damage*0.97

                        

     damage = round(damage)#一番最後に切り上げ処理
     if damage < 1:
        damage=1

     if 1 in myskill:#スーパーレアスキル ラピッドストライクの処理(特殊なので切り上げ処理の後に発動)
        a=random.uniform(1,10)
        a=math.floor(a)

        if a == 1:
         damage=0
     skillmess=""
     statmess=""
     if stat == 1:#状態異常 猛毒の処理 
       hpnow=hpnow-15
       statmess="猛毒で15ダメージ受けた！"
     if stat == 2:#状態異常 呪いの処理 
       hpnow=hpnow-(hpnow*0.2)
       hpnow=round(hpnow)
       statmess=f"呪いで体力の20%が削られた..."

     if enemyskill != 0:
       ensk=random.uniform(1,100)
       if ensk <= enemyskillpar:
         enskactivation(enemyskill)
       else:  
        hpnow = hpnow-damage
     else:
        hpnow = hpnow-damage 
     if hpnow < 1:
           print(myskill)
           if 9 in myskill:#レアスキル 緊急退避の処理

            hpnow = 1
            scene=12

           else:
            if area != 2:
             act = 1
            scene = 11
     
     main()

def escape():#逃走
     global scene

     a = random.uniform(0,4)
     a = round(a)
     if a==4:
      damaging()
     elif a!=4:
      scene = 12

     main()
     if a==4:
      title = tk.Label(root,text="逃げられなかった！",font=("Arial",15))
      title.place(x=100,y=100)
      title = tk.Label(root,text=f"{ename}から{damage}ダメージ受けた",font=("Arial",10))
      title.place(x=100,y=130)
      if skillmess != "":
       title = tk.Label(root,text=f"{skillmess}                          ",font=("Arial",10))
       title.place(x=20,y=130)

def skilling():
   global myskill
   global scene
   scene=20
   main()

def nextpage():#アイテム欄nextページへ
   global pages
   pages=pages+1
   main()

def prevpage():#アイテム欄previousページへ
   global pages
   pages=pages-1
   main()

def trush(a):#アイテム破棄(2025 2/04時点では没)

   global inventory
   global pages
   global inv_data1
   global inv_data2
   global inv_data3
   global inv_data4

   
   
   del inventory[(pages+1)*a]
   del inv_data1[(pages+1)*a]
   del inv_data2[(pages+1)*a]
   del inv_data3[(pages+1)*a]
   del inv_data4[(pages+1)*a]

   main()
def pulloff():
   global weaprank,armrank,accrank,loadflag,equip,weapon,armor,accessory1,accessory2,inventory,inv_data1,inv_data2,inv_data3,inv_data4,itemskill1,itemskill2,itemskill3,itemskill4,myskill,pages,itemtype,item_data,itemid,atex,atex2,atex3,dfex,dfex2,dfex3,at,df,hp,atdef,atdef,hpex,hpex2,hpex3,weaponname,armorname,accessoryname,rndskill1,rndskill2,rndskill3,rndskill4,rndrareskill,rndskillX,myskill,hpnow,skillmess
   if weapon != -1:  #もし装備していれば
       equip=weapon
       inventory.append(equip)
       inv_data1.append(itemskill1)
       inv_data2.append(itemskill2)
       inv_data3.append(itemskill3)
       inv_data4.append(0)
   if armor != -1:  
       equip=armor
       inventory.append(equip)
       inv_data1.append(0)
       inv_data2.append(0)
       inv_data3.append(0)
       inv_data4.append(0)
   if accessory1 != -1:  
       equip=accessory1
       inventory.append(equip)
       inv_data1.append(0)
       inv_data2.append(0)
       inv_data3.append(0)
       inv_data4.append(itemskill4)
   weapon=-1
   weaponname = "-"
   armor = -1
   armorname = "-"
   accessory1 = -1
   accessoryname = "-"
   atex=0
   atex2=0
   atex3=0
   dfex=0
   dfex2=0
   dfex3=0
   hpex=0
   hpex2=0
   hpex3=0
   hp=hpdef
   at=atdef
   df=dfdef
   weaprank=0
   accrank=0
   armrank=0
   itemskill1 = 0
   itemskill2 = 0
   itemskill3 = 0
   itemskill4 = 0
   myskill=[0,0,0,0]
   hp=hpdef+hpex+hpex2+hpex3
   if hpnow > hp:
      hpnow = hp
   global scene
   if scene== 3:
    main()
def towerkey(a):
  global scene
  global area
  global keynoiti
  area=1
  scene=3
  print(a)
  keynoiti=a
  main()

def entower():
  global area,scene,days,act,game_save,lv,at,df,hp,exp,hpnow,hpdef,atdef,dfdef,pages,keynoiti,inventory,inv_data1,inv_data2,inv_data3,inv_data4,lvdef,expdef,atdefdef,dfdefdef,hpdefdef,en_tables
  lvlv=inv_data1[keynoiti]
  exexp=inv_data2[keynoiti]
  daydays=inv_data3[keynoiti]

  print(f"{inventory}sadf;lkjsadf;lkjsadflkjsafd;lkjsdfっぽぽぽぽぽぽぽ")
  del inventory[keynoiti]
  del inv_data1[keynoiti]
  del inv_data2[keynoiti]
  del inv_data3[keynoiti]
  del inv_data4[keynoiti]
  game_save["itemsave"].pop(keynoiti)
  with open("save.json", "w", encoding="utf-8") as f:
   json.dump(game_save, f, indent=4, ensure_ascii=False)
  letsgo()
  lv=1
  at=5
  atdef=5
  df=3
  dfdef=3
  hp=50
  hpdef=50
  hpnow=50
  exp=0
  days = 17
  act=3
  area = 2
  scene=3
  pages=0
  if daydays != 0:
   if daydays != 17:
    lv=lvlv
    lvdef=lvlv
    exp=exexp
    expdef=exexp
    days=daydays
    hpdef=50+(lv*5)-5
    hpnow=hpdef
    atdef=5+(lv)-1
    dfdef=3+lv-1
    atdefdef=atdef
    dfdefdef=dfdef
    hpdefdef=hpdef
    act=len(en_tables[days])
 # sending={
 # "itemid":29,
 #"skill1":0,
 #"skill2":0,
 #"skill3":0,  
 #"skill4":0
 #}
  inv_data1.append(0)
  inv_data2.append(0)
  inv_data3.append(0)
  inv_data4.append(0)
  inventory.append(30)
 # game_save["itemsave"].append(sending)
 # with open("save.json", "w", encoding="utf-8") as f:
 #  json.dump(game_save, f, indent=4, ensure_ascii=False)
 # pulloff()
  main()
def pregameend():
  global scene
  scene=100
  main()
def towerback():
  global scene
  scene=100.5
  main()
def equipment(a):
   global weaprank,armrank,accrank,equip,weapon,armor,accessory1,accessory2,inventory,inv_data1,inv_data2,inv_data3,inv_data4,itemskill1,itemskill2,itemskill3,itemskill4,myskill,pages,itemtype,item_data,itemid,atex,atex2,atex3,dfex,dfex2,dfex3,at,df,atdef,atdef,hpex,hpex2,hpex3,weaponname,armorname,accessoryname,rndskill1,rndskill2,rndskill3,rndskill4,rndrareskill,rndskillX,hpnow,hp

   itemid = inventory[a]
   item_data = game_data["items"][itemid] 
   itemtype = item_data['type']
   itemname = item_data['name']
   itemrank = item_data['rank']

   print(itemid)
   print(itemtype)

   if itemtype==0:
      if weapon != -1:  #もし装備していれば
       equip=weapon
       inventory.append(equip)
       inv_data1.append(itemskill1)
       inv_data2.append(itemskill2)
       inv_data3.append(itemskill3)
       inv_data4.append(0)
      weapon=inventory[a]
      itemskill1=inv_data1[a]
      print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
      print(inv_data1)
      itemskill2=inv_data2[a] 
      itemskill3=inv_data3[a]
      #itemskill4=inv_data4[a]                 
      weaponname=itemname
      weaprank=itemrank
      print(itemrank)
      del inventory[a]
      del inv_data1[a]
      del inv_data2[a]
      del inv_data3[a]
      del inv_data4[a]
      atex = item_data['attack']
      dfex = item_data['defense']
      hpex = item_data['hp']
      

   elif itemtype==1:
      if armor != -1:  
       equip=armor
       inventory.append(equip)
       inv_data1.append(0)
       inv_data2.append(0)
       inv_data3.append(0)
       inv_data4.append(0)
      armor=inventory[a]
      armorname=itemname
      armrank=itemrank

      #itemskill1=inv_data1[a]
      #itemskill2=inv_data2[a] 
      #itemskill3=inv_data3[a]
      #itemskill4=inv_data4[a]   
      del inventory[a]
      del inv_data1[a]
      del inv_data2[a]
      del inv_data3[a]
      del inv_data4[a]
      atex2 = item_data['attack']
      dfex2 = item_data['defense']
      hpex2 = item_data['hp'] 

   elif itemtype==2:

      if accessory1 != -1:  
       equip=accessory1
       inventory.append(equip)
       inv_data1.append(0)
       inv_data2.append(0)
       inv_data3.append(0)
       inv_data4.append(itemskill4)
      accessory1=inventory[a]
      accessoryname=itemname
      accrank=itemrank
      #itemskill1=inv_data1[a]
      #itemskill2=inv_data2[a] 
      #itemskill3=inv_data3[a]
      itemskill4=inv_data4[a]   
      del inventory[a]
      del inv_data1[a]
      del inv_data2[a]
      del inv_data3[a]
      del inv_data4[a]

      atex3 = item_data['attack']
      dfex3 = item_data['defense']
      hpex3 = item_data['hp']

   print(f'アクセサリー{accessory1}')
   print(f'武器{weapon}')
   print(F'防具{armor}')
   
   myskill.clear()
   myskill.append(itemskill1)
   myskill.append(itemskill2)
   myskill.append(itemskill3)
   myskill.append(itemskill4)
   print(myskill)
   print("うまくいってくれた飲む")
   hp=hpdef+hpex+hpex2+hpex3
   if hpnow > hp:
      hpnow = hp
   main()
   
def skillactivation(button_id):
   
   global ehpnow,damagesave,skill_no,hpnow,scene,act,itemskill1,itemskill2,itemskill3,itemskill4
   skill_no=0
   
   if button_id == 1:
      skill_no=itemskill1
   elif button_id == 2:
      skill_no=itemskill2
   elif button_id == 3:
      skill_no=itemskill3
   elif button_id == 4:
      skill_no=itemskill4

   if skill_no == 14:#レアスキル タイタンスレイヤーの処理

      a=ehpnow
      ehpnow = ehpnow-(ehpnow*0.08)
      ehpnow=round(ehpnow)
      damagesave = a-ehpnow
      if ehpnow < 1:
        attacking()
      else:
       damaging()
   elif skill_no == 27:#デバッグ用スキルの処理
      global days
      days=16
      global exp
      exp=7777+1111

         
      damaging()
   elif skill_no == 10:#スキル 強攻撃の処理
      if hpnow > (hp*0.1):
       hpnow=hpnow-(hp*0.1)
       print("hpnow")
       hpnow=round(hpnow)
       attacking()
      else:
       main()
   elif skill_no == 20:#スキル 力任せの一撃の処理
       attacking()
   elif skill_no == 30:#スーパーレアスキル スカルフレイムの処理
       attacking()
   elif skill_no == 24:#スキル 戦略的撤退の処理
       scene=12
       act=act+1
       main()
   elif skill_no == 38:#スーパーレアスキル DrAgon Waveの処理
       daw()
       main()
print(clearflag)
def main():
  global clearflag,atdefdef,dfdefdef,hpdefdef,lvdef,expdef,area,resoursedata,money,weaprank,armrank,accrank,mochikomiyoubanme,loadflag,iteming,itemsname,weapon,armor,accessory1,scene,exp,lv,hp,df,at,hpdef,hpex,hpex2,hpex3,hpnow,damagesave,critmess,accessoryname,weaponname,armorname,atex,atex2,atex3,dfex,dfex2,dfex3  ,atdef,dfdef,item_data,item,itemname,itemid,inventory,inv_data1,inv_data2,inv_data3,inv_data4,itsk1,itsk2,itsk3,itsk4,stat,itemskill1,itemskill2,itemskill3,itemskill4,sknm1,sknm2,sknm3,sknm4,skdt1,skdt2,skdt3,skdt4,itemtypeinv,rndskill1,rndskill2,rndskill3,rndskill4,rndrareskill,invmochi,hpnow
  global nokakunin
  if scene==0:#タイトル画面
    update_scene()
    title = tk.Label(root,text="F O D A S",font=("Arial",40))
    title.place(x=75,y=50)
    title = tk.Label(root,text="~14日サバイバル~",font=("Arial",15))
    title.place(x=100,y=120)
    button=tk.Button(root,text="島に入る",font=("Arial",20),command=start)
    button.place(x=30,y=200)
    button=tk.Button(root,text="物資",font=("Arial",20),command=dataload)
    button.place(x=180,y=200)
    #button=tk.Button(root,text="アイテムエディタ",font=("Arial",20),command=ited)
    #button.place(x=100,y=10)
    if invmochi:
     title = tk.Label(root,text="注意!今ゲームを終了すると、転送中のアイテムが消えます。",font=("Arial",8))
     title.place(x=10,y=10)
    else:
     button=tk.Button(root,text="閉じる",font=("Arial",20),command=exit)
     button.place(x=280,y=200)
  elif scene==1:#ゲーム説明
    update_scene()
    title = tk.Label(root,text="ゲームの説明",font=("Arial",20))
    title.place(x=70,y=10)
    title = tk.Label(root,text="主人公は島に14日間滞在。1日5回行動ができるぞ!",font=("Arial",10))
    title.place(x=10,y=50)
    title = tk.Label(root,text="15日目に現れる島のボスを討伐して帰ろう!",font=("Arial",10))
    title.place(x=10,y=70)
    title = tk.Label(root,text="狩りでモンスターと戦ってレベルを上げ、",font=("Arial",10))
    title.place(x=10,y=90)
    title = tk.Label(root,text="探索でランダムなアイテムを集めて、",font=("Arial",10))
    title.place(x=10,y=110)
    title = tk.Label(root,text="時には休憩して体力回復もしよう!",font=("Arial",10))
    title.place(x=10,y=130)
    title = tk.Label(root,text="アイテムはいくつか持ち帰れるぞ! 繰り返し訪れるもよし。",font=("Arial",10))
    title.place(x=10,y=150)
    title = tk.Label(root,text="さぁ、行こう！！！",font=("Arial",15))
    title.place(x=80,y=170)
    button=tk.Button(root,text="行くぞ！",font=("Arial",20),command=letsgo)
    button.place(x=30,y=200)
    button=tk.Button(root,text="やだ！",font=("Arial",10),command=yada)
    button.place(x=250,y=200)

  elif scene==4:#やだ
    update_scene()
    title = tk.Label(root,text="ならば死ね！！！！",font=("Arial",20))
    title.place(x=70,y=10)  
    title = tk.Label(root,text="あなたは群馬県に放り出されて",font=("Arial",10))
    title.place(x=10,y=90)
    title = tk.Label(root,text="原住民族グンマーの夕飯になった！",font=("Arial",10))
    title.place(x=10,y=110)
    title = tk.Label(root,text="~GAMEOVER~",font=("Arial",20))
    title.place(x=100,y=150)
    button=tk.Button(root,text="タイトルに戻る",font=("Arial",10),command=yadaex)
    button.place(x=120,y=200)
  elif scene==3:#本編
    update_scene() 
    global act
    global days
    global myskill,lvdef,expdef
    if hpnow > hp:
     hpnow = hp
    if act == 0:
      days = days+1
      lvdef=lv
      expdef=exp
      if days == 15 or days == 16:
       act = -1
      else:
       if area != 2:
        act = 5
       else:
        act=len(en_tables[days])
 

    at=atdef+atex+atex2+atex3
    df=dfdef+dfex+dfex2+dfex3
    hp=hpdef+hpex+hpex2+hpex3
    skdt1=game_data["skills"][myskill[0]]
    skdt2=game_data["skills"][myskill[1]]
    skdt3=game_data["skills"][myskill[2]]
    skdt4=game_data["skills"][myskill[3]]
    
    sknm1 = skdt1["fullname"]
    sknm2 = skdt2["fullname"]
    sknm3 = skdt3["fullname"]
    sknm4 = skdt4["fullname"]   
    if area == 0:
     title = tk.Label(root,text=f"{days}日目",font=("Arial",30))
     title.place(x=140,y=20)
    elif area == 1:
     title = tk.Label(root,text=f"塔の前",font=("Arial",30))
     title.place(x=140,y=20)

     lvdef=1
     expdef=0
     atdefdef = 5
     dfdefdef = 3
     hpdefdef = 50
    elif area == 2:
     if days != 28:
      title = tk.Label(root,text=f"{days-16}階層",font=("Arial",30))
      title.place(x=140,y=20)
     else:
      title = tk.Label(root,text="最上階",font=("Arial",30))
      title.place(x=140,y=20)


    if days == 15:
     title = tk.Label(root,text="地面が少し揺れている...？",font=("Arial",12))
     title.place(x=120,y=80)
    elif days == 16 and area == 0:
     title = tk.Label(root,text="島は姿を消した...",font=("Arial",12))
     title.place(x=120,y=80)    
     title = tk.Label(root,text="帰還装置を使って帰ろう(物資から選択)",font=("Arial",8))
     title.place(x=150,y=5)    
     if 24 in inventory:
      pass
     else:
      inv_data1.append(0)
      inv_data2.append(0)
      inv_data3.append(0)
      inv_data4.append(0)
      inventory.append(24)
    elif days == 28:
     global clearflag
     title = tk.Label(root,text="綺麗な景色だ。",font=("Arial",12))
     title.place(x=120,y=80)    
     title = tk.Label(root,text="帰還装置を使って帰ろう(物資から選択)",font=("Arial",8))
     title.place(x=150,y=5)  
    else:
     if area == 0:
      title = tk.Label(root,text=f"行動回数残り:{act}",font=("Arial",15))
      title.place(x=120,y=80)       
     if area == 2:
      title = tk.Label(root,text=f"必要戦闘回数:{act}",font=("Arial",15))
      title.place(x=110,y=80)       
    statnamepre=game_data["stat"][stat]
    statname=statnamepre["name"]
    title = tk.Label(root,text=f"stat:{statname}",font=("Arial",8))
    title.place(x=0,y=170)
    title = tk.Label(root,text=f"Lv:{lv} exp:{exp}",font=("Arial",20))
    title.place(x=140,y=120)
    title = tk.Label(root,text=f"次のレベルまで:{((lv*lv)+(5*lv))-exp}",font=("Arial",9))
    title.place(x=265,y=100)
    title = tk.Label(root,text=f"HP: {hpnow}/{hp} ATK: {at} DEF: {df}",font=("Arial",17))
    title.place(x=60,y=160)
    title = tk.Label(root,text=f"(HP+{hpex+hpex2+hpex3}) (AT+{atex+atex2+atex3}) (DF+{dfex+dfex2+dfex3})",font=("Arial",11))
    title.place(x=60,y=225)
    if sknm3 == "-":
     title = tk.Label(root,text=f"武器:{weaponname}. 防具:{armorname}.",font=("Arial",9))
     title.place(x=0,y=185)
    if sknm3 != "-":
     title = tk.Label(root,text=f"武器:{weaponname}☆. 防具:{armorname}.",font=("Arial",9))
     title.place(x=0,y=185)
    title = tk.Label(root,text=f"({sknm1})",font=("Arial",8))
    title.place(x=260,y=185)
    title = tk.Label(root,text=f"({sknm2})",font=("Arial",8))
    title.place(x=260,y=200)
    if sknm3 != "-":
     title = tk.Label(root,text=f"(({sknm3}))",font=("Arial",8))
     title.place(x=260,y=215)
    title = tk.Label(root,text=f"[{sknm4}]",font=("Arial",8))
    title.place(x=260,y=230)
    title = tk.Label(root,text=f"アクセサリー:{accessoryname}.",font=("Arial",9))
    title.place(x=0,y=205)
    if area == 1:
     button=tk.Button(root,text="入る",font=("Arial",20),command=entower)
     button.place(x=20,y=250)
     def backker():
       global scene
       global area
       pulloff()
       area=0
       scene=0
       main()
     button=tk.Button(root,text="戻る",font=("Arial",20),command=backker)
     button.place(x=210,y=250)    
    else:
     button=tk.Button(root,text="狩り",font=("Arial",20),command=hunt)
     button.place(x=20,y=250)
     button=tk.Button(root,text="休憩",font=("Arial",20),command=rest)
     button.place(x=210,y=250)
    button=tk.Button(root,text="探索",font=("Arial",20),command=search)
    button.place(x=110,y=250)

    button=tk.Button(root,text="物資",font=("Arial",20),command=inv)
    button.place(x=300,y=250)
    button=tk.Button(root,text="装備を外す",font=("Arial",7),command=pulloff)
    button.place(x=0,y=225)
    
    
  elif scene==5:#戦闘
    update_scene() 

    skdt1=game_data["skills"][myskill[0]]
    skdt2=game_data["skills"][myskill[1]]
    skdt3=game_data["skills"][myskill[2]]
    skdt4=game_data["skills"][myskill[3]]
    
    sknm1 = skdt1["fullname"]
    sknm2 = skdt2["fullname"]
    sknm3 = skdt3["fullname"]
    sknm4 = skdt4["fullname"] 
    title = tk.Label(root,text=f"{ename}",font=("Arial",20))
    if ename != "「The Tower Master」":
     title.place(x=140,y=10)
    else:
     title.place(x=70,y=10)
    statnamepre=game_data["stat"][stat]
    statname=statnamepre["name"]
    title = tk.Label(root,text=f"stat:{statname}",font=("Arial",8))
    title.place(x=0,y=170)
    title = tk.Label(root,text=f"HP: {ehpnow}/{ehp} ATK: {eat} DEF: {edf}",font=("Arial",17))
    title.place(x=60,y=50)
    title = tk.Label(root,text=f"HP: {hpnow}/{hp} ATK: {at} DEF: {df}",font=("Arial",17))
    title.place(x=60,y=160)
    title = tk.Label(root,text=f"(HP+{hpex+hpex2+hpex3}) (AT+{atex+atex2+atex3}) (DF+{dfex+dfex2+dfex3})",font=("Arial",11))
    title.place(x=60,y=225)
    if sknm3 == "-":
     title = tk.Label(root,text=f"武器:{weaponname}. 防具:{armorname}.",font=("Arial",9))
     title.place(x=0,y=185)
    if sknm3 != "-":
     title = tk.Label(root,text=f"武器:{weaponname}☆. 防具:{armorname}.",font=("Arial",9))
     title.place(x=0,y=185)
    title = tk.Label(root,text=f"({sknm1})",font=("Arial",8))
    title.place(x=260,y=185)
    title = tk.Label(root,text=f"({sknm2})",font=("Arial",8))
    title.place(x=260,y=200)
    if sknm3 != "-":
     title = tk.Label(root,text=f"(({sknm3}))",font=("Arial",8))
     title.place(x=260,y=215)
    title = tk.Label(root,text=f"[{sknm4}]",font=("Arial",8))
    title.place(x=260,y=230)
    title = tk.Label(root,text=f"アクセサリー:{accessoryname}.",font=("Arial",9))
    title.place(x=0,y=205)
    button=tk.Button(root,text="攻撃",font=("Arial",20),command=attacking)
    button.place(x=40,y=250)
    button=tk.Button(root,text="スキル",font=("Arial",20),command=skilling)
    button.place(x=130,y=250)
    button=tk.Button(root,text="逃げる",font=("Arial",20),command=escape)
    button.place(x=250,y=250)
    if damagesave != -1:
     title = tk.Label(root,text=f"{ename}に{damagesave}ダメージ与えた",font=("Arial",10))
     title.place(x=100,y=80)
     if damage == 0:
      title = tk.Label(root,text="ダメージを受けなかった！",font=("Arial",10))
      title.place(x=100,y=130)
     else:
      title = tk.Label(root,text=f"{ename}から{damage}ダメージ受けた",font=("Arial",10))
      title.place(x=100,y=130)
      if skillmess != "":
       title = tk.Label(root,text=f"{skillmess}                      ",font=("Arial",10))
       title.place(x=20,y=130)
      if statmess != "":
       title = tk.Label(root,text=f"{statmess}",font=("Arial",7))
       title.place(x=0,y=147)
     if critmess == 1:
      title = tk.Label(root,text="クリティカルヒット！",font=("Arial",15))
      title.place(x=100,y=100)
      print("うおおおおおおおおおおおfffffおお")
    print("処理がここで終わってないとおかしい")

  elif scene==11:#敗北
    update_scene() 
    damagesave= -1

    global weapon,armor,accessory1,weaprank,armrank,accrank
    if area != 2:
     if weapon != -1:
           title = tk.Label(root,text=f"{weaponname} を落としてしまった...",font=("Arial",11))
           title.place(x=20,y=100)
     if armor != -1:
           title = tk.Label(root,text=f"{armorname} は破壊されてしまった...",font=("Arial",11))
           title.place(x=20,y=120)
     if accessory1 != -1:
           title = tk.Label(root,text=f"{accessoryname} は奪われてしまった...",font=("Arial",11))
           title.place(x=20,y=140)     
    if days != 15:
     if area == 0:
      title = tk.Label(root,text=f"{ename}に敗北した...",font=("Arial",15))
      title.place(x=40,y=10)
      title = tk.Label(root,text="逃げるのに夢中で、走り終わったころには",font=("Arial",10))
      title.place(x=20,y=50)
      title = tk.Label(root,text="とっくに日付が変わっていた。",font=("Arial",10))
      title.place(x=20,y=70)
     if area == 2:
      title = tk.Label(root,text=f"{ename}に敗北した...",font=("Arial",15))
      title.place(x=40,y=10)
      title = tk.Label(root,text="急いで階層の初めの部屋に戻ると",font=("Arial",10))
      title.place(x=20,y=50)
      title = tk.Label(root,text="扉は閉まり、鳴き声がまた聞こえてきた...",font=("Arial",10))
      title.place(x=20,y=70)
      title = tk.Label(root,text="この階層で得た経験値を失った...",font=("Arial",10))
      title.place(x=20,y=90)

    elif days == 15:
     title = tk.Label(root,text=f"{ename}に敗北した...",font=("Arial",15))
     title.place(x=40,y=10)
     title = tk.Label(root,text="島は姿を消し、海に引きずり込まれた！",font=("Arial",10))
     title.place(x=20,y=50)
     title = tk.Label(root,text="仕方なく帰還装置で帰ることにする...",font=("Arial",10))
     title.place(x=20,y=70)       
     title = tk.Label(root,text="装備転送ボックスを入手した",font=("Arial",10))
     title.place(x=30,y=200)      
     inv_data1.append(0)
     inv_data2.append(0)
     inv_data3.append(0)
     inv_data4.append(0)
     inventory.append(25)
    if area !=2:
     weaprank=0
     accrank=0
     armrank=0
     weapon=-1
     armor=-1
     accessory1=-1
     weaponname="-"
     armorname="-"
     accessoryname="-"
     myskill.clear()
     myskill = [0,0,0,0]
     itemskill1=0
     itemskill2=0
     itemskill3=0
     itemskill4=0
     atex=0
     atex2=0
     atex3=0
     dfex=0
     dfex2=0
     dfex3=0
     hpex=0
     hpex2=0
     hpex3=0
     at=atdef
     df=dfdef
     hp=hpdef
     button=tk.Button(root,text="OK",font=("Arial",20),command=rest)
     button.place(x=30,y=230)
    elif area == 2:
      atdef=atdefdef
      dfdef=dfdefdef
      hpdef=hpdefdef
      lv=lvdef
      exp=expdef
      pulloff()
      act=len(en_tables[days])
      button=tk.Button(root,text="OK",font=("Arial",20),command=rest)
      button.place(x=30,y=230)
      #main()
  elif scene==10:#勝利
    update_scene() 
    damagesave= -1
    title = tk.Label(root,text=f"{ename}に勝利した！",font=("Arial",15))
    title.place(x=40,y=10)
    title = tk.Label(root,text=f"経験値{eexp}を獲得！",font=("Arial",10))
    title.place(x=30,y=50)
    if days == 15:
     title = tk.Label(root,text="勝利の証を入手した...",font=("Arial",13))
     title.place(x=30,y=125) 
     inv_data1.append(0)
     inv_data2.append(0)
     inv_data3.append(0)
     inv_data4.append(0)
     inventory.append(26)
     act=0
     boxchance=1
     clearflag=1
    elif days == 27:
     title = tk.Label(root,text="呪いの元凶を倒した。",font=("Arial",13))
     title.place(x=30,y=125) 
     clearflag=1
     boxchance=-1
    else:   
     title = tk.Label(root,text="よかったね",font=("Arial",10))
     title.place(x=30,y=70)
     boxchance=random.uniform(1,100)
     boxchance=math.floor(boxchance)

      
    scene=3
    if area == 2:
     act=act-1
     if act == 0:
      if days != 28:
       title = tk.Label(root,text=f"{days-15}階層に到達した",font=("Arial",10))
       title.place(x=30,y=70)
      else:
       title = tk.Label(root,text="最上階に到達した",font=("Arial",10))
       title.place(x=30,y=70)

      scene=6
    print(boxchance)
    if enemy == 12:
      boxchance = 77
      title = tk.Label(root,text="謎のカギを入手した。",font=("Arial",10))
      title.place(x=30,y=90)  
      sending = {
      "itemid":29,
      "skill1":0,
      "skill2":0,
      "skill3":0,  
      "skill4":0
      }
      game_save["itemsave"].append(sending)
      with open("save.json", "w", encoding="utf-8") as f:
       json.dump(game_save, f, indent=4, ensure_ascii=False)
    if enemy == 9 and (weapon == 12 or weapon == 40) and armor == 13 and (accessory1 ==14 or accessory1 ==15):
      boxchance = 77
      title = tk.Label(root,text="ドラゴンウェーブを入手した。",font=("Arial",10))
      title.place(x=30,y=110)  
      inv_data1.append(38)
      inv_data2.append(0)
      inv_data3.append(0)
      inv_data4.append(0)
      inventory.append(40)
    if boxchance < 16 and area == 0:#15%
     title = tk.Label(root,text="装備転送ボックスを入手した",font=("Arial",10))
     title.place(x=30,y=90)      
     inv_data1.append(0)
     inv_data2.append(0)
     inv_data3.append(0)
     inv_data4.append(0)
     inventory.append(25)
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)
    a=0
    while exp >=  (lv*lv)+(5*lv):

        exp = exp - ((lv*lv)+(5*lv))
        lv=lv+1
        a=a+1
        title = tk.Label(root,text=f"レベルが{a}上がった",font=("Arial",10))
        title.place(x=30,y=70)
        hpdef=hpdef+5
        hpnow=hpnow+5
        atdef=atdef+1
        dfdef=dfdef+1
        if act== 0:
         lvdef=lv
         atdefdef=atdef
         dfdefdef=dfdef
         hpdefdef=hpdef
         expdef=exp
    else:
        breakpoint
    #lvdef=lv
   # expdef=exp
  elif scene==12:#逃走
    update_scene() 
    damagesave= -1
    if days != 15:
     title = tk.Label(root,text=f"{ename}から逃げた。",font=("Arial",15))
     title.place(x=40,y=10)
    elif days == 15:
     title = tk.Label(root,text="一旦体制を立て直すことにした。",font=("Arial",15))
     title.place(x=40,y=10)     
    scene = 3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)
  elif scene==13:#インベントリ
    update_scene() 


    resoursedata = game_save["resource"][0]
    money = resoursedata['money']
    print(money)
   
    if len(inventory)/12 < pages+1:
       pass
    else:
     button=tk.Button(root,text="次ページへ",font=("Arial",7),command=nextpage)
     button.place(x=345,y=250)
    title=tk.Label(root,text=f"{pages+1}ぺージ",font=("Arial",8))
    title.place(x=350,y=210) 
    if loadflag != 0:
     title=tk.Label(root,text="資金",font=("Arial",8))
     title.place(x=350,y=40)     
     title=tk.Label(root,text=f'{money}',font=("Arial",8))
     title.place(x=350,y=60)
     button=tk.Button(root,text="戻る",font=("Arial",9),command=back2)
     button.place(x=350,y=10)
    else:
     button=tk.Button(root,text="戻る",font=("Arial",9),command=back)
     button.place(x=350,y=10)
     title=tk.Label(root,text="残り",font=("Arial",8))
     title.place(x=350,y=40)
     title=tk.Label(root,text=f'{lv - weaprank - armrank - accrank}',font=("Arial",8))
     title.place(x=350,y=60)
    if pages != 0:
           button=tk.Button(root,text="前ページへ",font=("Arial",7),command=prevpage)
           button.place(x=345,y=280)
    b=0

    for a in range(12*(pages),min(12 * (pages + 1), len(inventory))): 
         b=b+1
         itemid = inventory[a]
         itsk1 = inv_data1[a]
         itsk2 = inv_data2[a]
         itsk3 = inv_data3[a]
         itsk4 = inv_data4[a]


         item_data = game_data["items"][itemid]
         if itemid != 29:
          skdt1=game_data["skills"][itsk1]
          skdt2=game_data["skills"][itsk2]
          skdt3=game_data["skills"][itsk3]
          skdt4=game_data["skills"][itsk4]
         else:
          skdt1=game_data["skills"][0]
          skdt2=game_data["skills"][0]
          skdt3=game_data["skills"][0]
          skdt4=game_data["skills"][0]
         

         itemtypeinv = item_data['type']

         itemname = item_data['name']
         sknm1 = skdt1['name']
         sknm2 = skdt2['name']
         sknm3 = skdt3['name']
         sknm4 = skdt4['name']
         itemrank = item_data['rank']
         
         if itemtypeinv == 0:
          if itsk3 == 0:
           title=tk.Label(root,text=f'ﾗﾝｸ{itemrank}:{itemname}({sknm1}),({sknm2}),[武器]',font=("Arial",8))
           title.place(x=5,y=(b*25-25))
          elif itsk3 != 0:
           title=tk.Label(root,text=f'ﾗﾝｸ{itemrank}:{itemname}☆({sknm1}),({sknm2}),(({sknm3})),[武器]',font=("Arial",8))
           title.place(x=5,y=(b*25-25)) 
         elif itemtypeinv == 1:
          title=tk.Label(root,text=f'ﾗﾝｸ{itemrank}:{itemname}[防具]',font=("Arial",8))
          title.place(x=5,y=(b*25-25))
         elif itemtypeinv == 2:
          title=tk.Label(root,text=f'ﾗﾝｸ{itemrank}:{itemname}({sknm4})[アクセサリー]',font=("Arial",8))
          title.place(x=5,y=(b*25-25))
         elif itemtypeinv == 3 or itemtypeinv == 4 or itemtypeinv == 5 or itemtypeinv == 6 or itemtypeinv == 7:
          if itsk3 == 0:
           title=tk.Label(root,text=f'ﾗﾝｸ{itemrank}:{itemname}[特殊]',font=("Arial",7))
           title.place(x=5,y=(b*25-25))
          else:
           title=tk.Label(root,text=f'ﾗﾝｸ{itemrank}:{itemname}(floor {itsk3-16} )[特殊]',font=("Arial",7))
           title.place(x=5,y=(b*25-25))
         #button=tk.Button(root,text=f'破棄{a}',font=("Arial",8),command=lambda a=a:trush(a))
         #button.place(x=300,y=b*25-25)
         if loadflag == 0:
          totalrank=weaprank + armrank + accrank
          if itemtypeinv < 3 :
           if totalrank+itemrank < lv+1:
            if area != 1:
             if itemtypeinv ==0:
                button=tk.Button(root,text=f'装備',font=("Arial",8),command=lambda a=a:equipment(a))
                button.place(x=310,y=b*25-25)
             if itemtypeinv ==1:
                button=tk.Button(root,text=f'装備',font=("Arial",8),command=lambda a=a:equipment(a))
                button.place(x=310,y=b*25-25)
             if itemtypeinv ==2:
                button=tk.Button(root,text=f'装備',font=("Arial",8),command=lambda a=a:equipment(a))
                button.place(x=310,y=b*25-25)

          if itemtypeinv == 3:
           button=tk.Button(root,text=f'帰還',font=("Arial",8),command=pregameend)
           button.place(x=310,y=b*25-25)     
          elif itemtypeinv == 4:      
           button=tk.Button(root,text=f'使用',font=("Arial",8),command=lambda a=a:itemsend(a))
           button.place(x=310,y=b*25-25)
          elif itemtypeinv == 6 and days == -10:      
           button=tk.Button(root,text=f'移動',font=("Arial",8),command=lambda a=a:towerkey(a))
           button.place(x=310,y=b*25-25)
          elif itemtypeinv == 7:
           #if weapon == -1 and armor == -1 and accessory1 == -1:
            button=tk.Button(root,text=f'帰還',font=("Arial",8),command=towerback)
            button.place(x=310,y=b*25-25)   
         else:
           if itemtypeinv == 6:
            button=tk.Button(root,text=f'移動',font=("Arial",8),command=lambda a=a:towerkey(a))
            button.place(x=310,y=b*25-25) 

           else:
            nokakunin=tk.IntVar(value=nokakunin.get())
            checkbox=tk.Checkbutton(root,variable=nokakunin)
            checkbox.place(x=345,y=190)
            title=tk.Label(root,text='確認せず持込',font=("Arial",6))
            title.place(x=345,y=180)
            button=tk.Button(root,text=f'持込',font=("Arial",8),command=lambda a=a:mochikomi(itemname,a))
            button.place(x=310,y=b*25-25)
         rtitle=tk.Button(root,text=f'詳細',font=("Arial",8),command=lambda a=a:Shosai(a))
         rtitle.place(x=280,y=b*25-25)

  elif scene==6:#アイテムガチャ

    update_scene() 
    itemRndm()

    inventory.append(iteming)
    rndskillX = random.uniform(1,1000)
    rndskill1=0
    rndskill2=0
    rndskill3=0
    rndskill4=0 
    
    item_data = game_data["items"][iteming]
    itemtypeinv = item_data['type']
    
    if rndskillX < 401:#40%
      rndskill1 = random.choice([3,5,6,10,21,22,23,36])
      if rndskillX < 201:#20%
        rndskill2 = random.choice([3,5,6,10,21,22,23,36])
        while rndskill2 == rndskill1:
         rndskill2 = random.choice([3,5,6,10,21,22,23,36])
        if 26 in myskill:#スーパーレアスキル Rainbow Rushの処理(テスト済み)
          if rndskillX < 11:#1%
           rndskill3 = random.choice([4,8,12,14])
        else:
         if rndskillX < 6:#0.5%
          rndskill3 = random.choice([4,8,12,14])

    if rndskillX < 301 :#30%
      rndskill4 = random.choice([2,7,15,17,19,24])
    
    a = item_data['skill']
    if a != -1:
      rndskill1 = a 
      rndskill4 = a 
    print("skill")
    print(rndskill1)
    print(rndskill2)
    print(rndskill3)
    print(rndskill4)

    if itemtypeinv == 0:
     inv_data1.append(rndskill1)
     inv_data2.append(rndskill2)
     inv_data3.append(rndskill3)
     inv_data4.append(0)
     rndskill4 = 0
    elif itemtypeinv == 1:
     inv_data1.append(0)
     inv_data2.append(0)
     inv_data3.append(0)
     inv_data4.append(0)
     rndskill1=0
     rndskill2=0
     rndskill3=0
     rndskill4=0
    elif itemtypeinv == 2:
     inv_data1.append(0)
     inv_data2.append(0)
     inv_data3.append(0)
     inv_data4.append(rndskill4) 
     rndskill1=0
     rndskill2=0
     rndskill3=0
    elif itemtypeinv == 3:
     inv_data1.append(0)
     inv_data2.append(0)
     inv_data3.append(0)
     inv_data4.append(0)  
     rndskill1=0
     rndskill2=0
     rndskill3=0
     rndskill4=0

    skdt1=game_data["skills"][rndskill1]
    skdt2=game_data["skills"][rndskill2]
    skdt3=game_data["skills"][rndskill3]
    skdt4=game_data["skills"][rndskill4]
    
    sknm1 = skdt1["fullname"]
    sknm2 = skdt2["fullname"]
    sknm3 = skdt3["fullname"]
    sknm4 = skdt4["fullname"]    
    if area == 0:
     title = tk.Label(root,text="島を探索した...",font=("Arial",15))
     title.place(x=40,y=10)
    elif area == 2:
     title = tk.Label(root,text="宝箱を発見した！",font=("Arial",15))
     title.place(x=40,y=10)      
    if rndskill3 != 0:
     title = tk.Label(root,text=f"アイテム {itemsname}☆ を獲得！！！",font=("Arial",10))
     title.place(x=30,y=50)
     title = tk.Label(root,text="！！！激レア！！！",font=("Arial",11))
     title.place(x=120,y=145)
    elif rndskill3 == 0:
     title = tk.Label(root,text=f"アイテム {itemsname}を獲得！",font=("Arial",10))
     title.place(x=30,y=50)
     title = tk.Label(root,text="よかったね",font=("Arial",10))
     title.place(x=30,y=70)
    if rndskill1 != 0:
          title = tk.Label(root,text=f"さらにスキル:{sknm1}がついていた！",font=("Arial",10))
          title.place(x=20,y=70)
          if rndskill2 != 0:
           title = tk.Label(root,text=f"さらにさらにスキル:{sknm2}もついていた！！",font=("Arial",10))
           title.place(x=20,y=90)
           if rndskill3 != 0:
                 title = tk.Label(root,text=f"おまけにレアスキル:{sknm3}までついていた！！！",font=("Arial",10))
                 title.place(x=20,y=115)

    if rndskill4 != 0:
          title = tk.Label(root,text=f"さらにスキル:{sknm4}がついていた！",font=("Arial",10))
          title.place(x=30,y=70)
              
         
    scene=3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)

  elif scene==20:#戦闘スキル処理
    update_scene() 
    skdt1=game_data["skills"][itemskill1]
    skdt2=game_data["skills"][itemskill2]
    skdt3=game_data["skills"][itemskill3]
    skdt4=game_data["skills"][itemskill4]
    
    sknm1 = skdt1["fullname"]
    sknm2 = skdt2["fullname"]
    sknm3 = skdt3["fullname"]
    sknm4 = skdt4["fullname"]   
    
    print(itemskill1)

    title = tk.Label(root,text="どのスキルを発動する？",font=("Arial",10))
    title.place(x=20,y=10)
    print(myskill)
    activeskills=[14, 10, 20, 24,27,30,38]
    if itemskill1 in activeskills:
        title = tk.Label(root,text=f"{sknm1}",font=("Arial",12))
        title.place(x=20,y=30)
        button=tk.Button(root,text="発動",font=("Arial",7),command=lambda: skillactivation(1))
        button.place(x=20,y=60)
 
    if itemskill2 in activeskills:
        title = tk.Label(root,text=f"{sknm2}",font=("Arial",12))
        title.place(x=20,y=90)
        button=tk.Button(root,text="発動",font=("Arial",7),command=lambda: skillactivation(2))
        button.place(x=20,y=120)

    if itemskill3 in activeskills:
        title = tk.Label(root,text=f"{sknm3}",font=("Arial",12))
        title.place(x=20,y=150)
        button=tk.Button(root,text="発動",font=("Arial",7),command=lambda: skillactivation(3))
        button.place(x=20,y=180)

    if itemskill4 in activeskills:
        title = tk.Label(root,text=f"{sknm4}",font=("Arial",12))
        title.place(x=20,y=210)
        button=tk.Button(root,text="発動",font=("Arial",7),command=lambda: skillactivation(4))
        button.place(x=20,y=240)
    
    
    scene=5
    button=tk.Button(root,text="戻る",font=("Arial",10),command=main)
    button.place(x=30,y=270)
  elif scene==21:#15日目の探索
    update_scene() 
    title = tk.Label(root,text="不思議なことに、",font=("Arial",15))
    title.place(x=40,y=10)
    title = tk.Label(root,text="島をいくら探索しても",font=("Arial",15))
    title.place(x=40,y=50)
    title = tk.Label(root,text="何も見つからなかった。",font=("Arial",16))
    title.place(x=40,y=80)
    scene = 3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)
  elif scene==23:#塔の前のとか
    update_scene() 
    title = tk.Label(root,text="不思議なことに、",font=("Arial",15))
    title.place(x=40,y=10)
    title = tk.Label(root,text="塔の周りには生き物も宝物も",font=("Arial",15))
    title.place(x=40,y=50)
    title = tk.Label(root,text="何も見つからなかった。",font=("Arial",16))
    title.place(x=40,y=80)
    scene = 3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)
  elif scene==23.5:#塔の中の探索とか
    update_scene()
    print(f"クリア！！！！！！！！！{clearflag}")
    print(f"今日は{days}日だぜ！") 
    if days != 28:
     title = tk.Label(root,text="凶暴な鳴き声のする扉と",font=("Arial",15))
     title.place(x=40,y=10)
     title = tk.Label(root,text="無機質な壁以外",font=("Arial",15))
     title.place(x=40,y=50)
     title = tk.Label(root,text="何もなかった。",font=("Arial",16))
     title.place(x=40,y=80)
    else:
     title = tk.Label(root,text="空にかかった虹と",font=("Arial",15))
     title.place(x=40,y=10)
     title = tk.Label(root,text="綺麗な景色以外",font=("Arial",15))
     title.place(x=40,y=50)
     title = tk.Label(root,text="何もなかった。",font=("Arial",16))
     title.place(x=40,y=80)
    scene = 3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)
  elif scene==44.4:#塔の中休憩
    update_scene() 
    title = tk.Label(root,text="あまりに危険なので",font=("Arial",15))
    title.place(x=40,y=10)
    title = tk.Label(root,text="階層の最初の部屋以外で",font=("Arial",15))
    title.place(x=40,y=50)
    title = tk.Label(root,text="休憩はできそうもない...！",font=("Arial",16))
    title.place(x=40,y=80)
    scene = 3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)
  elif scene==24:#16日目の狩り
    update_scene() 
    title = tk.Label(root,text="海はただ静かなだけだ...",font=("Arial",15))
    title.place(x=40,y=10)
    scene = 3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)  
  elif scene==999:#最上階の狩り
    update_scene() 
    title = tk.Label(root,text="島を一望できるだけだ。",font=("Arial",15))
    title.place(x=40,y=10)
    scene = 3
    button=tk.Button(root,text="OK",font=("Arial",20),command=main)
    button.place(x=30,y=230)  
  elif scene==2:#データロード
    update_scene() 
  elif scene==30:#装備転送ボックスの処理
    update_scene() 
    skdt1=game_data["skills"][myskill[0]]
    skdt2=game_data["skills"][myskill[1]]
    skdt3=game_data["skills"][myskill[2]]
    skdt4=game_data["skills"][myskill[3]]
    
    sknm1 = skdt1["fullname"]
    sknm2 = skdt2["fullname"]
    sknm3 = skdt3["fullname"]
    sknm4 = skdt4["fullname"] 
    if weapon + armor + accessory1 == -3:
     title = tk.Label(root,text="何か装備してください",font=("Arial",15))
     title.place(x=40,y=10)
    else:
     title = tk.Label(root,text="どの装備を持ち帰る？",font=("Arial",15))
     title.place(x=40,y=10)
    if weapon != -1:

     if sknm3 == "-":
      title = tk.Label(root,text=f"武器:{weaponname}",font=("Arial",12))
      title.place(x=40,y=50)
      title = tk.Label(root,text=f"({sknm1}),({sknm2})",font=("Arial",9))
      title.place(x=40,y=70)
     if sknm3 != "-":
      title = tk.Label(root,text=f"武器:{weaponname}☆",font=("Arial",12))
      title.place(x=40,y=50)
      title = tk.Label(root,text=f"({sknm1}),({sknm2}),(({sknm3}))",font=("Arial",9))
      title.place(x=40,y=70)
     button=tk.Button(root,text="決定",font=("Arial",7),command=lambda:itemsave(0))
     button.place(x=10,y=50)


    if armor != -1:
      title = tk.Label(root,text=f"防具:{armorname}",font=("Arial",12))
      title.place(x=40,y=100)  
      button=tk.Button(root,text="決定",font=("Arial",7),command=lambda:itemsave(1))
      button.place(x=10,y=100)
    if accessory1 != -1:
     title = tk.Label(root,text=f"アクセサリー:{accessoryname}",font=("Arial",12))
     title.place(x=40,y=150)
     title = tk.Label(root,text=f"[{sknm4}]",font=("Arial",9))
     title.place(x=40,y=170)
     button=tk.Button(root,text="決定",font=("Arial",7),command=lambda:itemsave(2))
     button.place(x=10,y=150)
    
    scene = 13
    button=tk.Button(root,text="戻る",font=("Arial",20),command=main)
    button.place(x=30,y=230)
  elif scene== 32:#セーブ完了
    update_scene() 
    scene = 13
    button=tk.Button(root,text="戻る",font=("Arial",20),command=main)
    button.place(x=30,y=230) 
    title = tk.Label(root,text="転送が完了しました！",font=("Arial",15))
    title.place(x=40,y=10)   
    del inventory[itemsendspot]
    del inv_data1[itemsendspot]
    del inv_data2[itemsendspot]
    del inv_data3[itemsendspot]
    del inv_data4[itemsendspot]
  elif scene== 40:#アイテム持ち込み
    loadflag = 1

    update_scene() 
    a=0
    for item in game_save["itemsave"]:
      itemiding = item["itemid"]
      inventory.append(itemiding)
      itemiding = item["skill1"]
      inv_data1.append(itemiding)
      itemiding = item["skill2"]
      inv_data2.append(itemiding)
      itemiding = item["skill3"]
      inv_data3.append(itemiding)
      itemiding = item["skill4"]
      inv_data4.append(itemiding)
      print(inventory)
      a=a+1
    if a==0:
     scene=0
     button=tk.Button(root,text="戻る",font=("Arial",20),command=main)
     button.place(x=30,y=230) 
     title = tk.Label(root,text="セーブデータにアイテムがありません",font=("Arial",15))
     title.place(x=40,y=10)   
    else:
     scene = 13
     main()
  elif scene== 100:#帰還
   update_scene()



   title = tk.Label(root,text="装置で帰還しますか？",font=("Arial",15))
   title.place(x=40,y=10)   
   scene=13
   button=tk.Button(root,text="いいえ",font=("Arial",20),command=main)
   button.place(x=280,y=230)
   button=tk.Button(root,text="はい",font=("Arial",20),command=gameend)
   button.place(x=30,y=230)
  elif scene== 100.5:#帰還
   update_scene()



   title = tk.Label(root,text="装置で帰還しますか？",font=("Arial",15))
   title.place(x=40,y=10)   
   scene=13
   button=tk.Button(root,text="いいえ",font=("Arial",20),command=main)
   button.place(x=280,y=230)
   button=tk.Button(root,text="はい",font=("Arial",20),command=gameending)
   button.place(x=30,y=230)
  elif scene== 222.22:#DAW(????????????????????????????????????)
   update_scene()
   global page
   global notes
   global mid
   global track1
   global track2
   global track3
   global track4
   global octave
   global risting
   global BPM
   global ptc
   notes=[]
      
   def on_canvas_click(event):
    global page
    global octave
    global track1
    global track2
    global track3
    global track4
    global mid
    global risting#リストのスペルlistで草 IQ3ですドーモ]
    global ptc
    ptc = ((144 - event.y) // 12) + ((octave + 1) * 12) - 1

    note_width = 15
    note_height = 12
    x = (event.x // note_width) * note_width
    y = (event.y // note_height) * note_height
    ptc=((144-y)//12)+((octave+1)*12)-1
    times=((((x-30)//15)+(page*16))*120)
    x=((x-15)//15)+(((page+1)*16)-16)
    if len(risting) == 0:
     risting.append(ptc)
    elif len(risting) < x:
     bh=len(risting)
     for a in range(x-bh-1):
      risting.append(-1)
     risting.append(ptc)
     if y >= 137:
       risting[x-1]=-1
    else:
      risting[x-1]=ptc
      if y >= 144:
       risting[x-1]=-1
    print(risting)
    main()

   title = tk.Label(root,text=f"{(page*4)+1}~{(page*4)+4}小節",font=("Arial",15))
   title.place(x=40,y=10)  
   title = tk.Label(root,text=f"|{(page*4)+1}",font=("Arial",15))
   title.place(x=135,y=82) 
   title = tk.Label(root,text=f"|{(page*4)+2}",font=("Arial",15))
   title.place(x=195,y=82) 
   title = tk.Label(root,text=f"|{(page*4)+3}",font=("Arial",15))
   title.place(x=255,y=82) 
   title = tk.Label(root,text=f"|{(page*4)+4}",font=("Arial",15))
   title.place(x=315,y=82)    
   title = tk.Label(root,text=f"C{octave}",font=("Arial",8))
   title.place(x=20,y=175)  
   button=tk.Button(root,text=f"{(page*4)+5}~{(page*4)+8}小節へ",font=("Arial",8),command=pageinc)
   button.place(x=270,y=10)
   button=tk.Button(root,text=f"octave↑",font=("Arial",8),command=octinc)
   button.place(x=50,y=150)
   if octave > 0:
    button=tk.Button(root,text=f"octave↓",font=("Arial",8),command=octdec)
    button.place(x=50,y=200)     
   if page > 0:
    button=tk.Button(root,text=f"{(page*4)-3}~{(page*4)}小節へ",font=("Arial",8),command=pagedec)
    button.place(x=180,y=10)
   canvas=tk.Canvas(root,width=270,height=180,background="blue")
   canvas.place(x=110, y=110)
   for b in range(16):
    canvas.create_line(b*15+30,0,b*15+30,180,fill="black")
   for b in range(12):    
    canvas.create_line(0,b*12+12,270,b*12+12,fill="black")
    canvas.create_rectangle(0,0,30,12,fill="white")
    canvas.create_rectangle(0,12,20,24,fill="black")
    canvas.create_rectangle(0,24,30,36,fill="white")
    canvas.create_rectangle(0,36,20,48,fill="black")
    canvas.create_rectangle(0,48,30,60,fill="white")
    canvas.create_rectangle(0,72,30,84,fill="white")
    canvas.create_rectangle(0,60,20,72,fill="black")
    canvas.create_rectangle(0,84,30,96,fill="white")
    canvas.create_rectangle(0,96,20,108,fill="black")
    canvas.create_rectangle(0,108,30,120,fill="white")
    canvas.create_rectangle(0,120,20,132,fill="black")
    canvas.create_rectangle(0,132,30,144,fill="white")
   canvas.bind("<Button-1>", on_canvas_click)
   if len(risting) > 0:
    for a in range(len(risting)):
     if a <= page*16+16 and page*16 <= a:
      rect = canvas.create_rectangle((a*15)+30-page*240,(144-((risting[a]-12)-octave*12)*12)-12, (a*15+45)-page*240, (144-((risting[a]-12)-octave*12)*12), fill="red")
   button=tk.Button(root,text="再生",font=("Arial",10),command=midsave)
   button.place(x=30,y=230)
   global entry 
   entry=tk.Entry(root)
   entry.place(x=130,y=60) 
   title = tk.Label(root,text=f"BPM:{BPM}",font=("Arial",8))
   title.place(x=195,y=40)  

   button=tk.Button(root,text="テンポ変更",font=("Arial",7),command=bpmchanging)
   button.place(x=130,y=40)   
   def backing():
     global scene
     scene=5
     attacking()
   button=tk.Button(root,text="やめる",font=("Arial",7),command=backing)
   button.place(x=0,y=270)  
   title=tk.Label(root,text="ノート削除→",font=("Arial",6))
   title.place(x=50,y=260)  
  elif scene==300:
    update_scene()
   
    global aur
    global aur2
    global aur3
    global aur4
    global aur5
    global iyaabaf
    global iyaabaf2
    global aaa
    def abaaiyaaaieee():
     global  iyaabaf
     global aur
     global aur2
     global aur3
     global aur4
     global aur5
     global iyaabaf2
     if iyaabaf == 4:
      iyaabaf=0
     else:
      iyaabaf=iyaabaf+1
     if iyaabaf == 0:
      iyaabaf2=aur
     elif iyaabaf == 1:
      iyaabaf2=aur2
     elif iyaabaf == 2:
      iyaabaf2=aur3
     elif iyaabaf == 3:
      iyaabaf2=aur4
     elif iyaabaf == 4:
      iyaabaf2=aur5
     main()
    def abaaiyaaaieee2():
     global  iyaabaf
     global aur
     global aur2
     global aur3
     global aur4
     global aur5
     global iyaabaf2
     if iyaabaf == 0:
      aur=aur+1
     elif iyaabaf == 1:
      aur2=aur2+1
     elif iyaabaf == 2:
      aur3=aur3+1
     elif iyaabaf == 3:
      aur4=aur4+1
     elif iyaabaf == 4:
      aur5=aur5+1
     main() 
    def abaaiyaaaieee3():
     global  iyaabaf
     global aur
     global aur2
     global aur3
     global aur4
     global aur5
     global iyaabaf2
     if iyaabaf == 0:
      aur=aur-1
     elif iyaabaf == 1:
      aur2=aur2-1
     elif iyaabaf == 2:
      aur3=aur3-1
     elif iyaabaf == 3:
      aur4=aur4-1
     elif iyaabaf == 4:
      aur5=aur5-1
     main()     
    def pone():
      global aur
      global aur2
      global aur3
      global aur4
      global aur5
      sending = {
      "itemid":aur,
      "skill1":aur2,
      "skill2":aur3,
      "skill3":aur4,  
      "skill4":aur5
      }
      game_save["itemsave"].append(sending)
      with open("save.json", "w", encoding="utf-8") as f:
       json.dump(game_save, f, indent=4, ensure_ascii=False)
    def pone2():
      global scene
      scene=0
      main()
    item_data = game_data["items"]
    title = tk.Label(root,text=f"{item_data[aur]['name']}",font=("Arial",8))
    title.place(x=80,y=0) 
    title = tk.Label(root,text=f"{game_data['skills'][aur2]['name']}",font=("Arial",8))
    title.place(x=80,y=20)
    title = tk.Label(root,text=f"{game_data['skills'][aur3]['name']}",font=("Arial",8))
    title.place(x=80,y=40)
    title = tk.Label(root,text=f"{game_data['skills'][aur4]['name']}",font=("Arial",8))
    title.place(x=80,y=60)
    title = tk.Label(root,text=f"{game_data['skills'][aur5]['name']}",font=("Arial",8))
    title.place(x=80,y=80)
    button=tk.Button(root,text="県",font=("Arial",7),command=abaaiyaaaieee)
    button.place(x=40,y=iyaabaf*20)  
    button=tk.Button(root,text="玉",font=("Arial",7),command=abaaiyaaaieee2)
    button.place(x=20,y=iyaabaf*20)     
    button=tk.Button(root,text="埼",font=("Arial",7),command=abaaiyaaaieee3)
    button.place(x=0,y=iyaabaf*20)  
    button=tk.Button(root,text="生成",font=("Arial",7),command=pone)
    button.place(x=40,y=150)  
    button=tk.Button(root,text="戻る",font=("Arial",7),command=pone2)
    button.place(x=20,y=150)  
  elif scene == 777:
   update_scene()



   title = tk.Label(root,text="？？？？？？？？を生成しますか？",font=("Arial",15))
   title.place(x=40,y=10)   
   scene=13
   button=tk.Button(root,text="いいえ",font=("Arial",20),command=main)
   button.place(x=280,y=230)
   button=tk.Button(root,text="はい",font=("Arial",20),command=raiiinbow)
   button.place(x=30,y=230)
  elif scene == 777.7:

      update_scene()
      rainbowing=0
      def rainbow():
       global rainbowing
       if not rtitle.winfo_exists():
        return
       rainbowing=rainbowing+1
       if rainbowing > 6:
        rainbowing=0
       rainbow_colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'magenta']
       current_color = rainbow_colors[rainbowing]
       rtitle.config(bg=current_color, activebackground=current_color)
       root.after(222, rainbow)
      sending = {
      "itemid":39,
      "skill1":0,
      "skill2":0,
      "skill3":0,  
      "skill4":37
      }
      money=money-7777
      game_save["itemsave"].append(sending)
      game_save["resource"][0]["money"]=money
      with open("save.json", "w", encoding="utf-8") as f:
       json.dump(game_save, f, indent=4, ensure_ascii=False)
      title = tk.Label(root,text="虹に向け、杖をかかげた......",font=("Arial",15))
      title.place(x=40,y=10)
      title = tk.Label(root,text="アイテム おさかなニンジン を獲得！！！",font=("Arial",10))
      title.place(x=30,y=50)
      title = tk.Label(root,text=f"さらにスキル:虹の夢がついていた！",font=("Arial",10))
      title.place(x=20,y=70)
      scene=0
      rtitle=tk.Button(root,text="OK",font=("Arial",20),command=main)
      rtitle.place(x=30,y=230)
      rainbow()
def raiiinbow():
  global scene
  scene=777.7
  main()
main()
root.mainloop()
