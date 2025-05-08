#!/bin/bash

# 检查是否提供了容器名称
if [ -z "$1" ]; then
    echo "请提供容器名称"
    echo "用法: $0 <容器名称> [cron表达式]"
    echo "示例: $0 my-container '0 4 * * *'"
    exit 1
fi

CONTAINER_NAME=$1
CRON_EXPRESSION=${2:-"0 4 * * *"}  # 默认每天凌晨4点重启

# 检查容器是否存在
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "错误: 容器 '${CONTAINER_NAME}' 不存在"
    exit 1
fi

# 创建重启脚本
RESTART_SCRIPT="/usr/local/bin/docker_restart_${CONTAINER_NAME}.sh"
cat > "${RESTART_SCRIPT}" << EOF
#!/bin/bash
docker restart ${CONTAINER_NAME}
echo "\$(date '+%Y-%m-%d %H:%M:%S') - 容器 ${CONTAINER_NAME} 已重启" >> /var/log/docker_restart.log
EOF

# 设置脚本权限
chmod +x "${RESTART_SCRIPT}"

# 添加到crontab
(crontab -l 2>/dev/null | grep -v "${CONTAINER_NAME}"; echo "${CRON_EXPRESSION} ${RESTART_SCRIPT}") | crontab -

echo "定时重启已设置成功！"
echo "容器名称: ${CONTAINER_NAME}"
echo "执行时间: ${CRON_EXPRESSION}"
echo "重启脚本: ${RESTART_SCRIPT}"
echo "日志文件: /var/log/docker_restart.log" 