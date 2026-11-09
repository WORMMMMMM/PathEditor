"""把编辑器导出的布局 JSON 画成俯视图 PNG。
用法: python tools/plan_png.py layouts/layout_v6.json plan.png
注意：假设路线至少有 5 个点（点 3 看镜子、点 4 看苹果、点 2 看书包）。"""
import math, sys, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle
# 中文字体：按顺序找系统里有的
import os
for f in ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc","C:/Windows/Fonts/msyh.ttc","/System/Library/Fonts/PingFang.ttc"]:
    if os.path.exists(f):
        font_manager.fontManager.addfont(f); plt.rcParams["font.family"]=font_manager.FontProperties(fname=f).get_name(); break
BAG="#4f46e5"
SPEC,POL,ROUTE,INK,ACR,MUT="#c27a0e","#b4307a","#1f5fbf","#111827","#2f9fb3","#6b7280"
L=json.load(open(sys.argv[1]))["layout"]
def ends(it):
    a=math.radians(it["angle"]);h=it["len"]/2
    return (it["x"]-h*math.cos(a),it["y"]-h*math.sin(a)),(it["x"]+h*math.cos(a),it["y"]+h*math.sin(a))
fig,ax=plt.subplots(figsize=(6.2,6.6),dpi=200)
fig.subplots_adjust(left=0.02,right=0.98,top=0.98,bottom=0.02)
ax.set_xlim(-0.1,4.48);ax.set_ylim(-0.1,4.88);ax.set_aspect("equal");ax.axis("off")
for g in [i*0.5 for i in range(1,9)]: ax.plot([g,g],[0,4.7],color="#eceae4",lw=0.6,zorder=0)
for g in [i*0.5 for i in range(1,10)]: ax.plot([0,4.3],[g,g],color="#eceae4",lw=0.6,zorder=0)
ax.add_patch(Rectangle((0,0),4.3,4.7,fill=False,ec=INK,lw=1.8))
ax.text(2.15,4.77,"4.3 m",ha="center",va="center",fontsize=10,color=MUT)
ax.text(4.38,2.35,"4.7 m",ha="center",va="center",rotation=90,fontsize=10,color=MUT)
for it in L["items"]:
    if it["type"] in("acrylic","opaque","mirror"):
        p,q=ends(it);c={"acrylic":ACR,"opaque":INK,"mirror":POL}[it["type"]]
        ax.plot([p[0],q[0]],[p[1],q[1]],color=c,lw=5 if it["type"]!="acrylic" else 4.5,solid_capstyle="round" if it["type"]!="mirror" else "butt",alpha=0.9)
a=[i for i in L["items"] if i["type"]=="apple"][0];A=(a["x"],a["y"])
ax.add_patch(Circle(A,0.2,fc="white",ec=SPEC,lw=2))
ax.add_patch(Circle((A[0]-0.07,A[1]),0.05,fc="#c0392b"));ax.add_patch(Circle((A[0]+0.07,A[1]),0.05,fc="white",ec="#c0392b",lw=1.4))
ax.text(A[0],A[1]+0.32,"真 / 假苹果",color="#c0392b",fontsize=10,ha="center",va="center")
for bg in [i for i in L["items"] if i["type"]=="bag"]:
    B=(bg["x"],bg["y"])
    ax.add_patch(Rectangle((B[0]-0.21,B[1]-0.1),0.18,0.2,fc=BAG,ec=BAG,lw=1.2,joinstyle="round"))
    ax.add_patch(Rectangle((B[0]+0.03,B[1]-0.1),0.18,0.2,fc="white",ec=BAG,lw=1.4))
    V=L["route"][2];ax.plot([V["x"]+0.1,B[0]-0.23],[V["y"]-0.07,B[1]+0.05],color=BAG,lw=1.3,ls="--")
    ax.text(B[0],B[1]-0.25,"真 / 假书包",color=BAG,fontsize=10,ha="center",va="center")
R=L["route"];m=[i for i in L["items"] if i["type"]=="mirror"][0];M=(m["x"],m["y"])
P=[(r["x"],r["y"]) for r in R]
ax.plot([P[3][0],M[0],A[0]+0.2],[P[3][1],M[1],A[1]],color=POL,lw=1.3,ls="--")
ax.plot([P[4][0]-0.15,A[0]+0.22],[P[4][1],A[1]],color=SPEC,lw=1.3,ls="--")
ax.plot(*zip(*P),color=ROUTE,lw=2.6,zorder=3)
dx,dy=P[-1][0]-P[-2][0],P[-1][1]-P[-2][1]
for i,(x,y) in enumerate(P):
    lab="S" if i==0 else str(i)
    fc="white" if i==0 else (SPEC if i==len(P)-1 else POL if R[i].get("stop") else ROUTE)
    tc=ROUTE if i==0 else "white"
    ax.add_patch(Circle((x,y),0.13,fc=fc,ec=ROUTE if i==0 else fc,lw=1.6,zorder=4))
    ax.text(x,y,lab,ha="center",va="center",fontsize=9,color=tc,weight="bold",zorder=5)
lab=dict(fontsize=10,ha="center",va="center")
ax.text(m["x"]+0.32,m["y"]+0.05,"镜子",color=POL,**lab)
ax.text(0.47,2.9,"亚克力板",rotation=90,color=ACR,**lab)
ax.text(2.3,0.92,"亚克力板",rotation=30,color=ACR,**lab)
ax.text(1.37,2.7,"不透明板",rotation=90,color=INK,**lab)
ax.text(3.03,2.4,"不透明板",rotation=90,color=INK,**lab)
fig.savefig(sys.argv[2],transparent=False,facecolor="white")
