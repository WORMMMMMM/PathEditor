# 机器狗展示路线编辑器

谱偏相机机器狗演示场地的俯视图编辑器：拖动亚克力板、不透明板、镜子、苹果、书包和路点，右侧实时算出动作序列、总长度、耗时，并检查路线离道具是否够远。

场地按 4.3 m × 4.7 m 绘制，坐标原点在观众一侧的左下角，x 向右，y 向后墙，单位 m。

## 使用

不需要安装任何东西：

- **直接打开**：下载或 clone 本仓库，双击 `index.html` 用浏览器（Chrome / Edge）打开即可。
- **本地服务器（可选）**：`python -m http.server 8000`，然后打开 http://localhost:8000 。
- **GitHub Pages（可选）**：仓库 Settings → Pages → Source 选 `main` 分支根目录，几分钟后就有一个公开网址。

## 操作

| 操作 | 方法 |
|---|---|
| 移动 | 按住对象拖动，吸附 5 cm |
| 精确修改 | 点选后在右侧输入 x、y、长度、角度（0° 水平，90° 竖直） |
| 旋转 / 删除 | 选中后按 R / Shift+R 旋转 15°，Delete 删除 |
| 添加 | 顶部按钮，新对象出现在场地中央 |
| 路点 | 可设停留朝向（0° 东，90° 后墙，180° 西，270° 观众）、停留秒数、备注 |
| 保存 | 修改自动存在当前浏览器；“导出 JSON 文件”下载布局，“导入 JSON 文件”读回 |

`layouts/layout_v6.json` 是当前定稿布局，也是编辑器打开时的默认布局。

## 布局文件格式

```json
{"layout": {
  "items": [{"id": "w1", "type": "acrylic", "x": 0.65, "y": 3.8, "len": 1.7, "angle": 90}],
  "route": [{"x": 0.5, "y": 0.5, "note": "起点"}, {"x": 2.35, "y": 3.2, "look": 36, "stop": 9}],
  "startHeading": 90
}}
```

- `type`：`acrylic` 亚克力板、`opaque` 不透明板、`mirror` 镜子、`apple` 苹果、`bag` 书包、`deadend` 透明挡板、`monitor` 显示器
- 板类对象：`x, y` 是中心，`len` 长度，`angle` 走向角度；镜子 / 显示器的朝向在走向左侧 90°
- 路点：`look` 停留时朝向（度），`stop` 停留秒数

## 出图（可选）

`tools/plan_png.py` 把布局 JSON 画成 PPT 用的俯视图：

```bash
pip install matplotlib
python tools/plan_png.py layouts/layout_v6.json plan.png
```
