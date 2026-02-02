# 公共数据集说明

本目录包含用于增强酒店预订数据分析的公共数据集。

## 数据文件列表

### 1. cpi_data.csv
**来源**: [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/series/CPIAUCSL)

**描述**: 美国消费者价格指数（CPI），用于衡量通货膨胀水平。

**时间范围**: 2015-2017年

**变量**:
- `Date`: 日期
- `CPI`: 消费者价格指数值

**用途**: 评估酒店ADR变化是否与通货膨胀相关，为定价策略提供宏观经济背景。

### 2. portugal_tourism.csv
**来源**: [葡萄牙国家统计局 (INE)](https://www.ine.pt/)

**描述**: 葡萄牙旅游业季度统计数据。

**时间范围**: 2015-2017年（按季度）

**变量**:
- `Year`: 年份
- `Quarter`: 季度
- `Arrivals_Thousands`: 游客到达人数（千人）
- `Nights_Thousands`: 住宿晚数（千晚）
- `Revenue_Million_EUR`: 旅游收入（百万欧元）

**用途**: 验证酒店预订趋势是否符合葡萄牙整体旅游市场趋势。

### 3. europe_tourism.csv
**来源**: [Eurostat](https://ec.europa.eu/eurostat/)

**描述**: 欧洲旅游业年度统计数据。

**时间范围**: 2015-2017年

**变量**:
- `Year`: 年份
- `Total_Arrivals_Million`: 总到达人数（百万）
- `Growth_Rate_Percent`: 增长率（%）
- `Average_Nights`: 平均住宿晚数
- `Tourism_Revenue_Billion_EUR`: 旅游收入（十亿欧元）

**用途**: 提供欧洲旅游业整体背景，用于基准比较。

### 4. seasonal_index.csv
**来源**: 基于行业标准季节性模式

**描述**: 旅游业月度季节性指数。

**变量**:
- `Month`: 月份
- `Seasonal_Index`: 季节性指数（1.0为平均水平）
- `Description`: 季节描述

**用途**: 帮助理解和预测不同月份的预订模式。

## 数据整合价值

这些公共数据集与酒店预订数据结合使用，可以：

1. **宏观经济分析**: 通过CPI数据评估价格变化的合理性
2. **行业基准**: 对比酒店表现与整体市场趋势
3. **季节性验证**: 确认观察到的季节性模式是否符合行业规律
4. **预测建模**: 为未来预订和收入预测提供外部变量
5. **战略决策**: 为营销和定价策略提供数据支持

## 数据使用示例

```python
import pandas as pd

# 读取公共数据
cpi = pd.read_csv('public_data/cpi_data.csv')
portugal = pd.read_csv('public_data/portugal_tourism.csv')
europe = pd.read_csv('public_data/europe_tourism.csv')
seasonal = pd.read_csv('public_data/seasonal_index.csv')

# 与酒店数据合并分析
# ...
```
