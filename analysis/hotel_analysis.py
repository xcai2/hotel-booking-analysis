#!/usr/bin/env python3
"""
酒店预订数据深度分析和可视化
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体和样式
rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')

# 读取数据
print("正在读取数据...")
df = pd.read_csv('/home/ubuntu/upload/hotel_bookings.csv')

# 数据清洗
print("正在清洗数据...")
# 处理children列的缺失值
df['children'].fillna(0, inplace=True)

# 创建总住宿晚数列
df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

# 创建总客人数列
df['total_guests'] = df['adults'] + df['children'] + df['babies']

# 过滤异常值（ADR为负数或过大的值）
df = df[df['adr'] >= 0]
df = df[df['adr'] < 1000]  # 过滤异常高价

# 创建年-月列便于时间序列分析
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
df['month_num'] = df['arrival_date_month'].map({m: i+1 for i, m in enumerate(month_order)})
df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + 
                                     df['month_num'].astype(str).str.zfill(2) + '-01')

print(f"清洗后数据形状: {df.shape}")

# ============= 1. 取消率分析 =============
print("\n=== 1. 取消率分析 ===")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1.1 按酒店类型的取消率
cancel_by_hotel = df.groupby('hotel')['is_canceled'].mean()
axes[0, 0].bar(cancel_by_hotel.index, cancel_by_hotel.values, color=['#3498db', '#e74c3c'])
axes[0, 0].set_title('不同酒店类型的取消率', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('取消率', fontsize=12)
axes[0, 0].set_ylim(0, 0.5)
for i, v in enumerate(cancel_by_hotel.values):
    axes[0, 0].text(i, v + 0.01, f'{v:.2%}', ha='center', fontsize=11)

# 1.2 按提前预订时间的取消率
df['lead_time_group'] = pd.cut(df['lead_time'], 
                                bins=[0, 7, 30, 90, 180, 365, 1000],
                                labels=['0-7天', '8-30天', '31-90天', '91-180天', '181-365天', '365天以上'])
cancel_by_leadtime = df.groupby('lead_time_group')['is_canceled'].mean()
axes[0, 1].plot(range(len(cancel_by_leadtime)), cancel_by_leadtime.values, 
                marker='o', linewidth=2, markersize=8, color='#e74c3c')
axes[0, 1].set_xticks(range(len(cancel_by_leadtime)))
axes[0, 1].set_xticklabels(cancel_by_leadtime.index, rotation=45, ha='right')
axes[0, 1].set_title('提前预订时间与取消率关系', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('取消率', fontsize=12)
axes[0, 1].grid(True, alpha=0.3)

# 1.3 按押金类型的取消率
cancel_by_deposit = df.groupby('deposit_type')['is_canceled'].mean().sort_values(ascending=False)
axes[1, 0].barh(cancel_by_deposit.index, cancel_by_deposit.values, color='#9b59b6')
axes[1, 0].set_title('押金类型与取消率关系', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('取消率', fontsize=12)
for i, v in enumerate(cancel_by_deposit.values):
    axes[1, 0].text(v + 0.01, i, f'{v:.2%}', va='center', fontsize=11)

# 1.4 按客户类型的取消率
cancel_by_customer = df.groupby('customer_type')['is_canceled'].mean().sort_values(ascending=False)
axes[1, 1].bar(range(len(cancel_by_customer)), cancel_by_customer.values, color='#f39c12')
axes[1, 1].set_xticks(range(len(cancel_by_customer)))
axes[1, 1].set_xticklabels(cancel_by_customer.index, rotation=45, ha='right')
axes[1, 1].set_title('客户类型与取消率关系', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('取消率', fontsize=12)
for i, v in enumerate(cancel_by_customer.values):
    axes[1, 1].text(i, v + 0.01, f'{v:.2%}', ha='center', fontsize=11)

plt.tight_layout()
plt.savefig('/home/ubuntu/cancellation_analysis.png', dpi=300, bbox_inches='tight')
print("取消率分析图已保存: cancellation_analysis.png")
plt.close()

# ============= 2. 收入分析 (ADR) =============
print("\n=== 2. 收入分析 (ADR) ===")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 2.1 按月份的平均ADR趋势
monthly_adr = df.groupby('arrival_date_month')['adr'].mean()
monthly_adr = monthly_adr.reindex(month_order)
axes[0, 0].plot(range(12), monthly_adr.values, marker='o', linewidth=2, 
                markersize=8, color='#27ae60')
axes[0, 0].set_xticks(range(12))
axes[0, 0].set_xticklabels([m[:3] for m in month_order], rotation=45)
axes[0, 0].set_title('月度平均房价(ADR)趋势', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('平均ADR ($)', fontsize=12)
axes[0, 0].grid(True, alpha=0.3)

# 2.2 按酒店类型和客户类型的ADR
adr_hotel_customer = df.groupby(['hotel', 'customer_type'])['adr'].mean().unstack()
adr_hotel_customer.plot(kind='bar', ax=axes[0, 1], width=0.8)
axes[0, 1].set_title('不同酒店和客户类型的平均房价', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('平均ADR ($)', fontsize=12)
axes[0, 1].set_xlabel('')
axes[0, 1].legend(title='客户类型', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[0, 1].tick_params(axis='x', rotation=0)

# 2.3 按市场细分的ADR
adr_by_segment = df.groupby('market_segment')['adr'].mean().sort_values(ascending=False)
axes[1, 0].barh(adr_by_segment.index, adr_by_segment.values, color='#16a085')
axes[1, 0].set_title('市场细分的平均房价', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('平均ADR ($)', fontsize=12)
for i, v in enumerate(adr_by_segment.values):
    axes[1, 0].text(v + 2, i, f'${v:.2f}', va='center', fontsize=10)

# 2.4 ADR分布（未取消的预订）
not_canceled = df[df['is_canceled'] == 0]
axes[1, 1].hist(not_canceled['adr'], bins=50, color='#3498db', alpha=0.7, edgecolor='black')
axes[1, 1].axvline(not_canceled['adr'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'平均值: ${not_canceled["adr"].mean():.2f}')
axes[1, 1].axvline(not_canceled['adr'].median(), color='green', linestyle='--', 
                   linewidth=2, label=f'中位数: ${not_canceled["adr"].median():.2f}')
axes[1, 1].set_title('ADR分布（未取消预订）', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('ADR ($)', fontsize=12)
axes[1, 1].set_ylabel('频数', fontsize=12)
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('/home/ubuntu/revenue_analysis.png', dpi=300, bbox_inches='tight')
print("收入分析图已保存: revenue_analysis.png")
plt.close()

# ============= 3. 预订模式分析 =============
print("\n=== 3. 预订模式分析 ===")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 3.1 时间序列：月度预订量
monthly_bookings = df.groupby('arrival_date').size()
axes[0, 0].plot(monthly_bookings.index, monthly_bookings.values, linewidth=2, color='#e74c3c')
axes[0, 0].set_title('月度预订量趋势', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('预订数量', fontsize=12)
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, alpha=0.3)

# 3.2 提前预订时间分布
axes[0, 1].hist(df['lead_time'], bins=50, color='#9b59b6', alpha=0.7, edgecolor='black')
axes[0, 1].axvline(df['lead_time'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'平均值: {df["lead_time"].mean():.1f}天')
axes[0, 1].axvline(df['lead_time'].median(), color='green', linestyle='--', 
                   linewidth=2, label=f'中位数: {df["lead_time"].median():.1f}天')
axes[0, 1].set_title('提前预订时间分布', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('提前天数', fontsize=12)
axes[0, 1].set_ylabel('频数', fontsize=12)
axes[0, 1].legend()
axes[0, 1].set_xlim(0, 400)

# 3.3 住宿晚数分布
axes[1, 0].hist(df[df['total_nights'] <= 14]['total_nights'], 
                bins=14, color='#f39c12', alpha=0.7, edgecolor='black')
axes[1, 0].set_title('住宿晚数分布（≤14晚）', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('住宿晚数', fontsize=12)
axes[1, 0].set_ylabel('频数', fontsize=12)

# 3.4 回头客vs新客户的比较
repeat_stats = df.groupby('is_repeated_guest').agg({
    'is_canceled': 'mean',
    'adr': 'mean',
    'total_nights': 'mean'
}).round(2)
repeat_stats.index = ['新客户', '回头客']

x = np.arange(len(repeat_stats.columns))
width = 0.35
colors = ['#3498db', '#e74c3c']

for i, idx in enumerate(repeat_stats.index):
    values_normalized = repeat_stats.loc[idx] / repeat_stats.max() * 100
    axes[1, 1].bar(x + i*width, values_normalized, width, label=idx, color=colors[i])

axes[1, 1].set_title('回头客 vs 新客户对比（标准化）', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('标准化值 (最大值=100)', fontsize=12)
axes[1, 1].set_xticks(x + width / 2)
axes[1, 1].set_xticklabels(['取消率', '平均ADR', '平均住宿晚数'], rotation=0)
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('/home/ubuntu/booking_patterns.png', dpi=300, bbox_inches='tight')
print("预订模式分析图已保存: booking_patterns.png")
plt.close()

# ============= 4. 客户来源分析 =============
print("\n=== 4. 客户来源分析 ===")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 4.1 前15个客户来源国
top_countries = df['country'].value_counts().head(15)
axes[0, 0].barh(range(len(top_countries)), top_countries.values, color='#1abc9c')
axes[0, 0].set_yticks(range(len(top_countries)))
axes[0, 0].set_yticklabels(top_countries.index)
axes[0, 0].set_title('前15个客户来源国', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('预订数量', fontsize=12)
axes[0, 0].invert_yaxis()

# 4.2 分销渠道分布
channel_dist = df['distribution_channel'].value_counts()
colors_pie = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#2ecc71']
axes[0, 1].pie(channel_dist.values, labels=channel_dist.index, autopct='%1.1f%%',
               colors=colors_pie, startangle=90)
axes[0, 1].set_title('分销渠道分布', fontsize=14, fontweight='bold')

# 4.3 市场细分分布
segment_dist = df['market_segment'].value_counts()
axes[1, 0].bar(range(len(segment_dist)), segment_dist.values, color='#34495e')
axes[1, 0].set_xticks(range(len(segment_dist)))
axes[1, 0].set_xticklabels(segment_dist.index, rotation=45, ha='right')
axes[1, 0].set_title('市场细分分布', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('预订数量', fontsize=12)

# 4.4 餐食类型分布
meal_dist = df['meal'].value_counts()
axes[1, 1].bar(range(len(meal_dist)), meal_dist.values, color='#e67e22')
axes[1, 1].set_xticks(range(len(meal_dist)))
axes[1, 1].set_xticklabels(meal_dist.index, rotation=0)
axes[1, 1].set_title('餐食类型分布', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('预订数量', fontsize=12)

plt.tight_layout()
plt.savefig('/home/ubuntu/customer_source_analysis.png', dpi=300, bbox_inches='tight')
print("客户来源分析图已保存: customer_source_analysis.png")
plt.close()

# ============= 5. 生成关键统计表格 =============
print("\n=== 5. 生成统计表格 ===")

# 5.1 按酒店类型的关键指标
hotel_stats = df.groupby('hotel').agg({
    'is_canceled': ['count', 'mean'],
    'adr': 'mean',
    'lead_time': 'mean',
    'total_nights': 'mean',
    'is_repeated_guest': 'mean'
}).round(2)
hotel_stats.columns = ['预订总数', '取消率', '平均ADR', '平均提前天数', '平均住宿晚数', '回头客比例']
hotel_stats.to_csv('/home/ubuntu/hotel_type_stats.csv', encoding='utf-8-sig')
print("酒店类型统计表已保存: hotel_type_stats.csv")

# 5.2 按月份的关键指标
monthly_stats = df.groupby('arrival_date_month').agg({
    'is_canceled': ['count', 'mean'],
    'adr': 'mean',
    'lead_time': 'mean'
}).round(2)
monthly_stats.columns = ['预订数量', '取消率', '平均ADR', '平均提前天数']
monthly_stats = monthly_stats.reindex(month_order)
monthly_stats.to_csv('/home/ubuntu/monthly_stats.csv', encoding='utf-8-sig')
print("月度统计表已保存: monthly_stats.csv")

# 5.3 按市场细分的关键指标
segment_stats = df.groupby('market_segment').agg({
    'is_canceled': ['count', 'mean'],
    'adr': 'mean',
    'lead_time': 'mean',
    'total_nights': 'mean'
}).round(2)
segment_stats.columns = ['预订数量', '取消率', '平均ADR', '平均提前天数', '平均住宿晚数']
segment_stats = segment_stats.sort_values('预订数量', ascending=False)
segment_stats.to_csv('/home/ubuntu/market_segment_stats.csv', encoding='utf-8-sig')
print("市场细分统计表已保存: market_segment_stats.csv")

print("\n所有分析和可视化完成！")

# ============= 6. 公共数据整合分析 =============
print("\n=== 6. 公共数据整合分析 ===")

# 读取公共数据
print("正在读取公共数据...")
cpi_df = pd.read_csv('/home/ubuntu/public_data/cpi_data.csv')
portugal_df = pd.read_csv('/home/ubuntu/public_data/portugal_tourism.csv')
seasonal_df = pd.read_csv('/home/ubuntu/public_data/seasonal_index.csv')

# 数据预处理
cpi_df['Date'] = pd.to_datetime(cpi_df['Date'])
cpi_df.set_index('Date', inplace=True)

# 6.1 ADR vs CPI
print("正在生成 ADR vs CPI 对比图...")
monthly_adr_ts = df.groupby('arrival_date')['adr'].mean()

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(monthly_adr_ts.index, monthly_adr_ts.values, color='#3498db', marker='o', linestyle='-', label='酒店平均ADR')
ax1.set_xlabel('日期', fontsize=12)
ax1.set_ylabel('平均ADR ($)', color='#3498db', fontsize=12)
ax1.tick_params(axis='y', labelcolor='#3498db')
ax1.set_title('酒店ADR与消费者价格指数(CPI)对比', fontsize=16, fontweight='bold')
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

ax2 = ax1.twinx()
ax2.plot(cpi_df.index, cpi_df['CPI'], color='#e74c3c', marker='s', linestyle='--', label='CPI指数')
ax2.set_ylabel('CPI指数', color='#e74c3c', fontsize=12)
ax2.tick_params(axis='y', labelcolor='#e74c3c')

fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()
plt.savefig('/home/ubuntu/adr_vs_cpi.png', dpi=300, bbox_inches='tight')
print("ADR vs CPI 对比图已保存: adr_vs_cpi.png")
plt.close()

# 6.2 预订量 vs 季节性指数
print("正在生成 预订量 vs 季节性指数 对比图...")
monthly_bookings_agg = df.groupby('arrival_date_month').size()
monthly_bookings_agg = monthly_bookings_agg.reindex(month_order)

seasonal_df.set_index('Month', inplace=True)
seasonal_index_ordered = seasonal_df.reindex(month_order)

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(monthly_bookings_agg.index, monthly_bookings_agg.values, color='#2ecc71', alpha=0.7, label='月度预订量')
ax1.set_xlabel('月份', fontsize=12)
ax1.set_ylabel('预订数量', color='#2ecc71', fontsize=12)
ax1.tick_params(axis='y', labelcolor='#2ecc71')
ax1.set_title('月度预订量与旅游季节性指数对比', fontsize=16, fontweight='bold')
ax1.set_xticklabels(monthly_bookings_agg.index, rotation=45, ha='right')

ax2 = ax1.twinx()
ax2.plot(seasonal_index_ordered.index, seasonal_index_ordered['Seasonal_Index'], color='#f39c12', marker='o', linestyle='--', linewidth=2, label='季节性指数')
ax2.set_ylabel('季节性指数', color='#f39c12', fontsize=12)
ax2.tick_params(axis='y', labelcolor='#f39c12')
ax2.set_ylim(0, 1.5)

fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()
plt.savefig('/home/ubuntu/bookings_vs_seasonal_index.png', dpi=300, bbox_inches='tight')
print("预订量 vs 季节性指数 对比图已保存: bookings_vs_seasonal_index.png")
plt.close()

print("\n公共数据整合分析完成！")
