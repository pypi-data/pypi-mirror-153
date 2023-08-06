# lesscode-python

#### 介绍
   lesscode-python 是基于tornado的web开发脚手架项目，该项目初衷为简化开发过程，让研发人员更加关注业务。
#### 软件功能
1. 路由自动注册，路由直接指向处理函数
2. 请求参数自动解析，调用处理函数自动注入
3. 多环境配置文件，支持命令行指定运行参数
4. 日志本地化存储，支持日志控制台与文件双输出，存储参数可配置
5. 统一异常处理，日志格式统一
6. 统一数据返回格式，自动包装处理
7. 定义常用业务处理状态码，支持信息自定义
8. 支持数据库连接池，支持多数据源统一配置，目前已支持PostgreSQL。
#### 安装教程

安装或升级到最新版本，请执行以下操作:
    
    pip install -U lesscode-py

#### 使用说明

1. 路由自动注册，路由直接指向处理函数
2. 请求参数自动解析，调用处理函数自动注入

   1. 建立Handler处理类，继承BaseHandler
   2. 使用 @Handler 标注一级路径
   3. 编写业务处理方法，使用@GetMapping/PostMapping进行标注二级路径
   4. 请求时使用两级路径拼接访问如：/level1/level2


       @Handler("/level1") 
       class DemoHandler(BaseHandler):

       @GetMapping("/level2")
       def query_demo(self):
        return "lesscode-python"


**注意：所有Handler处理类需要放在统一文件目录下，默认为"handlers"， 如需修改在配置文件中进行设置**
               
      定义：define("handler_path", default="handlers", type=str, help="处理器文件存储路径")
      配置：options.handler_path ="xxx"
3. 多环境配置文件，支持命令行指定运行参数
   
   1. config.py 默认配置文件
   2. config_dev.py 开发环境配置文件
   3. config_release.py 准生产环境配置文件
   4. config_prod.py 生产环境配置文件
   
   
   **注意：所有配置文件需要统一放置在项目根目录下的profile文件夹中，需要自行创建，不支持自定义**

   相同参数默认配置文件会覆盖定义默认值，其他环境配置文件会覆盖默认配置文件，命令行会覆盖配置文件
   
   优先级：命令行>环境配置文件>默认配置文件>定义默认值

      
      定义：define("profile", default="profiles.config", type=str, help="配置文件")

      配置1：在默认配置文件中指定：options.profile ="dev" 仅需要指定后缀即可

      配置2：在命令行指定：--profile=dev
      
4. 日志本地化存储，支持日志控制台与文件双输出，存储参数可配置


      **日志级别设置**

      CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET

      10-DEBUG       输出详细的运行情况，主要用于调试。

      20-INFO        确认一切按预期运行，一般用于输出重要运行情况。

      30-WARNING     系统运行时出现未知的事情（如：警告内存空间不足），但是软件还可以继续运行，可能以后运行时会出现问题。
      
      40-ERROR       系统运行时发生了错误，但是还可以继续运行。

      50-CRITICAL    一个严重的错误，表明程序本身可能无法继续运行。
      
      配置：options.logging = "INFO"

      **文件分割方式**

      时间与文件大小，默认采用时间分割time/size

      配置：options.log_rotate_mode = "time"
      
      **日志文件前缀**

      配置：options.log_file_prefix = "log"

      **间隔的时间单位**

       S 秒
       M 分
       H 小时、
       D 天、
       W 每星期（interval==0时代表星期一）
       midnight 每天凌晨

      配置：options.log_rotate_when = "D"
      
      **备份文件的个数**

      如果超过这个个数，就会自动删除

      配置：options.log_file_num_backups = 30
 
