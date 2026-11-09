"""把编辑器导出的布局 JSON 画成俯视图 PNG（适用于任意布局）。
用法: python tools/plan_png.py layouts/layout_v7.json plan.png
每块板子的标注自动放在板子中点旁边；路线点上的短箭头 = 该点相机朝向（look）。"""
import math, sys, json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
for f in ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc","C:/Windows/Fonts/msyh.ttc","/System/Library/Fonts/PingFang.ttc"]:
    if os.path.exists(f):
        font_manager.fontManager.addfont(f); plt.rcParams["font.family"]=font_manager.FontProperties(fname=f).get_name(); break
BAG,PLANT,APPLE="#4f46e5","#1e8f45","#c0392b"
POL,ROUTE,INK,ACR,MUT="#b4307a","#1f5fbf","#111827","#2f9fb3","#6b7280"
L=json.load(open(sys.argv[1],encoding="utf-8"))["layout"]
W,H=4.3,4.7
def ends(it):
    a=math.radians(it["angle"]);h=it["len"]/2
    return (it["x"]-h*math.cos(a),it["y"]-h*math.sin(a)),(it["x"]+h*math.cos(a),it["y"]+h*math.sin(a))
fig,ax=plt.subplots(figsize=(6.2,6.6),dpi=200)
fig.subplots_adjust(left=0.02,right=0.98,top=0.98,bottom=0.02)
ax.set_xlim(-0.1,W+0.18);ax.set_ylim(-0.1,H+0.18);ax.set_aspect("equal");ax.axis("off")
for g in [i*0.5 for i in range(1,int(W/0.5)+1)]: ax.plot([g,g],[0,H],color="#eceae4",lw=0.6,zorder=0)
for g in [i*0.5 for i in range(1,int(H/0.5)+1)]: ax.plot([0,W],[g,g],color="#eceae4",lw=0.6,zorder=0)
ax.add_patch(Rectangle((0,0),W,H,fill=False,ec=INK,lw=1.8))
ax.text(W/2,H+0.08,"4.3 m",ha="center",va="center",fontsize=10,color=MUT)
ax.text(W+0.09,H/2,"4.7 m",ha="center",va="center",rotation=90,fontsize=10,color=MUT)
lab=dict(fontsize=10,ha="center",va="center",zorder=6)
NAME={"acrylic":("亚克力板",ACR),"deadend":("亚克力板",ACR),"opaque":("不透明板",INK),"mirror":("镜子",POL),"monitor":("显示器",INK)}
R=L["route"];P=[(r["x"],r["y"]) for r in R]
OBJ=[(i["x"],i["y"]) for i in L["items"] if i["type"] in("plant","apple","bag")]
def clear(x,y):  # 离路线和物体越远越好
    return min([math.hypot(x-px,y-py) for px,py in P+OBJ]+[9])
for it in L["items"]:
    t=it["type"]
    if t in NAME:
        p,q=ends(it);name,c=NAME[t]
        ax.plot([p[0],q[0]],[p[1],q[1]],color=c,lw=4.5 if t in("acrylic","deadend") else 5,solid_capstyle="round",alpha=0.9,zorder=2)
        if it["len"]<0.5: continue
        a=math.radians(it["angle"]);n=(-math.sin(a),math.cos(a));d=0.16
        cands=[(it["x"]+s*d*n[0],it["y"]+s*d*n[1]) for s in(1,-1)]
        cands=[c_ for c_ in cands if 0.08<c_[0]<W-0.08 and 0.08<c_[1]<H-0.08] or cands
        x,y=max(cands,key=lambda c_:clear(*c_))
        rot=((it["angle"]+90)%180)-90
        ax.text(x,y,name,rotation=rot,color=c,**lab)
    elif t=="plant":
        ax.add_patch(Circle((it["x"],it["y"]),0.25,fc=PLANT,alpha=0.25,ec="none",zorder=2))
        ax.add_patch(Circle((it["x"],it["y"]),0.11,fc=PLANT,zorder=2))
plants=[i for i in L["items"] if i["type"]=="plant"]
if plants:
    px=max(plants,key=lambda i:i["x"]);xs=[i["x"] for i in plants];ys=[i["y"] for i in plants]
    if max(xs)-min(xs)<0.3:
        top=max(plants,key=lambda i:i["y"]);ax.text(top["x"],top["y"]+0.36,"绿植",color=PLANT,**lab)
    else:
        for i in plants: ax.text(i["x"],i["y"]-0.36,"绿植",color=PLANT,**lab)
for a in [i for i in L["items"] if i["type"]=="apple"]:
    A=(a["x"],a["y"])
    ax.add_patch(Circle(A,0.2,fc="white",ec=APPLE,lw=2,zorder=3))
    ax.add_patch(Circle((A[0]-0.07,A[1]),0.05,fc=APPLE,zorder=4));ax.add_patch(Circle((A[0]+0.07,A[1]),0.05,fc="white",ec=APPLE,lw=1.4,zorder=4))
    near=any(math.hypot(b["x"]-A[0],b["y"]-A[1])<0.9 for b in L["items"] if b["type"]=="bag")
    ax.text(A[0],A[1]+(0.33 if near else -0.33),"真 / 假苹果",color=APPLE,**lab)
for b in [i for i in L["items"] if i["type"]=="bag"]:
    B=(b["x"],b["y"])
    ax.add_patch(Rectangle((B[0]-0.21,B[1]-0.1),0.18,0.2,fc=BAG,ec=BAG,lw=1.2,zorder=3))
    ax.add_patch(Rectangle((B[0]+0.03,B[1]-0.1),0.18,0.2,fc="white",ec=BAG,lw=1.4,zorder=3))
    ax.text(B[0],B[1]-0.33,"真 / 假书包",color=BAG,**lab)
ax.plot(*zip(*P),color=ROUTE,lw=2.6,zorder=3)
for i,(x,y) in enumerate(P):
    lk=R[i].get("look")
    if lk is not None:
        a=math.radians(lk)
        ax.add_patch(FancyArrowPatch((x+0.14*math.cos(a),y+0.14*math.sin(a)),(x+0.42*math.cos(a),y+0.42*math.sin(a)),arrowstyle="-|>",mutation_scale=11,color=POL,lw=1.6,zorder=4))
    lab_="S" if i==0 else str(i);fc="white" if i==0 else ROUTE
    ax.add_patch(Circle((x,y),0.13,fc=fc,ec=ROUTE,lw=1.6,zorder=5))
    ax.text(x,y,lab_,ha="center",va="center",fontsize=9,color=ROUTE if i==0 else "white",weight="bold",zorder=6)
fig.savefig(sys.argv[2],facecolor="white")
