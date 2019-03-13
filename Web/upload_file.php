

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
	text1=new makeObj('divText1')
	}
//-->

</script>
</HEAD>
<body onLoad="init()">


  <table>
    <tbody>
      <tr>
	<td><img src="img/header.png" height=200 alt="Dove"> <br>
	<strong><font size=2.5 color=gray>UNDER CONSTRUCTION Dove</font> </strong>
		 <br> <br>
		 <strong> </font></strong></td>
</tr>

<!-- 	 <br>  &nbsp; &nbsp; &nbsp;&nbsp; <strong>WebServer </strong> -->
    </tr>
      <tr>
        <td valign="top">
       [<a href="index.html">Dove</a>]
       [<a href="https://github.rcac.purdue.edu/kiharalab/Dove_Pred">Source Code</a>]
       [<a href="http://kiharalab.org">Lab</a>]
       &nbsp; Contact: <a href="mailto:dkihara@purdue.edu">dkihara@purdue.edu</a>
        </td>
      </tr>
</table>

<tr>
   <td colspan="5"> <hr size="2" align="left"></td>
</tr>


<table cellspacing="0" cellpadding="5" width="1100">
<tbody>

<tr>
<td colspan="5">

<strong><font size=4 > Dove Result  </font></strong>
<p>


<td colspan="5"></td>


<tr bgcolor=white>
   <td colspan="5">
    <?php
  /* set upload directory */
    $dest_dir='uploads';

    /* test directory exists or not */
    if( !is_dir($dest_dir) || !is_writeable($dest_dir) )
    {
     mkdir($dest_dir);
    }
    $upfile=&$HTTP_POST_FILES['file'];
    $type=array("pdb");
    function fileext($filename)
    {
        return substr(strrchr($filename, '.'), 1);
    }
    if( !in_array( strtolower( fileext($upfile['name'] ) ),$type) )
     {
        $text=implode(",",$type);
        echo "We only support the following type files: ",$text,"<br>";

     }
    else
     {
        $dest=$dest_dir.'/'.date("ymdHis")."_".$upfile['name'];
        $state=move_uploaded_file($upfile['tmp_name'],$dest);
     }
     /* Move file finished then we need to use python to get the results*/
     echo("Congratulations, job has been submitted, please wait around 2-5 minutes!\n");
     $rand_id=rand(1000000, 9999999);
     $cmd = system("module load slurm; python Dove_Pred/run_slurm.py -F={$dest} --id={$rand_id}",$ret);
    /* Use ajax to wait*/
    function retrieve($url)
{
 preg_match('/\/([^\/]+\.[a-z]+)[^\/]*$/',$url,$match);
 return $match[1];
 }
 $file_name=retrieve($dest);
 $pdb_id=substr($file_name,0, -4);
    $Result_path=$dest.'/'.$pdb_id.$random_id.'/'.$pdb_id.'_jobid'.$random_id.'.txt';

?>
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
    xmlhttp.open("GET","checkResult.php?file="<?php echo $Result_path;?>,true);
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
Xiao Wang, Genki Terashi, Charles W. Christoffer, Mengmeng Zhu, and Daisuke Kihara

<br>


</BODY>
</HTML>
