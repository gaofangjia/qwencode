# 小学出题器 - 自动编译指南

## 📦 GitHub Actions 自动编译 Windows EXE

本项目已配置 GitHub Actions，可自动将 Python 程序编译为 Windows 可执行文件 (.exe)。

## 🚀 使用方法

### 方式一：自动触发（推荐）

1. **推送代码到主分支**
   ```bash
   git add .
   git commit -m "更新出题器功能"
   git push origin main
   ```

2. **创建标签发布版本**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

### 方式二：手动触发

1. 进入 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择左侧 **"Build Windows EXE"** 工作流
4. 点击 **"Run workflow"** 按钮
5. 选择分支后点击 **"Run workflow"**

## 📥 获取编译产物

### 从 Actions 下载（每次构建）

1. 进入 **Actions** 标签
2. 点击最近完成的工作流运行记录
3. 在页面底部找到 **"Artifacts"** 区域
4. 点击 **`primary-education-app-windows`** 下载
5. 解压后得到 `小学出题器.exe`

### 从 Releases 下载（仅标签构建）

1. 进入仓库 **Releases** 页面
2. 找到对应版本的发布
3. 下载附件中的 `小学出题器.exe`

## ⚙️ 编译配置说明

### 触发条件
- ✅ 推送到 `main` 或 `master` 分支
- ✅ 创建 Pull Request 到主分支
- ✅ 手动触发 (workflow_dispatch)
- ✅ 创建版本号标签 (如 v1.0.0)

### 监控的文件
- `primary_education_app.py` - 主程序
- `requirements.txt` - 依赖列表
- `.github/workflows/*.yml` - 工作流配置

### 编译环境
- **操作系统**: Windows Server 最新版 (windows-latest)
- **Python 版本**: 3.11
- **打包工具**: PyInstaller
- **输出类型**: 单文件 EXE (--onefile)
- **界面模式**: 无控制台窗口 (--windowed)

## 📋 输出产物

| 属性 | 说明 |
|------|------|
| 文件名 | `小学出题器.exe` |
| 类型 | 独立可执行文件 |
| 大小 | 约 30-50 MB (包含 Python 运行时) |
| 依赖 | 无需安装 Python，双击即可运行 |
| 兼容性 | Windows 7/8/10/11 (64位) |

## 🔧 自定义配置

### 修改应用图标

1. 准备 `.ico` 格式图标文件
2. 上传到仓库根目录，命名为 `app.ico`
3. 修改 `build-windows.yml`:
   ```yaml
   --icon=app.ico `
   ```

### 添加额外依赖

编辑 `requirements.txt`:
```txt
pillow>=10.0.0
numpy>=1.24.0
# 添加其他依赖...
```

### 更改输出名称

修改 `build-windows.yml` 中的 `--name` 参数:
```yaml
--name "我的出题器" `
```

## ⚠️ 注意事项

1. **首次运行慢**: 第一次编译可能需要 5-10 分钟
2. **文件大小**: 单文件 EXE 包含完整 Python 环境，体积较大
3. **杀毒软件**: 某些杀毒软件可能误报，需添加信任
4. **系统要求**: 需要 Windows 7 SP1 或更高版本
5. **存储限制**: Artifact 保留 30 天，请及时下载

## 🐛 故障排查

### 构建失败常见原因

| 问题 | 解决方案 |
|------|----------|
| 找不到源文件 | 确认 `primary_education_app.py` 在根目录 |
| 依赖安装失败 | 检查 `requirements.txt` 格式 |
| 内存不足 | PyInstaller 需要较多内存，通常会自动解决 |
| 路径含中文 | PyInstaller 对中文路径支持良好 |

### 查看构建日志

1. 进入 Actions 页面
2. 点击失败的构建记录
3. 展开各步骤查看详细错误信息

## 📞 技术支持

如有问题，请在 GitHub Issues 中提交：
- 构建日志截图
- 错误信息
- 复现步骤

---

**享受您的小学出题器！** 🎓✨
