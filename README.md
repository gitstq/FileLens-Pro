<div align="center">

# 🔍 FileLens

**Local Intelligent File Search Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Electron](https://img.shields.io/badge/Electron-47848F.svg?logo=electron&logoColor=white)](https://www.electronjs.org/)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

## English

### 🎉 Introduction

**FileLens** is a powerful local file search tool that brings intelligent semantic search capabilities to your documents. Unlike traditional keyword-based search tools, FileLens uses advanced vector embeddings to understand the meaning behind your queries, delivering more accurate and relevant results.

**Key Differentiators:**
- 🔒 **100% Local** - All data stays on your machine, ensuring complete privacy
- 🧠 **Semantic Search** - Understands context and meaning, not just keywords
- 📄 **Multi-Format Support** - PDF, Word, Excel, PowerPoint, Markdown, and code files
- ⚡ **Lightning Fast** - Vector-based search delivers results in milliseconds
- 🖥️ **Beautiful UI** - Modern Electron-based desktop application

### ✨ Features

- **🔍 Hybrid Search Mode** - Combines keyword and semantic search for best results
- **📁 Multi-Format Support** - Index and search PDF, DOCX, XLSX, PPTX, MD, TXT, and 30+ code formats
- **🧠 AI-Powered** - Uses state-of-the-art sentence transformers for embeddings
- **💾 Local Vector Database** - ChromaDB for efficient similarity search
- **⚡ Real-time Indexing** - Watch folders and auto-index new files
- **🎯 Relevance Scoring** - Results ranked by semantic similarity
- **🔒 Privacy First** - No data leaves your computer

### 🚀 Quick Start

#### Prerequisites
- Python 3.8+
- Node.js 18+
- 4GB+ RAM (8GB recommended for large document collections)

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/FileLens-Pro.git
cd FileLens-Pro

# Run setup script
# Linux/macOS:
chmod +x scripts/setup.sh && ./scripts/setup.sh

# Windows:
scripts\setup.bat
```

#### Start the Application

```bash
# Terminal 1: Start backend
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
python src/main.py

# Terminal 2: Start frontend
npm start
```

### 📖 Usage Guide

#### 1. Index Your Files

1. Open the app and navigate to "Index Management"
2. Click "Add Folder" and select directories to index
3. FileLens will automatically scan and index all supported files

#### 2. Search

1. Go to the "Search" tab
2. Enter your query (natural language works best!)
3. Choose search mode:
   - **Hybrid** (recommended) - Best of both worlds
   - **Semantic** - Concept-based search
   - **Keyword** - Traditional text matching

#### 3. View Results

- Click on any result to preview
- "Open" button opens the file with default application
- "Show in Folder" reveals file location

### 💡 Design Philosophy

FileLens was designed with three core principles:

1. **Privacy First** - Your documents never leave your machine
2. **Simplicity** - Powerful features with an intuitive interface
3. **Performance** - Fast search even with thousands of documents

### 📦 Building from Source

```bash
# Build for current platform
python scripts/build.py

# Output will be in dist/ directory
```

### 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 简体中文

### 🎉 项目介绍

**FileLens** 是一款强大的本地智能文件搜索工具，为您的文档提供语义搜索能力。与传统基于关键词的搜索工具不同，FileLens 使用先进的向量嵌入技术来理解查询背后的含义，提供更准确、更相关的结果。

**核心亮点：**
- 🔒 **100% 本地运行** - 所有数据保留在您的机器上，确保完全隐私
- 🧠 **语义搜索** - 理解上下文和含义，而不仅仅是关键词
- 📄 **多格式支持** - PDF、Word、Excel、PowerPoint、Markdown 和代码文件
- ⚡ **极速搜索** - 基于向量的搜索在毫秒内返回结果
- 🖥️ **精美界面** - 基于 Electron 的现代化桌面应用

### ✨ 核心特性

- **🔍 混合搜索模式** - 结合关键词和语义搜索，获得最佳结果
- **📁 多格式支持** - 索引和搜索 PDF、DOCX、XLSX、PPTX、MD、TXT 及 30+ 种代码格式
- **🧠 AI 驱动** - 使用最先进的句子转换器生成嵌入向量
- **💾 本地向量数据库** - 使用 ChromaDB 进行高效的相似度搜索
- **⚡ 实时索引** - 监控文件夹并自动索引新文件
- **🎯 相关性评分** - 按语义相似度对结果进行排序
- **🔒 隐私优先** - 数据不会离开您的计算机

### 🚀 快速开始

#### 环境要求
- Python 3.8+
- Node.js 18+
- 4GB+ 内存（大型文档集合建议 8GB）

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/FileLens-Pro.git
cd FileLens-Pro

# 运行安装脚本
# Linux/macOS:
chmod +x scripts/setup.sh && ./scripts/setup.sh

# Windows:
scripts\setup.bat
```

#### 启动应用

```bash
# 终端 1：启动后端
source venv/bin/activate  # Windows 使用：venv\Scripts\activate
python src/main.py

# 终端 2：启动前端
npm start
```

### 📖 使用指南

#### 1. 索引文件

1. 打开应用并导航到"索引管理"
2. 点击"添加文件夹"并选择要索引的目录
3. FileLens 将自动扫描并索引所有支持的文件

#### 2. 搜索

1. 进入"搜索"标签页
2. 输入查询（自然语言效果最好！）
3. 选择搜索模式：
   - **混合**（推荐）- 兼顾两者优势
   - **语义** - 基于概念的搜索
   - **关键词** - 传统文本匹配

#### 3. 查看结果

- 点击任意结果进行预览
- "打开"按钮使用默认应用打开文件
- "在文件夹中显示" 显示文件位置

### 💡 设计理念

FileLens 遵循三个核心原则设计：

1. **隐私优先** - 您的文档永远不会离开您的机器
2. **简洁易用** - 强大功能与直观界面相结合
3. **高性能** - 即使处理数千个文档也能快速搜索

### 📦 从源码构建

```bash
# 为当前平台构建
python scripts/build.py

# 输出将在 dist/ 目录中
```

### 🤝 贡献指南

我们欢迎贡献！详情请参阅我们的 [贡献指南](CONTRIBUTING.md)。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 协议 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

## 繁體中文

### 🎉 專案介紹

**FileLens** 是一款強大的本地智能檔案搜尋工具，為您的文件提供語義搜尋能力。與傳統基於關鍵字的搜尋工具不同，FileLens 使用先進的向量嵌入技術來理解查詢背後的含義，提供更準確、更相關的結果。

**核心亮點：**
- 🔒 **100% 本地運行** - 所有數據保留在您的機器上，確保完全隱私
- 🧠 **語義搜尋** - 理解上下文和含義，而不僅僅是關鍵字
- 📄 **多格式支援** - PDF、Word、Excel、PowerPoint、Markdown 和程式碼文件
- ⚡ **極速搜尋** - 基於向量的搜尋在毫秒內返回結果
- 🖥️ **精美介面** - 基於 Electron 的現代化桌面應用

### ✨ 核心特性

- **🔍 混合搜尋模式** - 結合關鍵字和語義搜尋，獲得最佳結果
- **📁 多格式支援** - 索引和搜尋 PDF、DOCX、XLSX、PPTX、MD、TXT 及 30+ 種程式碼格式
- **🧠 AI 驅動** - 使用最先進的句子轉換器生成嵌入向量
- **💾 本地向量資料庫** - 使用 ChromaDB 進行高效的相似度搜尋
- **⚡ 即時索引** - 監控資料夾並自動索引新檔案
- **🎯 相關性評分** - 按語義相似度對結果進行排序
- **🔒 隱私優先** - 數據不會離開您的電腦

### 🚀 快速開始

#### 環境要求
- Python 3.8+
- Node.js 18+
- 4GB+ 記憶體（大型文件集合建議 8GB）

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/FileLens-Pro.git
cd FileLens-Pro

# 執行安裝腳本
# Linux/macOS:
chmod +x scripts/setup.sh && ./scripts/setup.sh

# Windows:
scripts\setup.bat
```

#### 啟動應用

```bash
# 終端機 1：啟動後端
source venv/bin/activate  # Windows 使用：venv\Scripts\activate
python src/main.py

# 終端機 2：啟動前端
npm start
```

### 📖 使用指南

#### 1. 索引檔案

1. 開啟應用並導航到"索引管理"
2. 點擊"添加資料夾"並選擇要索引的目錄
3. FileLens 將自動掃描並索引所有支援的檔案

#### 2. 搜尋

1. 進入"搜尋"標籤頁
2. 輸入查詢（自然語言效果最好！）
3. 選擇搜尋模式：
   - **混合**（推薦）- 兼顧兩者優勢
   - **語義** - 基於概念的搜尋
   - **關鍵字** - 傳統文字匹配

#### 3. 查看結果

- 點擊任意結果進行預覽
- "開啟"按鈕使用預設應用開啟檔案
- "在資料夾中顯示" 顯示檔案位置

### 💡 設計理念

FileLens 遵循三個核心原則設計：

1. **隱私優先** - 您的文件永遠不會離開您的機器
2. **簡潔易用** - 強大功能與直觀介面相結合
3. **高效能** - 即使處理數千個文件也能快速搜尋

### 📦 從原始碼構建

```bash
# 為當前平台構建
python scripts/build.py

# 輸出將在 dist/ 目錄中
```

### 🤝 貢獻指南

我們歡迎貢獻！詳情請參閱我們的 [貢獻指南](CONTRIBUTING.md)。

1. Fork 本倉庫
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 📄 開源協議

本專案採用 MIT 協議 - 詳情請參閱 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by the FileLens Team**

[Report Bug](https://github.com/gitstq/FileLens-Pro/issues) · [Request Feature](https://github.com/gitstq/FileLens-Pro/issues)

</div>
