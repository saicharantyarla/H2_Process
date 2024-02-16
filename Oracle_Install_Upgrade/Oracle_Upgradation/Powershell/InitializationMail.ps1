
Param(
[string] $ORACLEServer,
[string] $UpgradationType,
[string] $ORACLESeUsername,
[string] $BinPath,
[string] $OraHome12,
[string] $OraBase,
[string] $InvLoc,
[string] $UnixGN,
[string] $InstEdi,
[string] $SelecLang,
[string] $DBAGN,
[string] $OPERGN,
[string] $DGDBAGN,
[string] $KMDBAGN,
[string] $BACKUPDBAGN,
[string] $SecUp,
[string] $OraHome11,
[string] $TNSList,
[string] $DBName
)
	
$Up=$UpgradationType.toupper()
$SelecLang="ENG"
if ($UpgradationType -eq "BOTH") 
{
	$UpgradationType="INSTALLATION and UPGRADATION"
}

$st='<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<table align="left" border="0" cellpadding="0" cellspacing="0" style="width:650px;">
    <tbody>
    <tr>
        <th rowspan="2" style="text-align: center; width: 50px; vertical-align: middle; background-color: rgb(102, 102, 102);"><span style="color:#FFFFFF;">IT</span></th>
        <td style="text-align: center; vertical-align: middle; width: 250px; background-color: rgb(0, 153, 153);"><span style="color:#FFFFFF;">Software Service Automation</span></td>
        <td rowspan="2" style="text-align: center; vertical-align: middle; width: 200px; background-color: rgb(0, 153, 51);"><span style="color:#FFFFFF;">ORACLE UPGRADATION</span></td>
    </tr>
    <tr>
        <td style="text-align: center; vertical-align: middle; background-color: rgb(0, 153, 153);">Automate <span style="color:#FFFFFF;">IT</span>, Change <span style="color:#FFFFFF;">IT</span>, Speed <span style="color:#FFFFFF;">IT</span></td>
    </tr>
    </tbody>
</table>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>Hi Team,</p>
<br>
<p>This is to inform that  the <b> Oracle Upgradation </b> process has been triggered</p>

<br>

<p>Also find the input details.</p>
<br>

<table align="left" border="1" cellpadding="1" cellspacing="1" dir="ltr" style="width:500px;">
    <thead>
    <tr>
        <th scope="col" style="text-align: left; vertical-align: middle; background-color: rgb(0, 51, 102);"><span style="color:#FFFFFF;">Components</span></th>
        <th scope="col" style="text-align: left; vertical-align: middle; background-color: rgb(0, 0, 102);"><span style="color:#FFFFFF;">Values</span></th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td> Upgradation type</td>
        <td>'+$UpgradationType+'</td>
    </tr>
    <tr>
        <td> Server IP / Hostname</td>
        <td>'+$ORACLEServer+'</td>
    </tr>'
if ($UpgradationType -eq "ONLY_UPGRADATION") 
{
        $u='
            <tr>
                <td> OS Username</td>
                <td>'+$ORACLESeUsername+'</td>
            </tr>
			 <tr>
                <td> Oracle Home (11.2.0.4)</td>
                <td>'+$OraHome11+'</td>
            </tr>
			<tr>
                <td> Oracle Home (12.1.0.2)</td>
                <td>'+$OraHome12+'</td>
            </tr>
			<tr>
                <td> TNS List</td>
                <td>'+$TNSList+'</td>
            </tr>
			<tr>
                <td> Upgrade will be performed on</td>
                <td>'+$DBName+'</td>
            </tr>'
}
else
{
 $u=  '<tr><td colspan="2" ><span style="color:#808000;"><b>Installation Details</b></td></tr>
 <tr>
                <td> Oracle Installer Username</td>
                <td>'+$ORACLESeUsername+'</td>
            </tr>
			 <tr>
                <td> Binary Location </td>
                <td>'+$BinPath+'</td>
            </tr>
			<tr>
                <td> Oracle Home (12.1.0.2)</td>
                <td>'+$OraHome12+'</td>
            </tr>
			<tr>
                <td> Oracle Base</td>
                <td>'+$OraBase+'</td>
            </tr>
			<tr>
                <td>UNIX Group Name</td>
                <td>'+$UnixGN+'</td>
            </tr>
			<tr>
                <td>Installation Edition</td>
                <td>'+$InstEdi+'</td>
            </tr>
			<tr>
                <td>UNIX Group Name</td>
                <td>'+$UnixGN+'</td>
            </tr>
			<tr>
                <td>Selected Languages</td>
                <td>'+$SelecLang+'</td>
            </tr>
			<tr>
                <td>DBA  Group Name</td>
                <td>'+$DBAGN+'</td>
            </tr>
			<tr>
                <td>OPER Group Name</td>
                <td>'+$OPERGN+'</td>
            </tr>
			<tr>
                <td>DGDBA  Group Name</td>
                <td>'+$DGDBAGN+'</td>
            </tr>
			<tr>
                <td>KMDBA Group Name</td>
                <td>'+$KMDBAGN+'</td>
            </tr>
			<tr>
                <td>BACKUPDBA  Group Name</td>
                <td>'+$BACKUPDBAGN+'</td>
            </tr>
			<tr>
                <td>Decline Security Updates</td>
                <td>'+$SecUp+'</td>
            </tr>
			<tr><td colspan="2"><span style="color:#808000;"><b>Upgradation Details</b></td></tr><tr>
			<tr>
                <td> Oracle Home (11.2.0.4)</td>
                <td>'+$OraHome11+'</td>
            </tr>
			<tr>
                <td> TNS List</td>
                <td>'+$TNSList+'</td>
            </tr>
			<tr>
                <td> Upgrade will be performed on</td>
                <td>'+$DBName+'</td>
            </tr>'
}
$fi='</tbody>
</table>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<p>&nbsp;</p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>Thanks &amp; Regards,</p>

<p>SS Automation Team</p>

<p>ssauto@capgemini.com</p>

</body>
</html>'
$fina=$st+$u+$fi
$fina