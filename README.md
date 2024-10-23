# AWS+Django运行图片工具站

本项目旨在演示如何用亚马逊云科技AWS的EC2和S3来发布一个基于Python Django的图片处理工具站



## 本地运行

1. 安装nodejs

   本项目使用了tailwindcss，它依赖nodejs，所以需要安装node。下面以Mac为例，其他操作系统请自行搜索安装方法：

   > 本项目使用了tailwindcss，它依赖nodejs，所以需要

2. 安装tailwindcss所需的包

   安装node后，进入本项目的theme/static_src目录下，运行如下命令：

   > npm install

3. 成功完成以上两个步骤后，运行以下命令，启动tailwind，它的功能是实时根据代码生成相应的css。这个步骤只有在开发环境中需要：

   > python manage.py tailwind start

4. 安装好Python，本项目建议使用**Python 3.12.5**

5. 安装本项目的依赖，进入项目根目录下，运行：

   > python -m pip install -r requirements.txt

6. 启动django服务器

   > python manage.py runserver

   成功启动后，可以在以下URL访问网站：http://127.0.0.1:8000/



## 服务器运行

以下步骤使用AWS的Linux 2023服务器，服务器具体操作步骤请参考视频。

1. 服务器设置，创建服务器时，上传本项目根目录下的`env_setup.sh`文件作为User Data Script

2. 登录到服务器
   进入你的key保存目录，对我来说是ms1024.key，运行如下命令：
   ```bash
   chmod 400 ms1024.key
   ssh -i ms1024.key ec2-user@<public IP address>
   ```
3. 登录服务器后，首先下载代码：

   ```shell
   cd /home/ec2-user
   git clone https://github.com/maishucode/ms-img-resizer.git
   ```
   

4. 进入/home/ec2-user下的MsImageResizer目录，运行以下命令：

   ```shell
   chmod +x python_setup.sh
   ./python_setup.sh
   ```

   这个命令可能要运行好几分钟，耐心等待命令执行完成。

5. 安装项目所需的Python包。进入项目根目录，执行如下命令：

   ```shell
   python -m pip install -r requirements.txt
   ```

6. 启动Django项目。在项目根目录下执行：

   ```shell
   python manage.py runserver
   ```
   上面的命令，有一点问题，当你退出窗口，服务就停掉了。如果想一直运行，可以使用下面的命令：
   ```shell
   nohup python manage.py runserver 0.0.0.0:8000 &
   ```

7. 访问网站。如果以下步骤都顺利执行，应该可以通过以下网址访问网站：

   http://<EC2的公共IP地址>/