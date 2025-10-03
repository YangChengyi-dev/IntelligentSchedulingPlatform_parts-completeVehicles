import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_connection import TransactionalSession
from database.models import user
from sqlalchemy.exc import SQLAlchemyError
from utils.log_utils import Logging

def create_admin_user():
    """
    创建或更新admin用户
    """
    print("开始创建admin用户...")
    
    # 初始化数据库连接
    t = TransactionalSession()
    session = t.session()
    
    try:
        # 检查admin用户是否已存在
        admin_user = session.query(user).filter(user.username == 'admin').first()
        
        if admin_user:
            # 更新现有用户密码
            admin_user.password = '123456'
            session.commit()
            print("✓ admin用户密码已更新为: 123456")
        else:
            # 创建新的admin用户
            new_admin = user(username='admin', password='123456')
            session.add(new_admin)
            session.commit()
            print("✓ admin用户已创建，账号: admin，密码: 123456")
        
        return True
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f"✗ 创建admin用户失败: {str(e)}")
        print("请确保MySQL数据库已启动并正确配置")
        print("检查config.ini中的数据库连接配置是否正确")
        return False
    
    except Exception as e:
        session.rollback()
        print(f"✗ 发生未知错误: {str(e)}")
        return False
    
    finally:
        session.close()

def check_database_connection():
    """
    检查数据库连接是否正常
    """
    print("检查数据库连接...")
    try:
        t = TransactionalSession()
        engine = t.engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ 数据库连接正常")
            return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {str(e)}")
        print("请确保:")
        print("1. MySQL服务器已启动")
        print("2. 数据库logistics_test已创建")
        print("3. 用户有权限访问该数据库")
        return False

def main():
    print("===== 用户管理工具 =====")
    
    # 先检查数据库连接
    if not check_database_connection():
        print("\n无法继续，请先解决数据库连接问题")
        return
    
    # 创建admin用户
    create_admin_user()
    
    print("\n===== 操作完成 =====")
    print("请使用以下凭证登录系统:")
    print("- 用户名: admin")
    print("- 密码: 123456")

if __name__ == '__main__':
    main()