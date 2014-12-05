<?php
ob_start(); 
$campus = $_REQUEST["campus"];
$filter = $_REQUEST["filter"];
$major = $_REQUEST["major"];
$minor = $_REQUEST["minor"];
$revaha = $_REQUEST["revaha"];
$year =  $_REQUEST["year"];
$year = array_map ('intval', $year);
$year = implode (',', $year);
$date = date('d.m.y');
if ($campus == '01') { 
$campusName = 'עין כרם';
}
elseif ($campus == '02') {
$campusName = 'רחובות';
}
elseif ($campus == '03') {
$campusName = 'גבעת רם';
}
elseif ($campus == '04') {
$campusName = 'הר הצופים';
}
else {
$campusName = 'כל הקמפוסים';
}
// Database Connection

$host = $studentreg_config["mysql_address"];
$uname = $studentreg_config["mysql_user"];
$pass = $studentreg_config["mysql_password"];
$database = $studentreg_config["mysql_db"];

$connection=mysql_connect($host,$uname,$pass); 

echo mysql_error();

//or die("Database Connection Failed");
$selectdb=mysql_select_db($database) or 
die("Database could not be selected"); 
$result=mysql_select_db($database)
or die("database cannot be selected <br>");

// Fetch Record from Database

$output = "";
$table = "studentreg"; // Table Name 
mysql_query("SET NAMES 'utf8'");

unset($sql);
if ($major) {
    $sql[] = " major = '$major' ";
}
if ($minor) {
    $sql[] = " minor = '$minor' ";
}
if ($revaha) {
    $sql[] = " revaha = '$revaha' ";
}
if ($filter) {
    $sql[] = " $filter = '1' ";
}
if ($campus) {
    $sql[] = " campus = '$campus' ";
}
if (empty($year)) {
	$sql[] = " year>0 ";
} elseif ($year == '4') {
$sql[] = " year>03 ";
} else {
$sql[] = " year IN($year) ";
}
$query = "SELECT * FROM $table";

if (!empty($sql)) {
    $query .= ' WHERE ' . implode(' AND ', $sql);
}
$sql = mysql_query($query);
$columns_total = mysql_num_fields($sql);

// Get The Field Name

for ($i = 0; $i < $columns_total; $i++) {
$heading = mysql_field_name($sql, $i);
$output .= '"'.$heading.'",';
}
$output .="\n";

// Get Records from the table

while ($row = mysql_fetch_array($sql)) {
for ($i = 0; $i < $columns_total; $i++) {
$output .='"'.$row["$i"].'",';
}
$output .="\n";
}

// Download the file

$filename = 'דוח סטודנטים:' .$campusName.'-'. $filter .'-'. $date .'.csv';
header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream'); 
header('Content-Disposition: attachment; filename='.$filename);
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
header('Pragma: public');
echo "\xEF\xBB\xBF"; // UTF-8 BOM

echo $output;
exit;

?>