# mr_remux_plugins

全自动制作remux MR插件

特别声明：
 
  原则上使用插件自动转出的remux文件仅限于自用，不建议发种到pt社区
  
  因为很多diy组是禁止原盘用于remux和压制的，
  
  除非你看清楚了对应的盘没有权限、版权声明，
  
  胡乱上传被ban不要来找我


手动安装插件方法：

	1、复制 /lib 及 /usr 文件夹到docker内相同目录，并执行：
	
	
		rm /lib/x86_64-linux-gnu/libm.so.6
		ln -s /lib/x86_64-linux-gnu/libm-2.31.so /lib/x86_64-linux-gnu/libm.so.6

		rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 
		ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28 /usr/lib/x86_64-linux-gnu/libstdc++.so.6 
	
	2、/remux 目录是插件本体，复制到mr plugins目录下，重启mr

	3、如果模块未自动安装成功，则需手动安装 pip install  "bitstring", "psutil"

	4、插件设置里设定remux保存目录


手动制作remux（可用于测试）

	在插件快捷功能中，直接填入需要制作的原盘目录



