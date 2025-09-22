# Python项目部署文档

## 部署概述
- 部署目标和范围
- 支持的部署环境
- 部署架构图
- 关键依赖服务

## 系统要求

### 硬件要求
- CPU: 最低/推荐配置
- 内存: 最低/推荐配置
- 存储: 磁盘空间要求
- 网络: 带宽要求

### 软件要求
- 操作系统: Linux/Windows/macOS版本
- Python版本: 3.x.x
- 数据库: MySQL/PostgreSQL/Redis等
- Web服务器: Nginx/Apache
- 其他中间件要求

## 环境准备

### 操作系统配置
```bash
# 系统更新
sudo apt update && sudo apt upgrade -y

# 安装必要的系统包
sudo apt install -y build-essential curl wget git
```

### Python环境安装
```bash
# 安装Python
sudo apt install python3 python3-pip python3-venv

# 验证安装
python3 --version
pip3 --version
```

### 依赖服务安装

#### 数据库安装
```bash
# MySQL安装示例
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### Redis安装
```bash
# Redis安装示例
sudo apt install redis-server
sudo systemctl enable redis-server
```

#### Nginx安装
```bash
# Nginx安装示例
sudo apt install nginx
sudo systemctl enable nginx
```

## 应用部署

### 代码部署

#### 1. 获取代码
```bash
# 克隆项目代码
git clone <repository-url> /opt/project-name
cd /opt/project-name

# 切换到指定版本
git checkout v1.0.0
```

#### 2. 虚拟环境配置
```bash
# 创建虚拟环境
python3 -m venv /opt/project-name/venv

# 激活虚拟环境
source /opt/project-name/venv/bin/activate

# 升级pip
pip install --upgrade pip
```

#### 3. 依赖包安装
```bash
# 安装生产环境依赖
pip install -r requirements.txt

# 安装额外的生产依赖（如果有）
pip install gunicorn supervisor
```

### 配置管理

#### 应用配置文件
```bash
# 复制配置模板
cp config/config.example.py config/config.py

# 编辑配置文件
vim config/config.py
```

#### 环境变量配置
```bash
# 创建环境变量文件
cat > /opt/project-name/.env << EOF
DATABASE_URL=mysql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
DEBUG=False
EOF
```

#### 数据库配置
```bash
# 数据库初始化
python manage.py migrate

# 创建超级用户（如适用）
python manage.py createsuperuser
```

### 静态文件处理
```bash
# 收集静态文件
python manage.py collectstatic --noinput

# 设置静态文件权限
chown -R www-data:www-data /opt/project-name/static/
```

## 服务配置

### Gunicorn配置

#### 创建Gunicorn配置文件
```python
# /opt/project-name/gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "www-data"
group = "www-data"
tmp_upload_dir = None
logfile = "/var/log/gunicorn/gunicorn.log"
loglevel = "info"
```

#### 创建systemd服务文件
```ini
# /etc/systemd/system/project-name.service
[Unit]
Description=Project Name Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/project-name
ExecStart=/opt/project-name/venv/bin/gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Nginx配置

#### 创建Nginx站点配置
```nginx
# /etc/nginx/sites-available/project-name
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /opt/project-name/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    location /media/ {
        alias /opt/project-name/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

#### 启用站点
```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/project-name /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载Nginx
sudo systemctl reload nginx
```

### SSL证书配置
```bash
# 使用Let's Encrypt获取SSL证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

## 启动服务

### 启动应用服务
```bash
# 重载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start project-name
sudo systemctl enable project-name

# 检查服务状态
sudo systemctl status project-name
```

### 启动Web服务器
```bash
# 启动Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 检查服务状态
sudo systemctl status nginx
```

## 监控和日志

### 日志配置
```bash
# 创建日志目录
sudo mkdir -p /var/log/project-name
sudo chown www-data:www-data /var/log/project-name

# 配置日志轮转
sudo cat > /etc/logrotate.d/project-name << EOF
/var/log/project-name/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
```

### 健康检查
```bash
# 创建健康检查脚本
cat > /opt/project-name/health_check.sh << EOF
#!/bin/bash
curl -f http://localhost:8000/health/ || exit 1
EOF

chmod +x /opt/project-name/health_check.sh
```

### 监控配置
- 应用性能监控
- 资源使用监控
- 错误日志监控
- 告警配置

## 备份策略

### 数据库备份
```bash
# MySQL备份脚本示例
#!/bin/bash
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u backup_user -p database_name > $BACKUP_DIR/backup_$DATE.sql
```

### 应用数据备份
```bash
# 媒体文件备份
rsync -av /opt/project-name/media/ /backup/media/

# 配置文件备份
tar -czf /backup/config/config_$DATE.tar.gz /opt/project-name/config/
```

## 更新部署

### 代码更新流程
```bash
# 1. 备份当前版本
cp -r /opt/project-name /backup/project-name-$(date +%Y%m%d)

# 2. 获取新版本代码
git pull origin main

# 3. 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 4. 数据库迁移
python manage.py migrate

# 5. 收集静态文件
python manage.py collectstatic --noinput

# 6. 重启服务
sudo systemctl restart project-name
```

### 回滚流程
```bash
# 1. 停止服务
sudo systemctl stop project-name

# 2. 恢复代码
rm -rf /opt/project-name
cp -r /backup/project-name-YYYYMMDD /opt/project-name

# 3. 恢复数据库（如需要）
mysql -u user -p database_name < /backup/mysql/backup_YYYYMMDD.sql

# 4. 重启服务
sudo systemctl start project-name
```

## 性能优化

### 应用优化
- 数据库连接池配置
- 缓存策略配置
- 静态文件CDN配置
- 代码性能优化

### 系统优化
- 内核参数调优
- 文件描述符限制
- 内存管理配置
- 网络参数优化

## 安全配置

### 防火墙配置
```bash
# UFW防火墙配置
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 安全加固
- 禁用不必要的服务
- 用户权限配置
- 文件权限设置
- 安全更新策略

## 故障排除

### 常见问题

#### 服务启动失败
```bash
# 查看服务状态
sudo systemctl status project-name

# 查看详细日志
sudo journalctl -u project-name -f
```

#### 数据库连接问题
```bash
# 测试数据库连接
python manage.py dbshell

# 检查数据库服务状态
sudo systemctl status mysql
```

#### Nginx配置问题
```bash
# 测试Nginx配置
sudo nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/error.log
```

### 日志分析
- 应用错误日志
- Web服务器访问日志
- 系统日志分析
- 性能指标监控

## 维护计划

### 日常维护
- 日志清理
- 系统更新
- 安全补丁
- 性能监控

### 定期维护
- 数据库优化
- 磁盘空间清理
- 备份验证
- 安全审计

## 联系信息
- 运维团队联系方式
- 紧急联系人
- 技术支持渠道
- 文档维护者