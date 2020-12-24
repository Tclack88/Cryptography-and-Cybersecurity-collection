<?php
# Natas 10 -> 11
$key1 =  base64_decode('ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSFlkrEBZZaAw=');

function xor_encrypt($in,$key) {
    $outText = '';
  
    // Iterate through each character
    for($i=0;$i<strlen($in);$i++) {
    $outText .= $in[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}



$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");
$data = json_encode($defaultdata);
$out = xor_encrypt($data,$key1);
echo "$out \n";

$newdata = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff");
$key2 = 'qw8J';
$newout = base64_encode(xor_encrypt(json_encode($newdata),$key2));
echo "$newout \n";
?>
