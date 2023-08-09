# pip install pandas
# pip install pymysql
# pip install openpyxl
import pandas as pd
import pymysql

# 连接到MySQL数据库
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='col_data'
)

# 创建游标对象
cursor = connection.cursor()

# 读取xlsx文件，跳过第一行标题头
data = pd.read_excel('../offline_data/tianyacha/data.xlsx', skiprows=[0, 1, 2])


# 处理NaN值和空值
data = data.fillna("")  # 填充NaN值
data = data.replace("", None)  # 将空字符串转为None

# 提取数据并插入到数据库中
for _, row in data.iterrows():
    # 将NaN值替换为None
    values = [None if pd.isna(val) else val for val in row.values]

    sql = "INSERT INTO ods_company_data_chongqing (company_name, status, legal_person, registered_capital, paid_capital, establishment_date, approval_date, business_term, province, city, district, credit_code, taxpayer_identification_number, registration_number, organization_code, insured_employees, company_type, industry, former_name, registered_address, latest_annual_report, website, available_phone, unavailable_phone, other_number, email, other_email, business_scope) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, tuple(values))

# 提交事务
connection.commit()

# 关闭游标和连接
cursor.close()
connection.close()



"""sql
drop table ods_company_data_chongqing;

CREATE TABLE ods_company_data_chongqing (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- 主键ID，自增
    company_name VARCHAR(255),  -- 公司名称
    status VARCHAR(255),  -- 经营状态
    legal_person VARCHAR(255),  -- 法定代表人
    registered_capital VARCHAR(255),  -- 注册资本
    paid_capital VARCHAR(255),  -- 实缴资本
    establishment_date VARCHAR(255),  -- 成立日期
    approval_date VARCHAR(255),  -- 核准日期
    business_term VARCHAR(255),  -- 营业期限
    province VARCHAR(255),  -- 所属省份
    city VARCHAR(255),  -- 所属城市
    district VARCHAR(255),  -- 所属区县
    credit_code VARCHAR(255),  -- 统一社会信用代码
    taxpayer_identification_number VARCHAR(255),  -- 纳税人识别号
    registration_number VARCHAR(255),  -- 注册号
    organization_code VARCHAR(255),  -- 组织机构代码
    insured_employees VARCHAR(255),  -- 参保人数
    company_type VARCHAR(255),  -- 公司类型
    industry VARCHAR(255),  -- 所属行业
    former_name VARCHAR(255),  -- 曾用名
    registered_address VARCHAR(255),  -- 注册地址
    latest_annual_report VARCHAR(255),  -- 最新年报地址
    website VARCHAR(255),  -- 网址
    available_phone VARCHAR(255),  -- 可用电话
    unavailable_phone VARCHAR(255),  -- 不可用电话
    other_number VARCHAR(255),  -- 其他号码
    email VARCHAR(255),  -- 邮箱
    other_email VARCHAR(255),  -- 其他邮箱
    business_scope TEXT  -- 经营范围
);
"""