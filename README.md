# mr_remux_plugins

手动安装插件方法：

	1、复制 /lib 及 /usr 文件夹到docker内相同目录，并执行：
	
	
		rm /lib/x86_64-linux-gnu/libm.so.6
		ln -s /lib/x86_64-linux-gnu/libm-2.31.so /lib/x86_64-linux-gnu/libm.so.6

		rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 
		ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28 /usr/lib/x86_64-linux-gnu/libstdc++.so.6 
	

	2、如果模块未自动安装成功，则需手动安装 pip install  "bitstring", "psutil"

	3、插件设置里设定remux保存目录


手动制作remux（可用于测试）

	在插件快捷功能中，直接填入需要制作的原盘目录



