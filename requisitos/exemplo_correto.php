<?php
$cont;
$a,$b,$c;
$cont = 10;
while ($cont > 0) {
  $a = floatval(readline());
  $b = floatval(readline());
  if ($a > $b) {
    $c = $a - $b;
  } else {
    $c = $b - $a;
  }
  echo $c . PHP_EOL;
  $cont = $cont - 1;
}
echo $c . PHP_EOL;
?>
