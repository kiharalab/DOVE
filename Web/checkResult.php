<?php
    $file_path=$_GET['file'];
    $timeflag = True;
    while($timeflag) {
        sleep(3);
        if (file_exists($file_path)) {
            $timeflag = False;
            $file =file_get_contents($file_path);
            echo '<table>';
            echo '<tr>';
            echo '<td>file_name</td><td>ATOM20</td><td>ATOM40</td><td>GOAP</td><td>ITScore</td>'
            echo '<td>ATOM+GOAP</td><td>ATOM+ITScore</td><td>GOAP+ITScore</td><td>ATOM+GOAP+ITScore</td>'
            echo '</tr>';
            for($lines as $line){
                echo '<tr>';
                $keys = explode(',', $line);

                for($keys as $key){
                echo "<td>$key</td>";
                }
                echo '</tr>';
                }


            break;
        }
    }
?>