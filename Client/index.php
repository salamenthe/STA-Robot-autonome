<?php
    $my_img = file_get_contents("images/camera.jpeg");
    
    $results = array(
      'image' => base64_encode($my_img)
    );
    
    header('Content-type: application/json');
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: *');
    header('Access-Control-Allow-Headers: Content-Type');
    $json = json_encode($results);
    echo $json;
?>