# BoxOffice
BoxOffice 是一款适用于 chatgpt-on-wechat 项目的电影票房查询插件，支持实时查询全网电影票房数据。

## 一. 主要功能
1. 实时票房：查询当日实时票房排行
2. 支持文字和图片两种展示方式

## 二. 安装必需环境
1. 安装 playwright：`pip install playwright`
2. 安装 chromium：`playwright install chromium`

## 三. 安装配置
1. 安装插件：`#installp https://github.com/[YourUsername]/BoxOffice.git`
2. 重启项目并扫描插件：`#scanp`

## 四. 使用指令
- 发送"票房"：获取当日实时票房排行榜

## 五. 自定义
- 修改 templates/boxoffice_template.html 可自定义图表样式
- 支持自定义排行榜显示数量 