# GitHub Pages 配置说明

此项目使用 GitHub Actions 自动构建和部署 Hexo 博客到 GitHub Pages。

## 配置步骤

### 1. 启用GitHub Pages

1. 在GitHub上打开仓库 → 进入 **Settings** 
2. 左侧菜单选择 **Pages**
3. 在 "Source" 下，选择：
   - **Deploy from a branch**
   - Branch: **gh-pages**
   - Folder: **/root**
4. 点击 **Save**

### 2. 检查工作流

- 每次推送到 `master` 分支时，GitHub Actions会自动：
  1. 安装依赖（npm install）
  2. 构建博客（npm run build）
  3. 部署到 `gh-pages` 分支

### 3. 查看部署状态

- 在仓库主页点击 **Actions** 标签
- 查看最新的 "Deploy Hexo Blog" 工作流状态

### 4. 访问博客

部署成功后，访问：
```
https://kaicmf.github.io/yntc
```

## 常见问题

**Q: 工作流失败怎么办？**
A: 点击 Actions 中的失败任务，查看错误日志。通常是依赖问题。

**Q: 多久后能看到更新？**
A: 推送后3-5分钟内通常完成部署。

**Q: 如何修改博客配置？**
A: 编辑 `_config.yml` 并推送，自动触发重建。

---

**现在您可以：**
1. 推送此文件到GitHub
2. 在仓库Settings中启用Pages
3. 等待Action完成部署
4. 访问您的博客！
