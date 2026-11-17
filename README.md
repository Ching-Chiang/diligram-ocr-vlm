# diligram-ocr-vlm

面向文档与证件的解析仓库：把 PDF / 扫描件 / 证件图片，转成**结构化、可追溯**的中间表示（page → block → field），供下游检索与问答使用。

> 状态：**v0.1 骨架**。契约（schema）已确定，流水线实现尚未开始。

## 定位

| 项 | 说明 |
|---|---|
| 输入 | PDF、扫描图片、证件照、截图（可含表格、公式、印章、签名） |
| 输出 | 符合 [`schema/doc.schema.json`](schema/doc.schema.json) 的 JSON：页面 → 区块 → 文本/表格/公式，附件级字段抽取 |
| 关键要求 | 每个文本块带 bbox 与页码；每个结果带模型版本 —— 下游要能回指原文 |

## 在体系中的位置

```
原始文件 ──► diligram-ocr-vlm ──► doc.schema.json ──► diligram-rag ──► 证据链 + 答案
                (本仓库)              (契约)            (检索/问答)
```

本仓库是**契约的生产方**。`schema/doc.schema.json` 是唯一权威定义，消费方（`diligram-rag`）按版本号引用，不复制、不改写。schema 的任何不兼容改动都必须提升 `schema_version`。

**边界：**本仓库不做检索、不做问答、不建索引。凡是「给定问题找证据」的逻辑都归 `diligram-rag`。

## 目录

```
schema/doc.schema.json    权威契约（v0.1）
docs/interface.md         契约说明：字段语义、坐标系、版本策略
examples/sample.doc.json  一份合规样例，可直接跑测试
src/diligram_ocr_vlm/     流水线代码（当前为桩）
configs/                  模型与流水线配置示例
tests/                    契约一致性测试
```

## 快速开始

```bash
pip install -e ".[dev]"
pytest            # 校验 examples/ 下所有样例符合 schema
```

## 计划中的流水线

1. **版面分析** — 页面切块，给出 block type 与阅读顺序
2. **文本识别** — OCR 引擎负责文字；低质区域回退到 VLM
3. **结构化抽取** — 表格重建、公式转 LaTeX、证件 key/value 抽取
4. **追溯信息** — bbox、页码、置信度、模型版本写入 `pipeline` 与各 block

引擎选型参考见工作区中的《OCR与文档解析工具整理》，不在本仓库内固化。

## 不做的事

- 不做检索与问答（→ `diligram-rag`）
- 不做前端展示
- 不承诺单一模型覆盖所有版面；允许多引擎组合，但必须在 `pipeline` 中如实记录

## 许可

尚未选择许可证。公开仓库在无许可证时默认保留所有权利，确定后再补 `LICENSE`。
