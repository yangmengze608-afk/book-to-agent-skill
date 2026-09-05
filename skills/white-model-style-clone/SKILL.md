---
name: white-model-style-clone
description: Create cleaner reference-styled images through a two-stage white-model workflow that locks composition and object count before controlled recoloring. Use when direct style transfer becomes noisy, dirty, overdecorated, cluttered, or introduces unwanted details. Keep ordinary image-style-clone requests on the original skill unless cleanliness or detail suppression is central.
---

# White Model Style Clone

将构图与风格解耦：先生成无纹理白模锁定结构，再把参考图限制为配色、光线和必要材质来源。

## Primary workflow

1. 审计输入角色：
   - `structure source`：决定镜头、构图、人物数量与站位、姿态、轮廓、建筑大体块、关键道具、负空间。
   - `style reference`：只决定配色、光线方向、材质类别和大尺度明暗。
   - 若只有一张参考图且需要新场景，先依据用户场景生成白模；不要直接生成完成图。
2. 白模阶段：输出符合目标画幅的光滑白色或浅灰哑光模型。保留结构源中的必要物件，删除纹样、雕花、文字、碎屑、烟尘、污渍、刮痕和所有微细节。
3. 白模 QA：确认人物数量、站位、身份轮廓、动作、主要道具、空间层级和留白。缺人、重复人物或主体错位时先修白模，禁止带错进入上色阶段。
4. 重新上色：同时提供白模和风格参考。明确指定白模为结构与物件数量的唯一 authority，风格图只提供颜色、光线和材质类别，并写出 `Do not add anything not present in the white model`。
5. 清洁 QA：检查颗粒、散斑、脏滤镜、灰雾蒙脸、密集刺绣、过量金属挂件、无叙事作用的碎屑、伪文字及暗部糊死。发现一项即定向修正，最多一轮。

## White-model prompt contract

必须列出要保留的结构不变量，并要求：

- smooth matte white and light neutral gray clay;
- crisp edges and broad readable shapes;
- soft studio ambient occlusion for depth only;
- no color, texture, text, ornament, debris, smoke, dust, grain or noise;
- production maquette, not finished artwork.

白模不是灰度完成图。不得保留原图的纹理与脏污，否则第二阶段会继续放大。

## Recolor prompt contract

必须明确：

- 白模控制 camera, geometry, positions, poses, silhouettes, negative space and object count；
- 风格参考只控制 palette, lighting, material category and large-scale tonal relationships；
- 表面使用大块干净材质，每类材质仅恢复少量可辨识特征；
- 禁止添加白模不存在的纹样、挂件、纸张、雕花、道具、烟雾或背景物。

## Batch consistency

批量故事图先完成一张两阶段基准样片。只有用户确认干净度后才批量继续。后续每张都独立经过白模和重新上色，不能拿已上色成图递归作为下一张风格源；角色身份仍以用户指定的原始参考图为准。

## Delivery

保留白模和最终上色图，使用稳定页码或名称成对保存。报告数量、尺寸、失败重试和任何因安全限制而改变的表达。不得覆盖原始参考图或原 `image-style-clone` skill。
