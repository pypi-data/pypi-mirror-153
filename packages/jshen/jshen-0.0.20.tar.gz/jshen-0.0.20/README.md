# jshen
Tools

## jtorch

### d2l.py

使用的是 https://github.com/d2l-ai/d2l-en/blob/master/d2l/torch.py

没有设置环境要求，若缺失哪个包，进行安装即可



## 参考资料
setup.py:

2. https://blog.csdn.net/coolcooljob/article/details/80082907
3. https://blog.csdn.net/weixin_43964444/article/details/108414571

setup.py参数介绍：https://www.cnblogs.com/maociping/p/6633948.html

官方文档：https://packaging.python.org/en/latest/tutorials/packaging-projects/

python setup.py build

python setup.py sdist   (推荐 source distribute)

python setup.py install

twine upload dist/*
更新：

pip install git+https://github.com/JieShenAI/jshen.git --upgrade

国内源下载：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jshen

### rst

rst官方语法格式：https://zh-sphinx-doc.readthedocs.io/en/latest/rest.html

本地rst语法检测

> 因为pypi的解析器不是sphinx，有些语法会有问题

安装库rst：

* pip install readme_renderer
* 执行命令：python setup.py check -r -s

