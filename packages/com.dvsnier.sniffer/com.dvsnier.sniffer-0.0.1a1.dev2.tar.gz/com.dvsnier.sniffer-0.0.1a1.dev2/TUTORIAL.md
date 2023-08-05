# Python NetWork Sniffer

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "the Python Test Project")

- [一. 配置](#一-配置)
  - [1.1. 脚本配置](#11-脚本配置)
    - [1.1.1. 嗅探单页](#111-嗅探单页)
    - [1.1.2. 嗅探多页](#112-嗅探多页)
  - [1.2. 文件配置](#12-文件配置)
  - [1.3. CLI 配置](#13-cli-配置)
- [二. 运行](#二-运行)
  - [2.1. 脚本运行](#21-脚本运行)
  - [2.1. CLI 运行](#21-cli-运行)

## 一. 配置

### 1.1. 脚本配置

打开 `.\scripts\crawler_script.py` 脚本配置如下:

#### 1.1.1. 嗅探单页

嗅探单页数据如下所示:

```python
if __name__ == "__main__":
    '''主函数入口'''
    page_size = 1
    crawler = Crawler_Bbs_TianYa()
    # crawler.set_flag(False)
    crawler.set_range(page_size).run()
```

#### 1.1.2. 嗅探多页

嗅探`[1, 5)` 页数据如下所示:

方式一:

```python
if __name__ == "__main__":
    '''主函数入口'''
    page_size = 5
    crawler = Crawler_Bbs_TianYa()
    # crawler.set_flag(False)
    crawler.set_range(page_size).run()
```

方式二:

```python
if __name__ == "__main__":
    '''主函数入口'''
    crawler = Crawler_Bbs_TianYa()
    # crawler.set_flag(False)
    crawler.set_range(page_start=1, page_stop=5).run()
```

### 1.2. 文件配置

文件配置列表如下:

```bash
# the version information
version_name = v0.0.1.dev1
version_code = 1
version_info = 0.0.1.dev1


# CRAWLER URL PREFIX
article-alias = 'crawler_alias'
sn-url-prefix = ['http://xxx.yyy.zzz/post-xxx-yyy-{}.shtml']


# REGION_INCLUSIVE_EXCLUSIVE = 0
# REGION_EXCLUSIVE_INCLUSIVE = 1
# REGION_EXCLUSIVE_EXCLUSIVE = 2
# REGION_INCLUSIVE_INCLUSIVE = 3
page-start = 1
page-stop = 0
page-flag = 0
# page-flag = 1
# page-flag = 2
# page-flag = 3
# False: first pull , second translate True: one pull after another translate
article-flag = True
# article-flag = False


# True: multi media resources are stored locally, otherwise they are not
# article-multi-media-persistence = True
# article-multi-media-persistence = False

# True: multi media resources are high quality, otherwise they are not
# article-multi-media-quality = True
# article-multi-media-quality = False


User-Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/512.36 (KHTML, like Gecko) Chrome/92.0.1235.131 Safari/277.36'
# User-Agent = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 12_10_3) AppleWebKit/512.36 (KHTML, like Gecko) Chrome/92.0.1235.131 Safari/277.36'


# output-directory = "..."
# output-uuid-encryptor = True
# output-uuid-encryptor = False
```

说明如下:

- `version_name`: 配置文件版本名称;
- `version_code`: 配置文件版本号;
- `version_info`: 配置文件版本信息;
- `article-alias`: 文章别名(`OPTIONAL`), 生成的目录格式为 `[bbs|json]_YYmmdd[_alias]`;
- `sn-url-prefix`: 文章的地址格式, 一般格式为 `http://xxx.yyy.zzz/post-xxx-yyy-{}.shtml`;
- `page-start`: 页面开始;
- `page-stop`: 页面结束(`OPTIONAL`);
- `page-flag`: 页面标记(`OPTIONAL`), 支持4 种类型, `REGION_INCLUSIVE_EXCLUSIVE`, `REGION_EXCLUSIVE_INCLUSIVE`, `REGION_EXCLUSIVE_EXCLUSIVE`, `REGION_INCLUSIVE_INCLUSIVE`;
- `article-flag`: 文章数据流生成风格(`OPTIONAL`);
- `article-multi-media-persistence`: 文章关联到的媒体资源持久化到本地(`OPTIONAL`, `RECOMMENDED`);
- `article-multi-media-quality`: 文章关联到的媒体资源质量(`OPTIONAL`);
- `User-Agent`: 文章请求的用户代理(`OPTIONAL`， `RECOMMENDED`);
- `output-directory`: 文章输出到指定目录(`OPTIONAL`， `RECOMMENDED`);
- `output-uuid-encryptor`: 文章输出 id 加密处理(`OPTIONAL`);

### 1.3. CLI 配置

```bash
$ dvs-sniffer -h
usage: dvs-sniffer [-h] [-V] [-amp] [-amq] [-a2 [article-alias]]
                   [-ad [article-describe]] [-af] [-rs [region-start]]
                   [-re [region-end]] [-rm [region-mask]] [-due]
                   [-ua [User-Agent]]
                   sn-url [destination-directory]

    this is a dvs network sniffer execution program.

    the sniffer destination url format must conform to the following continuous URLs:

        eg:

            1. http://bbs.xxx.cn/list-xyz-1.shtml
            2. http://bbs.xxx.cn/list-xyz-2.shtml
            3. http://bbs.xxx.cn/list-xyz-3.shtml
            4. ...
            5. http://bbs.xxx.cn/list-xyz-{}.shtml


positional arguments:
  sn-url                the sniffer destination url.
  destination-directory
                        the sniffer destination directory.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         the show version and exit.
  -amp, --article-multi-media-persistence
                        if True: multi media resources are stored locally,
                        otherwise they are not, and the default value is True.
  -amq, --article-multi-media-quality
                        if True: multi media resources are high quality,
                        otherwise they are not, and the default value is
                        False.
  -a2 [article-alias], --article-alias [article-alias]
                        a short text article alias of the sniffer to be.
  -ad [article-describe], --article-describe [article-describe]
                        a short text article description of the sniffer to be.
  -af, --article-flag   if False: first pull, second translate True: one pull
                        after another translate, and the default value is
                        True.
  -rs [region-start], --region-start [region-start]
                        a briefly describe the range start to be sniffed
                        mathematically.
  -re [region-end], --region-end [region-end]
                        a briefly describe the range end to be sniffed
                        mathematically.
  -rm [region-mask], --region-mask [region-mask]
                        The olfactory spatial range of the sniffer can only be
                        the following values: REGION_INCLUSIVE_EXCLUSIVE = 0,
                        REGION_EXCLUSIVE_INCLUSIVE = 1,
                        REGION_EXCLUSIVE_EXCLUSIVE = 2,
                        REGION_INCLUSIVE_INCLUSIVE = 3, and the default value
                        is REGION_INCLUSIVE_EXCLUSIVE.
  -due, --destination-uuid-encryptor
                        the sniffer destination uuid encryptor, and the
                        default value is True.
  -ua [User-Agent], --user-agent [User-Agent]
                        the user agent flag of set sniffer for default network
                        access, which is the macintosh system identifier by
                        default.

the copyright belongs to dvs that reserve the right of final interpretation.
```

## 二. 运行

### 2.1. 脚本运行

脚本运行如下:

```bash
# Windows
python ./scripts/crawler_script.py 
# Macintosh
python .\scripts\crawler_script.py 
```

### 2.1. CLI 运行

```bash
# Windows and Macintosh
# region: [1, 2)
dvs-sniffer -amq -rs 1 -re 2 http://xxx.yyy.zzz/post-1.html # the default destination directory
dvs-sniffer -amq -rs 1 -re 2 http://xxx.yyy.zzz/post-1.html \var\...\dvs-sniffer\ # the special destination directory
```
