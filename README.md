# 迷你空管Cute Mod管理器 - Mod管理页面

## 简介

这是一个用于管理[迷你空管](https://store.steampowered.com/app/2289650/_Mini_Airways/)Mod的网页应用，它允许用户查看和管理已安装的Mod。

目前仅适用于Windows

## 功能

- 查看已安装的Mod列表
- 查看Mod的详细信息，包括名称、版本、作者、描述等
- 无需安装
- 兼容已有的Mod管理器

## 使用

下载releases最新版exe。双击后会自动打开浏览器页面，选择你的游戏文件夹位置后即可使用。

## 开发

1.   确认你有Python 3.10及更新版本（略低的版本也可以通过手动修改代码来支持）
2.   `git clone`本仓库
3.   执行`cd MiniAirwaysCuteModManager`
4.   使用`pip install -r requirements.txt`安装依赖
5.   Just do it!
6.   执行`python build.py`手动生成安装包（在`dist`目录中）

## 开源协议

GPLv3，详见`LICENSE`文件