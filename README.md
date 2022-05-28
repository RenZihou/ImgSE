# ImageSearchEngine

This is my final project of SEARCH ENGINE course (40240762) in Tsinghua University.

## Required Features 项目要求

评分标准：

* 核心功能（35分）：用户界面（25分），图片检索（10分）。
* 其他（25分）：尺寸/颜色筛选（10分），以图搜图，查询纠错，跨语言搜索，跨数据集等等，根据实现难度给分。
* 主观体验（20分）：分展示、设计、技术、团队协作、QA共5个部分。
* 实验报告（20分）：统一要求+测试图片搜索功能。

使用的数据集为：

* [谷歌开放数据集](https://github.com/cvdfoundation/open-images-dataset) - 用于本项目中文本搜图功能实现；由于仅是 demo，本项目只使用了一部分数据。

## Usage 快速运行

### 配置环境

```bash
cd backend
pip3 install -r requirements.txt
cd ../frontend
npm install
```

### 建库

1. 修改`backend/settings.py`中的各项路径（`*_PATH`设置项）
2. 运行`python3 backend/setup.py`

### 启动后端（服务端）

```bash
cd backend
python3 -m uvicorn main:app --reload
```

### 启动前端（浏览器端）

```bash
cd frontend
npm run serve
```

## Change Log 更新日志

### v1.1.0

**Add**

* 前端：快捷添加标签（标签搜索）

**Fix**

* 前端：修复“即便没有新图片了，也会不断尝试拉取更多”的问题

**Technical Change**

* 后端：将计算颜色直方图所用的HSV编码改为HSL编码

### v1.0.0-alpha

**Add**

* 后端：以图搜图功能
* 前端：以图搜图功能、相似图片推荐

**Technical Change**

* 后端：重写搜索引擎框架以更好地复用代码

### v0.4.0

**Add**

* 后端：色调筛选功能、继续加载
* 前端：色调筛选、无限滚动

**Technical Change**

* 后端：搜索功能优化

### v0.3.0

**Add**

* 后端：大小（像素数）筛选功能
* 前端：大小筛选、未找到图片的警告

### v0.2.0

**Add**

* 后端：标签筛选功能
* 前端：标签展示、标签筛选

**Fix**

* 前端：水平居中展示

### v0.1.0

**Add**

* 后端：文本检索功能
* 前端：文本检索入口、图片列表展示

## Development Process 开发进度

- [x] 基本功能
    - [x] 文字-图片检索 (22/04/14)
- [x] 辅助功能
    - [x] 尺寸筛选 (22/04/17)
    - [x] 色调筛选 (22/04/18)
    - [x] 标签筛选 (22/04/17)
- [x] 拓展功能
    - [x] 图片-图片检索 (22/04/19)
    - [x] 相似推荐 (22/04/19)
