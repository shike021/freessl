# 开发文档

## 概述

本文档为Free SSL Service的开发指南，包括开发环境搭建、代码规范、测试等内容。

## 开发环境搭建

### 前置要求

- Docker 20.10+
- Docker Compose 1.29+
- Git
- VS Code（推荐）或其他IDE
- Postman（API测试）

### 1. 克隆代码

```bash
git clone https://github.com/yourrepo/free-ssl-service.git
cd free-ssl-service
```

### 2. 启动开发环境

```bash
# 启动所有服务
docker-compose -f free_ssl_service/docker-compose.yml up --build

# 或者在后台运行
docker-compose -f free_ssl_service/docker-compose.yml up -d
```

### 3. 验证环境

访问以下地址确认服务正常运行：

- 前端: http://localhost:8080
- 后端API: http://localhost:5000
- API文档: http://localhost:5000/apidocs

## 项目结构

```
free_ssl_service/
├── backend/              # 后端（Flask）
│   ├── app.py          # 应用入口
│   ├── config.py       # 配置文件
│   ├── models/         # 数据模型
│   ├── routes/         # 路由
│   ├── services/       # 业务逻辑
│   ├── utils/          # 工具函数
│   └── tests/          # 测试
└── frontend/          # 前端（Vue.js）
    ├── src/
    │   ├── components/  # 组件
    │   ├── views/       # 页面
    │   ├── router/      # 路由
    │   ├── store/       # 状态管理
    │   └── utils/      # 工具函数
    └── tests/          # 测试
```

## 后端开发

### 技术栈

- **框架**: Flask 2.0.1
- **ORM**: Flask-SQLAlchemy 2.5.1
- **数据库**: MariaDB 10.6
- **任务队列**: Celery 5.2.3
- **测试**: pytest

### 开发流程

#### 1. 进入后端容器

```bash
docker-compose exec backend sh
```

#### 2. 安装依赖

```bash
pip install package-name
pip freeze > requirements.txt
```

#### 3. 运行代码检查

```bash
# Flake8代码风格检查
flake8 .

# Pylint代码质量检查
pylint **/*.py
```

#### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api.py

# 运行测试并生成覆盖率报告
pytest --cov=. --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

### 代码规范

#### Python代码风格（PEP 8）

```python
# 导入顺序：标准库 -> 第三方库 -> 本地模块
import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models.user_model import User

# 类名使用大驼峰
class UserService:
    pass

# 函数和变量使用小写加下划线
def get_user_by_id(user_id):
    pass

# 常量使用大写加下划线
MAX_RETRY_COUNT = 3
```

#### 文档字符串

```python
def get_user_by_id(user_id):
    """
    根据用户ID获取用户信息
    
    Args:
        user_id (int): 用户ID
        
    Returns:
        User: 用户对象
        
    Raises:
        ValueError: 当用户ID无效时
    """
    pass
```

### 添加新功能

#### 1. 创建数据模型

在 `models/` 目录下创建模型文件：

```python
from models.db import db

class NewModel(db.Model):
    __tablename__ = 'new_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
```

#### 2. 创建服务层

在 `services/` 目录下创建服务文件：

```python
from models.new_model import NewModel

class NewService:
    @staticmethod
    def create_item(name):
        item = NewModel(name=name)
        db.session.add(item)
        db.session.commit()
        return item
    
    @staticmethod
    def get_item_by_id(item_id):
        return NewModel.query.get(item_id)
```

#### 3. 创建路由

在 `routes/` 目录下创建路由文件：

```python
from flask import Blueprint, request, jsonify
from services.new_service import NewService

new_bp = Blueprint('new', __name__, url_prefix='/api/new')

@new_bp.route('/', methods=['POST'])
def create_item():
    data = request.json
    item = NewService.create_item(data['name'])
    return jsonify(item.to_dict()), 201

@new_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = NewService.get_item_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item.to_dict())
```

#### 4. 注册路由

在 `app.py` 中注册新路由：

```python
from routes.new_routes import new_bp

app.register_blueprint(new_bp)
```

#### 5. 添加测试

在 `tests/` 目录下创建测试文件：

```python
import pytest
from app import app
from models.db import db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_create_item(client):
    response = client.post('/api/new/', json={'name': 'Test'})
    assert response.status_code == 201
    assert response.json['name'] == 'Test'
```

## 前端开发

### 技术栈

- **框架**: Vue.js 2.6.14
- **UI库**: Element UI 2.15.7
- **状态管理**: Vuex 3.6.2
- **路由**: Vue Router 3.5.3
- **HTTP**: Axios 0.21.1
- **测试**: Jest + @vue/test-utils

### 开发流程

#### 1. 进入前端容器

```bash
docker-compose exec frontend sh
```

#### 2. 安装依赖

```bash
npm install package-name
```

#### 3. 运行代码检查

```bash
# ESLint代码检查
npm run lint

# 自动修复代码问题
npm run lint -- --fix
```

#### 4. 运行测试

