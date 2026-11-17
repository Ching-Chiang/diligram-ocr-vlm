# 解析产物契约（v0.1）

本文件解释 [`schema/doc.schema.json`](../schema/doc.schema.json)。schema 本身是权威定义，本文件只补充语义与约定；两者冲突时以 schema 为准，并请修正本文件。

## 1. 版本策略

- `schema_version` 当前为 `"0.1"`。
- **破坏性改动**（删字段、改类型、改坐标语义、改 enum 取值）必须提升 minor 之后的版本号，并同步通知消费方 `diligram-rag`。
- **新增可选字段**不升版本，但要在本文件登记。
- 消费方按版本号引用契约，不复制 schema 文件。

## 2. 坐标系

`bbox` 为 `[x0, y0, x1, y1]`，**按页面宽高归一化到 0–1**，原点在页面左上角。

选择归一化的原因：不同来源的 DPI 与像素尺寸差异大，归一化后下游裁剪、高亮、并与页宽无关地比较位置。`page.width` / `page.height` 保留原始像素尺寸，供回切原图使用。

## 3. 溯源

一段文本要能被引用，至少需要三样东西：文档、页码、位置。

- `source.uri` + `source.sha256` 固定版本：同名文件内容变了要能被发现。
- `block.block_id` 在文档内唯一且稳定，用于 `diligram-rag` 输出证据引用。
- `block.bbox` + `page.page_no` 用于回指原文与高亮。
- `pipeline.*` 记录产出这条结果的模型与版本；`confidence` 为引擎自报置信度，**不可直接当作准确率使用**。

## 4. 字段说明要点

| 字段 | 约定 |
|---|---|
| `block.type` | `seal` / `stamp` / `signature` 是**检出标记**，不表示已验证真伪 |
| `block.order` | 页面内阅读顺序，从 0 连续递增；跨栏版面由版面分析负责排序 |
| `block.text` | 已做基本清洗与断行合并的**纯文本**，不保留排版标记 |
| `block.latex` | 仅 `type=formula` 使用 |
| `block.table` | 表格结构由 `cells` 表达；`rows`/`cols` 为网格规模，单元格可用 `row_span`/`col_span` 合并且 `cells` 允许不满格 |
| `fields` | 文档级 key/value，用于证件、票据等定向抽取；`page_no` + `bbox` 指回原文 |

## 5. 消费方可以依赖什么

`diligram-rag` 允许依赖以下不变量：

1. `pages` 按 `page_no` 升序且从 1 开始。
2. 每个 `block` 都有 `block_id`、`type`、`order`。
3. `bbox` 四元组合法且落在 0–1 内（缺失表示引擎未给出定位，消费方需容忍）。
4. `sha256` 为 64 位小写十六进制。

其余字段一律视为可选，消费方不得假设存在。
