# Reference Image Normalization

Normalization 的目标是让后续 Style DNA 只看“作品本身”，不被截图容器、平台控件和后期覆盖物污染。

## 1. Contamination taxonomy

### A. Platform / UI chrome — 默认移除
- 手机状态栏、导航栏、App tab bar
- 网页 header / sidebar / footer
- 播放、点赞、收藏、分享、关闭按钮
- 进度条、轮播点、滑块
- 编辑器菜单、图层框、选区、参考线
- 鼠标指针、触控提示

### B. Overlay text — 默认移除
- 字幕
- 社交媒体标题
- 用户名
- 话题标签
- 评论气泡
- 后期营销文案

### C. Ownership / distribution marks — 默认移除
- 水印
- 平台 Logo
- 二维码
- 账号 ID
- 后加签名

### D. Framing contamination — 通常移除
- 设备 mockup
- 浏览器窗框
- 截图留白
- 拼图分隔线
- 不属于原作品的圆角卡片背景

### E. Keep unless proven external
- 场景内自然文字
- 作品本身的版式文字
- 漫画气泡（如果是原始视觉语言）
- 海报自身标题排版
- 胶片边缘、扫描纸边（如果是媒介风格）
- 原始画面颗粒、纸纹、笔触、噪点

## 2. How to normalize

优先顺序：

1. 无损裁掉纯 UI 区域；
2. mask 掉局部 overlay；
3. 有编辑工具时，可在分析副本上 inpaint；
4. 无法修复时，把遮挡区域标记为 unknown。

不要为了统一尺寸而强行拉伸。

## 3. Aspect ratio

保留原始构图比例作为证据。

如果需要统一视觉检查，可生成“analysis canvas”，采用 contain / letterbox，而不是 crop-to-fill；letterbox 本身不得进入风格分析。

## 4. Exposure / color

除非参考图明显来自不同截图亮度，不要做自动白平衡或强行调色。色彩本身可能正是 Style DNA。

允许：
- 纠正明显截图色偏；
- 去除系统夜览 / 滤镜导致的全局污染（必须高置信）。

不允许：
- 为了“看起来一致”而人为统一所有参考图色调。

## 5. Occlusion score

记录：

- `0.00–0.10`: clean
- `0.11–0.25`: mild contamination
- `0.26–0.40`: moderate; lower confidence
- `>0.40`: heavy; do not use hidden regions as style evidence

## 6. Outlier pre-check

以下情况先标记 `possible_outlier`：

- 媒介不同（3D vs 摄影）；
- 光影体系完全不同；
- 线条 / 造型体系完全不同；
- 色彩关系与其他图相反；
- 看起来来自另一个系列。

最终是否剔除要等跨图比较后决定。
