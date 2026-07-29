# Task 3 修复报告

## 状态
修复完成。`_unit_scan` 遇到含行内链接/图片的普通正文时，先保留正文单元，再追加 asset 单元；纯链接/图片行仅产生 asset 单元。URL 序列比较保持不变，列表、表格、admonition 等既有分类优先级保持不变。

## 回归覆盖
新增最小 fixture：源为“必须保留的说明，[参考链接](https://example.com)”，目标仅含 `[参考链接](https://example.com)`。验证结果包含 `P0-SOURCE-COVERAGE`。

## 测试
`python3 -m unittest tests/test_verify_translation.py -v`

结果：6 个测试中 4 个通过，2 个既有测试失败：
- `test_halfwidth_punctuation_warns_and_strict_fails`
- `test_unlabelled_expansion_is_p1`

两项分别依赖当前分支尚未实现的 P2/P1 行为；本任务未提前实现 P1/P2/metrics。