```bash
# 运行所有测试
npm run test:unit

# 运行特定测试文件
npm run test:unit -- tests/unit/auth.spec.js

# 监听模式运行测试
npm run test:unit -- --watch
```

### 代码规范

#### Vue组件风格

```vue
<template>
  <div class="component">
    <h1>{{ title }}</h1>
    <button @click="handleClick">Click</button>
  </div>
</template>

<script>
export default {
  name: 'ComponentName',
  
  props: {
    title: {
      type: String,
      required: true
    }
  },
  
  data() {
    return {
      count: 0
    }
  },
  
  computed: {
    doubleCount() {
      return this.count * 2
    }
  },
  
  methods: {
    handleClick() {
      this.count++
    }
  }
}
</script>

<style scoped>
.component {
  padding: 20px;
}
</style>
```

#### JavaScript代码风格

```javascript
// 使用const/let，避免使用var
const API_URL = '/api'
let count = 0

// 使用箭头函数
const handleClick = () => {
  console.log('Clicked')
}

// 使用模板字符串
const message = `Hello, ${name}`

// 使用解构赋值
const { id, name } = user

// 使用默认参数
const greet = (name = 'World') => {
  return `Hello, ${name}`
}
```

### 添加新功能

#### 1. 创建组件

在 `src/components/` 目录下创建组件：

```vue
<template>
  <div class="new-component">
    <h1>{{ title }}</h1>
  </div>
</template>

<script>
export default {
  name: 'NewComponent',
  props: {
    title: String
  }
}
</script>

<style scoped>
.new-component {
  padding: 20px;
}
</style>
```

#### 2. 创建页面

在 `src/views/` 目录下创建页面：

```vue
<template>
  <div>
    <NewComponent :title="pageTitle" />
  </div>
</template>

<script>
import NewComponent from '@/components/NewComponent.vue'

export default {
  name: 'NewPage',
  components: {
    NewComponent
  },
  data() {
    return {
      pageTitle: 'New Page'
    }
  }
}
</script>
```

#### 3. 添加路由

在 `src/router/index.js` 中添加路由：

```javascript
import NewPage from '@/views/NewPage.vue'

const routes = [
  // ... 其他路由
  {
    path: '/new',
    name: 'NewPage',
    component: NewPage,
    meta: { requiresAuth: true }
  }
]
```

#### 4. 添加Vuex模块

在 `src/store/modules/` 目录下创建模块：

```javascript
const state = {
  items: []
}

const mutations = {
  SET_ITEMS(state, items) {
    state.items = items
  },
  ADD_ITEM(state, item) {
    state.items.push(item)
  }
}

const actions = {
  async fetchItems({ commit }) {
    const response = await api.get('/items')
    commit('SET_ITEMS', response.data)
  },
  async addItem({ commit }, item) {
    const response = await api.post('/items', item)
    commit('ADD_ITEM', response.data)
  }
}

const getters = {
  itemCount: state => state.items.length
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
```

在 `src/store/index.js` 中注册模块：

```javascript
import newModule from './modules/new'

export default new Vuex.Store({
  modules: {
    auth,
    certs,
    newModule
  }
})
```

#### 5. 添加测试

在 `tests/unit/` 目录下创建测试文件：

```javascript
import { shallowMount } from '@vue/test-utils'
import NewComponent from '@/components/NewComponent.vue'

describe('NewComponent.vue', () => {
  it('renders props.title when passed', () => {
    const title = 'new message'
    const wrapper = shallowMount(NewComponent, {
      propsData: { title }
    })
    expect(wrapper.text()).toMatch(title)
  })
})
```

## 调试

### 后端调试

```bash
# 查看日志
docker-compose logs -f backend

# 进入容器调试
docker-compose exec backend sh

# 使用Python调试器
import pdb; pdb.set_trace()
```

### 前端调试

```bash
# 查看日志
docker-compose logs -f frontend

# 在浏览器中打开开发者工具
# 使用console.log调试
console.log('Debug info')
```

## 常见问题

### 后端

**问题**: 数据库连接失败
**解决**: 检查MariaDB容器是否正常运行，检查环境变量配置

**问题**: 导入模块失败
**解决**: 确保在容器内操作，检查PYTHONPATH设置

### 前端

**问题**: 组件无法渲染
**解决**: 检查组件导入路径，检查props是否正确传递

**问题**: API请求失败
**解决**: 检查后端服务是否正常运行，检查API URL配置

## 提交代码

### Git工作流

```bash
# 创建功能分支
git checkout -b feature/your-feature

# 添加文件
git add .

# 提交代码
git commit -m 'feat: add new feature'

# 推送到远程
git push origin feature/your-feature

# 创建Pull Request
```

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：

```
feat: add user registration feature
fix: resolve database connection issue
docs: update API documentation
test: add unit tests for user service
```

## 相关文档

- [API文档](api.md)
- [部署文档](deployment.md)
- [故障排查](troubleshooting.md)
