#!/usr/bin/env bash
# ==============================================================================
# UC8 - STOP WORKCELL SCRIPT
# Dừng sạch sẽ toàn bộ các tiến trình ROS, MoveIt, State Machine và cổng 10000.
# ==============================================================================

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${YELLOW}[!] Đang dừng toàn bộ tiến trình Workcell UC8...${NC}"

# 1. Dừng Task State Machine
pkill -9 -f "task_state_machine.py" 2>/dev/null && echo -e "${GREEN}[✔] Đã dừng Task State Machine.${NC}" || echo -e "${CYAN}[-] Task State Machine không chạy.${NC}"

# 2. Dừng MoveIt & RViz
pkill -9 -f "ur10e_moveit_config" 2>/dev/null && echo -e "${GREEN}[✔] Đã dừng MoveIt & RViz.${NC}" || echo -e "${CYAN}[-] MoveIt không chạy.${NC}"

# 3. Dừng ROS-TCP-Endpoint & giải phóng cổng 10000
kill -9 $(lsof -t -i:10000) 2>/dev/null && echo -e "${GREEN}[✔] Đã giải phóng cổng 10000.${NC}" || echo -e "${CYAN}[-] Cổng 10000 đã trống.${NC}"
pkill -9 -f "ros_tcp_endpoint" 2>/dev/null

# 4. Dừng roscore / roslaunch nếu còn sót
pkill -9 -f "rosmaster" 2>/dev/null
pkill -9 -f "rosout" 2>/dev/null

echo -e "${GREEN}${BOLD}======================================================${NC}"
echo -e "${GREEN}${BOLD}   ĐÃ DỪNG VÀ GIẢI PHÓNG TOÀN BỘ HỆ THỐNG AN TOÀN!   ${NC}"
echo -e "${GREEN}${BOLD}======================================================${NC}"
