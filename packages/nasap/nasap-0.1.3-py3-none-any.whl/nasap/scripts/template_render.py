import os, sys
import fire

# 思路：
# 输入 output文件夹， 在output文件夹中写入index.html
# 0 写入 样式 style
# 1 读取output文件夹中的文件。
# 2 判断文件是否存在 把字段 文件名 提取出来 写入列表
# 3 把图片的link写入 html
# 4

html_content='''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nasap report</title>
	<script src="./statics/plotly-2.8.3.min.js"></script>
</head>
<body>
  <!-- navbar -->
  <div class="top-nav">
    <div class="top-nav-logo">
      <div><span style="font-size: 40px;">N</span><span class="logo">ASAP</span></div>
      <u>Nas</u><span>cent RNA data</span> <u>a</u><span>nalysis</span> <u>P</u><span>latform</span>
    </div>
    <div id="time"></div>
  </div>
{{ replace place }}
</body>

<style>
  *{
    padding: 0;
    margin: 0;
  }
  body{
    background: #eeeeee;
  }
  .top-nav {
    width: 100%;
    overflow: hidden;
    background: grey;
    position: fixed;
		z-index: 9999;
    top: 0;
  }
  .logo{
    width: 30%;
    font-size: 60px;
    text-shadow: 5px 5px 5px black, 0px 0px 2px black;
    color: rgb(129, 193, 236);
    text-align: left;
  }

  .control{
    width: 1075px;
    height: auto;
    margin: 0 auto;
  }
  .left,.content{
    height: auto;
    margin: 140px 5px;
  }
  .left{
    width: 200px;
    display: inline-block;
    vertical-align: top;

  }
  .subNav{
    height: auto;
    background-color: white;
    padding: 10px;
    width: 180px;
    position: fixed;
		z-index: 9999;
  }
  .content{
    width: 850px;
    background-color: white;
    display: inline-block;
  }
  .part{
    text-align: center;
    line-height: 60px;
    border-bottom: 1px solid #d9d9d9;
    border-radius: 5px;
    color: #000000;
  }
  a{
    text-decoration: none;
    color:black;
    display: block;
  }
	a:hover {
    color:#FFFFFF;
    text-decoration:none;
  }
  .part:hover{
    background: #eeeeee;
    cursor: pointer;
  }
  .part4{
    border: none;
  }
  .text{
    line-height: 30px;
    width: 80%;
    margin: 25px auto;
    height: auto;
  }
	.container {
		margin-top: 2rem;
	}
  .container2{
    background: #e5e5e5;
		overflow: hidden;
  }
  .title{
    line-height: 40px;
  }

	table{
		text-align: center;
	}
	img{
    max-width: 100%;
	}
	.main-svg {
		width: 100%;
		max-width: 100%;
		z-index: 0;
	}
	.main-svg svg {
		width: 100%;
		max-width: 100%;
	}
	.main-svg .bglayer {
		width: 100%;
		max-width: 100%;
	}
	.main-svg .bglayer .bg{
		width: 100%;
		max-width: 100%;
	}
	.draglayer{
		width: 100%;
		max-width: 100%;
	}
	.cursor-crosshair {
		width: 100%;
		max-width: 100%;
	}
</style>
<script type="text/javascript" language="javascript">// <![CDATA[
	window.onload=function (){
	setInterval("document.getElementById('time').innerHTML=new Date().toLocaleString()+' '+['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][new Date().getDay()];",1000);
	}
	// ]]></script>
</html>
'''


def main(output_root='./tmp_output/'):
  if not output_root.endswith('/'): output_root = output_root +'/'
  index_html = open(output_root + 'index.html', 'w')
  index_html.write( html_content )

  # 根据流程 找一遍, 每个流程可能有imgs, 需要的文件，report.txt
  # todo


if __name__ == '__main__':
  fire.Fire( main )