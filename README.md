# 人力考核系统（HR System by Django）

一个面向运维团队的内部人力绩效考核系统：员工注册后录入/申请各类工作量，
系统按月自动汇总积分并生成绩效排名，支持民主测评与审批流程。

## 功能特性

### 前台（员工）

- **业务展示**：工单类、割接类、项目类、日常工作、故障处理、特殊加分项六类业务列表
- **总分排名**：按月自动汇总六类业务积分 + 民主测评分，生成绩效看板与 TOP3 领奖台
- **工作台**（主页 / 工作台）：个人信息维护、年度工作量统计、绩效排名概览
- **工作量申请**（主页 / 工作量申请）：按类型提交工作量申请（含完成人员比例分摊）、查看流程历史
- **审批流**：审批人在“待办审批”中通过/驳回申请，通过后积分自动写入总分表
- **民主测评**：每周期对其他员工进行工作态度/责任心/工作纪律打分

### 后台（管理员）

- 基于 [SimpleUI](https://github.com/newpanjing/simpleui)（Vue.js + Element-UI）重新设计的管理后台
- 全部业务数据的录入、批量编辑、筛选、搜索
- 系统设置（项目名称、Logo、页脚、公告）、首页轮播图、用户审批与角色管理

## 技术栈

| 组件 | 版本 |
| --- | --- |
| Python | 3.12 |
| Django | 5.2 LTS |
| 管理后台 | django-simpleui（Vue.js + Element-UI） |
| 前端 | Bootstrap 4 + jQuery + DataTables |
| 数据库 | MySQL（生产）/ SQLite（开发，经 `local_settings.py` 覆盖） |

## 快速开始

```bash
# 1. 创建虚拟环境并安装依赖
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. （开发环境可选）使用 SQLite：创建 myproject/local_settings.py
cat > myproject/local_settings.py <<'EOF'
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
EOF

# 3. 初始化数据库与管理员
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser

# 4. （可选）生成演示数据：4 个测试用户 + 六类业务数据 + 民主测评
.venv/bin/python manage.py seed_test_data --count 8

# 5. 启动
.venv/bin/python manage.py runserver
```

- 前台首页：<http://127.0.0.1:8000/>
- 总分排名：<http://127.0.0.1:8000/scores/>
- 管理后台：<http://127.0.0.1:8000/admin/>

生产环境使用 MySQL：在 `myproject/settings.py` 的 `DATABASES` 中配置连接
（建议通过 `local_settings.py` 或环境变量注入密码），并执行
`manage.py collectstatic` 收集静态资源。

## 项目结构

```text
HRSystemByDjango/
├── accounts/    # 用户注册/登录、个人工作台、工作量申请与审批流、系统设置
├── scores/      # 总分排名、绩效计算、民主测评、演示数据命令
├── orders/      # 工单类
├── cutovers/    # 割接类
├── posts/       # 项目类
├── routine/     # 日常工作
├── faulty/      # 故障处理
├── bonuses/     # 特殊加分项
├── templates/   # 全局模板、共享样式、常量配置（constant_files.py）
├── static/      # 静态资源
└── myproject/   # Django 配置（settings / urls / wsgi）
```

## 积分规则简述

- 排名统计**上个月**的数据：工单/割接/项目按到期日期归月，日常/故障/特殊加分按登记日期归月
- 每条业务记录按“完成人员 × 完成比例 × 分值”分摊积分；割接每条固定 3 分（仅负责人）
- 工单 + 割接 + 故障 + 日常合计 40 分封顶，项目与特殊加分另计
- 民主测评三项平均分按 3.33% 折算计入互评分
- 审批通过的工作量申请按其类型与相关日期并入对应月份积分

## 测试

```bash
.venv/bin/python manage.py test
```