5. 统一异常处理，日志格式统一
      
    业务中需要抛出异常，直接抛出BusinessException

       抛出设定状态码异常
         raise BusinessException(StatusCode.USER_REGISTER_FAIL）
       抛出设定状态码异常，需要内容格式化,此类异常码为方法，调用时传入提示词
          raise BusinessException(StatusCode.REQUIRED_PARAM_IS_EMPTY(message))
       
6. 统一数据返回格式，自动包装处理

      ResponseResult  响应结果的统一包装类
      #### 业务请求状态编码
        self["status"] = status_code[0]
        # 返回状态码对应的说明信息
        self["message"] = status_code[1]
        # 返回数据对象 主对象 指定类型
        self["data"] = data
        # 时间戳
        self["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
      
        #### 响应格式

          {
                "status": "00000",
                "message": "请求成功",
                "data": "lesscode-python",
                "timestamp": "2021-11-18 16:20:07.823522"
           }
8. 定义常用业务处理状态码，支持信息自定义

    StatusCode 统一请求返回状态码
   1. A表示错误来源于用户，比如参数错误，用户安装版本过低，用户支付超时等问题；
   2. B表示错误来源于当前系统，往往是业务逻辑出错，或程序健壮性差等问题；
   3. C表示错误来源于第三方服务

    #### 响应服务请求的状态码与说明
       SUCCESS = ("00000", "请求成功")
       FAIL = ("99999", "请求失败")
       USER_VALIDATE_FAIL = ("A0001", "用户端错误")
       USER_REGISTER_FAIL = ("A0100", "用户注册错误")
       USER_NAME_VALIDATE_FAIL = ("A0110", "用户名校验失败")
       USER_NAME_EXIST = ("A0111", "用户名已存在")
       USER_NAME_INVALID = ("A0112", "用户名包含特殊字符")
       PASSWORD_VALIDATE_FAIL = ("A0120", "密码校验失败")
       PASSWORD_LENGTH_VALID = ("A0121", "密码长度不够")
       SHORT_MESSAGE_VALID_FAIL = ("A0130", "短信验证码错误")
       VALIDATE_CODE_ERROR = ("A0131", "验证码错误！")
       USER_LOGIN_EXCEPTION = ("A0200", "用户登陆异常")
       USER_ACCOUNT_NOT_EXIST = ("A0201", "用户账户不存在")
       REQUEST_PARAM_ERROR = ("A0300", "用户请求参数错误")
       INVALID_USER_INPUT = ("A0301", "无效的用户输入")
       REQUIRED_PARAM_IS_EMPTY = ("A0310", "请求缺少必要参数:{}")
       INVALID_TIME_STAMP = ("A0311", "非法的时间戳参数")
       USER_INPUT_INVALID = ("A0312", "用户输入内容非法")
       VALIDATE_CODE_EXPIRE = ("A0400", "验证码过期")
       FORM_VALIDATE_FAIL = ("A0401", "表单校验失败")
       PARAM_VALIDATE_FAIL = ("A0402", "参数校验失败")
       PARAM_BIND_FAIL = ("A0403", "参数绑定失败")
       PHONE_NUM_NOT_FOUND = ("A0404", "找不到该用户，手机号码有误")
       PHONE_ALREADY_REGISTER = ("A0405", "手机号已经注册")
       ACCESS_DENIED = ("B0001", "访问权限不足")
       RESOURCE_DISABLED = ("B0002", "资源被禁用")
       RESOURCE_NO_AUTHORITY = ("B0003", "该资源未定义访问权限")
       BUSINESS_FAIL = ("B0000", "{}")
       RESOURCE_NOT_FOUND = ("B0404", "访问资源不存在")
       TIMEOUT = ("B0100", "系统执行超时")
       STRIKE_RECOVERY = ("B0200", "系统容灾系统被触发")
       RPC_INVOKE_ERROR = ("C0001", "调用第三方服务出错")
       SERVER_ERROR = ("C0002", "服务器内部错误")
       UNKNOWN_ERROR = ("C0003", "未知异常")
#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 未来规划

1.  数据访问层封装
2.  数据缓存控制
3.  统一权限处理
4.  API 接口文档生成
5.  注册中心集成
6.  ......
