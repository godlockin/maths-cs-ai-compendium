# Task 1 修复报告

- 修复 `zh/TRANSLATION_GUIDE.md` F4、§7 自检、§13 规则：标题与列表结构比较明确排除 F12 认可学习增强块；增强块之外原文信息单元按顺序一一对应；移除“增强块不是 F4/F6 例外”的矛盾表述，并同步 reviewer 条目。
- 新增最小 `tests/__init__.py`，保持 unittest discover 可用。
- 未修改原文或现有中文正文。

验证：
- `python3 -m unittest tests/test_translation_policy.py -v`：通过（1 test）。
- `python3 -m unittest discover -v`：通过（1 test）。
