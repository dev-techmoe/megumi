# Megumi
Megumi是一款订阅下载工具，它可以通过RSS来自动获取到您喜爱的资源的更新并从中获取下载地址，并自动推送到配置好的下载器来进行下载。

❗**测试警告**：本项目目前处在早期版本，可能会出现各种无法预料的bug导致功能异常，请务必花时间来确认程序是否工作正常。如果您发现bug欢迎及时在issue中提交给作者。

# 快速开始
目前使用Megumi需要一个支持RPC或者类似协议的下载器，而当下主流符合条件的有aria2和transmission这两种。Megumi暂时只支持aria2，对于其他下载器今后将逐步支持。  
配置文件使用toml格式，一个最小配置如下  
```toml
[downloader]
# 下载器类型，目前只支持aria2
type = 'aria2'
# 下载文件保存位置
save_path = '/tmp/download'
# aria2配置
[downloader.aria2]
# aria2 rpc地址
address = 'http://localhost:6800'
# aria2 rpc连接密钥
secret = 'my_aria2c_secret'
```
将文件保存为`config.toml`，之后使用以下命令启动Megumi守护进程。
```bash
./Megumi --config-path=./config.toml
```
## 管理Job
Megumi的运行由Job组成，目前每个Job对应一个RSS源链接，当对应RSS有更新的时候Megumi会自动拉取新条目并调用已配置的下载器进行下载。

### 创建job
```bash
$ megumi job add <job_name> <rss_url>
Job delete successful. id=1
```

### 删除job
```bash
$ megumi job delete <job_id>
```

### 查看所有job
```bash
$ megumi job list
```

### 查看Job运行历史记录
```bash
$ megumi job history
```

# 相关项目
- [FlexGet](https://github.com/Flexget/Flexget) 如果它没有设计的这么难用并且WebUI一直在experimental状态，我也不会去下决心去开这个坑

# 贡献
待补充。

# License
MIT