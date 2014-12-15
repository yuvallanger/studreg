<?php
session_start();
if(isset($_SESSION['admin']) && !empty($_SESSION['admin'])){
 ?>


<?php 
}else{
 header("location:adminlogin.php");
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html>
<head>
<title>עדכון רשומות סטודנטים</title>
<meta http-equiv="content-type" content="text/html; charset=utf-8"></meta>
<link rel="stylesheet" type="text/css" href="admin/style.css">
<html xmlns="http://www.w3.org/1999/xhtml"> 
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
<script type="text/javascript">
    $(document).ready( function () {
        $('#deletedata').submit( function () {
			 
            var formdata = $("#deletedata").serialize();
            $.ajax({
                type: "POST",
                url: "admin/emptytable.php",
                data:$('#deletedata').serialize()
				
             });
			 var showmsg= document.getElementById("showMesage");
		showmsg.style.visibility = 'visible' ;
		showmsg.style.display ='';
		
            return false;
        });
		
    });
</script>
</head>
<body dir="rtl">
<?php include("navbar.php"); ?>
<div class="uploadbox">
  העלאת קובץ CSV: <br />
<p class="isa_info">יש להעלות קובץ CSV בלבד. </br>
בקבצים עם מספר רב של רשומות עדכון המסד עלול לקחת מספר דקות, נא לא לסגור את העמוד עד לקבלת הודעה שהעדכון הסתיים וניתן לצאת מהעמוד!</p>
<form action="" method="post" enctype="multipart/form-data" name="csv" id="csv"> 
 
  <input name="csv" type="file" id="csv" /> 
  <input type="submit" name="Submit1" value="עדכן רשומות" /> 
</form>

<?php  

require($_SERVER['DOCUMENT_ROOT'] . '/studreg/admin/connect.php');

if ($_FILES[csv][size] > 0) { 

    //get the csv file 
    $file = $_FILES[csv][tmp_name]; 
    $handle = fopen($file,"r"); 
    $pass = 0;
    //loop through the csv file and insert into database 
    do { 
        if ($data[0]) { 
			mysql_query("SET NAMES 'utf8'");
			mysql_query("INSERT INTO studentreg (id, fname, lname, email, tel, campus, faculty, degree, major, minor, revaha, year) VALUES 
                ( 
                    '".preg_replace('/[^a-zA-Z0-9]/', '', $data[2])."',
                    '".mysql_real_escape_string($data[1])."', 
                    '".mysql_real_escape_string($data[0])."',
					'".preg_replace('/( )+/', ' ', $data[3])."',
					'".stripslashes($data[5])."',
					'".stripslashes($data[8])."',
					'".stripslashes($data[9])."',
					'".stripslashes($data[10])."',
					'".stripslashes($data[12])."',
					'".stripslashes($data[13])."',
					'".stripslashes($data[18])."',
					'".stripslashes($data[11])."'
			
                ) 
				
				
            "); 
			mysql_query("UPDATE studentreg SET tel = '".stripslashes($data[5])."', campus = '".stripslashes($data[8])."', faculty = '".stripslashes($data[9])."', fname = '".mysql_real_escape_string($data[1])."', lname = '".mysql_real_escape_string($data[0])."',
			degree = '".stripslashes($data[10])."', major = '".stripslashes($data[12])."', minor = '".stripslashes($data[13])."', revaha = '".stripslashes($data[18])."', year = '".stripslashes($data[11])."'
			WHERE id = '".preg_replace('/[^a-zA-Z0-9]/', '', $data[2])."'
			 ");
			$pass++;
        } 
     
		
	}
	
	while ($data = fgetcsv($handle,4096,"\t")); 
	echo '<div class="isa_success"><b>'  . $pass . ' שורות נסרקו מהקובץ</b>. ניתן לצאת מהעמוד.</div> ';

	
} 

?> 
<hr />
יצוא נתונים לקובץ CSV:
יש לבחור לפחות ערך אחד לסינון.

<form action="admin/export.php" method="post" id="export">
<p>קמפוס:<select name="campus">
<option></option>
<option value="4">הר הצופים</option>
<option value="1">עין כרם</option>
<option value="3">גבעת רם</option>
<option value="2">רחובות</option>
</select>
</p>
<p>סינון:
<select name="filter">
<option></option>
<option value="matana">קיבלו מתנת פתיחת שנה</option>
<option value="arab">דוברי ערבית</option>
<option value="miluim">משרתי מילואים</option>
<option value="dorms">מתגוררים במעונות</option>
<option value="extra1">קיבל/ה מדבקה</option>
<option value="extra2">עדכונים מהקלמר</option>
<option value="extra3">לקח/ה תיק</option>
<option value="extra4">איסתא</option>
<option value="extra5">מבקש/ת להחליף א.בחירה</option>
<!--
<option value="extra6">פתיחת שנה</option>
<option value="extra7">מסיבת חנוכה</option>
<option value="extra8">מסיבת פורים</option>
<option value="extra9">יום הסטודנט</option>
<option value="extra10">מסיבת גן</option>
--></select></p>
<p>דמי רווחה: 
<select name="revaha">
<option></option>
<option value="1">משלמים</option>
<option value="0">לא משלמים</option>
</select></p>
<p>חוג ראשי: <input type="text" name="major" size="20"  placeholder="3 ספרות חוג ראשי"></p>
<p>חוג משני: <input type="text" name="minor" size="20"  placeholder="3 ספרות חוג משני"></p>
<p>
שנת לימוד:<br>

<input type="checkbox" name="year[]" value="01">שנה א<br>
<input type="checkbox" name="year[]" value="02">שנה ב<br>
<input type="checkbox" name="year[]" value="03">שנה ג<br>
<input type="checkbox" name="year[]" value="04">שנה ד ומעלה<br>
</p>

<input name="Submit" type="submit"  value="יצא נתונים"/>
</form>
<hr />
רישום משתמשים
<iframe src="http://aguda.org.il/studreg/admin/signup.php" name="signup" scrolling="no" frameborder="no" align="center" height = "190px" width = "350px">
</iframe>
<hr />

מחיקת נתונים מהמאגר:
<p class="isa_warning">שים לב: מחיקת הנתונים אינה הפיכה!</p>
<form action="admin/emptytable.php" method="post" id="deletedata">
בחר פעולה:
<select name="temptable" default="בחר נתונים למחיקה">
<option value="">--</option>
<option value="studentreg">מחק פרטי סטודנטים</option>
<option value="users">הסר גישת משתמשים למערכת</option>
</select>
<input name="Submit" type="submit"  value="מחק נתונים" />
</form>
<div id="showMesage" class="isa_success" style="visibility:hidden;display:none">נתונים נמחקו.</p>


</body> 
</html> 