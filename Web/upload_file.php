

<HTML>
<HEAD>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-122276036-12"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-122276036-12');
</script>


  <title>Dove Server</title>
  <meta name="KEYWORDS" content="Evaluation of Docking model with Dove">
  <meta name="DESCRIPTION" content="Dove algorithm">
 <link rel=stylesheet type=text/css href="hs.css">
<script language="Javascript" type="text/javascript">
<!--
// This script came from
// Uncle Jim's Javascript Examples
// JDStiles.com

function selectAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
}
//-->
</script>
<style>
//A{color:red; text-decoration:none}
A:hover{color:blue}
A:visited:{color:#000066}
</style>
<style>
//A{color:red; text-decoration:none}
A:hover{color:blue}
A:visited:{color:#000066}
</style>
    <meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
body,h1,h2,h3,h4,h5,h6 {font-family: "Lato", sans-serif}
.w3-bar,h1,button {font-family: "Montserrat", sans-serif}
.fa-anchor,.fa-coffee {font-size:500px}
</style>
<script language="javascript">
<!--

/*############################################################################
This script is made by bratta from www.bratta.com and can be used freely
as long as this msg is intact. Visit www.bratta.com for more great scripts.
############################################################################*/


	var n = (document.layers) ? 1:0;
	var ie = (document.all) ? 1:0;

/*The function for "making" the objects
######################################################################################*/
	function makeObj(obj){
    	this.css=(n) ? eval('document.'+obj):eval(obj+'.style')
		this.hideIt=b_hideIt;
		this.showIt=b_showIt;
		this.css.visibility="hidden"
		return this
	}

//######################################################################################
	function init(){
	//making the objects to show and hide:
	text1=new makeObj('divText1');
	checkResult();
	}
//-->

</script>
</HEAD>
<body onLoad="init()">



<tr>
   <td colspan="5"> <hr size="2" align="left"></td>
</tr>


<table cellspacing="0" cellpadding="5" width="1100">
<tbody>

<tr>
<td colspan="5">

<p>
<div class="w3-top">
  <div class="w3-bar w3-blue w3-card-2 w3-left-align w3-large">
    <a class="w3-bar-item w3-button w3-hide-medium w3-hide-large w3-opennav w3-right w3-padding-large w3-hover-white w3-large w3-blue" href="javascript:void(0);" onclick="myFunction()" title="Toggle Navigation Menu"><i class="fa fa-bars"></i></a>
    <a href="./index.html" class="w3-bar-item w3-button w3-padding-large w3-white">Home</a>
    <a href="./ReadMe.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Tutorials</a>
      <a href="https://github.com/kiharalab/DOVE" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Code</a>
    <a href="http://kiharalab.org/contact.php" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Contact Us</a>
    <a href="http://kiharalab.org/" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Lab</a>
  </div>
 <!-- Navbar on small screens -->
  <div id="navDemo" class="w3-bar-block w3-white w3-hide w3-hide-large w3-hide-medium w3-large">
   <a class="w3-bar-item w3-button w3-hide-medium w3-hide-large w3-opennav w3-right w3-padding-large w3-hover-white w3-large w3-blue" href="javascript:void(0);" onclick="myFunction()" title="Toggle Navigation Menu"><i class="fa fa-bars"></i></a>
    <a href="./index.html" class="w3-bar-item w3-button w3-padding-large w3-white">Home</a>
    <a href="./ReadMe.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Tutorials</a>
      <a href="https://github.com/kiharalab/DOVE" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Code</a>
    <a href="http://kiharalab.org/contact.php" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Contact Us</a>
    <a href="http://kiharalab.org/" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white">Lab</a>
  </div>
</div>
<br><br>
<div class="w3-container">

      <h1><img src="./img/header.jpg" style="width:8%;">A Deep-learning based dOcking decoy eValuation mEthod</h1>

</div>
<strong><font size=4 > Dove Result  </font></strong>
<td colspan="5"></td>


<tr bgcolor=white>
   <td colspan="5">
    <?php
  /* set upload directory */
    $dest_dir='/bio/kihara-web/www/dove/uploads';

    /* test directory exists or not */
    if(!file_exists($dest_dir)){

        $status=mkdir($dest_dir);
        $cmd = system("chmod 777 ".$dest_dir,$ret);
    }
    $upfile=$_FILES["file"];
    $type=array("pdb");
    function fileext($filename)
    {
        return substr(strrchr($filename, '.'), 1);
    }
    if( !in_array( strtolower( fileext($upfile['name'] ) ),$type) )
     {  $upload_type=strtolower( fileext($upfile['name'] ) );
        echo "Your updated file:",$upfile['name'],"  file type:",$upload_type,"<br>";
        $text=implode(",",$type);
        echo "We only support the following type files: ",$text,"<br>";
        echo "[<a href=\"index.html\">Resubmit</a>]";
        return;
     }
    else
     {$addtime=date("Ymd",time());
      $dest_dir=$dest_dir.'/'.$addtime;
      if(!file_exists($dest_dir)){

        $status=mkdir($dest_dir);
        $cmd = system("chmod 777 ".$dest_dir,$ret);
    }
        $dest=$dest_dir.'/'.$upfile['name'];
        $state=move_uploaded_file($upfile['tmp_name'],$dest);
     }
     /* Move file finished then we need to use python to get the results*/
     echo("We received the job you submitted. Please wait 2-5 minutes.<br>");
     echo "Your submitted file:",$upfile['name'],"<br>";
     $rand_id=rand(1000000, 9999999);
     $current_path=getcwd();
     $code_path=$current_path.'/Dove_Pred';
     chdir($code_path);
     $cmd = system("nohup /usr/bin/python3 main.py -F={$dest} --id={$rand_id} --mode=0 >>/tmp/logdove.txt &",$ret);
    /* Use ajax to wait*/
    function retrieve($url)
{
 preg_match('/\/([^\/]+\.[a-z]+)[^\/]*$/',$url,$match);
 return $match[1];
 }
 $file_name=retrieve($dest);
 $pdb_id=substr($file_name,0, -4);
    $Result_path=$dest_dir.'/'.$pdb_id.$rand_id.'/'.$pdb_id.'_jobid'.$rand_id.'.txt';

?>
<div id="txtHint">
<h5>.....Please click refresh when it's more than 3 minutes.....</h5>
<input type="submit" name="Refresh" value="Refresh" onclick="checkResult()">
</div>
<script type="text/javascript">
function checkResult()
{
    var xmlhttp;
    if (window.XMLHttpRequest) {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
    }
    else {
      // code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            document.getElementById("txtHint").innerHTML=xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET","checkResult.php?file=<?php echo $Result_path;?>",true);
    xmlhttp.send();
}
</script>

   <hr size="2" align="left"></td>
</tr>

</tbody>
</table>

<tr>
<td colspan="5"><hr size="2" align="left"></td>
</tr>

<b><font size=4 >If you use this program, please cite:</b><br>
<font size=4 >Docking Model Evaluation by 3D Deep Convo-lutional Neural Networks
Xiao Wang, Genki Terashi, Charles W. Christoffer, Mengmeng Zhu, and Daisuke Kihara,In submission (2019)

<br>
<footer class="w3-container w3-padding-64 w3-center w3-opacity">
  <div class="w3-xlarge w3-padding-32">
   <a href="https://twitter.com/kiharalab" class="w3-hover-text-light-blue"><i class="fa fa-twitter"></i></a>
 </div>
</footer>
<script>
// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}
</script>

</BODY>
</HTML>
