<?php
    $file_path=$_GET['file'];
    $timeflag = True;
    $count=1;
    while($timeflag) {
        sleep(3);
        if (file_exists($file_path)) {
            $timeflag = False;
            $lines =file_get_contents($file_path);
            echo '<table>';
            echo '<tr>';
            echo '<td>file_name</td><td>ATOM20</td><td>ATOM40</td><td>GOAP</td><td>ITScore</td>';
            echo '<td>ATOM+GOAP</td><td>ATOM+ITScore</td><td>GOAP+ITScore</td><td>ATOM+GOAP+ITScore</td>';
            echo '</tr>';



            $arr = explode("\r\n", $lines);
            for($i=0;$i<count($arr);$i++){
            echo '<tr>';
    $items = explode(",", $arr[$i]);
    for($j=0;$j<count($items);$j++){
       echo '<td>';
        echo $items[$j];
        echo '</td>';
    }
 echo '</tr>';
}




            echo '</table>';


            break;
        }
        $count=$count+1;
        if ($count>1000){
        $timeflag=False;
        echo "We get no results";
        }
    }
?>