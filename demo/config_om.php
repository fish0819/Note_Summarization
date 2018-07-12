<?php 
$conn = mysqli_connect("localhost", "root", "", "notesum_om");
mysqli_set_charset($conn,"utf8");
if (!$conn)
    die("Could not connect: ".mysqli_error());
 ?>