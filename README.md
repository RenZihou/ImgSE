# ImageSearchEngine

This is my final project of SEARCH ENGINE course (40240762) in Tsinghua University.

## Required Features 项目要求

评分标准：

* 核心功能（35分）：用户界面（25分），图片检索（10分）。
* 其他（25分）：尺寸/颜色筛选（10分），以图搜图，查询纠错，跨语言搜索，跨数据集等等，根据实现难度给分。
* 主观体验（20分）：分展示、设计、技术、团队协作、QA共5个部分。
* 实验报告（20分）：统一要求+测试图片搜索功能。

使用的数据集为：

* [谷歌开放数据集](https://github.com/cvdfoundation/open-images-dataset) - 用于本项目中文本搜图功能实现；
  由于仅是 demo，本项目只使用了一部分数据。
* [Kaggle 以图搜图数据集](https://www.kaggle.com/competitions/landmark-retrieval-2019/overview) -
  用于本项目中以图搜图功能实现。

## Change Log 更新日志

### v0.1

**Add**

* 后端：文本检索功能
* 前端：文本检索入口、图片列表展示

### v0.2

**Add**

* 后端：标签筛选功能
* 前端：标签展示、标签筛选

**Fix**

* 前端：水平居中展示

## Development Process 开发进度

### 后端：搜索引擎

- [x] 基本功能
    - [x] 文字-图片检索 (22/04/14)
- [ ] 辅助功能
    - [ ] 尺寸筛选
    - [ ] 色调筛选
    - [x] 标签筛选 (22/04/17)
- [ ] 拓展功能
    - [ ] 图片-图片检索
    - [ ] 相似推荐
